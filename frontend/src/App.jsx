import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import FarmerMode from './components/FarmerMode';
import AdminDashboard from './components/AdminDashboard';
import FarmsSuppliers from './components/FarmsSuppliers';
import BatchesExplorer from './components/BatchesExplorer';
import SupplyChainExplorer from './components/SupplyChainExplorer';
import AnalyticsReports from './components/AnalyticsReports';
import TraceabilityModal from './components/TraceabilityModal';
import CypherModal from './components/CypherModal';

export default function App() {
  const [appMode, setAppMode] = useState('admin'); // 'admin' or 'farmer'
  const [activePage, setActivePage] = useState('dashboard');
  const [currentLang, setCurrentLang] = useState('en');
  const [languages, setLanguages] = useState([]);
  const [translations, setTranslations] = useState({});
  const [crops, setCrops] = useState([]);
  const [categories, setCategories] = useState([]);
  const [batches, setBatches] = useState([]);
  const [kpis, setKpis] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [health, setHealth] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Modals
  const [traceData, setTraceData] = useState(null);
  const [isCypherModalOpen, setIsCypherModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // Is Urdu RTL?
  const isRtl = currentLang === 'ur';

  // Load Initial Metadata
  useEffect(() => {
    async function init() {
      try {
        const [langList, healthRes] = await Promise.all([
          api.getLanguages(),
          api.getHealth(),
        ]);
        setLanguages(langList);
        setHealth(healthRes);
      } catch (err) {
        console.error('Initialization error:', err);
      }
    }
    init();
  }, []);

  // Load Localized Data when Language Changes
  useEffect(() => {
    async function loadLocalized() {
      try {
        const [transRes, cropsRes, catsRes] = await Promise.all([
          api.getTranslations(currentLang),
          api.getCrops(currentLang),
          api.getCategories(currentLang),
        ]);
        setTranslations(transRes.translations || {});
        setCrops(cropsRes);
        setCategories(catsRes);
      } catch (err) {
        console.error('Error loading localized resources:', err);
      }
    }
    loadLocalized();
  }, [currentLang]);

  // Load Batches, KPIs and Graph Data
  const refreshData = async () => {
    try {
      const [batchesRes, analyticsRes, gData] = await Promise.all([
        api.getBatches(),
        api.getAnalyticsSummary(),
        api.getGraphData(),
      ]);
      setBatches(batchesRes);
      setKpis(analyticsRes.kpis);
      setGraphData(gData);
    } catch (err) {
      console.error('Error loading core data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshData();
  }, []);

  // Handle Register Harvest
  const handleRegisterHarvest = async (formData) => {
    const res = await api.registerHarvest(formData);
    await refreshData();
    return res;
  };

  // Handle Trace Batch
  const handleSelectBatchForTrace = async (batchId) => {
    try {
      const traceRes = await api.traceBatch(batchId);
      setTraceData(traceRes);
    } catch (err) {
      alert(`Could not trace batch: ${err.message}`);
    }
  };

  return (
    <div
      dir={isRtl ? 'rtl' : 'ltr'}
      className="min-h-screen bg-surface font-body text-on-surface antialiased flex"
    >
      {/* Left/Right Sidebar */}
      <Sidebar
        appMode={appMode}
        setAppMode={setAppMode}
        activePage={activePage}
        setActivePage={setActivePage}
        currentLang={currentLang}
        setCurrentLang={setCurrentLang}
        languages={languages}
        health={health}
        t={translations}
        isRtl={isRtl}
      />

      {/* Main Content Area */}
      <div className={`flex-1 flex flex-col min-h-screen ${isRtl ? 'pr-72' : 'pl-72'}`}>
        {/* Top Header */}
        <Header
          appMode={appMode}
          activePage={activePage}
          health={health}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onOpenCypherModal={() => setIsCypherModalOpen(true)}
          isRtl={isRtl}
        />

        {/* Dynamic Main View */}
        <main className="flex-1 pt-20 px-6 sm:px-10 max-w-7xl w-full mx-auto">
          {appMode === 'farmer' ? (
            <FarmerMode
              crops={crops}
              categories={categories}
              batches={batches}
              currentLang={currentLang}
              languages={languages}
              t={translations}
              isRtl={isRtl}
              onRegisterHarvest={handleRegisterHarvest}
              onSelectBatchForTrace={handleSelectBatchForTrace}
            />
          ) : (
            <>
              {activePage === 'dashboard' && (
                <AdminDashboard
                  kpis={kpis}
                  batches={batches}
                  crops={crops}
                  graphData={graphData}
                  onSelectBatchForTrace={handleSelectBatchForTrace}
                  onOpenCypherModal={() => setIsCypherModalOpen(true)}
                />
              )}
              {activePage === 'farms-and-suppliers' && <FarmsSuppliers />}
              {activePage === 'botanical-batches' && (
                <BatchesExplorer
                  batches={batches}
                  crops={crops}
                  onSelectBatchForTrace={handleSelectBatchForTrace}
                />
              )}
              {activePage === 'supply-chain-explorer' && (
                <SupplyChainExplorer
                  graphData={graphData}
                  batches={batches}
                  onSelectBatchForTrace={handleSelectBatchForTrace}
                />
              )}
              {activePage === 'traceability-search' && (
                <BatchesExplorer
                  batches={batches}
                  crops={crops}
                  onSelectBatchForTrace={handleSelectBatchForTrace}
                />
              )}
              {activePage === 'analytics-and-reports' && <AnalyticsReports />}
            </>
          )}
        </main>
      </div>

      {/* 10-Tier Custody Traceability Modal */}
      {traceData && (
        <TraceabilityModal
          traceData={traceData}
          onClose={() => setTraceData(null)}
        />
      )}

      {/* Cypher Script Modal */}
      <CypherModal
        isOpen={isCypherModalOpen}
        onClose={() => setIsCypherModalOpen(false)}
      />
    </div>
  );
}
