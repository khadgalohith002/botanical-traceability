"""
PhytoTrace - Multilingual Botanical Supply Chain Traceability Using Property Graphs
===================================================================================
A production-quality Streamlit application featuring:
1. Multilingual Voice-Assisted Farmer Mode (12 Indian Languages + English)
2. Detailed Stitch-inspired Admin Dashboard for Supply Chain Analysis
3. Grounded Academic Demonstration Data with Neo4j live-check / Demo Mode

Author: College Micro-Project Demonstration
"""

import json
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Import dedicated translations dictionary and botanical crop catalog
from translations import LANGUAGES, TRANSLATIONS, t
from crop_catalog import (
    CROP_CATALOG,
    CATEGORIES,
    get_crop_by_id,
    get_crop_by_name,
    get_crops_by_category,
    format_crop_display,
    get_category_label,
    get_not_listed_label,
    get_not_listed_notice,
    get_crop_color_map,
    NOT_LISTED_ID,
)
from graph_engine import (
    build_supply_chain_graph,
    get_graph_metrics,
    compute_degree_centrality,
    trace_batch_path,
    render_graph_network_plot,
    generate_cypher_export_script,
)

# Persistent batch storage
BATCHES_PERSIST_FILE = "custom_batches.json"

def load_persisted_batches():
    if os.path.exists(BATCHES_PERSIST_FILE):
        try:
            with open(BATCHES_PERSIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_persisted_batches(batches_list):
    try:
        with open(BATCHES_PERSIST_FILE, "w", encoding="utf-8") as f:
            json.dump(batches_list, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="PhytoTrace | Multilingual Botanical Supply Chain",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 2. SESSION STATE & LANGUAGE SETUP
# ==============================================================================
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = "farmer"  # Default to Farmer Mode or Admin

if "custom_batches" not in st.session_state:
    st.session_state["custom_batches"] = load_persisted_batches()

if "voice_transcript" not in st.session_state:
    st.session_state["voice_transcript"] = ""

# ==============================================================================
# 3. NEO4J CONNECTION STATUS (REAL CONNECTION CHECK)
# ==============================================================================
@st.cache_data(ttl=60)
def check_neo4j_live_connection():
    """Safely checks if a local Neo4j instance is actually reachable."""
    try:
        import neo4j
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"), connection_timeout=1.0)
        with driver.session() as session:
            res = session.run("RETURN 1 AS connected")
            rec = res.single()
            if rec and rec["connected"] == 1:
                return True, "Connected to Neo4j (bolt://localhost:7687)"
    except Exception:
        pass
    return False, "Demo Mode (In-Memory Graph Schema)"

is_neo4j_connected, neo4j_status_label = check_neo4j_live_connection()

# ==============================================================================
# 4. MASTER DEMONSTRATION DATASET (UNIFIED & DYNAMIC)
# ==============================================================================
@st.cache_data
def get_base_demonstration_data():
    """Initial base batches for diverse botanical crops across Indian agricultural hubs."""
    base_batches = [
        {
            "batch_id": "TUR-2026-001",
            "crop_id": "TUR",
            "category": "Roots & Rhizomes",
            "botanical": "Turmeric",
            "scientific_name": "Curcuma longa",
            "variety": "Alleppey Finger",
            "farmer": "Rajesh V. Kurup",
            "farm_id": "FRM-KL-001",
            "farm_name": "Sahyadri Bio-Farms",
            "location": "Wayanad, Kerala",
            "supplier": "Western Ghats Organic Farmers Coop",
            "harvest_date": "2026-08-14",
            "harvest_qty_kg": 850,
            "processor": "Nilgiri Botanical Extraction Facility",
            "processed_batch_id": "PRC-TUR-001",
            "manufacturer": "AyurPharma Formulation Labs",
            "finished_batch_id": "FIN-TUR-001",
            "distributor": "South Zone Agro-Logistics Depot",
            "retailer": "PureBotanics Herbal Dispensary",
            "retail_location": "Bengaluru, Karnataka",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Completed full 10-tier custody pipeline."
        },
        {
            "batch_id": "NEE-2026-002",
            "crop_id": "NEE",
            "category": "Medicinal Plants",
            "botanical": "Neem",
            "scientific_name": "Azadirachta indica",
            "variety": "Wildcraft Kernel",
            "farmer": "K. Ramanathan",
            "farm_id": "FRM-TN-002",
            "farm_name": "Vaigai Agro-Forestry Plot",
            "location": "Madurai, Tamil Nadu",
            "supplier": "Vaigai Herbal Producers Collective",
            "harvest_date": "2026-08-28",
            "harvest_qty_kg": 1100,
            "processor": "Tamil Nadu Bio-Refinery Unit 4",
            "processed_batch_id": "PRC-NEE-002",
            "manufacturer": "Kaveri Eco-Agro Solutions",
            "finished_batch_id": "FIN-NEE-002",
            "distributor": "Tamil Nadu Freight Corridor Hub",
            "retailer": "GreenEarth Natural Agri-Store",
            "retail_location": "Chennai, Tamil Nadu",
            "current_stage": "Distributor",
            "simple_stage": "stage_packaged",
            "status": "In Transit",
            "notes": "Consignment in transit between manufacturer and central depot."
        },
        {
            "batch_id": "TUR-2026-003",
            "crop_id": "TUR",
            "category": "Roots & Rhizomes",
            "botanical": "Turmeric",
            "scientific_name": "Curcuma longa",
            "variety": "Erode Yellow",
            "farmer": "S. Murugesan",
            "farm_id": "FRM-TN-003",
            "farm_name": "Bhavani River Basin Farm",
            "location": "Erode, Tamil Nadu",
            "supplier": "Erode Turmeric Cultivators FPO",
            "harvest_date": "2026-09-02",
            "harvest_qty_kg": 1250,
            "processor": "Erode Agro-Steam Drying & Milling",
            "processed_batch_id": "PRC-TUR-003",
            "manufacturer": "Sanjivani Herbal Formulations",
            "finished_batch_id": "FIN-TUR-003",
            "distributor": "Regional Freight Terminal (Coimbatore)",
            "retailer": "VedaLife Ayurvedic Center",
            "retail_location": "Mysuru, Karnataka",
            "current_stage": "Manufacturer",
            "simple_stage": "stage_processing",
            "status": "Verified",
            "notes": "Under secondary encapsulation at manufacturing stage."
        },
        {
            "batch_id": "NEE-2026-004",
            "crop_id": "NEE",
            "category": "Medicinal Plants",
            "botanical": "Neem",
            "scientific_name": "Azadirachta indica",
            "variety": "Western Ghats Seed",
            "farmer": "Manjunath Hegde",
            "farm_id": "FRM-KA-004",
            "farm_name": "Malnad Eco-Grove",
            "location": "Shivamogga, Karnataka",
            "supplier": "Malnad Bio-Commons Producer Co.",
            "harvest_date": "2026-09-10",
            "harvest_qty_kg": 720,
            "processor": "Malnad Cold-Press Oil Mill",
            "processed_batch_id": "PRC-NEE-004",
            "manufacturer": "BioProtect Plant Nutrition",
            "finished_batch_id": "FIN-NEE-004",
            "distributor": "Western Karnataka Logistics Node",
            "retailer": "Krishi Seva Kendra Dispensary",
            "retail_location": "Dharwad, Karnataka",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Delivered to retail shelves and logged."
        },
        {
            "batch_id": "TUR-2026-005",
            "crop_id": "TUR",
            "category": "Roots & Rhizomes",
            "botanical": "Turmeric",
            "scientific_name": "Curcuma longa",
            "variety": "Lakadong Super-Grade",
            "farmer": "Jayanti Pradhan",
            "farm_id": "FRM-OD-005",
            "farm_name": "Kandhamal Tribal Agro-Commons",
            "location": "Kandhamal, Odisha",
            "supplier": "Odisha Tribal Forest Products Federation",
            "harvest_date": "2026-09-18",
            "harvest_qty_kg": 680,
            "processor": "Tribal Supercritical CO2 Facility",
            "processed_batch_id": "PRC-TUR-005",
            "manufacturer": "Eastern Phyto-Chemicals",
            "finished_batch_id": "FIN-TUR-005",
            "distributor": "Eastern Express Transit Depot",
            "retailer": "HerbalCraft Apothecary",
            "retail_location": "Kolkata, West Bengal",
            "current_stage": "Processor",
            "simple_stage": "stage_processing",
            "status": "In Transit",
            "notes": "Bulk rhizome mass in transit to supercritical extraction unit."
        },
        {
            "batch_id": "NEE-2026-006",
            "crop_id": "NEE",
            "category": "Medicinal Plants",
            "botanical": "Neem",
            "scientific_name": "Azadirachta indica",
            "variety": "Charotar Standardized Foliage",
            "farmer": "Bhavesh Patel",
            "farm_id": "FRM-GJ-006",
            "farm_name": "Charotar Botanical Grove",
            "location": "Anand, Gujarat",
            "supplier": "Charotar Medicinal Crops Guild",
            "harvest_date": "2026-09-25",
            "harvest_qty_kg": 540,
            "processor": "Gujarat Bio-Derivatives Unit (Vadodara)",
            "processed_batch_id": "PRC-NEE-006 (Pending)",
            "manufacturer": "Pending Processor Intake",
            "finished_batch_id": "Pending",
            "distributor": "Pending",
            "retailer": "Pending",
            "retail_location": "Pending",
            "current_stage": "Processor",
            "simple_stage": "stage_processing",
            "status": "Pending Verification",
            "notes": "Harvest batch flagged for intake moisture check before processing."
        },
        {
            "batch_id": "TUR-2026-007",
            "crop_id": "TUR",
            "category": "Roots & Rhizomes",
            "botanical": "Turmeric",
            "scientific_name": "Curcuma longa",
            "variety": "Rajapore Golden",
            "farmer": "Aniket Patil",
            "farm_id": "FRM-MH-007",
            "farm_name": "Krishna Valley Bio-Farm",
            "location": "Sangli, Maharashtra",
            "supplier": "Sangli Botanical Aggregators Union",
            "harvest_date": "2026-09-29",
            "harvest_qty_kg": 960,
            "processor": "Krishna Valley Dehydration Facility",
            "processed_batch_id": "PRC-TUR-007",
            "manufacturer": "Nectar Vedic Formulations",
            "finished_batch_id": "FIN-TUR-007",
            "distributor": "Mumbai Central Freight Hub",
            "retailer": "Apex Organic Market",
            "retail_location": "Mumbai, Maharashtra",
            "current_stage": "Manufacturer",
            "simple_stage": "stage_processing",
            "status": "Verified",
            "notes": "Bulk formulation completed; batch awaiting primary packaging."
        },
        {
            "batch_id": "NEE-2026-008",
            "crop_id": "NEE",
            "category": "Medicinal Plants",
            "botanical": "Neem",
            "scientific_name": "Azadirachta indica",
            "variety": "Mysuru Agro-Seed",
            "farmer": "Suresh Gowda",
            "farm_id": "FRM-KA-008",
            "farm_name": "Chamundi Agro-Forestry",
            "location": "Mysuru, Karnataka",
            "supplier": "Cauvery Basin Farmers Collective",
            "harvest_date": "2026-10-04",
            "harvest_qty_kg": 480,
            "processor": "Pending Processor Allocation",
            "processed_batch_id": "Pending",
            "manufacturer": "Pending",
            "finished_batch_id": "Pending",
            "distributor": "Pending",
            "retailer": "Pending",
            "retail_location": "Pending",
            "current_stage": "Harvest Batch",
            "simple_stage": "stage_harvested",
            "status": "Pending Verification",
            "notes": "Fresh intake logged at collection center; farm provenance review pending."
        },
        {
            "batch_id": "TUL-2026-009",
            "crop_id": "TUL",
            "category": "Herbs",
            "botanical": "Tulsi / Holy Basil",
            "scientific_name": "Ocimum tenuiflorum",
            "variety": "Krishna Tulsi",
            "farmer": "Devendra Joshi",
            "farm_id": "FRM-UK-009",
            "farm_name": "Haridwar Bio-Herbal Grove",
            "location": "Haridwar, Uttarakhand",
            "supplier": "Himalayan Herb Producers FPO",
            "harvest_date": "2026-09-20",
            "harvest_qty_kg": 420,
            "processor": "Ganga Bio-Extracts Plant",
            "processed_batch_id": "PRC-TUL-009",
            "manufacturer": "Rishi Herbals Manufacturing",
            "finished_batch_id": "FIN-TUL-009",
            "distributor": "North India Agro Transit Hub",
            "retailer": "AyurVeda Sanjeevani Store",
            "retail_location": "Dehradun, Uttarakhand",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Wild-certified holy basil leaves processed and packaged."
        },
        {
            "batch_id": "ASH-2026-010",
            "crop_id": "ASH",
            "category": "Medicinal Plants",
            "botanical": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "variety": "Nagori Premium Root",
            "farmer": "Balram Singh",
            "farm_id": "FRM-MP-010",
            "farm_name": "Malwa Agro-Commons",
            "location": "Neemuch, Madhya Pradesh",
            "supplier": "Malwa Medicinal Crops Guild",
            "harvest_date": "2026-09-22",
            "harvest_qty_kg": 650,
            "processor": "Central India Alkaloid Extraction Lab",
            "processed_batch_id": "PRC-ASH-010",
            "manufacturer": "VedaRoot Health Science",
            "finished_batch_id": "FIN-ASH-010",
            "distributor": "Indore Regional Logistics Center",
            "retailer": "PureBotanics Herbal Dispensary",
            "retail_location": "Bhopal, Madhya Pradesh",
            "current_stage": "Distributor",
            "simple_stage": "stage_packaged",
            "status": "In Transit",
            "notes": "Standardized withanolides consignment dispatched to regional depot."
        },
        {
            "batch_id": "GIN-2026-011",
            "crop_id": "GIN",
            "category": "Roots & Rhizomes",
            "botanical": "Ginger",
            "scientific_name": "Zingiber officinale",
            "variety": "Maran High-Oleoresin",
            "farmer": "Biddappa Somanna",
            "farm_id": "FRM-KA-011",
            "farm_name": "Coorg Organic Valley",
            "location": "Kodagu, Karnataka",
            "supplier": "Western Ghats Ginger Collective",
            "harvest_date": "2026-09-27",
            "harvest_qty_kg": 980,
            "processor": "Malnad Steam Dehydration Facility",
            "processed_batch_id": "PRC-GIN-011",
            "manufacturer": "Nectar Vedic Formulations",
            "finished_batch_id": "FIN-GIN-011",
            "distributor": "Mysuru Agro Freight Node",
            "retailer": "GreenEarth Natural Agri-Store",
            "retail_location": "Bengaluru, Karnataka",
            "current_stage": "Manufacturer",
            "simple_stage": "stage_processing",
            "status": "Verified",
            "notes": "Rhizome batch under primary maceration and encapsulation."
        },
        {
            "batch_id": "AML-2026-012",
            "crop_id": "AML",
            "category": "Medicinal Plants",
            "botanical": "Amla / Indian Gooseberry",
            "scientific_name": "Phyllanthus emblica",
            "variety": "Banarasi Standard",
            "farmer": "Ramakant Shukla",
            "farm_id": "FRM-UP-012",
            "farm_name": "Awadh Agro-Grove",
            "location": "Pratapgarh, Uttar Pradesh",
            "supplier": "Awadh Bio-Horticulture Producers",
            "harvest_date": "2026-10-01",
            "harvest_qty_kg": 1450,
            "processor": "Awadh Cold-Pressed Juice Lab",
            "processed_batch_id": "PRC-AML-012",
            "manufacturer": "Chyawanprash Formulation Center",
            "finished_batch_id": "FIN-AML-012",
            "distributor": "Varanasi Cargo Hub",
            "retailer": "Krishi Seva Kendra Dispensary",
            "retail_location": "Lucknow, Uttar Pradesh",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "High Vitamin C certificate verified and distributed."
        },
        {
            "batch_id": "BLP-2026-013",
            "crop_id": "BLP",
            "category": "Spices",
            "botanical": "Black Pepper",
            "scientific_name": "Piper nigrum",
            "variety": "Panniyur-1 Grade A",
            "farmer": "Thomas Chacko",
            "farm_id": "FRM-KL-013",
            "farm_name": "High Range Spices Ridge",
            "location": "Idukki, Kerala",
            "supplier": "Cardamom Hills Spices Guild",
            "harvest_date": "2026-10-02",
            "harvest_qty_kg": 520,
            "processor": "Kochi Supercritical Oleoresin Unit",
            "processed_batch_id": "PRC-BLP-013",
            "manufacturer": "SpiceHeritage Agro-Tech",
            "finished_batch_id": "Pending",
            "distributor": "Pending",
            "retailer": "Pending",
            "retail_location": "Pending",
            "current_stage": "Processor",
            "simple_stage": "stage_processing",
            "status": "In Transit",
            "notes": "Bulk sun-dried peppercorn consignment en route to supercritical processor."
        },
        {
            "batch_id": "CAR-2026-014",
            "crop_id": "CAR",
            "category": "Spices",
            "botanical": "Cardamom",
            "scientific_name": "Elettaria cardamomum",
            "variety": "Malabar Extra Bold 8mm",
            "farmer": "K. J. Mathew",
            "farm_id": "FRM-KL-014",
            "farm_name": "Periyar Hills Plantation",
            "location": "Thekkady, Kerala",
            "supplier": "Kerala Spices Growers Society",
            "harvest_date": "2026-10-03",
            "harvest_qty_kg": 310,
            "processor": "Periyar Automated Curing Kilns",
            "processed_batch_id": "PRC-CAR-014",
            "manufacturer": "AromaPharma Exports",
            "finished_batch_id": "FIN-CAR-014",
            "distributor": "Cochin Port Transit Depot",
            "retailer": "Apothecary International",
            "retail_location": "Kochi, Kerala",
            "current_stage": "Distributor",
            "simple_stage": "stage_packaged",
            "status": "Verified",
            "notes": "GI-tagged green cardamom lot vacuum packaged for distribution."
        },
        {
            "batch_id": "GIL-2026-015",
            "crop_id": "GIL",
            "category": "Medicinal Plants",
            "botanical": "Giloy",
            "scientific_name": "Tinospora cordifolia",
            "variety": "Amrithavalli Desi",
            "farmer": "Mangal Ram Netam",
            "farm_id": "FRM-CG-015",
            "farm_name": "Bastar Bio-Commons",
            "location": "Bastar, Chhattisgarh",
            "supplier": "Dandakaranya Tribal Forest Federation",
            "harvest_date": "2026-10-05",
            "harvest_qty_kg": 460,
            "processor": "Pending Processor Intake",
            "processed_batch_id": "Pending",
            "manufacturer": "Pending",
            "finished_batch_id": "Pending",
            "distributor": "Pending",
            "retailer": "Pending",
            "retail_location": "Pending",
            "current_stage": "Harvest Batch",
            "simple_stage": "stage_harvested",
            "status": "Pending Verification",
            "notes": "Freshly harvested stem cuttings submitted to regional tribal aggregator."
        },
        {
            "batch_id": "ALO-2026-016",
            "crop_id": "ALO",
            "category": "Medicinal Plants",
            "botanical": "Aloe Vera",
            "scientific_name": "Aloe vera",
            "variety": "Barbadensis Miller",
            "farmer": "Shrawan Bishnoi",
            "farm_id": "FRM-RJ-016",
            "farm_name": "Thar Green Agro-Belt",
            "location": "Barmer, Rajasthan",
            "supplier": "Marwar Arid Herbs Collective",
            "harvest_date": "2026-10-06",
            "harvest_qty_kg": 1400,
            "processor": "Jaipur Cold-Filtration Gel Refinery",
            "processed_batch_id": "PRC-ALO-016",
            "manufacturer": "DesertVedic Cosmeceuticals",
            "finished_batch_id": "FIN-ALO-016",
            "distributor": "Northern Logistics Corridor",
            "retailer": "Apex Organic Market",
            "retail_location": "Jaipur, Rajasthan",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Aloin-free cold extracted gel certified and shelved."
        },
        {
            "batch_id": "MOR-2026-017",
            "crop_id": "MOR",
            "category": "Herbs",
            "botanical": "Moringa",
            "scientific_name": "Moringa oleifera",
            "variety": "PKM-1 Super Leaf",
            "farmer": "S. Murugesan",
            "farm_id": "FRM-TN-017",
            "farm_name": "Theni Bio-Greens Plantation",
            "location": "Theni, Tamil Nadu",
            "supplier": "Vaigai Herbal Producers Collective",
            "harvest_date": "2026-10-07",
            "harvest_qty_kg": 890,
            "processor": "Theni Solar Dehydration & Powdering Unit",
            "processed_batch_id": "PRC-MOR-017",
            "manufacturer": "GreenLife Phyto-Nutrition",
            "finished_batch_id": "FIN-MOR-017",
            "distributor": "Madurai Cargo Logistics",
            "retailer": "Krishi Seva Kendra Dispensary",
            "retail_location": "Madurai, Tamil Nadu",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Certified leaf powder batch delivered to dispensaries."
        },
        {
            "batch_id": "BRA-2026-018",
            "crop_id": "BRA",
            "category": "Medicinal Plants",
            "botanical": "Brahmi",
            "scientific_name": "Bacopa monnieri",
            "variety": "Subodhak High-Bacoside",
            "farmer": "Subhash Mondal",
            "farm_id": "FRM-WB-018",
            "farm_name": "Sundarban Wetlands Agro-Grove",
            "location": "South 24 Parganas, West Bengal",
            "supplier": "Bengal Coastal Med-Herbs Society",
            "harvest_date": "2026-10-08",
            "harvest_qty_kg": 380,
            "processor": "Kolkata Phyto-Chemicals Lab",
            "processed_batch_id": "PRC-BRA-018",
            "manufacturer": "Smriti Medha Formulations",
            "finished_batch_id": "FIN-BRA-018",
            "distributor": "Eastern Express Transit Depot",
            "retailer": "HerbalCraft Apothecary",
            "retail_location": "Kolkata, West Bengal",
            "current_stage": "Distributor",
            "simple_stage": "stage_packaged",
            "status": "In Transit",
            "notes": "Standardized bacoside lot en route to regional apothecary."
        },
        {
            "batch_id": "SHA-2026-019",
            "crop_id": "SHA",
            "category": "Roots & Rhizomes",
            "botanical": "Shatavari",
            "scientific_name": "Asparagus racemosus",
            "variety": "Kalyani Tuberous",
            "farmer": "Ghanshyam Meena",
            "farm_id": "FRM-MP-019",
            "farm_name": "Satpura Mountain Agro-Commons",
            "location": "Hoshangabad, Madhya Pradesh",
            "supplier": "Narmada Valley Herbal Guild",
            "harvest_date": "2026-10-08",
            "harvest_qty_kg": 560,
            "processor": "Bhopal Root Processing Center",
            "processed_batch_id": "PRC-SHA-019",
            "manufacturer": "VedaRoot Health Science",
            "finished_batch_id": "FIN-SHA-019",
            "distributor": "Indore Regional Logistics Center",
            "retailer": "PureBotanics Herbal Dispensary",
            "retail_location": "Bhopal, Madhya Pradesh",
            "current_stage": "Manufacturer",
            "simple_stage": "stage_processing",
            "status": "Verified",
            "notes": "Peeled root mass under extraction protocol."
        },
        {
            "batch_id": "LEM-2026-020",
            "crop_id": "LEM",
            "category": "Herbs",
            "botanical": "Lemongrass",
            "scientific_name": "Cymbopogon citratus",
            "variety": "Sugandhi OD-19",
            "farmer": "George Varghese",
            "farm_id": "FRM-KL-020",
            "farm_name": "Anamudi Essential Herbs Estate",
            "location": "Munnar, Kerala",
            "supplier": "High Ranges Bio-Oil Cooperative",
            "harvest_date": "2026-10-09",
            "harvest_qty_kg": 740,
            "processor": "Munnar Steam Distillation Refinery",
            "processed_batch_id": "PRC-LEM-020",
            "manufacturer": "Kerala Natural Aromatics",
            "finished_batch_id": "FIN-LEM-020",
            "distributor": "Cochin Port Transit Depot",
            "retailer": "VedaLife Ayurvedic Center",
            "retail_location": "Kochi, Kerala",
            "current_stage": "Distributor",
            "simple_stage": "stage_packaged",
            "status": "Verified",
            "notes": "High-citral essential oil distillation completed."
        },
        {
            "batch_id": "PEP-2026-021",
            "crop_id": "PEP",
            "category": "Herbs",
            "botanical": "Peppermint",
            "scientific_name": "Mentha × piperita",
            "variety": "Kosi High-Menthol",
            "farmer": "Mahesh Chandra",
            "farm_id": "FRM-UP-021",
            "farm_name": "Rohilkhand Mentha Basin",
            "location": "Sambhal, Uttar Pradesh",
            "supplier": "North India Essential Oils Federation",
            "harvest_date": "2026-10-09",
            "harvest_qty_kg": 1120,
            "processor": "Sambhal Hydro-Distillation Plant",
            "processed_batch_id": "PRC-PEP-021",
            "manufacturer": "Himalaya Cool Herbals",
            "finished_batch_id": "FIN-PEP-021",
            "distributor": "North India Agro Transit Hub",
            "retailer": "AyurVeda Sanjeevani Store",
            "retail_location": "Delhi NCR",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Pharmaceutical grade menthol oil verified."
        },
        {
            "batch_id": "SEN-2026-022",
            "crop_id": "SEN",
            "category": "Herbs",
            "botanical": "Senna",
            "scientific_name": "Senna alexandrina",
            "variety": "Tinnevelly Export Standard",
            "farmer": "Laxman Ram",
            "farm_id": "FRM-RJ-022",
            "farm_name": "Jodhpur Arid Zone Cultivators",
            "location": "Jodhpur, Rajasthan",
            "supplier": "Marwar Arid Herbs Collective",
            "harvest_date": "2026-10-10",
            "harvest_qty_kg": 830,
            "processor": "Jodhpur Pod & Leaf Sorting Plant",
            "processed_batch_id": "PRC-SEN-022",
            "manufacturer": "DesertVedic Cosmeceuticals",
            "finished_batch_id": "FIN-SEN-022",
            "distributor": "Jaipur Logistics Terminal",
            "retailer": "Apex Organic Market",
            "retail_location": "Jaipur, Rajasthan",
            "current_stage": "Processor",
            "simple_stage": "stage_processing",
            "status": "In Transit",
            "notes": "Dried pods arriving at grading center for sennoside testing."
        },
        {
            "batch_id": "CIN-2026-023",
            "crop_id": "CIN",
            "category": "Spices",
            "botanical": "Cinnamon",
            "scientific_name": "Cinnamomum verum",
            "variety": "Navashree Ceylon Type",
            "farmer": "Antony Mathew",
            "farm_id": "FRM-KL-023",
            "farm_name": "Malabar Spice Enclave",
            "location": "Kannur, Kerala",
            "supplier": "Kerala Spices Growers Society",
            "harvest_date": "2026-10-10",
            "harvest_qty_kg": 290,
            "processor": "Kannur Quilling & Drying Center",
            "processed_batch_id": "PRC-CIN-023",
            "manufacturer": "SpiceHeritage Agro-Tech",
            "finished_batch_id": "FIN-CIN-023",
            "distributor": "Cochin Port Transit Depot",
            "retailer": "Apothecary International",
            "retail_location": "Kochi, Kerala",
            "current_stage": "Manufacturer",
            "simple_stage": "stage_processing",
            "status": "Verified",
            "notes": "True cinnamon quills rolled and undergoing antimicrobial assay."
        },
        {
            "batch_id": "CLO-2026-024",
            "crop_id": "CLO",
            "category": "Spices",
            "botanical": "Clove",
            "scientific_name": "Syzygium aromaticum",
            "variety": "Kanyakumari Head Grade",
            "farmer": "N. Selvaraj",
            "farm_id": "FRM-TN-024",
            "farm_name": "Marunthuvazh Hills Plantation",
            "location": "Kanyakumari, Tamil Nadu",
            "supplier": "Southern Tip Spices Collective",
            "harvest_date": "2026-10-10",
            "harvest_qty_kg": 210,
            "processor": "Kanyakumari Solar Drying Kilns",
            "processed_batch_id": "PRC-CLO-024",
            "manufacturer": "AromaPharma Exports",
            "finished_batch_id": "FIN-CLO-024",
            "distributor": "Regional Freight Terminal (Coimbatore)",
            "retailer": "VedaLife Ayurvedic Center",
            "retail_location": "Madurai, Tamil Nadu",
            "current_stage": "Harvest Batch",
            "simple_stage": "stage_harvested",
            "status": "Pending Verification",
            "notes": "Sun-dried flower buds pending essential oil volatile checks."
        },
        {
            "batch_id": "COR-2026-025",
            "crop_id": "COR",
            "category": "Spices",
            "botanical": "Coriander",
            "scientific_name": "Coriandrum sativum",
            "variety": "Kumbhraj Special",
            "farmer": "Dinesh Patidar",
            "farm_id": "FRM-MP-025",
            "farm_name": "Malwa Spice Fields",
            "location": "Guna, Madhya Pradesh",
            "supplier": "Central India Spice Producers FPO",
            "harvest_date": "2026-10-11",
            "harvest_qty_kg": 940,
            "processor": "Guna Automated Cleaning & Milling Plant",
            "processed_batch_id": "PRC-COR-025",
            "manufacturer": "PureSpices Botanical Formulation",
            "finished_batch_id": "FIN-COR-025",
            "distributor": "Indore Regional Logistics Center",
            "retailer": "Apex Organic Market",
            "retail_location": "Bhopal, Madhya Pradesh",
            "current_stage": "Processor",
            "simple_stage": "stage_processing",
            "status": "Verified",
            "notes": "Green coriander seed consignment milled under low-temperature protocol."
        },
        {
            "batch_id": "FEN-2026-026",
            "crop_id": "FEN",
            "category": "Spices",
            "botanical": "Fenugreek",
            "scientific_name": "Trigonella foenum-graecum",
            "variety": "Methi Pusa Early",
            "farmer": "Pravin Bhai Patel",
            "farm_id": "FRM-GJ-026",
            "farm_name": "Mehsana Agro-Commons",
            "location": "Mehsana, Gujarat",
            "supplier": "Gujarat Organic Growers Guild",
            "harvest_date": "2026-10-11",
            "harvest_qty_kg": 670,
            "processor": "Ahmedabad Supercritical Extraction Facility",
            "processed_batch_id": "PRC-FEN-026",
            "manufacturer": "BioProtect Plant Nutrition",
            "finished_batch_id": "FIN-FEN-026",
            "distributor": "Western Karnataka Logistics Node",
            "retailer": "GreenEarth Natural Agri-Store",
            "retail_location": "Ahmedabad, Gujarat",
            "current_stage": "Retailer",
            "simple_stage": "stage_delivered",
            "status": "Verified",
            "notes": "Standardized saponin content lot delivered to retail inventory."
        }
    ]
    return base_batches

def get_active_batches_df():
    """Combines base demonstration batches with newly registered batches from Farmer Mode."""
    all_data = get_base_demonstration_data() + st.session_state["custom_batches"]
    return pd.DataFrame(all_data)

df_batches = get_active_batches_df()

# Compute consistent mathematical metrics
df_farms = df_batches.groupby(["farm_id", "farm_name", "location", "botanical", "scientific_name", "category", "supplier", "farmer"]).agg(
    total_harvest_kg=("harvest_qty_kg", "sum"),
    batch_count=("batch_id", "count")
).reset_index()

df_suppliers = df_batches.groupby("supplier").agg(
    farms_represented=("farm_id", "nunique"),
    crops_handled=("botanical", "nunique"),
    total_volume_kg=("harvest_qty_kg", "sum"),
    active_batches=("batch_id", "count")
).reset_index()

TOTAL_FARMS = df_farms["farm_id"].nunique()
TOTAL_SUPPLIERS = df_suppliers["supplier"].nunique()
TOTAL_BATCHES = len(df_batches)
TOTAL_PENDING = len(df_batches[df_batches["status"] == "Pending Verification"])
TOTAL_HARVEST_KG = df_batches["harvest_qty_kg"].sum()
TOTAL_CROPS = df_batches["botanical"].nunique()

# Build in-memory NetworkX property graph with 10 node labels and 9 directed relationships
G_supply_chain = build_supply_chain_graph(df_batches.to_dict(orient="records"))
graph_metrics = get_graph_metrics(G_supply_chain)

# ==============================================================================
# 5. CSS STYLING WITH UNICODE & RTL (URDU) SUPPORT
# ==============================================================================
curr_lang = st.session_state["lang"]
is_rtl = LANGUAGES.get(curr_lang, {}).get("rtl", False)
lang_dir = "rtl" if is_rtl else "ltr"

APP_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* Global Typography & Direction */
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: #F4F6F4 !important;
        font-family: 'Hanken Grotesk', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #202820 !important;
        direction: {lang_dir};
    }}

    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2.8rem !important;
        padding-left: 1.6rem !important;
        padding-right: 1.6rem !important;
        max-width: 1400px !important;
    }}

    /* Force all text in main content to dark #202820 */
    .main, 
    .main p, 
    .main span, 
    .main div, 
    .main label, 
    .main h1, 
    .main h2, 
    .main h3, 
    .main h4,
    [data-testid="stMain"],
    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label {{
        color: #202820;
    }}

    /* FIX TEXT CONTRAST: Streamlit Widget Labels in Main Area */
    .main [data-testid="stWidgetLabel"] label,
    .main [data-testid="stWidgetLabel"] label p,
    .main [data-testid="stWidgetLabel"] p,
    .main [data-testid="stWidgetLabel"] span,
    .main [data-testid="stWidgetLabel"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"] label,
    [data-testid="stMain"] [data-testid="stWidgetLabel"] label p,
    [data-testid="stMain"] [data-testid="stWidgetLabel"] p {{
        color: #202820 !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
        line-height: 1.4 !important;
    }}

    /* Radio Group options in Main Area */
    .main div[role="radiogroup"],
    [data-testid="stMain"] div[role="radiogroup"] {{
        gap: 12px !important;
    }}

    .main div[role="radiogroup"] label,
    [data-testid="stMain"] div[role="radiogroup"] label {{
        color: #202820 !important;
        background-color: #F8FAF8 !important;
        border: 1px solid #D8E2DC !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }}

    .main div[role="radiogroup"] label:hover,
    [data-testid="stMain"] div[role="radiogroup"] label:hover {{
        background-color: #EDFAF3 !important;
        border-color: #26734D !important;
    }}

    .main div[role="radiogroup"] label[data-checked="true"],
    .main div[role="radiogroup"] label:has(input:checked),
    [data-testid="stMain"] div[role="radiogroup"] label[data-checked="true"],
    [data-testid="stMain"] div[role="radiogroup"] label:has(input:checked) {{
        background-color: #EDFAF3 !important;
        border: 2px solid #26734D !important;
    }}

    .main div[role="radiogroup"] label p,
    [data-testid="stMain"] div[role="radiogroup"] label p,
    .main div[role="radiogroup"] label span,
    [data-testid="stMain"] div[role="radiogroup"] label span {{
        color: #202820 !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
    }}

    /* Inputs (Text, Number, Date) in Main Area */
    .main input,
    .main input[type="text"],
    .main input[type="number"],
    [data-testid="stMain"] input {{
        color: #202820 !important;
        background-color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }}

    .main div[data-baseweb="input"],
    [data-testid="stMain"] div[data-baseweb="input"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #D8E2DC !important;
        border-radius: 8px !important;
    }}

    .main div[data-baseweb="input"]:focus-within,
    [data-testid="stMain"] div[data-baseweb="input"]:focus-within {{
        border-color: #26734D !important;
        box-shadow: 0 0 0 2px rgba(38, 115, 77, 0.15) !important;
    }}

    /* Selectbox in Main Area */
    .main div[data-baseweb="select"],
    [data-testid="stMain"] div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #D8E2DC !important;
        border-radius: 8px !important;
    }}

    .main div[data-baseweb="select"] div,
    .main div[data-baseweb="select"] span,
    [data-testid="stMain"] div[data-baseweb="select"] div,
    [data-testid="stMain"] div[data-baseweb="select"] span {{
        color: #202820 !important;
        font-weight: 500 !important;
    }}

    /* Form Container Card */
    div[data-testid="stForm"],
    [data-testid="stMain"] div[data-testid="stForm"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #D8E2DC !important;
        border-radius: 12px !important;
        padding: 24px 28px !important;
        box-shadow: 0 2px 8px rgba(17, 45, 35, 0.04) !important;
        margin-top: 14px !important;
        margin-bottom: 18px !important;
    }}

    /* PRIMARY FORM SUBMIT BUTTON: Forest green (#26734D) with bold white text */
    div[data-testid="stFormSubmitButton"] button,
    button[kind="primaryFormSubmit"],
    button[data-testid="baseButton-primaryFormSubmit"],
    button[data-testid="baseButton-secondaryFormSubmit"],
    .main div[data-testid="stFormSubmitButton"] button {{
        background-color: #26734D !important;
        color: #FFFFFF !important;
        border: 1px solid #1E5638 !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px rgba(38, 115, 77, 0.25) !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        width: 100% !important;
    }}

    div[data-testid="stFormSubmitButton"] button:hover,
    button[kind="primaryFormSubmit"]:hover {{
        background-color: #1F5C3E !important;
        color: #FFFFFF !important;
        border-color: #16432C !important;
        box-shadow: 0 4px 10px rgba(38, 115, 77, 0.35) !important;
        transform: translateY(-1px) !important;
    }}

    div[data-testid="stFormSubmitButton"] button p,
    button[kind="primaryFormSubmit"] p,
    div[data-testid="stFormSubmitButton"] button span,
    button[kind="primaryFormSubmit"] span {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}

    /* Regular Buttons */
    .stButton button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}

    /* Cards */
    .white-card {{
        background-color: #FFFFFF;
        border: 1px solid #D8E2DC;
        border-radius: 10px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 1px 4px rgba(17, 45, 35, 0.04);
        color: #202820;
    }}

    /* Farmer Big Touch Cards */
    .farmer-touch-card {{
        background-color: #FFFFFF;
        border: 2px solid #D8E2DC;
        border-radius: 12px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(17, 45, 35, 0.05);
        cursor: pointer;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }}

    .farmer-touch-card:hover {{
        border-color: #26734D;
        transform: translateY(-2px);
    }}

    .touch-card-icon {{
        font-size: 2.2rem;
        margin-bottom: 8px;
    }}

    .touch-card-title {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 700;
        color: #202820;
        margin-bottom: 4px;
    }}

    .touch-card-desc {{
        font-size: 0.9rem;
        color: #424845;
        line-height: 1.35;
    }}

    /* Sidebar (#112D23) - Dark theme strictly scoped */
    section[data-testid="stSidebar"] {{
        background-color: #112D23 !important;
        border-right: 1px solid #0A1C15 !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #E2EBE5 !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {{
        color: #E2EBE5 !important;
        font-weight: 600 !important;
    }}

    .sidebar-brand-box {{
        padding: 8px 4px 16px 4px;
        border-bottom: 1px solid rgba(226, 235, 229, 0.15);
        margin-bottom: 14px;
    }}

    .sidebar-brand-title {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0;
        letter-spacing: -0.02em;
    }}

    .sidebar-brand-tag {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem;
        color: #A4C4B1 !important;
        margin-top: 2px;
    }}

    /* Sidebar Radio Buttons */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
        padding: 9px 12px !important;
        border-radius: 6px !important;
        color: #CAEADA !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.15s ease;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
        background-color: rgba(44, 105, 78, 0.3) !important;
        color: #FFFFFF !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
        background-color: #2C694E !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    /* Status Badges */
    .badge-chip {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.74rem;
        font-weight: 600;
    }}

    .badge-verified {{
        background-color: #CAEADA;
        color: #032017 !important;
    }}

    .badge-transit {{
        background-color: #E0F2FE;
        color: #0369A1 !important;
    }}

    .badge-pending {{
        background-color: #FEF3C7;
        color: #92400E !important;
        border: 1px solid #FDE68A;
    }}

    .badge-demo {{
        background-color: #F0F3FF;
        color: #334155 !important;
        border: 1px solid #D8E2DC;
    }}

    /* Stage Stepper for Farmers */
    .stage-step-box {{
        background: #F8FAF8;
        border: 1px solid #D8E2DC;
        border-radius: 8px;
        padding: 12px 14px;
        text-align: center;
        flex: 1;
        min-width: 120px;
    }}

    .stage-step-box.current {{
        border: 2px solid #26734D;
        background: #EAF4EE;
    }}

    .stage-step-title {{
        font-size: 0.86rem;
        font-weight: 700;
        color: #202820;
    }}

    .stage-step-sub {{
        font-size: 0.74rem;
        color: #64748B;
        margin-top: 2px;
    }}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

# ==============================================================================
# 6. REUSABLE PLOTLY STYLING
# ==============================================================================
def apply_chart_theme(fig, height=260):
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Hanken Grotesk, sans-serif", size=11, color="#1E293B"),
        xaxis=dict(
            tickfont=dict(family="JetBrains Mono", size=10, color="#64748B"),
            title_font=dict(family="Space Grotesk", size=11, color="#0F172A"),
            gridcolor="#F0F3FF",
            linecolor="#D8E2DC"
        ),
        yaxis=dict(
            tickfont=dict(family="JetBrains Mono", size=10, color="#64748B"),
            title_font=dict(family="Space Grotesk", size=11, color="#0F172A"),
            gridcolor="#F0F3FF",
            linecolor="#D8E2DC"
        ),
        legend=dict(
            font=dict(family="Hanken Grotesk", size=10, color="#1E293B"),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#D8E2DC",
            borderwidth=1
        )
    )
    return fig

# ==============================================================================
# 7. VOICE ASSISTANT COMPONENT (WEB SPEECH API + SPEECH SYNTHESIS)
# ==============================================================================
def render_voice_assistant_component(prompt_to_speak="", lang_code="en-IN"):
    """
    Renders a Web Speech API browser component for speech recognition and synthesis.
    Works natively in modern browsers (Chrome, Edge) with automatic fallback message.
    """
    safe_prompt = prompt_to_speak.replace('"', '\\"').replace("'", "\\'")
    speech_js = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <style>
            body {{
                font-family: 'Hanken Grotesk', -apple-system, sans-serif;
                margin: 0;
                padding: 12px;
                background: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #D8E2DC;
                color: #202820;
            }}
            .voice-controls {{
                display: flex;
                align-items: center;
                gap: 12px;
                flex-wrap: wrap;
            }}
            .mic-btn {{
                background-color: #26734D;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 700;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 2px 6px rgba(38, 115, 77, 0.25);
                transition: background-color 0.15s ease, transform 0.1s ease;
            }}
            .mic-btn:hover {{
                background-color: #1F5C3E;
                transform: translateY(-1px);
            }}
            .mic-btn.listening {{
                background-color: #DC2626 !important;
                animation: pulse 1.2s infinite;
            }}
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
                100% {{ opacity: 1; }}
            }}
            .stop-btn {{
                background-color: #F8FAF8;
                color: #202820;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.15s ease;
            }}
            .stop-btn:hover {{
                background-color: #EDFAF3;
                border-color: #26734D;
            }}
            .transcript-box {{
                margin-top: 10px;
                background: #F8FAF8;
                border: 1px solid #D8E2DC;
                border-radius: 6px;
                padding: 10px 14px;
                font-size: 13px;
                color: #202820;
                min-height: 24px;
            }}
            .error-box {{
                margin-top: 8px;
                color: #DC2626;
                font-size: 13px;
                font-weight: 600;
                display: none;
            }}
        </style>
    </head>
    <body>
        <div class="voice-controls">
            <button id="micBtn" class="mic-btn" onclick="toggleRecognition()">
                🎙️ {t('tap_to_speak', curr_lang)}
            </button>
            <button class="stop-btn" onclick="stopAllSpeech()">
                ⏹️ {t('stop_voice', curr_lang)}
            </button>
            <button class="stop-btn" onclick="speakCurrentPrompt()">
                {t('btn_speak_guidance', curr_lang)}
            </button>
        </div>
        <div id="transcriptBox" class="transcript-box">
            <i>Voice transcription and spoken feedback will appear here...</i>
        </div>
        <div id="errorBox" class="error-box"></div>

        <script>
            let recognition = null;
            let isListening = false;
            const langCode = "{lang_code}";
            const welcomeText = "{safe_prompt}";

            function initRecognition() {{
                const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRec) {{
                    document.getElementById('errorBox').style.display = 'block';
                    document.getElementById('errorBox').innerText = "{t('speech_not_supported', curr_lang)}";
                    return null;
                }}
                const rec = new SpeechRec();
                rec.lang = langCode;
                rec.continuous = false;
                rec.interimResults = true;

                rec.onstart = function() {{
                    isListening = true;
                    document.getElementById('micBtn').classList.add('listening');
                    document.getElementById('micBtn').innerHTML = "🔴 Listening... Speak now";
                    document.getElementById('errorBox').style.display = 'none';
                    document.getElementById('transcriptBox').innerHTML = "<i>Listening... Speak now into your microphone.</i>";
                }};

                rec.onresult = function(event) {{
                    let transcript = "";
                    for (let i = 0; i < event.results.length; i++) {{
                        transcript += event.results[i][0].transcript;
                    }}
                    document.getElementById('transcriptBox').innerHTML = "<b>Recognized:</b> " + transcript;
                }};

                rec.onerror = function(event) {{
                    document.getElementById('errorBox').style.display = 'block';
                    document.getElementById('errorBox').innerText = "Microphone error: " + event.error + ". Please ensure browser microphone permission is granted or type below.";
                    stopRecognition();
                }};

                rec.onend = function() {{
                    stopRecognition();
                }};

                return rec;
            }}

            function toggleRecognition() {{
                if (isListening) {{
                    stopRecognition();
                }} else {{
                    if (!recognition) recognition = initRecognition();
                    if (recognition) {{
                        try {{
                            recognition.start();
                        }} catch (e) {{
                            console.error(e);
                        }}
                    }}
                }}
            }}

            function stopRecognition() {{
                isListening = false;
                if (recognition) {{
                    try {{ recognition.stop(); }} catch(e) {{}}
                }}
                document.getElementById('micBtn').classList.remove('listening');
                document.getElementById('micBtn').innerHTML = "🎙️ {t('tap_to_speak', curr_lang)}";
            }}

            function stopAllSpeech() {{
                if (window.speechSynthesis) window.speechSynthesis.cancel();
                stopRecognition();
                const box = document.getElementById('transcriptBox');
                if (box) {{
                    box.innerHTML = "<i>Voice stopped. Tap microphone to speak again.</i>";
                }}
            }}

            function speakCurrentPrompt() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const text = welcomeText || "Welcome to PhytoTrace Botanical Traceability.";
                    const utter = new SpeechSynthesisUtterance(text);
                    utter.lang = langCode;
                    utter.rate = 0.95;
                    window.speechSynthesis.speak(utter);
                    document.getElementById('transcriptBox').innerHTML = "<b>Speaking:</b> " + text;
                }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(speech_js, height=145)

# ==============================================================================
# 8. SIDEBAR CONTROLS (LANGUAGE SELECTOR & MODE SWITCHER)
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand-box">
            <h1 class="sidebar-brand-title">🌿 PhytoTrace</h1>
            <div class="sidebar-brand-tag">Multilingual Supply Chain</div>
        </div>
    """, unsafe_allow_html=True)

    # 1. Prominent Language Selector
    lang_options = list(LANGUAGES.keys())
    def format_lang(code):
        return f"{LANGUAGES[code]['native']} ({LANGUAGES[code]['name']})"

    selected_lang_code = st.selectbox(
        t("language_select", curr_lang),
        options=lang_options,
        index=lang_options.index(st.session_state["lang"]),
        format_func=format_lang,
        key="lang_selector"
    )
    if selected_lang_code != st.session_state["lang"]:
        st.session_state["lang"] = selected_lang_code
        st.rerun()

    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid rgba(226, 235, 229, 0.15);' />", unsafe_allow_html=True)

    # 2. Application Mode Switcher (Farmer Mode vs Admin Dashboard)
    mode_options = ["farmer", "admin"]
    mode_labels = {
        "farmer": t("farmer_mode", curr_lang),
        "admin": t("admin_mode", curr_lang)
    }
    selected_mode = st.radio(
        t("mode_select", curr_lang),
        options=mode_options,
        index=0 if st.session_state["app_mode"] == "farmer" else 1,
        format_func=lambda x: mode_labels[x],
        key="mode_radio"
    )
    if selected_mode != st.session_state["app_mode"]:
        st.session_state["app_mode"] = selected_mode
        st.rerun()

    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid rgba(226, 235, 229, 0.15);' />", unsafe_allow_html=True)

    # 3. Dynamic Sub-Navigation based on Mode
    if st.session_state["app_mode"] == "farmer":
        farmer_nav_items = [
            "my_farm",
            "register_harvest",
            "track_batch",
            "collection_status",
            "voice_help"
        ]
        farmer_nav_labels = {
            "my_farm": f"🌾 {t('nav_my_farm', curr_lang)}",
            "register_harvest": f"📝 {t('nav_register', curr_lang)}",
            "track_batch": f"🔍 {t('nav_track', curr_lang)}",
            "collection_status": f"🚚 {t('nav_collection', curr_lang)}",
            "voice_help": f"🎙️ {t('nav_voice', curr_lang)}"
        }
        active_subpage = st.radio(
            "Farmer Menu",
            options=farmer_nav_items,
            format_func=lambda x: farmer_nav_labels[x],
            label_visibility="collapsed"
        )
    else:
        admin_nav_items = [
            "admin_dash",
            "admin_farms",
            "admin_batches",
            "admin_explorer",
            "admin_search",
            "admin_analytics"
        ]
        admin_nav_labels = {
            "admin_dash": "📊 Dashboard",
            "admin_farms": "🏡 Farms & Suppliers",
            "admin_batches": "🌿 Botanical Batches",
            "admin_explorer": "🌐 Supply Chain Explorer",
            "admin_search": "🔍 Traceability Search",
            "admin_analytics": "📈 Analytics & Reports"
        }
        active_subpage = st.radio(
            "Admin Menu",
            options=admin_nav_items,
            format_func=lambda x: admin_nav_labels[x],
            label_visibility="collapsed"
        )

    # 4. Database Connection Status Box in Sidebar
    st.markdown(f"""
        <div class="sidebar-db-status" style="margin-top: 20px; font-family:'JetBrains Mono'; font-size:0.72rem; background:rgba(0,24,15,0.4); padding:10px 12px; border-radius:6px; border:1px solid rgba(164,196,177,0.2);">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#A4C4B1;">
                <span>Database:</span>
                <span style="color:#FFFFFF; font-weight:700;">{'Neo4j Live' if is_neo4j_connected else 'Demo Graph'}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#A4C4B1;">
                <span>Status:</span>
                <span style="color:{'#AEEECB' if is_neo4j_connected else '#FEF3C7'}; font-weight:700;">{'● Connected' if is_neo4j_connected else '● Demo Mode'}</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#A4C4B1;">
                <span>Active Batches:</span>
                <span style="color:#FFFFFF; font-weight:700;">{TOTAL_BATCHES}</span>
            </div>
        </div>
        <div style="font-size:0.68rem; color:#A4C4B1; margin-top:8px; line-height:1.3;">
            {t('demo_notice', curr_lang)}
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 9. FARMER MODE IMPLEMENTATION (SIMPLE, MULTILINGUAL, VOICE-ASSISTED)
# ==============================================================================
if st.session_state["app_mode"] == "farmer":

    # Farmer Top Header Banner
    st.markdown(f"""
        <div class="white-card" style="border-left: 5px solid #2C694E; margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <h1 style="font-family:'Space Grotesk'; font-size:1.6rem; font-weight:700; color:#0F172A; margin:0;">
                        {t('farmer_welcome', curr_lang)}
                    </h1>
                    <p style="font-size:0.92rem; color:#424845; margin:4px 0 0 0;">
                        {t('farmer_intro', curr_lang)}
                    </p>
                </div>
                <div>
                    <span class="badge-chip badge-verified">👨‍🌾 {t('farmer_mode', curr_lang)}</span>
                    <span class="badge-chip badge-demo">{LANGUAGES[curr_lang]['native']}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ---------------- A. MY FARM PROFILE ----------------
    if active_subpage == "my_farm":
        st.markdown(f"""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700; color:#202820; margin:0;">
                        🌾 {t('my_farm_title', curr_lang)}
                    </h2>
                    <span class="badge-chip badge-demo">Demonstration Data • Session In-Memory</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                    <div style="background:#F8FAF8; padding:18px; border-radius:8px; border:1px solid #D8E2DC; font-size:0.95rem; line-height:1.9; color:#202820;">
                        • <b>{t('farmer_name_label', curr_lang)}</b> Rajesh V. Kurup<br>
                        • <b>Farm ID:</b> <code>FRM-KL-001</code> (Sahyadri Bio-Farms)<br>
                        • <b>{t('farm_loc_label', curr_lang)}</b> Wayanad, Kerala (11.6854°N, 76.1320°E)<br>
                        • <b>{t('coop_label', curr_lang)}</b> Western Ghats Organic Farmers Coop<br>
                        • <b>Status:</b> <span class="badge-chip badge-verified">● Verified Cultivator</span>
                    </div>
                    <div style="background:#F8FAF8; padding:18px; border-radius:8px; border:1px solid #D8E2DC; font-size:0.95rem; line-height:1.9; color:#202820;">
                        • <b>Active Crops:</b> Turmeric (Curcuma longa)<br>
                        • <b>Soil Type:</b> Humus-Rich Laterite Loam<br>
                        • <b>Acreage:</b> 14.5 Acres<br>
                        • <b>{t('total_harvest_label', curr_lang)}</b> <b>850 kg</b> registered this season<br>
                        • <b>Certification:</b> NPOP Organic Standard
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------- B. REGISTER HARVEST FORM ----------------
    elif active_subpage == "register_harvest":
        st.markdown(f"""
            <div class="white-card" style="margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700; color:#202820; margin:0 0 4px 0;">
                            📝 {t('reg_title', curr_lang)}
                        </h2>
                        <p style="font-size:0.88rem; color:#424845; margin:0;">
                            {t('reg_subtitle', curr_lang)}
                        </p>
                    </div>
                    <div>
                        <span class="badge-chip badge-demo">Demonstration Data • Session In-Memory</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Embedded voice assistance toolbar
        render_voice_assistant_component(
            prompt_to_speak=t("voice_welcome_msg", curr_lang),
            lang_code=LANGUAGES[curr_lang]["code"]
        )

        # Text input fallback for blocked microphones or quiet environments
        with st.expander(f"⌨️ {t('mic_fallback_hint', curr_lang)}", expanded=False):
            st.text_input(
                "Voice Text Fallback:",
                placeholder="e.g. Register 450 kg turmeric for Rajesh V. Kurup",
                key="voice_text_fallback_reg",
                label_visibility="collapsed"
            )

        # Category Filter Bar for intuitive browsing
        cat_keys = [c["id"] for c in CATEGORIES]
        selected_cat_id = st.radio(
            f"📂 {t('crop_category_filter', curr_lang)}:",
            options=cat_keys,
            format_func=lambda cid: get_category_label(cid, curr_lang),
            horizontal=True,
            key="farmer_reg_cat_radio"
        )

        if selected_cat_id == "all":
            category_crops = CROP_CATALOG
        else:
            category_crops = get_crops_by_category(selected_cat_id)

        crop_options = [c["id"] for c in category_crops] + [NOT_LISTED_ID]

        def format_crop_choice(cid):
            if cid == NOT_LISTED_ID:
                return f"❓ {get_not_listed_label(curr_lang)}"
            c_data = get_crop_by_id(cid)
            if not c_data:
                return cid
            return format_crop_display(c_data, curr_lang, include_category=False)

        # Registration Form inside clean white card container
        with st.form("farmer_reg_form", clear_on_submit=False):
            st.markdown(f"""
                <div style="font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:700; color:#202820; margin-bottom:14px; border-bottom:1px solid #D8E2DC; padding-bottom:8px;">
                    🌱 Harvest Identification & Provenance
                </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                chosen_crop_id = st.selectbox(
                    f"🌱 {t('field_crop', curr_lang)}:",
                    options=crop_options,
                    format_func=format_crop_choice,
                    key="farmer_chosen_crop"
                )

                if chosen_crop_id == NOT_LISTED_ID:
                    st.warning(get_not_listed_notice(curr_lang))
                else:
                    c_info = get_crop_by_id(chosen_crop_id)
                    native_n = c_info.get("translations", {}).get(curr_lang, c_info["name"])
                    st.markdown(f"""
                        <div style="background:#F0F5F2; border-left:3px solid #2C694E; border-radius:4px; padding:6px 12px; margin-bottom:8px; font-size:0.83rem;">
                            <span style="font-weight:700; color:#173D2B;">{c_info['icon']} {native_n} ({c_info['name']})</span> &nbsp;•&nbsp; 
                            <i style="color:#4B6358;">{c_info['scientific_name']}</i> &nbsp;•&nbsp; 
                            <span style="color:#2C694E; font-weight:600;">{c_info['category']}</span>
                        </div>
                    """, unsafe_allow_html=True)

                harvest_qty = st.number_input(
                    f"⚖️ {t('field_qty', curr_lang)}:",
                    min_value=0,
                    max_value=25000,
                    value=450,
                    step=10,
                    help="Enter harvest weight in kilograms"
                )
            with c2:
                harvest_dt = st.date_input(
                    f"📅 {t('field_date', curr_lang)}:",
                    value=date.today()
                )
                farmer_name_inp = st.text_input(
                    f"👨‍🌾 {t('field_farmer_name', curr_lang)}:",
                    value="Rajesh V. Kurup"
                )
                farm_id_inp = st.selectbox(
                    f"🏡 {t('field_farm', curr_lang)}:",
                    options=df_farms["farm_name"].tolist()
                )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            submit_harvest = st.form_submit_button(
                f"✅ {t('btn_save_harvest', curr_lang)}",
                use_container_width=True
            )

        if submit_harvest:
            # Positive quantity, not-listed check, and required field validation
            if chosen_crop_id == NOT_LISTED_ID:
                st.error(f"⚠️ {t('not_listed_error', curr_lang)}")
                st.info(get_not_listed_notice(curr_lang))
            elif harvest_qty <= 0:
                st.error(f"⚠️ {t('error_qty', curr_lang)}")
            elif not farmer_name_inp.strip():
                st.error(f"⚠️ {t('error_farmer_name', curr_lang)}")
            elif not farm_id_inp:
                st.error(f"⚠️ {t('error_farm_select', curr_lang)}")
            else:
                c_obj = get_crop_by_id(chosen_crop_id)
                prefix = c_obj["id"]
                new_id = f"{prefix}-2026-{TOTAL_BATCHES + 1:03d}"

                # Match farm origin metadata
                farm_rows = df_batches[df_batches["farm_name"] == farm_id_inp]
                f_loc = farm_rows.iloc[0]["location"] if not farm_rows.empty else "Wayanad, Kerala"
                f_sup = farm_rows.iloc[0]["supplier"] if not farm_rows.empty else "Western Ghats Organic Farmers Coop"
                f_id = farm_rows.iloc[0]["farm_id"] if not farm_rows.empty else "FRM-KL-001"

                new_entry = {
                    "batch_id": new_id,
                    "crop_id": c_obj["id"],
                    "category": c_obj["category"],
                    "botanical": c_obj["name"],
                    "scientific_name": c_obj["scientific_name"],
                    "variety": c_obj.get("variety_sample", "Standard Harvest Grade"),
                    "farmer": farmer_name_inp.strip(),
                    "farm_id": f_id,
                    "farm_name": farm_id_inp,
                    "location": f_loc,
                    "supplier": f_sup,
                    "harvest_date": str(harvest_dt),
                    "harvest_qty_kg": int(harvest_qty),
                    "processor": f"{c_obj['name']} Processing & Extraction Lab",
                    "processed_batch_id": f"PRC-{prefix}-{TOTAL_BATCHES + 1:03d}",
                    "manufacturer": "AyurPharma Formulation Labs",
                    "finished_batch_id": f"FIN-{prefix}-{TOTAL_BATCHES + 1:03d}",
                    "distributor": "Regional Agri-Logistics Depot",
                    "retailer": "PureBotanics Herbal Dispensary",
                    "retail_location": "Bengaluru, Karnataka",
                    "current_stage": "Harvest Batch",
                    "simple_stage": "stage_harvested",
                    "status": "Pending Verification",
                    "notes": f"Registered via Farmer Mode mobile interface (Demonstration Data • In-Memory)."
                }
                st.session_state["custom_batches"].append(new_entry)
                save_persisted_batches(st.session_state["custom_batches"])

                st.success(f"{t('success_harvest', curr_lang)}")
                st.markdown(f"""
                    <div style="background:#EDFAF3; border:2px solid #52B788; border-radius:10px; padding:20px; margin-top:14px; text-align:center;">
                        <div style="font-size:0.92rem; color:#26734D; font-weight:700;">{t('new_batch_id', curr_lang)}</div>
                        <div style="font-family:'Space Grotesk',sans-serif; font-size:2.2rem; font-weight:800; color:#202820; margin:6px 0; letter-spacing:0.02em;">{new_id}</div>
                        <div style="font-size:0.95rem; font-weight:600; color:#173D2B; margin-bottom:4px;">{c_obj['icon']} {c_obj['name']} &bull; <i>{c_obj['scientific_name']}</i> ({c_obj['category']})</div>
                        <div style="font-size:0.86rem; color:#424845;">{t('keep_safe', curr_lang)}</div>
                        <div style="margin-top:10px; display:flex; justify-content:center; gap:8px;">
                            <span class="badge-chip badge-demo">Demonstration Data • Session In-Memory</span>
                            <span class="badge-chip badge-pending">Pending Quality Inspection</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # ---------------- C. TRACK MY BATCH ----------------
    elif active_subpage == "track_batch":
        st.markdown(f"""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700; color:#202820; margin:0 0 4px 0;">
                            🔍 {t('track_title', curr_lang)}
                        </h2>
                        <p style="font-size:0.88rem; color:#424845; margin:0;">
                            {t('track_subtitle', curr_lang)}
                        </p>
                    </div>
                    <div>
                        <span class="badge-chip badge-demo">Demonstration Data • Session In-Memory</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Voice input assistance
        render_voice_assistant_component(
            prompt_to_speak="Enter or speak your Batch ID to see current stage.",
            lang_code=LANGUAGES[curr_lang]["code"]
        )

        tr_col1, tr_col2 = st.columns([3, 1])
        with tr_col1:
            entered_batch_id = st.text_input(
                "Batch ID:",
                value="TUR-2026-001",
                placeholder=t("input_batch_placeholder", curr_lang),
                label_visibility="collapsed"
            ).strip().upper()
        with tr_col2:
            st.markdown("<span style='font-size:0.75rem; color:#64748B;'>Sample: <code>TUR-2026-001</code>, <code>NEE-2026-002</code></span>", unsafe_allow_html=True)

        b_res = df_batches[
            (df_batches["batch_id"] == entered_batch_id) |
            (df_batches["batch_id"].str.contains(entered_batch_id, case=False, na=False)) |
            (df_batches["botanical"].str.lower() == entered_batch_id.lower())
        ]

        if not b_res.empty:
            b_val = b_res.iloc[0]
            curr_simp_stage = b_val.get("simple_stage", "stage_harvested")

            st.markdown(f"""
                <div style="background:#F8FAF8; border:1px solid #D8E2DC; border-radius:8px; padding:16px; margin-top:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span class="badge-chip badge-demo">{b_val['batch_id']}</span>
                            <span style="font-size:1.15rem; font-weight:700; color:#202820; margin-left:8px;">{b_val['botanical']} ({b_val['variety']})</span>
                        </div>
                        <span class="badge-chip badge-verified">{b_val['status']}</span>
                    </div>
                    <div style="margin-top:6px; font-size:0.86rem; color:#424845;">
                        Origin: <b>{b_val['farm_name']}</b> | Quantity: <b>{b_val['harvest_qty_kg']} kg</b> | Date: <b>{b_val['harvest_date']}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 5-Stage Visual Stepper
            st.markdown("<div style='margin-top:16px; font-weight:700; font-size:0.95rem; color:#202820;'>📦 Supply Journey Progress:</div>", unsafe_allow_html=True)
            stages_5 = [
                ("stage_harvested", t("stage_harvested", curr_lang)),
                ("stage_collected", t("stage_collected", curr_lang)),
                ("stage_processing", t("stage_processing", curr_lang)),
                ("stage_packaged", t("stage_packaged", curr_lang)),
                ("stage_delivered", t("stage_delivered", curr_lang)),
            ]
            s_cols = st.columns(5)
            stage_keys = [k for k, _ in stages_5]
            cur_idx = stage_keys.index(curr_simp_stage) if curr_simp_stage in stage_keys else 0

            for idx_s, (sk, sname) in enumerate(stages_5):
                is_done = idx_s <= cur_idx
                is_active = idx_s == cur_idx
                with s_cols[idx_s]:
                    st.markdown(f"""
                        <div class="stage-step-box {'current' if is_active else ''}">
                            <div style="font-size:1.2rem;">{'✅' if is_done else '⏳'}</div>
                            <div class="stage-step-title">{sname}</div>
                            <div class="stage-step-sub">{'Active Stage' if is_active else 'Completed' if is_done else 'Pending'}</div>
                        </div>
                    """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div style="background:#FFF1F2; border:1px solid #FECDD3; border-radius:6px; padding:14px; color:#9F1239; font-size:0.88rem; margin-top:12px;">
                    ❌ {t('batch_not_found', curr_lang)}
                </div>
            """, unsafe_allow_html=True)

    # ---------------- D. COLLECTION STATUS ----------------
    elif active_subpage == "collection_status":
        st.markdown(f"""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                    <div>
                        <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700; color:#202820; margin:0 0 4px 0;">
                            🚚 {t('nav_collection', curr_lang)}
                        </h2>
                        <p style="font-size:0.88rem; color:#424845; margin:0;">
                            Status of your dispatched harvests at the cooperative collection center.
                        </p>
                    </div>
                    <div>
                        <span class="badge-chip badge-demo">Demonstration Data • Session In-Memory</span>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        my_lots = df_batches.head(4)
        for _, row_lot in my_lots.iterrows():
            st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; background:#F8FAF8; border:1px solid #D8E2DC; border-radius:8px; padding:12px 16px; margin-bottom:10px;">
                    <div>
                        <span class="badge-chip badge-demo">{row_lot['batch_id']}</span>
                        <span style="font-weight:700; font-size:0.95rem; color:#202820; margin-left:6px;">{row_lot['botanical']} ({row_lot['harvest_qty_kg']} kg)</span>
                        <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">Collector: {row_lot['supplier']} • Logged: {row_lot['harvest_date']}</div>
                    </div>
                    <div>
                        <span class="badge-chip {'badge-verified' if row_lot['status']=='Verified' else 'badge-pending'}">{row_lot['status']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- E. HELP / VOICE ASSISTANT ----------------
    elif active_subpage == "voice_help":
        st.markdown(f"""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                    <div>
                        <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700; color:#202820; margin:0 0 4px 0;">
                            🎙️ {t('voice_page_title', curr_lang)}
                        </h2>
                        <p style="font-size:0.88rem; color:#424845; margin:0;">
                            {t('voice_page_desc', curr_lang)}
                        </p>
                    </div>
                    <div>
                        <span class="badge-chip badge-demo">Demonstration Data • Session In-Memory</span>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        render_voice_assistant_component(
            prompt_to_speak=t("voice_welcome_msg", curr_lang),
            lang_code=LANGUAGES[curr_lang]["code"]
        )

        with st.expander(f"⌨️ {t('mic_fallback_hint', curr_lang)}", expanded=False):
            st.text_input(
                "Voice Help Text Fallback:",
                placeholder="e.g. How to track batch TUR-2026-001?",
                key="voice_text_fallback_help",
                label_visibility="collapsed"
            )

        st.markdown(f"""
            <div style="background:#F0F3FF; border:1px solid #D8E2DC; border-radius:8px; padding:14px; margin-top:14px;">
                <div style="font-weight:700; color:#202820; font-size:0.9rem; margin-bottom:6px;">💡 Spoken Commands Supported:</div>
                <div style="font-size:0.84rem; color:#424845; line-height:1.7;">
                    • <i>"Register turmeric harvest"</i><br>
                    • <i>"Check status of TUR-2026-001"</i><br>
                    • <i>"Where is my neem batch?"</i>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 10. ADMIN DASHBOARD IMPLEMENTATION (DETAILED SUPPLY CHAIN ANALYSIS)
# ==============================================================================
else:
    # ---------------- ADMIN 1: MAIN DASHBOARD ----------------
    if active_subpage == "admin_dash":
        st.markdown("""
            <div class="white-card" style="border-left: 5px solid #2C694E; margin-bottom: 16px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h1 style="font-family:'Space Grotesk'; font-size:1.6rem; font-weight:700; color:#0F172A; margin:0;">
                            Botanical Supply Chain Overview
                        </h1>
                        <p style="font-size:0.88rem; color:#424845; margin:4px 0 0 0;">
                            Track botanical batches from farm origin through processing and distribution.
                        </p>
                    </div>
                    <div>
                        <span class="badge-chip badge-demo">Demonstration Data</span>
                        <span class="badge-chip badge-verified">Property Graph Schema</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 4 Dynamic KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
                <div class="white-card" style="margin-bottom:0;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#64748B; text-transform:uppercase;">Total Farms</div>
                    <div style="font-family:'Space Grotesk'; font-size:2rem; font-weight:700; color:#0F172A; margin:4px 0;">{TOTAL_FARMS}</div>
                    <div style="font-size:0.75rem; color:#2C694E; font-weight:600;">Karnataka, TN, KL, MH, OD</div>
                </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
                <div class="white-card" style="margin-bottom:0;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#64748B; text-transform:uppercase;">Active Suppliers</div>
                    <div style="font-family:'Space Grotesk'; font-size:2rem; font-weight:700; color:#0F172A; margin:4px 0;">{TOTAL_SUPPLIERS}</div>
                    <div style="font-size:0.75rem; color:#2C694E; font-weight:600;">Regional Farmer FPOs</div>
                </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
                <div class="white-card" style="margin-bottom:0;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#64748B; text-transform:uppercase;">Active Batches</div>
                    <div style="font-family:'Space Grotesk'; font-size:2rem; font-weight:700; color:#0F172A; margin:4px 0;">{TOTAL_BATCHES}</div>
                    <div style="font-size:0.75rem; color:#2C694E; font-weight:600;">{TOTAL_HARVEST_KG:,} kg Total Yield</div>
                </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
                <div class="white-card" style="margin-bottom:0;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#64748B; text-transform:uppercase;">Pending Verification</div>
                    <div style="font-family:'Space Grotesk'; font-size:2rem; font-weight:700; color:{'#D97706' if TOTAL_PENDING > 0 else '#0F172A'}; margin:4px 0;">{TOTAL_PENDING}</div>
                    <div style="font-size:0.75rem; color:#D97706; font-weight:600;">Quality Review Flagged</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Property Graph Engine Topology Status
        st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #D8E2DC; border-radius:8px; padding:10px 16px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">🕸️</span>
                    <span style="font-weight:700; color:#173D2B; font-size:0.9rem;">NetworkX Property Graph Engine:</span>
                    <span class="badge-chip badge-verified">Active In-Memory Schema</span>
                </div>
                <div style="display:flex; gap:16px; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#4B6358;">
                    <span>Nodes: <b style="color:#0F172A;">{graph_metrics['num_nodes']}</b></span>
                    <span>Edges: <b style="color:#0F172A;">{graph_metrics['num_edges']}</b></span>
                    <span>Density: <b style="color:#0F172A;">{graph_metrics['density']:.3f}</b></span>
                    <span>Components: <b style="color:#0F172A;">{graph_metrics['num_components']}</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Large 10-Tier Property Graph
        st.markdown("""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <h2 style="font-family:'Space Grotesk'; font-size:1.15rem; font-weight:700; color:#0F172A; margin:0;">
                            10-Tier Botanical Supply Chain Property Graph
                        </h2>
                        <div style="font-size:0.8rem; color:#64748B;">
                            Farmer → Farm → Botanical → Harvest Batch → Processor → Processed Batch → Manufacturer → Finished Product Batch → Distributor → Retailer
                        </div>
                    </div>
                    <span class="badge-chip badge-demo">Sample Graph Schema</span>
                </div>
        """, unsafe_allow_html=True)

        node_names_10 = [
            "Farmer\n(R. Kurup)", "Farm\n(Sahyadri)", "Botanical\n(C. longa)",
            "Harvest Batch\n(TUR-001)", "Processor\n(Nilgiri Extr.)", "Processed\n(PRC-TUR-001)",
            "Manufacturer\n(AyurPharma)", "Finished Lot\n(FIN-TUR-001)", "Distributor\n(South Hub)", "Retailer\n(PureBotanics)"
        ]
        x_10 = np.linspace(0.05, 0.95, 10).tolist()
        y_10 = [0.5] * 10
        colors_10 = ["#112D23", "#2C694E", "#52B788", "#0284C7", "#7C3AED", "#6366F1", "#D97706", "#F59E0B", "#0D9488", "#475569"]

        fig_g10 = go.Figure()
        for i in range(9):
            fig_g10.add_trace(go.Scatter(
                x=[x_10[i], x_10[i+1]], y=[y_10[i], y_10[i+1]],
                mode="lines", line=dict(color="#A4C4B1", width=2.5),
                hoverinfo="none", showlegend=False
            ))

        fig_g10.add_trace(go.Scatter(
            x=x_10, y=y_10,
            mode="markers+text",
            text=node_names_10, textposition="top center",
            textfont=dict(family="Space Grotesk", size=9, color="#0F172A"),
            marker=dict(size=[24, 26, 24, 28, 26, 24, 26, 24, 24, 22], color=colors_10, line=dict(color="#FFFFFF", width=2)),
            showlegend=False
        ))
        fig_g10.update_layout(
            height=170, margin=dict(l=10, r=10, t=30, b=20),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.0, 1.0]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.38, 0.65])
        )
        st.plotly_chart(fig_g10, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 2-Column Analytics Charts
        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown("<div class='white-card'><h3 style='font-family:Space Grotesk; font-size:1.05rem; margin-top:0;'>Harvest Quantities by Farm (kg)</h3>", unsafe_allow_html=True)
            fig_fb = px.bar(
                df_batches, x="farm_name", y="harvest_qty_kg", color="botanical",
                color_discrete_map=get_crop_color_map(),
                labels={"harvest_qty_kg": "Harvest (kg)", "farm_name": "Farm", "botanical": "Botanical Crop"}
            )
            fig_fb = apply_chart_theme(fig_fb, height=240)
            fig_fb.update_layout(xaxis=dict(tickangle=-15))
            st.plotly_chart(fig_fb, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with ac2:
            st.markdown("<div class='white-card'><h3 style='font-family:Space Grotesk; font-size:1.05rem; margin-top:0;'>Botanical Batch Distribution</h3>", unsafe_allow_html=True)
            b_cnt = df_batches["botanical"].value_counts().reset_index()
            b_cnt.columns = ["Botanical", "Count"]
            fig_bp = px.pie(
                b_cnt, names="Botanical", values="Count", hole=0.55,
                color="Botanical", color_discrete_map=get_crop_color_map()
            )
            fig_bp = apply_chart_theme(fig_bp, height=240)
            st.plotly_chart(fig_bp, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ADMIN 2: FARMS & SUPPLIERS ----------------
    elif active_subpage == "admin_farms":
        st.markdown("""
            <div class="white-card" style="border-left: 5px solid #2C694E;">
                <h1 style="font-family:'Space Grotesk'; font-size:1.5rem; font-weight:700; color:#0F172A; margin:0;">
                    Farms & Certified Suppliers
                </h1>
                <p style="font-size:0.88rem; color:#424845; margin:4px 0 0 0;">
                    Agricultural origin directory with regional locations, crops, and aggregate yield.
                </p>
            </div>
            <div class="white-card">
        """, unsafe_allow_html=True)

        st.dataframe(
            df_farms[["farm_id", "farm_name", "location", "botanical", "scientific_name", "category", "supplier", "farmer", "total_harvest_kg", "batch_count"]],
            column_config={
                "farm_id": st.column_config.TextColumn("Farm ID"),
                "farm_name": st.column_config.TextColumn("Farm Name"),
                "location": st.column_config.TextColumn("Location"),
                "botanical": st.column_config.TextColumn("Crop"),
                "scientific_name": st.column_config.TextColumn("Scientific Name"),
                "category": st.column_config.TextColumn("Category"),
                "supplier": st.column_config.TextColumn("Cooperative / FPO"),
                "farmer": st.column_config.TextColumn("Lead Cultivator"),
                "total_harvest_kg": st.column_config.NumberColumn("Total Harvest (kg)", format="%d kg"),
                "batch_count": st.column_config.NumberColumn("Active Batches")
            },
            hide_index=True,
            use_container_width=True,
            height=340
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ADMIN 3: BOTANICAL BATCHES ----------------
    elif active_subpage == "admin_batches":
        st.markdown("""
            <div class="white-card" style="border-left: 5px solid #2C694E;">
                <h1 style="font-family:'Space Grotesk'; font-size:1.5rem; font-weight:700; color:#0F172A; margin:0;">
                    Botanical Harvest Batches Registry
                </h1>
                <p style="font-size:0.88rem; color:#424845; margin:4px 0 0 0;">
                    Complete inventory of all recorded batches across custody stages with crop classification.
                </p>
            </div>
            <div class="white-card">
        """, unsafe_allow_html=True)

        bf1, bf2 = st.columns(2)
        with bf1:
            cat_list = ["All Categories"] + [c["name"] for c in CATEGORIES if c["id"] != "all"]
            sel_b_cat = st.selectbox("Filter by Category:", cat_list, key="adm_batch_cat_filter")
        with bf2:
            crop_list = ["All Crops"] + sorted(df_batches["botanical"].unique().tolist())
            sel_b_crop = st.selectbox("Filter by Crop:", crop_list, key="adm_batch_crop_filter")

        filtered_df_batches = df_batches.copy()
        if sel_b_cat != "All Categories":
            filtered_df_batches = filtered_df_batches[filtered_df_batches["category"] == sel_b_cat]
        if sel_b_crop != "All Crops":
            filtered_df_batches = filtered_df_batches[filtered_df_batches["botanical"] == sel_b_crop]

        st.dataframe(
            filtered_df_batches[["batch_id", "botanical", "scientific_name", "category", "variety", "harvest_date", "harvest_qty_kg", "current_stage", "farm_name", "location", "status"]],
            column_config={
                "batch_id": st.column_config.TextColumn("Batch ID"),
                "botanical": st.column_config.TextColumn("Crop"),
                "scientific_name": st.column_config.TextColumn("Scientific Name"),
                "category": st.column_config.TextColumn("Category"),
                "variety": st.column_config.TextColumn("Variety"),
                "harvest_date": st.column_config.TextColumn("Harvest Date"),
                "harvest_qty_kg": st.column_config.NumberColumn("Qty (kg)", format="%d kg"),
                "current_stage": st.column_config.TextColumn("Stage"),
                "farm_name": st.column_config.TextColumn("Farm"),
                "location": st.column_config.TextColumn("Location"),
                "status": st.column_config.TextColumn("Status")
            },
            hide_index=True,
            use_container_width=True,
            height=360
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ADMIN 4: SUPPLY CHAIN EXPLORER ----------------
    elif active_subpage == "admin_explorer":
        st.markdown("""
            <div class="white-card" style="border-left: 5px solid #2C694E;">
                <h1 style="font-family:'Space Grotesk'; font-size:1.5rem; font-weight:700; color:#0F172A; margin:0;">
                    Supply Chain Property Graph Explorer
                </h1>
                <p style="font-size:0.88rem; color:#424845; margin:4px 0 0 0;">
                    Select any batch to inspect its unbroken path from cultivator to retail point.
                </p>
            </div>
        """, unsafe_allow_html=True)

        sel_exp_id = st.selectbox(
            "Select Batch ID:",
            options=df_batches["batch_id"].tolist(),
            format_func=lambda x: f"{x} - {df_batches[df_batches['batch_id']==x]['botanical'].values[0]} ({df_batches[df_batches['batch_id']==x]['scientific_name'].values[0]}) • {df_batches[df_batches['batch_id']==x]['farm_name'].values[0]}"
        )
        sel_row = df_batches[df_batches["batch_id"] == sel_exp_id].iloc[0]

        st.markdown(f"""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="badge-chip badge-demo">{sel_row['batch_id']}</span>
                        <span style="font-weight:700; font-size:1.15rem; color:#0F172A; margin-left:8px;">{sel_row['botanical']} ({sel_row['variety']})</span>
                        <span style="font-size:0.88rem; font-style:italic; color:#4B6358; margin-left:6px;">{sel_row['scientific_name']}</span>
                        <span class="badge-chip" style="margin-left:6px; background:#EDFAF3; color:#173D2B;">{sel_row['category']}</span>
                    </div>
                    <span class="badge-chip badge-verified">{sel_row['status']}</span>
                </div>
                <div style="font-size:0.85rem; color:#64748B; margin-top:4px;">
                    Origin: {sel_row['farm_name']} ({sel_row['location']}) • Farmer: {sel_row['farmer']} • Yield: {sel_row['harvest_qty_kg']} kg
                </div>
            </div>
        """, unsafe_allow_html=True)

        trace_info = trace_batch_path(G_supply_chain, sel_exp_id)

        # Graph Traversal & Shortest Path Metrics
        if trace_info:
            tm1, tm2, tm3, tm4 = st.columns(4)
            with tm1:
                st.markdown(f"""
                    <div class="white-card" style="margin-bottom:12px; padding:12px;">
                        <div style="font-size:0.72rem; color:#64748B; font-family:'JetBrains Mono'; text-transform:uppercase;">Directed Path Hops</div>
                        <div style="font-size:1.6rem; font-weight:700; color:#173D2B;">{trace_info['hop_count']} Hops</div>
                        <div style="font-size:0.75rem; color:#26734D;">Shortest Traversal Route</div>
                    </div>
                """, unsafe_allow_html=True)
            with tm2:
                st.markdown(f"""
                    <div class="white-card" style="margin-bottom:12px; padding:12px;">
                        <div style="font-size:0.72rem; color:#64748B; font-family:'JetBrains Mono'; text-transform:uppercase;">Subnetwork Nodes</div>
                        <div style="font-size:1.6rem; font-weight:700; color:#173D2B;">{trace_info['subgraph_nodes_count']} Entities</div>
                        <div style="font-size:0.75rem; color:#26734D;">Connected Provenance Subgraph</div>
                    </div>
                """, unsafe_allow_html=True)
            with tm3:
                st.markdown(f"""
                    <div class="white-card" style="margin-bottom:12px; padding:12px;">
                        <div style="font-size:0.72rem; color:#64748B; font-family:'JetBrains Mono'; text-transform:uppercase;">Chain of Custody</div>
                        <div style="font-size:1.6rem; font-weight:700; color:#173D2B;">Unbroken</div>
                        <div style="font-size:0.75rem; color:#26734D;">100% Milestone Logged</div>
                    </div>
                """, unsafe_allow_html=True)
            with tm4:
                st.markdown(f"""
                    <div class="white-card" style="margin-bottom:12px; padding:12px;">
                        <div style="font-size:0.72rem; color:#64748B; font-family:'JetBrains Mono'; text-transform:uppercase;">Graph Algorithm</div>
                        <div style="font-size:1.6rem; font-weight:700; color:#173D2B;">Dijkstra / BFS</div>
                        <div style="font-size:0.75rem; color:#26734D;">nx.shortest_path() Verified</div>
                    </div>
                """, unsafe_allow_html=True)

        # 2D Interactive Property Graph Network Visualization
        st.markdown("""
            <div class="white-card" style="margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <h3 style="font-family:'Space Grotesk'; font-size:1.1rem; margin:0; color:#0F172A;">
                            Interactive Property Graph Network Map
                        </h3>
                        <div style="font-size:0.8rem; color:#64748B;">
                            Selected batch path is highlighted in forest green across the multi-entity topology.
                        </div>
                    </div>
                    <span class="badge-chip badge-verified">NetworkX DiGraph Engine</span>
                </div>
        """, unsafe_allow_html=True)
        fig_net = render_graph_network_plot(G_supply_chain, highlight_batch_id=sel_exp_id, height=400)
        st.plotly_chart(fig_net, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 10-Tier Directed Trace for the Selected Batch
        st.markdown("""
            <div class="white-card">
                <h3 style="font-family:'Space Grotesk'; font-size:1.1rem; margin-top:0;">
                    Lineage Property Path: Cultivator &rarr; Processor &rarr; Consumer
                </h3>
        """, unsafe_allow_html=True)

        exp_nodes = [
            f"Farmer\n({sel_row['farmer'].split()[0]})",
            f"Farm\n({sel_row['farm_name'][:10]}..)",
            f"{sel_row['botanical']}\n({sel_row['scientific_name'].split()[0]})",
            f"Batch\n({sel_row['batch_id']})",
            f"Processor\n({sel_row['processor'][:10]}..)",
            f"Extract Lot\n({sel_row['processed_batch_id'].split()[0]})",
            f"Maker\n({sel_row['manufacturer'][:10]}..)",
            f"Pack Lot\n({sel_row['finished_batch_id'].split()[0]})",
            f"Distributor\n({sel_row['distributor'][:10]}..)",
            f"Retailer\n({sel_row['retailer'][:10]}..)"
        ]
        x_exp = np.linspace(0.05, 0.95, 10).tolist()
        y_exp = [0.5] * 10
        colors_exp = ["#112D23", "#2C694E", "#52B788", "#0284C7", "#7C3AED", "#6366F1", "#D97706", "#F59E0B", "#0D9488", "#475569"]

        fig_exp = go.Figure()
        for i in range(9):
            fig_exp.add_trace(go.Scatter(
                x=[x_exp[i], x_exp[i+1]], y=[y_exp[i], y_exp[i+1]],
                mode="lines", line=dict(color="#A4C4B1", width=2.5),
                hoverinfo="none", showlegend=False
            ))

        fig_exp.add_trace(go.Scatter(
            x=x_exp, y=y_exp,
            mode="markers+text",
            text=exp_nodes, textposition="top center",
            textfont=dict(family="Space Grotesk", size=9, color="#0F172A"),
            marker=dict(size=[24, 26, 24, 28, 26, 24, 26, 24, 24, 22], color=colors_exp, line=dict(color="#FFFFFF", width=2)),
            showlegend=False
        ))
        fig_exp.update_layout(
            height=175, margin=dict(l=10, r=10, t=30, b=20),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.0, 1.0]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.38, 0.65])
        )
        st.plotly_chart(fig_exp, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ADMIN 5: TRACEABILITY SEARCH ----------------
    elif active_subpage == "admin_search":
        st.markdown("""
            <div class="white-card" style="border-left: 5px solid #2C694E;">
                <h1 style="font-family:'Space Grotesk'; font-size:1.5rem; font-weight:700; color:#0F172A; margin:0;">
                    Batch Traceability Search
                </h1>
                <p style="font-size:0.88rem; color:#424845; margin:4px 0 0 0;">
                    Search by Batch ID, Botanical Crop Name, Scientific Name, Farm, or Cultivator.
                </p>
            </div>
        """, unsafe_allow_html=True)

        search_q = st.text_input(
            "Search Query:",
            value="TUR-2026-001",
            placeholder="e.g. TUR-2026-001, Tulsi, Curcuma longa, Rajesh Kurup, Wayanad..."
        ).strip()

        if search_q:
            sq = search_q.lower()
            found_m = df_batches[
                (df_batches["batch_id"].str.lower().str.contains(sq)) |
                (df_batches["botanical"].str.lower().str.contains(sq)) |
                (df_batches["scientific_name"].str.lower().str.contains(sq)) |
                (df_batches["farmer"].str.lower().str.contains(sq)) |
                (df_batches["farm_name"].str.lower().str.contains(sq)) |
                (df_batches["location"].str.lower().str.contains(sq))
            ]

            if not found_m.empty:
                if len(found_m) > 1:
                    st.info(f"🔍 Found {len(found_m)} matching records for '{search_q}'. Select one to inspect below:")
                    sel_batch_match = st.selectbox(
                        "Matching Batches:",
                        options=found_m["batch_id"].tolist(),
                        format_func=lambda bid: f"{bid} — {found_m[found_m['batch_id']==bid]['botanical'].values[0]} ({found_m[found_m['batch_id']==bid]['farmer'].values[0]}, {found_m[found_m['batch_id']==bid]['farm_name'].values[0]})"
                    )
                    item = found_m[found_m["batch_id"] == sel_batch_match].iloc[0]
                else:
                    item = found_m.iloc[0]

                st.markdown(f"""
                    <div class="white-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span class="badge-chip badge-demo">{item['batch_id']}</span>
                                <h2 style="font-family:'Space Grotesk'; font-size:1.35rem; font-weight:700; color:#0F172A; margin:6px 0 2px 0;">
                                    {item['botanical']} ({item['scientific_name']})
                                </h2>
                            </div>
                            <span class="badge-chip badge-verified">{item['status']}</span>
                        </div>
                        <div style="font-size:0.84rem; color:#64748B; margin-bottom:14px;">Origin: {item['farm_name']} | Stage: {item['current_stage']} | Quantity: {item['harvest_qty_kg']} kg</div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; background:#F8FAF8; padding:14px; border-radius:6px; border:1px solid #D8E2DC;">
                            <div>
                                <b>1. Agricultural Origin & Cultivator</b><br>
                                • Farm: {item['farm_name']}<br>
                                • Lead Farmer: {item['farmer']}<br>
                                • Location: {item['location']}<br>
                                • Harvest Date: {item['harvest_date']}<br>
                                • Category: {item['category']}
                            </div>
                            <div>
                                <b>2. Processing & Manufacturing Milestones</b><br>
                                • Processor: {item['processor']}<br>
                                • Lot: {item['processed_batch_id']}<br>
                                • Manufacturer: {item['manufacturer']}<br>
                                • Finished Lot: {item['finished_batch_id']}<br>
                                • Retailer: {item['retailer']} ({item['retail_location']})
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"No botanical batches matching query '{search_q}' were found in the demonstration registry.")

    # ---------------- ADMIN 6: ANALYTICS & REPORTS ----------------
    elif active_subpage == "admin_analytics":
        st.markdown("""
            <div class="white-card" style="border-left: 5px solid #2C694E;">
                <h1 style="font-family:'Space Grotesk'; font-size:1.5rem; font-weight:700; color:#0F172A; margin:0;">
                    Supply Chain Analytics & Exportable Reports
                </h1>
                <p style="font-size:0.88rem; color:#424845; margin:4px 0 0 0;">
                    Aggregate biomass analytics, stage distributions, and downloadable CSV manifests.
                </p>
            </div>
        """, unsafe_allow_html=True)

        c_a1, c_a2, c_a3 = st.columns(3)
        with c_a1:
            st.markdown("<div class='white-card'><h3 style='font-family:Space Grotesk; font-size:1.02rem; margin-top:0;'>Batches by Stage</h3>", unsafe_allow_html=True)
            sc = df_batches["current_stage"].value_counts().reset_index()
            sc.columns = ["Stage", "Count"]
            fig_st = px.bar(sc, x="Stage", y="Count", color_discrete_sequence=["#2C694E"])
            fig_st = apply_chart_theme(fig_st, height=230)
            st.plotly_chart(fig_st, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_a2:
            st.markdown("<div class='white-card'><h3 style='font-family:Space Grotesk; font-size:1.02rem; margin-top:0;'>Verification Status</h3>", unsafe_allow_html=True)
            vc = df_batches["status"].value_counts().reset_index()
            vc.columns = ["Status", "Count"]
            fig_vc = px.pie(vc, names="Status", values="Count", hole=0.55, color="Status", color_discrete_map={"Verified": "#2C694E", "In Transit": "#0284C7", "Pending Verification": "#D97706"})
            fig_vc = apply_chart_theme(fig_vc, height=230)
            st.plotly_chart(fig_vc, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_a3:
            st.markdown("<div class='white-card'><h3 style='font-family:Space Grotesk; font-size:1.02rem; margin-top:0;'>Yield by Category (kg)</h3>", unsafe_allow_html=True)
            cat_yield = df_batches.groupby("category")["harvest_qty_kg"].sum().reset_index()
            fig_cy = px.pie(cat_yield, names="category", values="harvest_qty_kg", hole=0.55, color_discrete_sequence=["#2C694E", "#52B788", "#0284C7", "#D97706"])
            fig_cy = apply_chart_theme(fig_cy, height=230)
            st.plotly_chart(fig_cy, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Property Graph Analytics & Algorithms Section
        st.markdown("""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div>
                        <h2 style="font-family:'Space Grotesk'; font-size:1.25rem; font-weight:700; color:#0F172A; margin:0;">
                            🕸️ Property Graph Analytics & Network Centrality
                        </h2>
                        <div style="font-size:0.82rem; color:#64748B;">
                            Graph Data Science metrics computed using NetworkX DiGraph schema (10 Node Labels & 9 Directed Relationships).
                        </div>
                    </div>
                    <span class="badge-chip badge-verified">Property Graph Engine</span>
                </div>
        """, unsafe_allow_html=True)

        g_k1, g_k2, g_k3, g_k4 = st.columns(4)
        with g_k1:
            st.markdown(f"""
                <div style="background:#F8FAF8; border:1px solid #D8E2DC; border-radius:8px; padding:12px; text-align:center;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Total Graph Nodes</div>
                    <div style="font-family:'Space Grotesk'; font-size:1.8rem; font-weight:700; color:#173D2B;">{graph_metrics['num_nodes']}</div>
                    <div style="font-size:0.75rem; color:#26734D;">10 Entity Classes</div>
                </div>
            """, unsafe_allow_html=True)
        with g_k2:
            st.markdown(f"""
                <div style="background:#F8FAF8; border:1px solid #D8E2DC; border-radius:8px; padding:12px; text-align:center;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Directed Relationships</div>
                    <div style="font-family:'Space Grotesk'; font-size:1.8rem; font-weight:700; color:#173D2B;">{graph_metrics['num_edges']}</div>
                    <div style="font-size:0.75rem; color:#26734D;">9 Typed Edges</div>
                </div>
            """, unsafe_allow_html=True)
        with g_k3:
            st.markdown(f"""
                <div style="background:#F8FAF8; border:1px solid #D8E2DC; border-radius:8px; padding:12px; text-align:center;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Graph Density</div>
                    <div style="font-family:'Space Grotesk'; font-size:1.8rem; font-weight:700; color:#173D2B;">{graph_metrics['density']:.4f}</div>
                    <div style="font-size:0.75rem; color:#26734D;">Network Connectivity</div>
                </div>
            """, unsafe_allow_html=True)
        with g_k4:
            st.markdown(f"""
                <div style="background:#F8FAF8; border:1px solid #D8E2DC; border-radius:8px; padding:12px; text-align:center;">
                    <div style="font-family:'JetBrains Mono'; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Connected Clusters</div>
                    <div style="font-family:'Space Grotesk'; font-size:1.8rem; font-weight:700; color:#173D2B;">{graph_metrics['num_components']}</div>
                    <div style="font-size:0.75rem; color:#26734D;">Supply Subgraphs</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Degree Centrality Analysis Table & Visual
        st.markdown("<h3 style='font-family:Space Grotesk; font-size:1.05rem; margin:10px 0 6px 0; color:#0F172A;'>Degree Centrality — Key Bottlenecks & Network Aggregators</h3>", unsafe_allow_html=True)
        st.caption("Identifies the most critical hubs (processors, cooperatives, and high-volume farms) in the botanical supply chain using nx.degree_centrality().")

        df_centrality = compute_degree_centrality(G_supply_chain, top_k=10)
        st.dataframe(
            df_centrality,
            column_config={
                "node_id": st.column_config.TextColumn("Node Identifier"),
                "display_name": st.column_config.TextColumn("Entity Name"),
                "label": st.column_config.TextColumn("Entity Type"),
                "degree_centrality": st.column_config.NumberColumn("Degree Centrality", format="%.4f"),
                "in_centrality": st.column_config.NumberColumn("In-Centrality", format="%.4f"),
                "out_centrality": st.column_config.NumberColumn("Out-Centrality", format="%.4f"),
                "total_connections": st.column_config.NumberColumn("Degree (Edges)", format="%d")
            },
            hide_index=True,
            use_container_width=True,
            height=280
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # Neo4j Cypher Script Generator & Export Section
        cypher_script_text = generate_cypher_export_script(df_batches.to_dict(orient="records"))
        st.markdown("""
            <div class="white-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <h3 style="font-family:'Space Grotesk'; font-size:1.1rem; margin:0; color:#0F172A;">
                            Neo4j Cypher Graph Script Export
                        </h3>
                        <div style="font-size:0.8rem; color:#64748B;">
                            Auto-generated idempotent Cypher script (MERGE statements & Constraints) ready to load directly into Neo4j Browser or AuraDB.
                        </div>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        cy_col1, cy_col2 = st.columns([1, 3])
        with cy_col1:
            st.download_button(
                "⚡ Download Cypher Script (.cypher)",
                cypher_script_text.encode('utf-8'),
                "phytotrace_neo4j_graph.cypher",
                "text/plain",
                use_container_width=True
            )
        with cy_col2:
            st.caption("Includes CREATE CONSTRAINT statements for all 10 entity types and MERGE statements for all active batches and relationships.")

        with st.expander("👁️ Preview Generated Neo4j Cypher Script", expanded=False):
            st.code(cypher_script_text[:3500] + ("\n\n// ... [truncated for preview; download full file above] ..." if len(cypher_script_text) > 3500 else ""), language="cypher")

        st.markdown("</div>", unsafe_allow_html=True)

        # Working CSV Download Buttons
        st.markdown("""
            <div class="white-card">
                <h3 style="font-family:'Space Grotesk'; font-size:1.1rem; margin-top:0;">Export Datasets</h3>
        """, unsafe_allow_html=True)
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            st.download_button(
                "📥 Download Farms CSV",
                df_farms.to_csv(index=False).encode('utf-8'),
                "phytotrace_farms.csv",
                "text/csv",
                use_container_width=True
            )
        with d_col2:
            st.download_button(
                "📥 Download Suppliers CSV",
                df_suppliers.to_csv(index=False).encode('utf-8'),
                "phytotrace_suppliers.csv",
                "text/csv",
                use_container_width=True
            )
        with d_col3:
            st.download_button(
                "📥 Download Batches CSV",
                df_batches.to_csv(index=False).encode('utf-8'),
                "phytotrace_batches.csv",
                "text/csv",
                use_container_width=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 11. FOOTER
# ==============================================================================
st.markdown("""
    <div style="text-align:center; padding:20px 0 10px 0; color:#64748B; font-family:'JetBrains Mono'; font-size:0.75rem; border-top:1px solid #D8E2DC; margin-top:24px;">
        PhytoTrace — Multilingual Botanical Supply Chain Traceability • College Micro-Project Demonstration
    </div>
""", unsafe_allow_html=True)
