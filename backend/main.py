"""
PhytoTrace FastAPI Backend Application
======================================
REST API service for Botanical Supply Chain Traceability Using Property Graphs.
Supports live Neo4j database or seamless NetworkX in-memory graph fallback.
"""

import sys
import os

# Add root directory to path to import crop_catalog, translations, graph_engine
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
import datetime

# Import existing core modules
from crop_catalog import (
    CROP_CATALOG,
    CATEGORIES,
    format_crop_display,
    get_category_label,
    get_crop_color_map,
    get_crop_by_id
)
from translations import TRANSLATIONS, LANGUAGES
from graph_engine import (
    build_supply_chain_graph,
    get_graph_metrics,
    compute_degree_centrality,
    trace_batch_path,
    generate_cypher_export_script
)
from backend.data_store import (
    get_all_batches,
    add_harvest_batch,
    compute_kpis,
    check_neo4j_status
)

app = FastAPI(
    title="PhytoTrace API",
    description="Botanical Supply Chain Traceability Backend powered by Property Graphs",
    version="2.4.0"
)

# CORS Configuration
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in allowed_origins else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Request Models
class HarvestRequest(BaseModel):
    crop_id: str = Field(..., description="Crop identifier, e.g., TUR, NEE, ASH")
    farmer: str = Field(..., min_length=2, description="Name of the cultivator")
    farm_name: str = Field(..., min_length=2, description="Name of the farm / grove")
    farm_id: Optional[str] = Field(None, description="Farm identifier")
    location: str = Field(default="Karnataka, India", description="Geographic location")
    supplier: Optional[str] = Field(default="Regional FPO Collective", description="Aggregating FPO / Collective")
    variety: Optional[str] = Field(default="Certified Organic", description="Botanical variety")
    harvest_qty_kg: int = Field(..., gt=0, description="Harvested weight in kilograms (must be positive)")
    harvest_date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    notes: Optional[str] = Field(default="", description="Harvest condition notes")

    @field_validator("harvest_date")
    @classmethod
    def validate_date(cls, v):
        if v:
            try:
                datetime.date.fromisoformat(v)
            except ValueError:
                raise ValueError("harvest_date must be in YYYY-MM-DD format")
        return v or datetime.date.today().isoformat()


# -----------------------------------------------------------------------------
# System & Health
# -----------------------------------------------------------------------------
@app.get("/api/health")
def get_health():
    """System health check and Neo4j connection status."""
    neo_status = check_neo4j_status()
    all_batches = get_all_batches()
    return {
        "status": "healthy",
        "service": "PhytoTrace API",
        "version": "2.4.0",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "database": neo_status,
        "total_active_batches": len(all_batches),
    }


# -----------------------------------------------------------------------------
# Languages & Translations
# -----------------------------------------------------------------------------
@app.get("/api/languages")
def get_languages():
    """Returns all 12 supported languages with native names, BCP-47 speech codes and RTL direction."""
    return [
        {
            "code": code,
            "name": meta["name"],
            "native": meta["native"],
            "speech_code": meta.get("code", f"{code}-IN"),
            "is_rtl": meta.get("rtl", False)
        }
        for code, meta in LANGUAGES.items()
    ]


@app.get("/api/translations/{lang}")
def get_translations(lang: str):
    """Returns UI translation key-value mappings for the requested language code."""
    if lang not in TRANSLATIONS:
        lang = "en"
    return {
        "lang": lang,
        "is_rtl": (lang == "ur"),
        "translations": TRANSLATIONS[lang]
    }


# -----------------------------------------------------------------------------
# Botanical Catalog & Crops
# -----------------------------------------------------------------------------
@app.get("/api/crops")
def get_crops(lang: str = Query("en", description="Language code for common names")):
    """Returns the full 20-crop botanical catalog with metadata and translations."""
    crops_list = []
    for c in CROP_CATALOG:
        name_localized = c.get("translations", {}).get(lang, c["name"])
        crops_list.append({
            "id": c["id"],
            "common_name": c["name"],
            "localized_name": name_localized,
            "scientific_name": c["scientific_name"],
            "category_id": c.get("category_id", "all"),
            "category": c["category"],
            "category_label": get_category_label(c.get("category_id", "all"), lang),
            "variety_sample": c.get("variety_sample", "Certified"),
            "accent_color": c.get("color", "#26734D"),
            "icon": c.get("icon", "🌿"),
            "translations": c.get("translations", {})
        })
    return crops_list


@app.get("/api/categories")
def get_categories(lang: str = Query("en")):
    """Returns crop categories with localized labels."""
    return [
        {
            "id": cat["id"],
            "icon": cat.get("icon", "🌿"),
            "label": get_category_label(cat["id"], lang),
            "count": len([c for c in CROP_CATALOG if c.get("category_id") == cat["id"]]) if cat["id"] != "all" else len(CROP_CATALOG)
        }
        for cat in CATEGORIES
    ]


# -----------------------------------------------------------------------------
# Batches Management & Search
# -----------------------------------------------------------------------------
@app.get("/api/batches")
def list_batches(
    crop_id: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    stage: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "harvest_date",
    order: Optional[str] = "desc"
):
    """Retrieves all botanical batches with multi-field search and filters."""
    batches = get_all_batches()

    if crop_id:
        batches = [b for b in batches if b.get("crop_id") == crop_id]
    if category:
        batches = [b for b in batches if b.get("category") == category]
    if status:
        batches = [b for b in batches if b.get("status") == status]
    if stage:
        batches = [b for b in batches if b.get("current_stage") == stage]
    if search:
        s = search.lower()
        batches = [
            b for b in batches
            if s in b.get("batch_id", "").lower()
            or s in b.get("botanical", "").lower()
            or s in b.get("farmer", "").lower()
            or s in b.get("farm_name", "").lower()
            or s in b.get("location", "").lower()
            or s in b.get("supplier", "").lower()
            or s in b.get("scientific_name", "").lower()
        ]

    reverse_sort = (order.lower() == "desc")
    batches.sort(key=lambda x: str(x.get(sort_by, "")), reverse=reverse_sort)

    return batches


@app.get("/api/batches/{batch_id}")
def get_batch(batch_id: str):
    """Retrieves details for a single batch by ID."""
    batches = get_all_batches()
    for b in batches:
        if b["batch_id"].upper() == batch_id.upper():
            return b
    raise HTTPException(status_code=404, detail=f"Batch with ID '{batch_id}' not found.")


@app.post("/api/harvest", status_code=status.HTTP_201_CREATED)
def register_harvest(req: HarvestRequest):
    """
    Registers a new harvest batch from Farmer Mode.
    Validates input, assigns unique batch ID, persists to disk, and updates graph.
    """
    crop_info = get_crop_by_id(req.crop_id)
    botanical_name = crop_info["name"] if crop_info else "Custom Botanical"
    scientific_name = crop_info["scientific_name"] if crop_info else "Plantae sp."
    category = crop_info["category"] if crop_info else "Medicinal Plants"

    batch_payload = {
        "crop_id": req.crop_id,
        "botanical": botanical_name,
        "scientific_name": scientific_name,
        "category": category,
        "variety": req.variety or (crop_info.get("default_variety") if crop_info else "Certified"),
        "farmer": req.farmer,
        "farm_id": req.farm_id or f"FRM-{req.crop_id}-{datetime.date.today().strftime('%m%d')}",
        "farm_name": req.farm_name,
        "location": req.location,
        "supplier": req.supplier or "Regional FPO Collective",
        "harvest_date": req.harvest_date,
        "harvest_qty_kg": req.harvest_qty_kg,
        "notes": req.notes or "Registered via Farmer Mode portal."
    }

    created = add_harvest_batch(batch_payload)
    return {
        "success": True,
        "message": f"Harvest registered successfully! Batch ID: {created['batch_id']}",
        "batch": created
    }


# -----------------------------------------------------------------------------
# Supply Chain Traceability & Graph Engine
# -----------------------------------------------------------------------------
@app.get("/api/trace/{batch_id}")
def trace_batch(batch_id: str):
    """
    Traces end-to-end multi-hop supply chain path for a batch:
    Farmer -> Farm -> Botanical -> Harvest Batch -> Processor -> Processed Batch -> Manufacturer -> Finished Lot -> Distributor -> Retailer.
    """
    batches = get_all_batches()
    target_batch = next((b for b in batches if b["batch_id"].upper() == batch_id.upper()), None)
    if not target_batch:
        raise HTTPException(status_code=404, detail=f"Batch '{batch_id}' not found in registry.")

    # Build property graph
    G = build_supply_chain_graph(batches)
    trace_result = trace_batch_path(G, target_batch["batch_id"])

    # Define standard 10-tier custody sequence
    custody_chain = [
        {
            "tier": 1,
            "label": "Farmer",
            "name": target_batch.get("farmer", "Lead Cultivator"),
            "role": "Producer / Cultivator",
            "icon": "person",
            "status": "Verified",
            "date": target_batch.get("harvest_date")
        },
        {
            "tier": 2,
            "label": "Farm Origin",
            "name": target_batch.get("farm_name", "Origin Farm"),
            "location": target_batch.get("location", "India"),
            "farm_id": target_batch.get("farm_id"),
            "icon": "agriculture",
            "status": "Verified"
        },
        {
            "tier": 3,
            "label": "Botanical Crop",
            "name": target_batch.get("botanical", "Botanical"),
            "scientific_name": target_batch.get("scientific_name"),
            "category": target_batch.get("category"),
            "icon": "spa",
            "status": "Verified"
        },
        {
            "tier": 4,
            "label": "Harvest Batch",
            "batch_id": target_batch["batch_id"],
            "harvest_qty_kg": target_batch.get("harvest_qty_kg"),
            "harvest_date": target_batch.get("harvest_date"),
            "icon": "inventory_2",
            "status": target_batch.get("status", "Verified")
        },
        {
            "tier": 5,
            "label": "Processor",
            "name": target_batch.get("processor", "Extraction Lab"),
            "facility_type": "Extraction & Primary Processing",
            "icon": "factory",
            "status": "Verified" if target_batch.get("current_stage") in ["Processor", "Manufacturer", "Distributor", "Retailer"] else "Pending"
        },
        {
            "tier": 6,
            "label": "Processed Batch",
            "processed_batch_id": target_batch.get("processed_batch_id"),
            "icon": "science",
            "status": "Verified" if target_batch.get("current_stage") in ["Manufacturer", "Distributor", "Retailer"] else "In Transit"
        },
        {
            "tier": 7,
            "label": "Manufacturer",
            "name": target_batch.get("manufacturer", "Formulation Lab"),
            "certification": "GMP Ayurvedic Standard",
            "icon": "precision_manufacturing",
            "status": "Verified" if target_batch.get("current_stage") in ["Manufacturer", "Distributor", "Retailer"] else "Pending"
        },
        {
            "tier": 8,
            "label": "Finished Product Lot",
            "finished_batch_id": target_batch.get("finished_batch_id"),
            "icon": "check_circle",
            "status": "Verified" if target_batch.get("current_stage") in ["Distributor", "Retailer"] else "Pending"
        },
        {
            "tier": 9,
            "label": "Distributor",
            "name": target_batch.get("distributor", "Logistics Hub"),
            "hub_type": "Regional Freight Center",
            "icon": "local_shipping",
            "status": "Verified" if target_batch.get("current_stage") in ["Distributor", "Retailer"] else "Pending"
        },
        {
            "tier": 10,
            "label": "Retailer",
            "name": target_batch.get("retailer", "Herbal Dispensary"),
            "city": target_batch.get("retail_location", "Bengaluru"),
            "icon": "storefront",
            "status": "Delivered" if target_batch.get("current_stage") == "Retailer" else "Pending"
        }
    ]

    return {
        "batch": target_batch,
        "custody_chain": custody_chain,
        "graph_trace": {
            "shortest_path": trace_result["shortest_path"] if trace_result else [],
            "hop_count": trace_result["hop_count"] if trace_result else 0,
            "subgraph_nodes_count": trace_result["subgraph_nodes_count"] if trace_result else 0,
            "subgraph_edges_count": trace_result["subgraph_edges_count"] if trace_result else 0,
            "steps": trace_result["steps"] if trace_result else []
        }
    }


@app.get("/api/graph/data")
def get_graph_data(highlight_batch_id: Optional[str] = None):
    """
    Returns graph nodes, edges, positions, and highlighting suitable for
    interactive frontend rendering with Plotly.js or SVG canvas.
    """
    import networkx as nx

    batches = get_all_batches()
    G = build_supply_chain_graph(batches)

    tier_order = {
        "Farmer": 0,
        "Farm": 1,
        "HarvestBatch": 2,
        "Botanical": 2.5,
        "Processor": 3,
        "ProcessedBatch": 4,
        "Manufacturer": 5,
        "FinishedLot": 6,
        "Distributor": 7,
        "Retailer": 8
    }

    for n, d in G.nodes(data=True):
        lbl = d.get("label", "Farmer")
        d["subset"] = tier_order.get(lbl, 2)

    try:
        pos = nx.multipartite_layout(G, subset_key="subset")
    except Exception:
        pos = nx.spring_layout(G, seed=42)

    # Highlight path if specified
    highlight_nodes = set()
    highlight_edges = set()
    if highlight_batch_id and highlight_batch_id in G:
        trace_res = trace_batch_path(G, highlight_batch_id)
        if trace_res:
            p = trace_res["shortest_path"]
            highlight_nodes = set(p)
            for i in range(len(p) - 1):
                highlight_edges.add((p[i], p[i + 1]))

    nodes_data = []
    for n, d in G.nodes(data=True):
        x, y = pos[n]
        is_hl = n in highlight_nodes
        nodes_data.append({
            "id": n,
            "label": d.get("label", "Node"),
            "display_name": d.get("display_name", n),
            "color": d.get("color", "#2D6A4F"),
            "size": (d.get("size", 20) + 6) if is_hl else d.get("size", 20),
            "x": float(x),
            "y": float(y),
            "highlighted": is_hl,
            "metadata": {k: v for k, v in d.items() if k not in ["color", "size", "subset"]}
        })

    edges_data = []
    for u, v, d in G.edges(data=True):
        is_hl = (u, v) in highlight_edges
        edges_data.append({
            "source": u,
            "target": v,
            "rel_type": d.get("rel_type", "CONNECTED_TO"),
            "highlighted": is_hl,
            "metadata": d
        })

    return {
        "nodes": nodes_data,
        "edges": edges_data,
        "total_nodes": len(nodes_data),
        "total_edges": len(edges_data),
        "highlight_batch_id": highlight_batch_id
    }


@app.get("/api/graph/metrics")
def get_graph_metrics_endpoint():
    """Returns degree centrality, density, components count, and node distribution."""
    batches = get_all_batches()
    G = build_supply_chain_graph(batches)
    metrics = get_graph_metrics(G)
    centrality_df = compute_degree_centrality(G, top_k=10)
    centrality_list = centrality_df.to_dict(orient="records") if not centrality_df.empty else []

    return {
        **metrics,
        "centrality_ranking": centrality_list
    }


@app.get("/api/graph/cypher")
def get_cypher_export():
    """Generates an idempotent Cypher script for Neo4j import."""
    batches = get_all_batches()
    cypher_code = generate_cypher_export_script(batches)
    return {
        "statement_count": cypher_code.count("MERGE") + cypher_code.count("CREATE"),
        "cypher_script": cypher_code
    }


# -----------------------------------------------------------------------------
# Analytics & Reports
# -----------------------------------------------------------------------------
@app.get("/api/analytics/summary")
def get_analytics_summary():
    """Provides high-level KPIs and breakdown summaries for executive dashboard."""
    kpis = compute_kpis()
    batches = get_all_batches()

    # Crop volume breakdown
    crop_volumes = {}
    for b in batches:
        cname = b.get("botanical", "Other")
        qty = int(b.get("harvest_qty_kg", 0))
        crop_volumes[cname] = crop_volumes.get(cname, 0) + qty

    sorted_crops = sorted([{"crop": k, "volume_kg": v} for k, v in crop_volumes.items()], key=lambda x: x["volume_kg"], reverse=True)

    return {
        "kpis": kpis,
        "crop_volumes": sorted_crops,
        "generated_at": datetime.datetime.utcnow().isoformat()
    }


@app.get("/api/farms")
def get_farms_summary():
    """Aggregates farm origins with batches produced, crops handled, and locations."""
    batches = get_all_batches()
    farms_map = {}
    for b in batches:
        fid = b.get("farm_id") or "UNKNOWN_FARM"
        if fid not in farms_map:
            farms_map[fid] = {
                "farm_id": fid,
                "farm_name": b.get("farm_name", "Farm Plot"),
                "farmer": b.get("farmer", "Cultivator"),
                "location": b.get("location", "India"),
                "supplier": b.get("supplier", "FPO"),
                "crops": set(),
                "total_harvest_kg": 0,
                "batch_count": 0
            }
        farms_map[fid]["crops"].add(b.get("botanical", "Crop"))
        farms_map[fid]["total_harvest_kg"] += int(b.get("harvest_qty_kg", 0))
        farms_map[fid]["batch_count"] += 1

    result = []
    for f in farms_map.values():
        f["crops"] = list(f["crops"])
        result.append(f)

    result.sort(key=lambda x: x["total_harvest_kg"], reverse=True)
    return result


@app.get("/api/suppliers")
def get_suppliers_summary():
    """Aggregates suppliers and FPO collectives."""
    batches = get_all_batches()
    sup_map = {}
    for b in batches:
        sname = b.get("supplier") or "Direct Procurement"
        if sname not in sup_map:
            sup_map[sname] = {
                "supplier": sname,
                "farms": set(),
                "crops": set(),
                "total_volume_kg": 0,
                "batch_count": 0
            }
        sup_map[sname]["farms"].add(b.get("farm_id"))
        sup_map[sname]["crops"].add(b.get("botanical"))
        sup_map[sname]["total_volume_kg"] += int(b.get("harvest_qty_kg", 0))
        sup_map[sname]["batch_count"] += 1

    result = []
    for s in sup_map.values():
        result.append({
            "supplier": s["supplier"],
            "farms_represented": len(s["farms"]),
            "crops_handled": list(s["crops"]),
            "total_volume_kg": s["total_volume_kg"],
            "batch_count": s["batch_count"]
        })

    result.sort(key=lambda x: x["total_volume_kg"], reverse=True)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
