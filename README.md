# PhytoTrace — Botanical Supply Chain Traceability Using Property Graphs

[![Frontend: React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react)](https://react.dev/)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Graph: Neo4j & NetworkX](https://img.shields.io/badge/Property%20Graph-Neo4j%20%2B%20NetworkX-008CC1?logo=neo4j)](https://neo4j.com/)
[![Hosting: Netlify](https://img.shields.io/badge/Deploy-Netlify-00C7B7?logo=netlify)](https://www.netlify.com/)
[![Languages: 12 Indian Languages](https://img.shields.io/badge/Languages-12%20Supported-26734D)](https://en.wikipedia.org/wiki/Languages_of_India)

PhytoTrace is an agricultural analytics SaaS web application for end-to-end botanical supply chain provenance and verification. Powered by a deterministic Property Graph schema, PhytoTrace models every custody hop—from smallholder cultivation through extraction facilities, GMP manufacturing, regional freight distribution, to retail dispensaries.

---

## 🏛️ Architecture Overview

The application is decoupled into a modern web stack:

```
┌────────────────────────────────────────────────────────┐
│             React + Vite Frontend (Netlify)            │
│  • Google Stitch Design System (Forest Green & Sage)   │
│  • Multilingual Farmer Mode (12 Indian Languages + RTL)│
│  • Web Speech API (Voice-to-Text & Text-to-Speech)     │
│  • Interactive Property Graph Visualizer               │
│  • 10-Tier Custody Stepper & Shortest Path Tracer      │
└───────────────────────────┬────────────────────────────┘
                            │ REST API (JSON)
┌───────────────────────────▼────────────────────────────┐
│               Python FastAPI Backend Service           │
│  • Data persistence (custom_batches.json)              │
│  • Topological Graph Engine (NetworkX DiGraph)         │
│  • Graph Centrality & Connected Components Algorithms  │
│  • Live Neo4j Driver Connection Check with Fallback    │
│  • Idempotent Cypher Query Generator                   │
└───────────────────────────┬────────────────────────────┘
                            │ Bolt Protocol (bolt://localhost:7687)
┌───────────────────────────▼────────────────────────────┐
│                  Neo4j Enterprise / Fallback           │
│  • 10 Node Labels: Farmer, Farm, Botanical, Batch...   │
│  • 9 Typed Relationships: OWNS_FARM, HARVESTED_AT...   │
└────────────────────────────────────────────────────────┘
```

---

## 🌿 Key Capabilities

### 1. Multilingual Farmer Mode with Voice Assistance
- **12 Supported Languages**: English, Kannada (ಕನ್ನಡ), Telugu (తెలుగు), Hindi (हिन्दी), Tamil (தமிழ்), Malayalam (മലയാളം), Marathi (मराठी), Bengali (বাংলা), Punjabi (ਪੰਜਾਬੀ), Odia (ଓଡ଼ିଆ), Gujarati (ગુજરાતી), and Urdu (اردو with right-to-left `dir="rtl"` layout).
- **Web Speech API**: In-browser speech recognition allows farmers to speak their crop name, harvested yield (in kg or quintals), and cultivator details. Web Speech Synthesis reads back registration confirmation and guidance in their native language.
- **20 Botanical Crops Catalog**: High-contrast cards for 20 commercial Indian botanical crops (Turmeric, Neem, Tulsi, Ashwagandha, Aloe Vera, Ginger, Amla, Moringa, Brahmi, Shatavari, Giloy, Lemongrass, Peppermint, Senna, Black Pepper, Cardamom, Cinnamon, Clove, Coriander, Fenugreek) across 4 categories (*Roots & Rhizomes*, *Medicinal Plants*, *Herbs*, *Spices*). Botanical taxonomy and scientific names are strictly preserved.
- **Instant Validation & Batch Generation**: Assigns deterministic batch identifiers (e.g. `TUR-2026-001`, `ASH-2026-002`) and persists records immediately.

### 2. Admin Dashboard & Supply Chain Traceability
- **Design Matched to Google Stitch**:
  - Dark forest-green sidebar (`#112D23`)
  - Light off-white background (`#F9F9FF`)
  - White container cards (`#FFFFFF`)
  - Sage green accents (`#26734D`)
  - Space Grotesk & Hanken Grotesk typography
- **KPI Metrics Calculated Dynamically**: Total Farms, Active Suppliers, Harvest Batches, Pending Verification, Total Harvest Volume (kg).
- **Interactive Property Graph Visualizer**: SVG canvas rendering all 10 entity tiers, directed relationships, and real-time path highlighting for any selected batch.
- **10-Tier Custody Lineage Stepper**:
  $$\text{Farmer} \rightarrow \text{Farm} \rightarrow \text{Botanical} \rightarrow \text{Harvest Batch} \rightarrow \text{Processor} \rightarrow \text{Processed Batch} \rightarrow \text{Manufacturer} \rightarrow \text{Finished Lot} \rightarrow \text{Distributor} \rightarrow \text{Retailer}$$
- **Graph Algorithms**:
  - Shortest path custody tracing
  - Degree centrality ranking to uncover supply bottlenecks
  - Weakly connected components calculation
  - Graph density analysis
  - Idempotent Cypher query export

---

## 📁 Project Directory Structure

```
botanical-traceability/
├── backend/
│   ├── main.py                    # FastAPI application & API endpoints
│   ├── data_store.py              # 26 base demonstration batches & persistence
│   ├── requirements.txt           # Backend dependencies
│   └── .env.example               # Backend environment template
├── frontend/
│   ├── index.html                 # Entry HTML with Google Fonts & Material Symbols
│   ├── package.json               # Vite + React + Tailwind dependencies
│   ├── vite.config.js             # Vite configuration with /api proxy to FastAPI
│   ├── tailwind.config.js         # Stitch color palette & typography
│   ├── netlify.toml               # Netlify SPA routing & build settings
│   └── src/
│       ├── App.jsx                # Root coordinator with mode toggle & language state
│       ├── main.jsx               # React DOM bootstrap
│       ├── index.css              # Tailwind base & RTL stylesheet
│       ├── services/
│       │   ├── api.js             # Unified client API wrapper
│       │   └── speech.js          # Web Speech STT and TTS engine
│       └── components/
│           ├── Sidebar.jsx        # Navigation, mode toggle, language selector
│           ├── Header.jsx         # Search, database status, breadcrumbs
│           ├── FarmerMode.jsx     # Voice assistant, 20-crop grid, harvest form
│           ├── AdminDashboard.jsx # 4 KPI cards, embedded graph, batch table
│           ├── InteractiveGraph.jsx # Scaled SVG Property Graph network
│           ├── TraceabilityModal.jsx# 10-tier custody stepper & shortest path
│           ├── FarmsSuppliers.jsx # Aggregated farm & collective directories
│           ├── BatchesExplorer.jsx# Filterable batch registry & CSV export
│           ├── SupplyChainExplorer.jsx # Full-page graph lineage inspector
│           ├── AnalyticsReports.jsx# Degree centrality & volume distribution
│           └── CypherModal.jsx    # Neo4j Cypher script viewer & copier
├── netlify.toml                   # Root Netlify configuration file
├── crop_catalog.py                # Preserved 20-crop catalog module
├── translations.py                # Preserved 12-language translation dictionary
├── graph_engine.py                # Preserved NetworkX Property Graph engine
├── phytotrace_neo4j_graph.cypher  # Preserved Neo4j Cypher constraint script
├── app.py                         # Preserved Streamlit fallback application
└── custom_batches.json            # Persistent user-registered batches
```

---

## 🚀 Running the Project Locally

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Start the FastAPI Backend Service
```bash
# Optional: create and activate a virtual environment
# python -m venv venv
# source venv/bin/activate (or venv\Scripts\activate on Windows)

# Install backend dependencies
pip install -r backend/requirements.txt

# Launch FastAPI on port 8000
python -m uvicorn backend.main:app --reload --port 8000
```
- API Documentation (Swagger UI): **http://localhost:8000/docs**
- Health Check: **http://localhost:8000/api/health**

### 2. Start the React + Vite Frontend
In a separate terminal window:
```bash
cd frontend

# Install frontend dependencies
npm install

# Start Vite development server
npm run dev
```
- Local Application: **http://localhost:5173**
- The frontend automatically proxies all `/api/*` calls to `http://localhost:8000`.

### 3. Preserved Streamlit Application (Fallback)
The existing Python Streamlit application is completely preserved and functional:
```bash
streamlit run app.py
```

---

## ☁️ Deploying to Netlify

The repository includes a ready-to-use `netlify.toml`:

```toml
[build]
  base = "frontend"
  publish = "dist"
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Steps:
1. Push your repository to **GitHub**:
   ```bash
   git add .
   git commit -m "Convert PhytoTrace to React Vite and FastAPI"
   git push origin main
   ```
2. Log into [Netlify](https://app.netlify.com/) and click **"Add new site" > "Import an existing project"**.
3. Select your GitHub repository.
4. Netlify will automatically detect the settings in `netlify.toml`:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
5. In **Site Configuration > Environment Variables**, add:
   - `VITE_API_BASE_URL`: The URL of your hosted FastAPI backend (e.g., hosted on Render, Railway, Fly.io, or AWS).
6. Click **Deploy Site**.
