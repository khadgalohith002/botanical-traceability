// ============================================================================
// PhytoTrace Neo4j Property Graph Schema & Seed Script
// Project: Botanical Supply Chain Traceability Using Property Graphs
// ============================================================================

// 1. UNIQUE CONSTRAINTS
CREATE CONSTRAINT IF NOT EXISTS FOR (f:Farmer) REQUIRE f.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (fm:Farm) REQUIRE fm.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (b:Botanical) REQUIRE b.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (hb:HarvestBatch) REQUIRE hb.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Processor) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (pb:ProcessedBatch) REQUIRE pb.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Manufacturer) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (fl:FinishedLot) REQUIRE fl.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Distributor) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (r:Retailer) REQUIRE r.id IS UNIQUE;

// 2. NODES & RELATIONSHIPS INGESTION
// Batch TUR-2026-001 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Rajesh_V._Kurup'})
  ON CREATE SET farmer.name = 'Rajesh V. Kurup', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KL-001'})
  ON CREATE SET farm.name = 'Sahyadri Bio-Farms', farm.location = 'Wayanad, Kerala', farm.cooperative = 'Western Ghats Organic Farmers Coop'

MERGE (bot:Botanical {id: 'TUR'})
  ON CREATE SET bot.name = 'Turmeric', bot.scientific_name = 'Curcuma longa', bot.category = 'Roots & Rhizomes'

MERGE (batch:HarvestBatch {id: 'TUR-2026-001'})
  ON CREATE SET batch.harvest_date = date('2026-08-14'), batch.quantity_kg = 850, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Nilgiri_Botanical_Ex'})
  ON CREATE SET proc.name = 'Nilgiri Botanical Extraction Facility'

MERGE (pbatch:ProcessedBatch {id: 'PRC-TUR-001'})

MERGE (mfr:Manufacturer {id: 'MFR_AyurPharma_Formulati'})
  ON CREATE SET mfr.name = 'AyurPharma Formulation Labs'

MERGE (flot:FinishedLot {id: 'FIN-TUR-001'})

MERGE (dist:Distributor {id: 'DIST_South_Zone_Agro-Logi'})
  ON CREATE SET dist.name = 'South Zone Agro-Logistics Depot'

MERGE (ret:Retailer {id: 'RET_PureBotanics_Herbal_'})
  ON CREATE SET ret.name = 'PureBotanics Herbal Dispensary', ret.city = 'Bengaluru, Karnataka'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-08-14'), qty_kg: 850}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch NEE-2026-002 Lineage
MERGE (farmer:Farmer {id: 'FARMER_K._Ramanathan'})
  ON CREATE SET farmer.name = 'K. Ramanathan', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-TN-002'})
  ON CREATE SET farm.name = 'Vaigai Agro-Forestry Plot', farm.location = 'Madurai, Tamil Nadu', farm.cooperative = 'Vaigai Herbal Producers Collective'

MERGE (bot:Botanical {id: 'NEE'})
  ON CREATE SET bot.name = 'Neem', bot.scientific_name = 'Azadirachta indica', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'NEE-2026-002'})
  ON CREATE SET batch.harvest_date = date('2026-08-28'), batch.quantity_kg = 1100, batch.status = 'In Transit', batch.stage = 'Distributor'

MERGE (proc:Processor {id: 'PROC_Tamil_Nadu_Bio-Refin'})
  ON CREATE SET proc.name = 'Tamil Nadu Bio-Refinery Unit 4'

MERGE (pbatch:ProcessedBatch {id: 'PRC-NEE-002'})

MERGE (mfr:Manufacturer {id: 'MFR_Kaveri_Eco-Agro_Solu'})
  ON CREATE SET mfr.name = 'Kaveri Eco-Agro Solutions'

MERGE (flot:FinishedLot {id: 'FIN-NEE-002'})

MERGE (dist:Distributor {id: 'DIST_Tamil_Nadu_Freight_C'})
  ON CREATE SET dist.name = 'Tamil Nadu Freight Corridor Hub'

MERGE (ret:Retailer {id: 'RET_GreenEarth_Natural_A'})
  ON CREATE SET ret.name = 'GreenEarth Natural Agri-Store', ret.city = 'Chennai, Tamil Nadu'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-08-28'), qty_kg: 1100}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch TUR-2026-003 Lineage
MERGE (farmer:Farmer {id: 'FARMER_S._Murugesan'})
  ON CREATE SET farmer.name = 'S. Murugesan', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-TN-003'})
  ON CREATE SET farm.name = 'Bhavani River Basin Farm', farm.location = 'Erode, Tamil Nadu', farm.cooperative = 'Erode Turmeric Cultivators FPO'

MERGE (bot:Botanical {id: 'TUR'})
  ON CREATE SET bot.name = 'Turmeric', bot.scientific_name = 'Curcuma longa', bot.category = 'Roots & Rhizomes'

MERGE (batch:HarvestBatch {id: 'TUR-2026-003'})
  ON CREATE SET batch.harvest_date = date('2026-09-02'), batch.quantity_kg = 1250, batch.status = 'Verified', batch.stage = 'Manufacturer'

MERGE (proc:Processor {id: 'PROC_Erode_Agro-Steam_Dry'})
  ON CREATE SET proc.name = 'Erode Agro-Steam Drying & Milling'

MERGE (pbatch:ProcessedBatch {id: 'PRC-TUR-003'})

MERGE (mfr:Manufacturer {id: 'MFR_Sanjivani_Herbal_For'})
  ON CREATE SET mfr.name = 'Sanjivani Herbal Formulations'

MERGE (flot:FinishedLot {id: 'FIN-TUR-003'})

MERGE (dist:Distributor {id: 'DIST_Regional_Freight_Ter'})
  ON CREATE SET dist.name = 'Regional Freight Terminal (Coimbatore)'

MERGE (ret:Retailer {id: 'RET_VedaLife_Ayurvedic_C'})
  ON CREATE SET ret.name = 'VedaLife Ayurvedic Center', ret.city = 'Mysuru, Karnataka'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-02'), qty_kg: 1250}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch NEE-2026-004 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Manjunath_Hegde'})
  ON CREATE SET farmer.name = 'Manjunath Hegde', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KA-004'})
  ON CREATE SET farm.name = 'Malnad Eco-Grove', farm.location = 'Shivamogga, Karnataka', farm.cooperative = 'Malnad Bio-Commons Producer Co.'

MERGE (bot:Botanical {id: 'NEE'})
  ON CREATE SET bot.name = 'Neem', bot.scientific_name = 'Azadirachta indica', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'NEE-2026-004'})
  ON CREATE SET batch.harvest_date = date('2026-09-10'), batch.quantity_kg = 720, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Malnad_Cold-Press_Oi'})
  ON CREATE SET proc.name = 'Malnad Cold-Press Oil Mill'

MERGE (pbatch:ProcessedBatch {id: 'PRC-NEE-004'})

MERGE (mfr:Manufacturer {id: 'MFR_BioProtect_Plant_Nut'})
  ON CREATE SET mfr.name = 'BioProtect Plant Nutrition'

MERGE (flot:FinishedLot {id: 'FIN-NEE-004'})

MERGE (dist:Distributor {id: 'DIST_Western_Karnataka_Lo'})
  ON CREATE SET dist.name = 'Western Karnataka Logistics Node'

MERGE (ret:Retailer {id: 'RET_Krishi_Seva_Kendra_D'})
  ON CREATE SET ret.name = 'Krishi Seva Kendra Dispensary', ret.city = 'Dharwad, Karnataka'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-10'), qty_kg: 720}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch TUR-2026-005 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Jayanti_Pradhan'})
  ON CREATE SET farmer.name = 'Jayanti Pradhan', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-OD-005'})
  ON CREATE SET farm.name = 'Kandhamal Tribal Agro-Commons', farm.location = 'Kandhamal, Odisha', farm.cooperative = 'Odisha Tribal Forest Products Federation'

MERGE (bot:Botanical {id: 'TUR'})
  ON CREATE SET bot.name = 'Turmeric', bot.scientific_name = 'Curcuma longa', bot.category = 'Roots & Rhizomes'

MERGE (batch:HarvestBatch {id: 'TUR-2026-005'})
  ON CREATE SET batch.harvest_date = date('2026-09-18'), batch.quantity_kg = 680, batch.status = 'In Transit', batch.stage = 'Processor'

MERGE (proc:Processor {id: 'PROC_Tribal_Supercritical'})
  ON CREATE SET proc.name = 'Tribal Supercritical CO2 Facility'

MERGE (pbatch:ProcessedBatch {id: 'PRC-TUR-005'})

MERGE (mfr:Manufacturer {id: 'MFR_Eastern_Phyto-Chemic'})
  ON CREATE SET mfr.name = 'Eastern Phyto-Chemicals'

MERGE (flot:FinishedLot {id: 'FIN-TUR-005'})

MERGE (dist:Distributor {id: 'DIST_Eastern_Express_Tran'})
  ON CREATE SET dist.name = 'Eastern Express Transit Depot'

MERGE (ret:Retailer {id: 'RET_HerbalCraft_Apotheca'})
  ON CREATE SET ret.name = 'HerbalCraft Apothecary', ret.city = 'Kolkata, West Bengal'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-18'), qty_kg: 680}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch NEE-2026-006 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Bhavesh_Patel'})
  ON CREATE SET farmer.name = 'Bhavesh Patel', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-GJ-006'})
  ON CREATE SET farm.name = 'Charotar Botanical Grove', farm.location = 'Anand, Gujarat', farm.cooperative = 'Charotar Medicinal Crops Guild'

MERGE (bot:Botanical {id: 'NEE'})
  ON CREATE SET bot.name = 'Neem', bot.scientific_name = 'Azadirachta indica', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'NEE-2026-006'})
  ON CREATE SET batch.harvest_date = date('2026-09-25'), batch.quantity_kg = 540, batch.status = 'Pending Verification', batch.stage = 'Processor'

MERGE (proc:Processor {id: 'PROC_Gujarat_Bio-Derivati'})
  ON CREATE SET proc.name = 'Gujarat Bio-Derivatives Unit (Vadodara)'

MERGE (pbatch:ProcessedBatch {id: 'PRC-NEE-006 (Pending)'})

MERGE (mfr:Manufacturer {id: 'MFR_Pending_Processor_In'})
  ON CREATE SET mfr.name = 'Pending Processor Intake'

MERGE (flot:FinishedLot {id: 'Pending'})

MERGE (dist:Distributor {id: 'DIST_Pending'})
  ON CREATE SET dist.name = 'Pending'

MERGE (ret:Retailer {id: 'RET_Pending'})
  ON CREATE SET ret.name = 'Pending', ret.city = 'Pending'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-25'), qty_kg: 540}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch TUR-2026-007 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Aniket_Patil'})
  ON CREATE SET farmer.name = 'Aniket Patil', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-MH-007'})
  ON CREATE SET farm.name = 'Krishna Valley Bio-Farm', farm.location = 'Sangli, Maharashtra', farm.cooperative = 'Sangli Botanical Aggregators Union'

MERGE (bot:Botanical {id: 'TUR'})
  ON CREATE SET bot.name = 'Turmeric', bot.scientific_name = 'Curcuma longa', bot.category = 'Roots & Rhizomes'

MERGE (batch:HarvestBatch {id: 'TUR-2026-007'})
  ON CREATE SET batch.harvest_date = date('2026-09-29'), batch.quantity_kg = 960, batch.status = 'Verified', batch.stage = 'Manufacturer'

MERGE (proc:Processor {id: 'PROC_Krishna_Valley_Dehyd'})
  ON CREATE SET proc.name = 'Krishna Valley Dehydration Facility'

MERGE (pbatch:ProcessedBatch {id: 'PRC-TUR-007'})

MERGE (mfr:Manufacturer {id: 'MFR_Nectar_Vedic_Formula'})
  ON CREATE SET mfr.name = 'Nectar Vedic Formulations'

MERGE (flot:FinishedLot {id: 'FIN-TUR-007'})

MERGE (dist:Distributor {id: 'DIST_Mumbai_Central_Freig'})
  ON CREATE SET dist.name = 'Mumbai Central Freight Hub'

MERGE (ret:Retailer {id: 'RET_Apex_Organic_Market'})
  ON CREATE SET ret.name = 'Apex Organic Market', ret.city = 'Mumbai, Maharashtra'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-29'), qty_kg: 960}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch NEE-2026-008 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Suresh_Gowda'})
  ON CREATE SET farmer.name = 'Suresh Gowda', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KA-008'})
  ON CREATE SET farm.name = 'Chamundi Agro-Forestry', farm.location = 'Mysuru, Karnataka', farm.cooperative = 'Cauvery Basin Farmers Collective'

MERGE (bot:Botanical {id: 'NEE'})
  ON CREATE SET bot.name = 'Neem', bot.scientific_name = 'Azadirachta indica', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'NEE-2026-008'})
  ON CREATE SET batch.harvest_date = date('2026-10-04'), batch.quantity_kg = 480, batch.status = 'Pending Verification', batch.stage = 'Harvest Batch'

MERGE (proc:Processor {id: 'PROC_Pending_Processor_Al'})
  ON CREATE SET proc.name = 'Pending Processor Allocation'

MERGE (pbatch:ProcessedBatch {id: 'Pending'})

MERGE (mfr:Manufacturer {id: 'MFR_Pending'})
  ON CREATE SET mfr.name = 'Pending'

MERGE (flot:FinishedLot {id: 'Pending'})

MERGE (dist:Distributor {id: 'DIST_Pending'})
  ON CREATE SET dist.name = 'Pending'

MERGE (ret:Retailer {id: 'RET_Pending'})
  ON CREATE SET ret.name = 'Pending', ret.city = 'Pending'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-04'), qty_kg: 480}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch TUL-2026-009 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Devendra_Joshi'})
  ON CREATE SET farmer.name = 'Devendra Joshi', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-UK-009'})
  ON CREATE SET farm.name = 'Haridwar Bio-Herbal Grove', farm.location = 'Haridwar, Uttarakhand', farm.cooperative = 'Himalayan Herb Producers FPO'

MERGE (bot:Botanical {id: 'TUL'})
  ON CREATE SET bot.name = 'Tulsi / Holy Basil', bot.scientific_name = 'Ocimum tenuiflorum', bot.category = 'Herbs'

MERGE (batch:HarvestBatch {id: 'TUL-2026-009'})
  ON CREATE SET batch.harvest_date = date('2026-09-20'), batch.quantity_kg = 420, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Ganga_Bio-Extracts_P'})
  ON CREATE SET proc.name = 'Ganga Bio-Extracts Plant'

MERGE (pbatch:ProcessedBatch {id: 'PRC-TUL-009'})

MERGE (mfr:Manufacturer {id: 'MFR_Rishi_Herbals_Manufa'})
  ON CREATE SET mfr.name = 'Rishi Herbals Manufacturing'

MERGE (flot:FinishedLot {id: 'FIN-TUL-009'})

MERGE (dist:Distributor {id: 'DIST_North_India_Agro_Tra'})
  ON CREATE SET dist.name = 'North India Agro Transit Hub'

MERGE (ret:Retailer {id: 'RET_AyurVeda_Sanjeevani_'})
  ON CREATE SET ret.name = 'AyurVeda Sanjeevani Store', ret.city = 'Dehradun, Uttarakhand'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-20'), qty_kg: 420}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch ASH-2026-010 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Balram_Singh'})
  ON CREATE SET farmer.name = 'Balram Singh', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-MP-010'})
  ON CREATE SET farm.name = 'Malwa Agro-Commons', farm.location = 'Neemuch, Madhya Pradesh', farm.cooperative = 'Malwa Medicinal Crops Guild'

MERGE (bot:Botanical {id: 'ASH'})
  ON CREATE SET bot.name = 'Ashwagandha', bot.scientific_name = 'Withania somnifera', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'ASH-2026-010'})
  ON CREATE SET batch.harvest_date = date('2026-09-22'), batch.quantity_kg = 650, batch.status = 'In Transit', batch.stage = 'Distributor'

MERGE (proc:Processor {id: 'PROC_Central_India_Alkalo'})
  ON CREATE SET proc.name = 'Central India Alkaloid Extraction Lab'

MERGE (pbatch:ProcessedBatch {id: 'PRC-ASH-010'})

MERGE (mfr:Manufacturer {id: 'MFR_VedaRoot_Health_Scie'})
  ON CREATE SET mfr.name = 'VedaRoot Health Science'

MERGE (flot:FinishedLot {id: 'FIN-ASH-010'})

MERGE (dist:Distributor {id: 'DIST_Indore_Regional_Logi'})
  ON CREATE SET dist.name = 'Indore Regional Logistics Center'

MERGE (ret:Retailer {id: 'RET_PureBotanics_Herbal_'})
  ON CREATE SET ret.name = 'PureBotanics Herbal Dispensary', ret.city = 'Bhopal, Madhya Pradesh'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-22'), qty_kg: 650}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch GIN-2026-011 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Biddappa_Somanna'})
  ON CREATE SET farmer.name = 'Biddappa Somanna', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KA-011'})
  ON CREATE SET farm.name = 'Coorg Organic Valley', farm.location = 'Kodagu, Karnataka', farm.cooperative = 'Western Ghats Ginger Collective'

MERGE (bot:Botanical {id: 'GIN'})
  ON CREATE SET bot.name = 'Ginger', bot.scientific_name = 'Zingiber officinale', bot.category = 'Roots & Rhizomes'

MERGE (batch:HarvestBatch {id: 'GIN-2026-011'})
  ON CREATE SET batch.harvest_date = date('2026-09-27'), batch.quantity_kg = 980, batch.status = 'Verified', batch.stage = 'Manufacturer'

MERGE (proc:Processor {id: 'PROC_Malnad_Steam_Dehydra'})
  ON CREATE SET proc.name = 'Malnad Steam Dehydration Facility'

MERGE (pbatch:ProcessedBatch {id: 'PRC-GIN-011'})

MERGE (mfr:Manufacturer {id: 'MFR_Nectar_Vedic_Formula'})
  ON CREATE SET mfr.name = 'Nectar Vedic Formulations'

MERGE (flot:FinishedLot {id: 'FIN-GIN-011'})

MERGE (dist:Distributor {id: 'DIST_Mysuru_Agro_Freight_'})
  ON CREATE SET dist.name = 'Mysuru Agro Freight Node'

MERGE (ret:Retailer {id: 'RET_GreenEarth_Natural_A'})
  ON CREATE SET ret.name = 'GreenEarth Natural Agri-Store', ret.city = 'Bengaluru, Karnataka'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-09-27'), qty_kg: 980}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch AML-2026-012 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Ramakant_Shukla'})
  ON CREATE SET farmer.name = 'Ramakant Shukla', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-UP-012'})
  ON CREATE SET farm.name = 'Awadh Agro-Grove', farm.location = 'Pratapgarh, Uttar Pradesh', farm.cooperative = 'Awadh Bio-Horticulture Producers'

MERGE (bot:Botanical {id: 'AML'})
  ON CREATE SET bot.name = 'Amla / Indian Gooseberry', bot.scientific_name = 'Phyllanthus emblica', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'AML-2026-012'})
  ON CREATE SET batch.harvest_date = date('2026-10-01'), batch.quantity_kg = 1450, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Awadh_Cold-Pressed_J'})
  ON CREATE SET proc.name = 'Awadh Cold-Pressed Juice Lab'

MERGE (pbatch:ProcessedBatch {id: 'PRC-AML-012'})

MERGE (mfr:Manufacturer {id: 'MFR_Chyawanprash_Formula'})
  ON CREATE SET mfr.name = 'Chyawanprash Formulation Center'

MERGE (flot:FinishedLot {id: 'FIN-AML-012'})

MERGE (dist:Distributor {id: 'DIST_Varanasi_Cargo_Hub'})
  ON CREATE SET dist.name = 'Varanasi Cargo Hub'

MERGE (ret:Retailer {id: 'RET_Krishi_Seva_Kendra_D'})
  ON CREATE SET ret.name = 'Krishi Seva Kendra Dispensary', ret.city = 'Lucknow, Uttar Pradesh'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-01'), qty_kg: 1450}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch BLP-2026-013 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Thomas_Chacko'})
  ON CREATE SET farmer.name = 'Thomas Chacko', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KL-013'})
  ON CREATE SET farm.name = 'High Range Spices Ridge', farm.location = 'Idukki, Kerala', farm.cooperative = 'Cardamom Hills Spices Guild'

MERGE (bot:Botanical {id: 'BLP'})
  ON CREATE SET bot.name = 'Black Pepper', bot.scientific_name = 'Piper nigrum', bot.category = 'Spices'

MERGE (batch:HarvestBatch {id: 'BLP-2026-013'})
  ON CREATE SET batch.harvest_date = date('2026-10-02'), batch.quantity_kg = 520, batch.status = 'In Transit', batch.stage = 'Processor'

MERGE (proc:Processor {id: 'PROC_Kochi_Supercritical_'})
  ON CREATE SET proc.name = 'Kochi Supercritical Oleoresin Unit'

MERGE (pbatch:ProcessedBatch {id: 'PRC-BLP-013'})

MERGE (mfr:Manufacturer {id: 'MFR_SpiceHeritage_Agro-T'})
  ON CREATE SET mfr.name = 'SpiceHeritage Agro-Tech'

MERGE (flot:FinishedLot {id: 'Pending'})

MERGE (dist:Distributor {id: 'DIST_Pending'})
  ON CREATE SET dist.name = 'Pending'

MERGE (ret:Retailer {id: 'RET_Pending'})
  ON CREATE SET ret.name = 'Pending', ret.city = 'Pending'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-02'), qty_kg: 520}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch CAR-2026-014 Lineage
MERGE (farmer:Farmer {id: 'FARMER_K._J._Mathew'})
  ON CREATE SET farmer.name = 'K. J. Mathew', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KL-014'})
  ON CREATE SET farm.name = 'Periyar Hills Plantation', farm.location = 'Thekkady, Kerala', farm.cooperative = 'Kerala Spices Growers Society'

MERGE (bot:Botanical {id: 'CAR'})
  ON CREATE SET bot.name = 'Cardamom', bot.scientific_name = 'Elettaria cardamomum', bot.category = 'Spices'

MERGE (batch:HarvestBatch {id: 'CAR-2026-014'})
  ON CREATE SET batch.harvest_date = date('2026-10-03'), batch.quantity_kg = 310, batch.status = 'Verified', batch.stage = 'Distributor'

MERGE (proc:Processor {id: 'PROC_Periyar_Automated_Cu'})
  ON CREATE SET proc.name = 'Periyar Automated Curing Kilns'

MERGE (pbatch:ProcessedBatch {id: 'PRC-CAR-014'})

MERGE (mfr:Manufacturer {id: 'MFR_AromaPharma_Exports'})
  ON CREATE SET mfr.name = 'AromaPharma Exports'

MERGE (flot:FinishedLot {id: 'FIN-CAR-014'})

MERGE (dist:Distributor {id: 'DIST_Cochin_Port_Transit_'})
  ON CREATE SET dist.name = 'Cochin Port Transit Depot'

MERGE (ret:Retailer {id: 'RET_Apothecary_Internati'})
  ON CREATE SET ret.name = 'Apothecary International', ret.city = 'Kochi, Kerala'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-03'), qty_kg: 310}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch GIL-2026-015 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Mangal_Ram_Netam'})
  ON CREATE SET farmer.name = 'Mangal Ram Netam', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-CG-015'})
  ON CREATE SET farm.name = 'Bastar Bio-Commons', farm.location = 'Bastar, Chhattisgarh', farm.cooperative = 'Dandakaranya Tribal Forest Federation'

MERGE (bot:Botanical {id: 'GIL'})
  ON CREATE SET bot.name = 'Giloy', bot.scientific_name = 'Tinospora cordifolia', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'GIL-2026-015'})
  ON CREATE SET batch.harvest_date = date('2026-10-05'), batch.quantity_kg = 460, batch.status = 'Pending Verification', batch.stage = 'Harvest Batch'

MERGE (proc:Processor {id: 'PROC_Pending_Processor_In'})
  ON CREATE SET proc.name = 'Pending Processor Intake'

MERGE (pbatch:ProcessedBatch {id: 'Pending'})

MERGE (mfr:Manufacturer {id: 'MFR_Pending'})
  ON CREATE SET mfr.name = 'Pending'

MERGE (flot:FinishedLot {id: 'Pending'})

MERGE (dist:Distributor {id: 'DIST_Pending'})
  ON CREATE SET dist.name = 'Pending'

MERGE (ret:Retailer {id: 'RET_Pending'})
  ON CREATE SET ret.name = 'Pending', ret.city = 'Pending'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-05'), qty_kg: 460}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch ALO-2026-016 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Shrawan_Bishnoi'})
  ON CREATE SET farmer.name = 'Shrawan Bishnoi', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-RJ-016'})
  ON CREATE SET farm.name = 'Thar Green Agro-Belt', farm.location = 'Barmer, Rajasthan', farm.cooperative = 'Marwar Arid Herbs Collective'

MERGE (bot:Botanical {id: 'ALO'})
  ON CREATE SET bot.name = 'Aloe Vera', bot.scientific_name = 'Aloe vera', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'ALO-2026-016'})
  ON CREATE SET batch.harvest_date = date('2026-10-06'), batch.quantity_kg = 1400, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Jaipur_Cold-Filtrati'})
  ON CREATE SET proc.name = 'Jaipur Cold-Filtration Gel Refinery'

MERGE (pbatch:ProcessedBatch {id: 'PRC-ALO-016'})

MERGE (mfr:Manufacturer {id: 'MFR_DesertVedic_Cosmeceu'})
  ON CREATE SET mfr.name = 'DesertVedic Cosmeceuticals'

MERGE (flot:FinishedLot {id: 'FIN-ALO-016'})

MERGE (dist:Distributor {id: 'DIST_Northern_Logistics_C'})
  ON CREATE SET dist.name = 'Northern Logistics Corridor'

MERGE (ret:Retailer {id: 'RET_Apex_Organic_Market'})
  ON CREATE SET ret.name = 'Apex Organic Market', ret.city = 'Jaipur, Rajasthan'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-06'), qty_kg: 1400}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch MOR-2026-017 Lineage
MERGE (farmer:Farmer {id: 'FARMER_S._Murugesan'})
  ON CREATE SET farmer.name = 'S. Murugesan', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-TN-017'})
  ON CREATE SET farm.name = 'Theni Bio-Greens Plantation', farm.location = 'Theni, Tamil Nadu', farm.cooperative = 'Vaigai Herbal Producers Collective'

MERGE (bot:Botanical {id: 'MOR'})
  ON CREATE SET bot.name = 'Moringa', bot.scientific_name = 'Moringa oleifera', bot.category = 'Herbs'

MERGE (batch:HarvestBatch {id: 'MOR-2026-017'})
  ON CREATE SET batch.harvest_date = date('2026-10-07'), batch.quantity_kg = 890, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Theni_Solar_Dehydrat'})
  ON CREATE SET proc.name = 'Theni Solar Dehydration & Powdering Unit'

MERGE (pbatch:ProcessedBatch {id: 'PRC-MOR-017'})

MERGE (mfr:Manufacturer {id: 'MFR_GreenLife_Phyto-Nutr'})
  ON CREATE SET mfr.name = 'GreenLife Phyto-Nutrition'

MERGE (flot:FinishedLot {id: 'FIN-MOR-017'})

MERGE (dist:Distributor {id: 'DIST_Madurai_Cargo_Logist'})
  ON CREATE SET dist.name = 'Madurai Cargo Logistics'

MERGE (ret:Retailer {id: 'RET_Krishi_Seva_Kendra_D'})
  ON CREATE SET ret.name = 'Krishi Seva Kendra Dispensary', ret.city = 'Madurai, Tamil Nadu'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-07'), qty_kg: 890}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch BRA-2026-018 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Subhash_Mondal'})
  ON CREATE SET farmer.name = 'Subhash Mondal', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-WB-018'})
  ON CREATE SET farm.name = 'Sundarban Wetlands Agro-Grove', farm.location = 'South 24 Parganas, West Bengal', farm.cooperative = 'Bengal Coastal Med-Herbs Society'

MERGE (bot:Botanical {id: 'BRA'})
  ON CREATE SET bot.name = 'Brahmi', bot.scientific_name = 'Bacopa monnieri', bot.category = 'Medicinal Plants'

MERGE (batch:HarvestBatch {id: 'BRA-2026-018'})
  ON CREATE SET batch.harvest_date = date('2026-10-08'), batch.quantity_kg = 380, batch.status = 'In Transit', batch.stage = 'Distributor'

MERGE (proc:Processor {id: 'PROC_Kolkata_Phyto-Chemic'})
  ON CREATE SET proc.name = 'Kolkata Phyto-Chemicals Lab'

MERGE (pbatch:ProcessedBatch {id: 'PRC-BRA-018'})

MERGE (mfr:Manufacturer {id: 'MFR_Smriti_Medha_Formula'})
  ON CREATE SET mfr.name = 'Smriti Medha Formulations'

MERGE (flot:FinishedLot {id: 'FIN-BRA-018'})

MERGE (dist:Distributor {id: 'DIST_Eastern_Express_Tran'})
  ON CREATE SET dist.name = 'Eastern Express Transit Depot'

MERGE (ret:Retailer {id: 'RET_HerbalCraft_Apotheca'})
  ON CREATE SET ret.name = 'HerbalCraft Apothecary', ret.city = 'Kolkata, West Bengal'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-08'), qty_kg: 380}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch SHA-2026-019 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Ghanshyam_Meena'})
  ON CREATE SET farmer.name = 'Ghanshyam Meena', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-MP-019'})
  ON CREATE SET farm.name = 'Satpura Mountain Agro-Commons', farm.location = 'Hoshangabad, Madhya Pradesh', farm.cooperative = 'Narmada Valley Herbal Guild'

MERGE (bot:Botanical {id: 'SHA'})
  ON CREATE SET bot.name = 'Shatavari', bot.scientific_name = 'Asparagus racemosus', bot.category = 'Roots & Rhizomes'

MERGE (batch:HarvestBatch {id: 'SHA-2026-019'})
  ON CREATE SET batch.harvest_date = date('2026-10-08'), batch.quantity_kg = 560, batch.status = 'Verified', batch.stage = 'Manufacturer'

MERGE (proc:Processor {id: 'PROC_Bhopal_Root_Processi'})
  ON CREATE SET proc.name = 'Bhopal Root Processing Center'

MERGE (pbatch:ProcessedBatch {id: 'PRC-SHA-019'})

MERGE (mfr:Manufacturer {id: 'MFR_VedaRoot_Health_Scie'})
  ON CREATE SET mfr.name = 'VedaRoot Health Science'

MERGE (flot:FinishedLot {id: 'FIN-SHA-019'})

MERGE (dist:Distributor {id: 'DIST_Indore_Regional_Logi'})
  ON CREATE SET dist.name = 'Indore Regional Logistics Center'

MERGE (ret:Retailer {id: 'RET_PureBotanics_Herbal_'})
  ON CREATE SET ret.name = 'PureBotanics Herbal Dispensary', ret.city = 'Bhopal, Madhya Pradesh'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-08'), qty_kg: 560}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch LEM-2026-020 Lineage
MERGE (farmer:Farmer {id: 'FARMER_George_Varghese'})
  ON CREATE SET farmer.name = 'George Varghese', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KL-020'})
  ON CREATE SET farm.name = 'Anamudi Essential Herbs Estate', farm.location = 'Munnar, Kerala', farm.cooperative = 'High Ranges Bio-Oil Cooperative'

MERGE (bot:Botanical {id: 'LEM'})
  ON CREATE SET bot.name = 'Lemongrass', bot.scientific_name = 'Cymbopogon citratus', bot.category = 'Herbs'

MERGE (batch:HarvestBatch {id: 'LEM-2026-020'})
  ON CREATE SET batch.harvest_date = date('2026-10-09'), batch.quantity_kg = 740, batch.status = 'Verified', batch.stage = 'Distributor'

MERGE (proc:Processor {id: 'PROC_Munnar_Steam_Distill'})
  ON CREATE SET proc.name = 'Munnar Steam Distillation Refinery'

MERGE (pbatch:ProcessedBatch {id: 'PRC-LEM-020'})

MERGE (mfr:Manufacturer {id: 'MFR_Kerala_Natural_Aroma'})
  ON CREATE SET mfr.name = 'Kerala Natural Aromatics'

MERGE (flot:FinishedLot {id: 'FIN-LEM-020'})

MERGE (dist:Distributor {id: 'DIST_Cochin_Port_Transit_'})
  ON CREATE SET dist.name = 'Cochin Port Transit Depot'

MERGE (ret:Retailer {id: 'RET_VedaLife_Ayurvedic_C'})
  ON CREATE SET ret.name = 'VedaLife Ayurvedic Center', ret.city = 'Kochi, Kerala'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-09'), qty_kg: 740}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch PEP-2026-021 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Mahesh_Chandra'})
  ON CREATE SET farmer.name = 'Mahesh Chandra', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-UP-021'})
  ON CREATE SET farm.name = 'Rohilkhand Mentha Basin', farm.location = 'Sambhal, Uttar Pradesh', farm.cooperative = 'North India Essential Oils Federation'

MERGE (bot:Botanical {id: 'PEP'})
  ON CREATE SET bot.name = 'Peppermint', bot.scientific_name = 'Mentha × piperita', bot.category = 'Herbs'

MERGE (batch:HarvestBatch {id: 'PEP-2026-021'})
  ON CREATE SET batch.harvest_date = date('2026-10-09'), batch.quantity_kg = 1120, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Sambhal_Hydro-Distil'})
  ON CREATE SET proc.name = 'Sambhal Hydro-Distillation Plant'

MERGE (pbatch:ProcessedBatch {id: 'PRC-PEP-021'})

MERGE (mfr:Manufacturer {id: 'MFR_Himalaya_Cool_Herbal'})
  ON CREATE SET mfr.name = 'Himalaya Cool Herbals'

MERGE (flot:FinishedLot {id: 'FIN-PEP-021'})

MERGE (dist:Distributor {id: 'DIST_North_India_Agro_Tra'})
  ON CREATE SET dist.name = 'North India Agro Transit Hub'

MERGE (ret:Retailer {id: 'RET_AyurVeda_Sanjeevani_'})
  ON CREATE SET ret.name = 'AyurVeda Sanjeevani Store', ret.city = 'Delhi NCR'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-09'), qty_kg: 1120}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch SEN-2026-022 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Laxman_Ram'})
  ON CREATE SET farmer.name = 'Laxman Ram', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-RJ-022'})
  ON CREATE SET farm.name = 'Jodhpur Arid Zone Cultivators', farm.location = 'Jodhpur, Rajasthan', farm.cooperative = 'Marwar Arid Herbs Collective'

MERGE (bot:Botanical {id: 'SEN'})
  ON CREATE SET bot.name = 'Senna', bot.scientific_name = 'Senna alexandrina', bot.category = 'Herbs'

MERGE (batch:HarvestBatch {id: 'SEN-2026-022'})
  ON CREATE SET batch.harvest_date = date('2026-10-10'), batch.quantity_kg = 830, batch.status = 'In Transit', batch.stage = 'Processor'

MERGE (proc:Processor {id: 'PROC_Jodhpur_Pod_&_Leaf_S'})
  ON CREATE SET proc.name = 'Jodhpur Pod & Leaf Sorting Plant'

MERGE (pbatch:ProcessedBatch {id: 'PRC-SEN-022'})

MERGE (mfr:Manufacturer {id: 'MFR_DesertVedic_Cosmeceu'})
  ON CREATE SET mfr.name = 'DesertVedic Cosmeceuticals'

MERGE (flot:FinishedLot {id: 'FIN-SEN-022'})

MERGE (dist:Distributor {id: 'DIST_Jaipur_Logistics_Ter'})
  ON CREATE SET dist.name = 'Jaipur Logistics Terminal'

MERGE (ret:Retailer {id: 'RET_Apex_Organic_Market'})
  ON CREATE SET ret.name = 'Apex Organic Market', ret.city = 'Jaipur, Rajasthan'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-10'), qty_kg: 830}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch CIN-2026-023 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Antony_Mathew'})
  ON CREATE SET farmer.name = 'Antony Mathew', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-KL-023'})
  ON CREATE SET farm.name = 'Malabar Spice Enclave', farm.location = 'Kannur, Kerala', farm.cooperative = 'Kerala Spices Growers Society'

MERGE (bot:Botanical {id: 'CIN'})
  ON CREATE SET bot.name = 'Cinnamon', bot.scientific_name = 'Cinnamomum verum', bot.category = 'Spices'

MERGE (batch:HarvestBatch {id: 'CIN-2026-023'})
  ON CREATE SET batch.harvest_date = date('2026-10-10'), batch.quantity_kg = 290, batch.status = 'Verified', batch.stage = 'Manufacturer'

MERGE (proc:Processor {id: 'PROC_Kannur_Quilling_&_Dr'})
  ON CREATE SET proc.name = 'Kannur Quilling & Drying Center'

MERGE (pbatch:ProcessedBatch {id: 'PRC-CIN-023'})

MERGE (mfr:Manufacturer {id: 'MFR_SpiceHeritage_Agro-T'})
  ON CREATE SET mfr.name = 'SpiceHeritage Agro-Tech'

MERGE (flot:FinishedLot {id: 'FIN-CIN-023'})

MERGE (dist:Distributor {id: 'DIST_Cochin_Port_Transit_'})
  ON CREATE SET dist.name = 'Cochin Port Transit Depot'

MERGE (ret:Retailer {id: 'RET_Apothecary_Internati'})
  ON CREATE SET ret.name = 'Apothecary International', ret.city = 'Kochi, Kerala'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-10'), qty_kg: 290}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch CLO-2026-024 Lineage
MERGE (farmer:Farmer {id: 'FARMER_N._Selvaraj'})
  ON CREATE SET farmer.name = 'N. Selvaraj', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-TN-024'})
  ON CREATE SET farm.name = 'Marunthuvazh Hills Plantation', farm.location = 'Kanyakumari, Tamil Nadu', farm.cooperative = 'Southern Tip Spices Collective'

MERGE (bot:Botanical {id: 'CLO'})
  ON CREATE SET bot.name = 'Clove', bot.scientific_name = 'Syzygium aromaticum', bot.category = 'Spices'

MERGE (batch:HarvestBatch {id: 'CLO-2026-024'})
  ON CREATE SET batch.harvest_date = date('2026-10-10'), batch.quantity_kg = 210, batch.status = 'Pending Verification', batch.stage = 'Harvest Batch'

MERGE (proc:Processor {id: 'PROC_Kanyakumari_Solar_Dr'})
  ON CREATE SET proc.name = 'Kanyakumari Solar Drying Kilns'

MERGE (pbatch:ProcessedBatch {id: 'PRC-CLO-024'})

MERGE (mfr:Manufacturer {id: 'MFR_AromaPharma_Exports'})
  ON CREATE SET mfr.name = 'AromaPharma Exports'

MERGE (flot:FinishedLot {id: 'FIN-CLO-024'})

MERGE (dist:Distributor {id: 'DIST_Regional_Freight_Ter'})
  ON CREATE SET dist.name = 'Regional Freight Terminal (Coimbatore)'

MERGE (ret:Retailer {id: 'RET_VedaLife_Ayurvedic_C'})
  ON CREATE SET ret.name = 'VedaLife Ayurvedic Center', ret.city = 'Madurai, Tamil Nadu'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-10'), qty_kg: 210}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch COR-2026-025 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Dinesh_Patidar'})
  ON CREATE SET farmer.name = 'Dinesh Patidar', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-MP-025'})
  ON CREATE SET farm.name = 'Malwa Spice Fields', farm.location = 'Guna, Madhya Pradesh', farm.cooperative = 'Central India Spice Producers FPO'

MERGE (bot:Botanical {id: 'COR'})
  ON CREATE SET bot.name = 'Coriander', bot.scientific_name = 'Coriandrum sativum', bot.category = 'Spices'

MERGE (batch:HarvestBatch {id: 'COR-2026-025'})
  ON CREATE SET batch.harvest_date = date('2026-10-11'), batch.quantity_kg = 940, batch.status = 'Verified', batch.stage = 'Processor'

MERGE (proc:Processor {id: 'PROC_Guna_Automated_Clean'})
  ON CREATE SET proc.name = 'Guna Automated Cleaning & Milling Plant'

MERGE (pbatch:ProcessedBatch {id: 'PRC-COR-025'})

MERGE (mfr:Manufacturer {id: 'MFR_PureSpices_Botanical'})
  ON CREATE SET mfr.name = 'PureSpices Botanical Formulation'

MERGE (flot:FinishedLot {id: 'FIN-COR-025'})

MERGE (dist:Distributor {id: 'DIST_Indore_Regional_Logi'})
  ON CREATE SET dist.name = 'Indore Regional Logistics Center'

MERGE (ret:Retailer {id: 'RET_Apex_Organic_Market'})
  ON CREATE SET ret.name = 'Apex Organic Market', ret.city = 'Bhopal, Madhya Pradesh'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-11'), qty_kg: 940}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);
// Batch FEN-2026-026 Lineage
MERGE (farmer:Farmer {id: 'FARMER_Pravin_Bhai_Patel'})
  ON CREATE SET farmer.name = 'Pravin Bhai Patel', farmer.role = 'Lead Cultivator'

MERGE (farm:Farm {id: 'FRM-GJ-026'})
  ON CREATE SET farm.name = 'Mehsana Agro-Commons', farm.location = 'Mehsana, Gujarat', farm.cooperative = 'Gujarat Organic Growers Guild'

MERGE (bot:Botanical {id: 'FEN'})
  ON CREATE SET bot.name = 'Fenugreek', bot.scientific_name = 'Trigonella foenum-graecum', bot.category = 'Spices'

MERGE (batch:HarvestBatch {id: 'FEN-2026-026'})
  ON CREATE SET batch.harvest_date = date('2026-10-11'), batch.quantity_kg = 670, batch.status = 'Verified', batch.stage = 'Retailer'

MERGE (proc:Processor {id: 'PROC_Ahmedabad_Supercriti'})
  ON CREATE SET proc.name = 'Ahmedabad Supercritical Extraction Facility'

MERGE (pbatch:ProcessedBatch {id: 'PRC-FEN-026'})

MERGE (mfr:Manufacturer {id: 'MFR_BioProtect_Plant_Nut'})
  ON CREATE SET mfr.name = 'BioProtect Plant Nutrition'

MERGE (flot:FinishedLot {id: 'FIN-FEN-026'})

MERGE (dist:Distributor {id: 'DIST_Western_Karnataka_Lo'})
  ON CREATE SET dist.name = 'Western Karnataka Logistics Node'

MERGE (ret:Retailer {id: 'RET_GreenEarth_Natural_A'})
  ON CREATE SET ret.name = 'GreenEarth Natural Agri-Store', ret.city = 'Ahmedabad, Gujarat'

MERGE (farmer)-[:OWNS_FARM]->(farm)
MERGE (farm)-[:PRODUCES {harvest_date: date('2026-10-11'), qty_kg: 670}]->(batch)
MERGE (batch)-[:OF_BOTANICAL]->(bot)
MERGE (batch)-[:SHIPPED_TO_PROCESSOR]->(proc)
MERGE (proc)-[:PROCESSED_INTO]->(pbatch)
MERGE (pbatch)-[:SUPPLIED_TO_MAKER]->(mfr)
MERGE (mfr)-[:FORMULATED_INTO]->(flot)
MERGE (flot)-[:CONSIGNED_TO_DISTRIBUTOR]->(dist)
MERGE (dist)-[:DELIVERS_TO_RETAILER]->(ret);