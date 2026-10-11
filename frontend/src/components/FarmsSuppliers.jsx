import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function FarmsSuppliers() {
  const [farms, setFarms] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [activeTab, setActiveTab] = useState('farms');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [fData, sData] = await Promise.all([api.getFarms(), api.getSuppliers()]);
        setFarms(fData);
        setSuppliers(sData);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredFarms = farms.filter((f) => {
    const s = search.toLowerCase();
    return (
      !s ||
      f.farm_name.toLowerCase().includes(s) ||
      f.farmer.toLowerCase().includes(s) ||
      f.location.toLowerCase().includes(s) ||
      f.supplier.toLowerCase().includes(s)
    );
  });

  const filteredSuppliers = suppliers.filter((sup) => {
    const s = search.toLowerCase();
    return !s || sup.supplier.toLowerCase().includes(s);
  });

  return (
    <div className="flex flex-col gap-6 pb-16">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-headline text-2xl font-bold text-on-surface">
            Farms &amp; Agricultural Suppliers
          </h1>
          <p className="text-xs text-on-surface-variant font-mono">
            Origin farms, FPO producer cooperatives, and verified botanical aggregators.
          </p>
        </div>

        {/* Tab switch */}
        <div className="flex items-center gap-1 bg-surface-container-low p-1 rounded-xl border border-outline-variant/30 text-xs font-semibold">
          <button
            onClick={() => setActiveTab('farms')}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'farms' ? 'bg-secondary text-white shadow-sm' : 'text-on-surface-variant'
            }`}
          >
            Farms ({farms.length})
          </button>
          <button
            onClick={() => setActiveTab('suppliers')}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'suppliers' ? 'bg-secondary text-white shadow-sm' : 'text-on-surface-variant'
            }`}
          >
            Suppliers &amp; FPOs ({suppliers.length})
          </button>
        </div>
      </div>

      {/* Search Input */}
      <div className="bg-white p-4 rounded-xl border border-outline-variant/30 flex items-center gap-2">
        <span className="material-symbols-outlined text-outline text-[18px]">search</span>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={activeTab === 'farms' ? 'Search farms by name, cultivator, or state...' : 'Search supplier collectives...'}
          className="w-full text-xs text-on-surface focus:outline-none"
        />
      </div>

      {/* Farms Table */}
      {activeTab === 'farms' && (
        <div className="bg-white rounded-2xl border border-outline-variant/40 shadow-sm overflow-hidden p-6">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase font-mono text-[10px]">
                <th className="py-2.5 px-3">Farm ID</th>
                <th className="py-2.5 px-3">Farm Name</th>
                <th className="py-2.5 px-3">Lead Farmer</th>
                <th className="py-2.5 px-3">Location</th>
                <th className="py-2.5 px-3">Crops Cultivated</th>
                <th className="py-2.5 px-3">Total Yield</th>
                <th className="py-2.5 px-3">Batches</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/15">
              {filteredFarms.map((f) => (
                <tr key={f.farm_id} className="hover:bg-surface-container-low transition">
                  <td className="py-3 px-3 font-mono font-bold text-secondary">{f.farm_id}</td>
                  <td className="py-3 px-3 font-semibold text-on-surface">{f.farm_name}</td>
                  <td className="py-3 px-3 text-on-surface">{f.farmer}</td>
                  <td className="py-3 px-3 text-on-surface-variant">{f.location}</td>
                  <td className="py-3 px-3">
                    <div className="flex flex-wrap gap-1">
                      {f.crops.map((c) => (
                        <span key={c} className="px-2 py-0.5 rounded bg-surface-container text-on-surface font-mono text-[10px]">
                          {c}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-on-surface">{f.total_harvest_kg} kg</td>
                  <td className="py-3 px-3 font-mono text-secondary font-semibold">{f.batch_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Suppliers Table */}
      {activeTab === 'suppliers' && (
        <div className="bg-white rounded-2xl border border-outline-variant/40 shadow-sm overflow-hidden p-6">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase font-mono text-[10px]">
                <th className="py-2.5 px-3">FPO Collective / Supplier</th>
                <th className="py-2.5 px-3">Farms Represented</th>
                <th className="py-2.5 px-3">Botanicals Handled</th>
                <th className="py-2.5 px-3">Aggregate Volume</th>
                <th className="py-2.5 px-3">Active Batches</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/15">
              {filteredSuppliers.map((s) => (
                <tr key={s.supplier} className="hover:bg-surface-container-low transition">
                  <td className="py-3 px-3 font-semibold text-on-surface">{s.supplier}</td>
                  <td className="py-3 px-3 font-mono text-secondary font-bold">{s.farms_represented} Farms</td>
                  <td className="py-3 px-3">
                    <div className="flex flex-wrap gap-1">
                      {s.crops_handled.map((c) => (
                        <span key={c} className="px-2 py-0.5 rounded bg-surface-container text-on-surface font-mono text-[10px]">
                          {c}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-on-surface">{s.total_volume_kg.toLocaleString()} kg</td>
                  <td className="py-3 px-3 font-mono text-secondary font-semibold">{s.batch_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
