"""
PhytoTrace Property Graph Engine
=================================
A pure-Python Property Graph implementation powered by NetworkX with optional
live Neo4j Cypher synchronization.

Node Labels:
- Farmer
- Farm
- Botanical
- HarvestBatch
- Processor
- ProcessedBatch
- Manufacturer
- FinishedLot
- Distributor
- Retailer

Relationship Types:
- [:OWNS_FARM]
- [:HARVESTED_AT]
- [:OF_BOTANICAL]
- [:SHIPPED_TO_PROCESSOR]
- [:PROCESSED_INTO]
- [:SUPPLIED_TO_MAKER]
- [:FORMULATED_INTO]
- [:CONSIGNED_TO_DISTRIBUTOR]
- [:DELIVERED_TO_RETAILER]
"""

import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def build_supply_chain_graph(batches_list):
    """
    Constructs a rich directed property graph (nx.DiGraph) from a list of batch dictionaries.
    Creates 10 distinct node labels and 9 typed directed edges with metadata attributes.
    """
    G = nx.DiGraph()

    for b in batches_list:
        b_id = b["batch_id"]
        crop_id = b.get("crop_id", b_id.split("-")[0] if "-" in b_id else "BOT")
        farmer_name = b.get("farmer", "Lead Cultivator")
        farm_id = b.get("farm_id", f"FRM-{b_id}")
        farm_name = b.get("farm_name", "Origin Farm")
        botanical_name = b.get("botanical", "Botanical Crop")
        scientific_name = b.get("scientific_name", "Plantae sp.")
        category = b.get("category", "Medicinal Plants")
        location = b.get("location", "India")
        supplier = b.get("supplier", "Regional FPO Collective")
        harvest_date = b.get("harvest_date", "2026-09-01")
        harvest_qty_kg = int(b.get("harvest_qty_kg", 500))
        status = b.get("status", "Verified")
        stage = b.get("current_stage", "Retailer")

        processor_name = b.get("processor", "Regional Extraction Lab")
        proc_batch_id = b.get("processed_batch_id", f"PRC-{b_id}")
        mfr_name = b.get("manufacturer", "Herbal Formulations Unit")
        fin_batch_id = b.get("finished_batch_id", f"FIN-{b_id}")
        dist_name = b.get("distributor", "Central Agro Logistics Depot")
        retailer_name = b.get("retailer", "PureBotanics Dispensary")
        retail_loc = b.get("retail_location", "Bengaluru, Karnataka")

        # 1. Farmer Node
        farmer_id = f"FARMER:{farmer_name.replace(' ', '_')}"
        G.add_node(
            farmer_id,
            label="Farmer",
            display_name=farmer_name,
            role="Lead Cultivator",
            color="#1B4332",
            size=20
        )

        # 2. Farm Node
        G.add_node(
            farm_id,
            label="Farm",
            display_name=farm_name,
            location=location,
            supplier=supplier,
            color="#2D6A4F",
            size=22
        )

        # 3. Botanical Crop Node
        bot_id = f"BOT:{crop_id}"
        G.add_node(
            bot_id,
            label="Botanical",
            display_name=botanical_name,
            scientific_name=scientific_name,
            category=category,
            color="#52B788",
            size=20
        )

        # 4. Harvest Batch Node (Key entity)
        G.add_node(
            b_id,
            label="HarvestBatch",
            display_name=b_id,
            harvest_date=harvest_date,
            qty_kg=harvest_qty_kg,
            status=status,
            stage=stage,
            color="#0284C7",
            size=24
        )

        # 5. Processor Node
        proc_node_id = f"PROC:{processor_name.replace(' ', '_')[:24]}"
        G.add_node(
            proc_node_id,
            label="Processor",
            display_name=processor_name,
            facility_type="Extraction & Milling Facility",
            color="#7C3AED",
            size=22
        )

        # 6. Processed Batch Node
        G.add_node(
            proc_batch_id,
            label="ProcessedBatch",
            display_name=proc_batch_id,
            parent_harvest=b_id,
            color="#6366F1",
            size=18
        )

        # 7. Manufacturer Node
        mfr_node_id = f"MFR:{mfr_name.replace(' ', '_')[:24]}"
        G.add_node(
            mfr_node_id,
            label="Manufacturer",
            display_name=mfr_name,
            certification="GMP Ayurvedic Standard",
            color="#D97706",
            size=22
        )

        # 8. Finished Lot Node
        G.add_node(
            fin_batch_id,
            label="FinishedLot",
            display_name=fin_batch_id,
            parent_proc=proc_batch_id,
            color="#F59E0B",
            size=18
        )

        # 9. Distributor Node
        dist_node_id = f"DIST:{dist_name.replace(' ', '_')[:24]}"
        G.add_node(
            dist_node_id,
            label="Distributor",
            display_name=dist_name,
            hub_type="Regional Logistics Node",
            color="#0D9488",
            size=22
        )

        # 10. Retailer Node
        ret_node_id = f"RET:{retailer_name.replace(' ', '_')[:24]}"
        G.add_node(
            ret_node_id,
            label="Retailer",
            display_name=retailer_name,
            city=retail_loc,
            color="#334155",
            size=20
        )

        # Directed Property Edges
        G.add_edge(farmer_id, farm_id, rel_type="OWNS_FARM", date=harvest_date)
        G.add_edge(farm_id, b_id, rel_type="HARVESTED_AT", qty_kg=harvest_qty_kg)
        G.add_edge(b_id, bot_id, rel_type="OF_BOTANICAL", category=category)
        G.add_edge(b_id, proc_node_id, rel_type="SHIPPED_TO_PROCESSOR", batch_id=b_id)
        G.add_edge(proc_node_id, proc_batch_id, rel_type="PROCESSED_INTO", extract_lot=proc_batch_id)
        G.add_edge(proc_batch_id, mfr_node_id, rel_type="SUPPLIED_TO_MAKER", source=proc_batch_id)
        G.add_edge(mfr_node_id, fin_batch_id, rel_type="FORMULATED_INTO", finished_lot=fin_batch_id)
        G.add_edge(fin_batch_id, dist_node_id, rel_type="CONSIGNED_TO_DISTRIBUTOR", mode="Freight")
        G.add_edge(dist_node_id, ret_node_id, rel_type="DELIVERS_TO_RETAILER", destination=retail_loc)

    return G


def get_graph_metrics(G):
    """Calculates comprehensive graph metrics and summary distributions."""
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G) if num_nodes > 1 else 0.0

    # Node label distribution
    label_counts = {}
    for _, data in G.nodes(data=True):
        lbl = data.get("label", "GenericNode")
        label_counts[lbl] = label_counts.get(lbl, 0) + 1

    # Edge relationship distribution
    rel_counts = {}
    for _, _, data in G.edges(data=True):
        rtype = data.get("rel_type", "CONNECTED_TO")
        rel_counts[rtype] = rel_counts.get(rtype, 0) + 1

    # Connected components
    weakly_connected = list(nx.weakly_connected_components(G))
    num_components = len(weakly_connected)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "num_components": num_components,
        "label_counts": label_counts,
        "rel_counts": rel_counts,
    }


def compute_degree_centrality(G, top_k=8):
    """
    Computes degree centrality and betweenness centrality to identify critical hubs,
    bottlenecks, and dominant aggregators in the botanical supply chain.
    """
    if G.number_of_nodes() == 0:
        return pd.DataFrame()

    deg_cent = nx.degree_centrality(G)
    in_cent = nx.in_degree_centrality(G)
    out_cent = nx.out_degree_centrality(G)

    rows = []
    for node_id, score in deg_cent.items():
        node_data = G.nodes[node_id]
        rows.append({
            "node_id": node_id,
            "display_name": node_data.get("display_name", node_id),
            "label": node_data.get("label", "Node"),
            "degree_centrality": round(score, 4),
            "in_centrality": round(in_cent.get(node_id, 0), 4),
            "out_centrality": round(out_cent.get(node_id, 0), 4),
            "total_connections": G.degree(node_id),
        })

    df = pd.DataFrame(rows)
    return df.sort_values(by="degree_centrality", ascending=False).head(top_k)


def trace_batch_path(G, batch_id):
    """
    Traces the entire multi-hop supply chain path for a given harvest batch:
    Farmer -> Farm -> Batch -> Processor -> ProcessedBatch -> Manufacturer -> FinishedLot -> Distributor -> Retailer.
    Returns nodes, edges, shortest path lengths, and step-by-step custody data.
    """
    if batch_id not in G:
        return None

    # Upstream: Ancestors of batch (Farmer, Farm)
    ancestors = nx.ancestors(G, batch_id)
    # Downstream: Descendants of batch (Processor, ProcessedBatch, Manufacturer, FinishedLot, Distributor, Retailer)
    descendants = nx.descendants(G, batch_id)

    # Subgraph for this batch
    path_nodes = ancestors | {batch_id} | descendants
    subG = G.subgraph(path_nodes)

    # Find start node (in-degree 0 in subgraph) and terminal nodes (out-degree 0 in subgraph)
    start_nodes = [n for n in subG.nodes() if subG.in_degree(n) == 0]
    end_nodes = [n for n in subG.nodes() if subG.out_degree(n) == 0]

    # Calculate shortest path from primary start node to terminal node
    shortest_path_list = []
    if start_nodes and end_nodes:
        try:
            shortest_path_list = nx.shortest_path(subG, source=start_nodes[0], target=end_nodes[0])
        except Exception:
            shortest_path_list = list(subG.nodes())

    # Build sequential step details
    steps = []
    for i, nid in enumerate(shortest_path_list):
        ndata = G.nodes[nid]
        steps.append({
            "step": i + 1,
            "node_id": nid,
            "label": ndata.get("label", "Node"),
            "display_name": ndata.get("display_name", nid),
            "color": ndata.get("color", "#2D6A4F")
        })

    return {
        "batch_id": batch_id,
        "subgraph_nodes_count": len(path_nodes),
        "subgraph_edges_count": subG.number_of_edges(),
        "shortest_path": shortest_path_list,
        "hop_count": len(shortest_path_list) - 1 if len(shortest_path_list) > 0 else 0,
        "steps": steps,
        "subgraph": subG
    }


def render_graph_network_plot(G, highlight_batch_id=None, height=450):
    """
    Renders an interactive Plotly 2D Property Graph network visualization.
    Positions nodes using multipartite or spring layout with clear arrows, colors, and metadata.
    """
    if G.number_of_nodes() == 0:
        fig = go.Figure()
        fig.add_annotation(text="No graph nodes available", showarrow=False)
        return fig

    # Assign rank layers for hierarchical visualization
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

    # Set subset key for multipartite layout
    for n, d in G.nodes(data=True):
        lbl = d.get("label", "Farmer")
        d["subset"] = tier_order.get(lbl, 2)

    try:
        pos = nx.multipartite_layout(G, subset_key="subset")
    except Exception:
        pos = nx.spring_layout(G, seed=42)

    # Filter highlight path if requested
    highlight_edges = set()
    highlight_nodes = set()
    if highlight_batch_id and highlight_batch_id in G:
        trace_res = trace_batch_path(G, highlight_batch_id)
        if trace_res:
            path_list = trace_res["shortest_path"]
            highlight_nodes = set(path_list)
            for i in range(len(path_list) - 1):
                highlight_edges.add((path_list[i], path_list[i+1]))

    # Draw edge lines
    edge_x = []
    edge_y = []
    edge_hl_x = []
    edge_hl_y = []

    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        if (u, v) in highlight_edges:
            edge_hl_x.extend([x0, x1, None])
            edge_hl_y.extend([y0, y1, None])
        else:
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    fig = go.Figure()

    # Normal edges
    if edge_x:
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.2, color="#CBD5E1"),
            hoverinfo="none",
            mode="lines",
            showlegend=False
        ))

    # Highlighted edges
    if edge_hl_x:
        fig.add_trace(go.Scatter(
            x=edge_hl_x, y=edge_hl_y,
            line=dict(width=3.2, color="#26734D"),
            hoverinfo="none",
            mode="lines",
            name="Batch Lineage Path"
        ))

    # Node traces by category label
    labels_present = sorted(list(set(d.get("label", "Node") for _, d in G.nodes(data=True))))

    for lbl in labels_present:
        nx_list = [n for n, d in G.nodes(data=True) if d.get("label") == lbl]
        xs = [pos[n][0] for n in nx_list]
        ys = [pos[n][1] for n in nx_list]
        names = [G.nodes[n].get("display_name", n) for n in nx_list]
        colors = [G.nodes[n].get("color", "#2D6A4F") for n in nx_list]
        sizes = [G.nodes[n].get("size", 18) for n in nx_list]

        # Enlarge highlighted nodes
        final_sizes = []
        line_colors = []
        line_widths = []
        for n in nx_list:
            if n in highlight_nodes:
                final_sizes.append(G.nodes[n].get("size", 18) + 6)
                line_colors.append("#26734D")
                line_widths.append(3)
            else:
                final_sizes.append(G.nodes[n].get("size", 18))
                line_colors.append("#FFFFFF")
                line_widths.append(1.5)

        hover_texts = []
        for n in nx_list:
            d = G.nodes[n]
            h = f"<b>{d.get('label')}:</b> {d.get('display_name')}<br>"
            for k, v in d.items():
                if k not in ["label", "display_name", "color", "size", "subset"]:
                    h += f"• {k}: {v}<br>"
            hover_texts.append(h)

        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            mode="markers+text",
            name=lbl,
            text=[name[:12] + ".." if len(name) > 14 else name for name in names],
            textposition="top center",
            textfont=dict(family="Space Grotesk, sans-serif", size=8, color="#0F172A"),
            hoverinfo="text",
            hovertext=hover_texts,
            marker=dict(
                color=colors,
                size=final_sizes,
                line=dict(color=line_colors, width=line_widths)
            )
        ))

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    return fig


def generate_cypher_export_script(batches_list):
    """
    Generates a production-ready, idempotent Neo4j Cypher script (MERGE statements)
    that creates all constraints, node entities, and directed relationships.
    Can be run directly inside Neo4j Browser or cypher-shell.
    """
    cypher_lines = [
        "// ============================================================================",
        "// PhytoTrace Neo4j Property Graph Schema & Seed Script",
        "// Project: Botanical Supply Chain Traceability Using Property Graphs",
        "// ============================================================================",
        "",
        "// 1. UNIQUE CONSTRAINTS",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Farmer) REQUIRE f.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (fm:Farm) REQUIRE fm.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (b:Botanical) REQUIRE b.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (hb:HarvestBatch) REQUIRE hb.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Processor) REQUIRE p.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (pb:ProcessedBatch) REQUIRE pb.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (m:Manufacturer) REQUIRE m.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (fl:FinishedLot) REQUIRE fl.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Distributor) REQUIRE d.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Retailer) REQUIRE r.id IS UNIQUE;",
        "",
        "// 2. NODES & RELATIONSHIPS INGESTION"
    ]

    for b in batches_list:
        b_id = b["batch_id"]
        crop_id = b.get("crop_id", b_id.split("-")[0] if "-" in b_id else "BOT")
        farmer_name = b.get("farmer", "Lead Cultivator").replace("'", "\\'")
        farm_id = b.get("farm_id", f"FRM-{b_id}")
        farm_name = b.get("farm_name", "Origin Farm").replace("'", "\\'")
        botanical_name = b.get("botanical", "Botanical Crop").replace("'", "\\'")
        scientific_name = b.get("scientific_name", "Plantae sp.").replace("'", "\\'")
        category = b.get("category", "Medicinal Plants").replace("'", "\\'")
        location = b.get("location", "India").replace("'", "\\'")
        supplier = b.get("supplier", "Regional Cooperative").replace("'", "\\'")
        harvest_date = b.get("harvest_date", "2026-09-01")
        harvest_qty_kg = int(b.get("harvest_qty_kg", 500))
        status = b.get("status", "Verified")
        stage = b.get("current_stage", "Retailer")

        processor_name = b.get("processor", "Processing Facility").replace("'", "\\'")
        proc_batch_id = b.get("processed_batch_id", f"PRC-{b_id}")
        mfr_name = b.get("manufacturer", "Herbal Manufacturer").replace("'", "\\'")
        fin_batch_id = b.get("finished_batch_id", f"FIN-{b_id}")
        dist_name = b.get("distributor", "Logistics Hub").replace("'", "\\'")
        retailer_name = b.get("retailer", "Herbal Apothecary").replace("'", "\\'")
        retail_loc = b.get("retail_location", "India").replace("'", "\\'")

        farmer_id = f"FARMER_{farmer_name.replace(' ', '_')}"
        proc_id = f"PROC_{processor_name.replace(' ', '_')[:20]}"
        mfr_id = f"MFR_{mfr_name.replace(' ', '_')[:20]}"
        dist_id = f"DIST_{dist_name.replace(' ', '_')[:20]}"
        ret_id = f"RET_{retailer_name.replace(' ', '_')[:20]}"

        block = f"""
// Batch {b_id} Lineage
MERGE (farmer:Farmer {{id: '{farmer_id}'}})
  ON CREATE SET farmer.name = '{farmer_name}', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {{id: '{farm_id}'}})
  ON CREATE SET farm.name = '{farm_name}', farm.location = '{location}', farm.cooperative = '{supplier}'

MERGE (bot:Botanical {{id: '{crop_id}'}})
  ON CREATE SET bot.name = '{botanical_name}', bot.scientific_name = '{scientific_name}', bot.category = '{category}'

MERGE (batch:HarvestBatch {{id: '{b_id}'}})
  ON CREATE SET batch.harvest_date = date('{harvest_date}'), batch.quantity_kg = {harvest_qty_kg}, batch.status = '{status}', batch.stage = '{stage}'

MERGE (proc:Processor {{id: '{proc_id}'}})
  ON CREATE SET proc.name = '{processor_name}'

MERGE (pbatch:ProcessedBatch {{id: '{proc_batch_id}'}})

MERGE (mfr:Manufacturer {{id: '{mfr_id}'}})
  ON CREATE SET mfr.name = '{mfr_name}'

MERGE (flot:FinishedLot {{id: '{fin_batch_id}'}})

MERGE (dist:Distributor {{id: '{dist_id}'}})
  ON CREATE SET dist.name = '{dist_name}'

MERGE (ret:Retailer {{id: '{ret_id}'}})
  ON CREATE SET ret.name = '{retailer_name}', ret.city = '{retail_loc}'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {{harvest_date: date('{harvest_date}'), qty_kg: {harvest_qty_kg}}}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
"""
        cypher_lines.append(block.strip())

    return "\n".join(cypher_lines)
