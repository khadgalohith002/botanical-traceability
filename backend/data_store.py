"""
PhytoTrace Data Store and Neo4j Service
=======================================
Provides unified access to demonstration botanical batches, persistent storage
for farmer-registered batches, and live Neo4j / NetworkX graph synchronization.
"""

import os
import json
import uuid
import datetime
from typing import List, Dict, Any, Optional

PERSIST_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "custom_batches.json")

BASE_BATCHES: List[Dict[str, Any]] = [
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


def load_persisted_batches() -> List[Dict[str, Any]]:
    """Loads farmer-registered custom batches saved to disk."""
    if os.path.exists(PERSIST_FILE):
        try:
            with open(PERSIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_persisted_batches(batches: List[Dict[str, Any]]) -> None:
    """Saves custom batches to disk."""
    try:
        with open(PERSIST_FILE, "w", encoding="utf-8") as f:
            json.dump(batches, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving batches: {e}")


def get_all_batches() -> List[Dict[str, Any]]:
    """Combines demonstration batches with persistent farmer submissions."""
    custom = load_persisted_batches()
    return BASE_BATCHES + custom


def add_harvest_batch(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates, constructs, saves, and returns a newly registered harvest batch.
    Generates a unique deterministic batch ID format: {CROP_ID}-2026-{XXX}.
    """
    all_b = get_all_batches()
    crop_id = data.get("crop_id", "BOT")
    
    # Calculate next sequence number for this crop
    matching_crop = [b for b in all_b if b.get("crop_id") == crop_id or b.get("batch_id", "").startswith(f"{crop_id}-")]
    next_idx = len(matching_crop) + 1
    generated_batch_id = f"{crop_id}-2026-{next_idx:03d}"
    
    farm_id = data.get("farm_id") or f"FRM-{crop_id}-{uuid.uuid4().hex[:4].upper()}"
    today_str = datetime.date.today().isoformat()
    harvest_date = data.get("harvest_date") or today_str
    
    new_batch = {
        "batch_id": generated_batch_id,
        "crop_id": crop_id,
        "category": data.get("category", "Medicinal Plants"),
        "botanical": data.get("botanical", "Botanical Herb"),
        "scientific_name": data.get("scientific_name", "Plantae sp."),
        "variety": data.get("variety", "Standard Certified"),
        "farmer": data.get("farmer", "Registered Cultivator"),
        "farm_id": farm_id,
        "farm_name": data.get("farm_name", f"{data.get('farmer', 'Farmer')}'s Organic Plot"),
        "location": data.get("location", "Karnataka, India"),
        "supplier": data.get("supplier", "Regional FPO Collective"),
        "harvest_date": harvest_date,
        "harvest_qty_kg": int(data.get("harvest_qty_kg", 500)),
        "processor": "Regional Botanical Extraction Facility",
        "processed_batch_id": f"PRC-{generated_batch_id}",
        "manufacturer": "AyurPharma Formulation Labs",
        "finished_batch_id": f"FIN-{generated_batch_id}",
        "distributor": "Central Agro-Logistics Depot",
        "retailer": "PureBotanics Herbal Dispensary",
        "retail_location": "Bengaluru, Karnataka",
        "current_stage": "Harvest Batch",
        "simple_stage": "stage_harvested",
        "status": "Pending Verification",
        "notes": data.get("notes", "Farmer harvest registered via PhytoTrace Portal."),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    # Save to disk
    custom = load_persisted_batches()
    custom.append(new_batch)
    save_persisted_batches(custom)
    
    return new_batch


def check_neo4j_status(uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password") -> Dict[str, Any]:
    """Safely checks if live Neo4j database is accessible."""
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=1.0)
        with driver.session() as session:
            res = session.run("RETURN 1 AS connected")
            rec = res.single()
            if rec and rec["connected"] == 1:
                return {
                    "connected": True,
                    "mode": "Live Neo4j Enterprise",
                    "uri": uri,
                    "database": "phyto_prod"
                }
    except Exception:
        pass
    
    return {
        "connected": False,
        "mode": "In-Memory Property Graph (NetworkX)",
        "uri": "bolt://localhost:7687 (Simulated In-Memory)",
        "database": "phyto_graph_memory"
    }


def compute_kpis() -> Dict[str, Any]:
    """Calculates consistent supply chain business metrics from active batches."""
    batches = get_all_batches()
    total_batches = len(batches)
    farms = set(b.get("farm_id") for b in batches if b.get("farm_id"))
    suppliers = set(b.get("supplier") for b in batches if b.get("supplier"))
    total_qty = sum(int(b.get("harvest_qty_kg", 0)) for b in batches)
    pending = len([b for b in batches if b.get("status") == "Pending Verification"])
    verified = len([b for b in batches if b.get("status") == "Verified"])
    in_transit = len([b for b in batches if b.get("status") == "In Transit"])
    
    # Categories count
    categories = {}
    for b in batches:
        cat = b.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
        
    # Stages count
    stages = {}
    for b in batches:
        stg = b.get("current_stage", "Unknown")
        stages[stg] = stages.get(stg, 0) + 1
        
    return {
        "total_farms": len(farms),
        "total_suppliers": len(suppliers),
        "active_batches": total_batches,
        "pending_verification": pending,
        "verified_batches": verified,
        "in_transit_batches": in_transit,
        "total_harvest_kg": total_qty,
        "categories_distribution": categories,
        "stages_distribution": stages
    }
