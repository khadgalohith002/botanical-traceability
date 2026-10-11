import React, { useState } from 'react';
import InteractiveGraph from './InteractiveGraph';

export default function AdminDashboard({
  kpis,
  batches,
  crops,
  graphData,
  onSelectBatchForTrace,
  onOpenCypherModal,
}) {
  const [selectedCropFilter, setSelectedCropFilter] = useState('ALL');
  const [selectedStatusFilter, setSelectedStatusFilter] = useState('ALL');
  const [tableSearch, setTableSearch] = useState('');

  // Filter batches for the table
  const filteredBatches = batches.filter((b) => {
    const matchCrop = selectedCropFilter === 'ALL' || b.crop_id === selectedCropFilter;
    const matchStatus = selectedStatusFilter === 'ALL' || b.status === selectedStatusFilter;
    const s = tableSearch.toLowerCase();
    const matchSearch =
      !s ||
      b.batch_id.toLowerCase().includes(s) ||
      b.botanical.toLowerCase().includes(s) ||
      b.farmer.toLowerCase().includes(s) ||
      b.farm_name.toLowerCase().includes(s) ||
      b.location.toLowerCase().includes(s);

    return matchCrop && matchStatus && matchSearch;
  });

  return (
    <div className="flex flex-col gap-8 pb-16">
      {/* DASHBOARD HEADER - MATCH STITCH REFERENCE */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-secondary-fixed text-on-secondary-fixed-variant font-mono text-[10px] uppercase font-bold tracking-wider">
              Neo4j Property Graph
            </span>
            <span className="text-outline-variant font-mono text-xs">|</span>
            <span className="font-mono text-xs text-on-surface-variant flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-secondary inline-block"></span>
              Bolt Session Active
            </span>
          </div>
          <h1 className="font-headline text-2xl lg:text-3xl font-bold text-on-surface tracking-tight">
            Botanical Supply Chain Overview
          </h1>
          <p className="font-body text-xs sm:text-sm text-on-surface-variant max-w-2xl">
            Track botanical origins, suppliers, and product journeys from farm to retailer with deterministic acyclic graph verification.
          </p>
        </div>

        {/* Action Toolbar */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Botanical Filter */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 bg-surface-container-low rounded-lg border border-outline-variant/40 shadow-sm text-xs font-mono">
            <span className="material-symbols-outlined text-[16px] text-secondary">filter_alt</span>
            <select
              value={selectedCropFilter}
              onChange={(e) => setSelectedCropFilter(e.target.value)}
              className="bg-transparent text-on-surface focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Botanicals ({crops.length} Taxa)</option>
              {crops.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.common_name} ({c.id})
                </option>
              ))}
            </select>
          </div>

          {/* Run Cypher Button */}
          <button
            onClick={onOpenCypherModal}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-secondary text-white font-mono text-xs font-semibold rounded-lg shadow-sm hover:bg-secondary/90 transition"
          >
            <span className="material-symbols-outlined text-[16px]">terminal</span>
            <span>Run Cypher Query</span>
          </button>
        </div>
      </div>

      {/* 4-COLUMN KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Total Farms */}
        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-semibold">
                Total Farms
              </span>
              <span className="font-headline text-3xl font-bold text-on-surface leading-tight mt-1">
                {kpis?.total_farms || 26}
              </span>
            </div>
            <div className="w-10 h-10 rounded-xl bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">location_on</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-outline-variant/20 flex items-center justify-between">
            <div className="flex items-center gap-1 text-secondary font-mono text-[11px] font-medium">
              <span className="material-symbols-outlined text-[14px]">trending_up</span>
              <span>100% geo-tagged</span>
            </div>
            <span className="text-outline text-[11px] font-mono">Origins</span>
          </div>
        </div>

        {/* Card 2: Active Suppliers */}
        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-semibold">
                Active Suppliers
              </span>
              <span className="font-headline text-3xl font-bold text-on-surface leading-tight mt-1">
                {kpis?.total_suppliers || 23}
              </span>
            </div>
            <div className="w-10 h-10 rounded-xl bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">diversity_3</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-outline-variant/20 flex items-center justify-between">
            <span className="text-on-surface-variant font-mono text-[11px]">FPO Collectives</span>
            <span className="px-2 py-0.5 rounded bg-secondary-fixed text-on-secondary-fixed-variant font-mono text-[10px] font-semibold">
              Tier-1 Valid
            </span>
          </div>
        </div>

        {/* Card 3: Harvest Batches */}
        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-semibold">
                Harvest Batches
              </span>
              <span className="font-headline text-3xl font-bold text-on-surface leading-tight mt-1">
                {kpis?.active_batches || batches.length}
              </span>
            </div>
            <div className="w-10 h-10 rounded-xl bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">spa</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-outline-variant/20 flex items-center justify-between">
            <span className="text-on-surface-variant font-mono text-[11px]">
              {(kpis?.total_harvest_kg || 18500).toLocaleString()} kg yield
            </span>
            <span className="text-secondary font-mono text-[11px] font-semibold">
              {crops.length} Taxa Active
            </span>
          </div>
        </div>

        {/* Card 4: Pending Verification */}
        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-semibold">
                Pending Verification
              </span>
              <span className="font-headline text-3xl font-bold text-amber-700 leading-tight mt-1">
                {kpis?.pending_verification || 4}
              </span>
            </div>
            <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center text-amber-700">
              <span className="material-symbols-outlined text-[22px]">verified_user</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-outline-variant/20 flex items-center justify-between">
            <div className="flex items-center gap-1 text-amber-700 font-mono text-[11px]">
              <span className="material-symbols-outlined text-[14px]">warning</span>
              <span>Intake inspection</span>
            </div>
            <span className="text-outline text-[11px] font-mono">QA Queue</span>
          </div>
        </div>
      </div>

      {/* SUPPLY CHAIN GRAPH NETWORK COMPONENT */}
      <InteractiveGraph
        graphData={graphData}
        highlightBatchId={null}
        onSelectBatchForTrace={onSelectBatchForTrace}
      />

      {/* BATCH REGISTRY TABLE - MATCH STITCH REFERENCE */}
      <div className="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-secondary text-[22px]">potted_plant</span>
            <div>
              <h2 className="font-headline text-lg font-bold text-on-surface">
                Botanical Batches Registry
              </h2>
              <span className="text-xs text-on-surface-variant font-mono">
                {filteredBatches.length} of {batches.length} batches matching criteria
              </span>
            </div>
          </div>

          {/* Search & Status Filter */}
          <div className="flex flex-wrap items-center gap-2">
            <input
              type="text"
              value={tableSearch}
              onChange={(e) => setTableSearch(e.target.value)}
              placeholder="Search table..."
              className="h-8 px-3 text-xs bg-surface-container-low border border-outline-variant/40 rounded-lg text-on-surface focus:outline-none focus:border-secondary"
            />
            <select
              value={selectedStatusFilter}
              onChange={(e) => setSelectedStatusFilter(e.target.value)}
              className="h-8 px-2.5 text-xs bg-surface-container-low border border-outline-variant/40 rounded-lg text-on-surface font-mono cursor-pointer"
            >
              <option value="ALL">All Statuses</option>
              <option value="Verified">Verified</option>
              <option value="In Transit">In Transit</option>
              <option value="Pending Verification">Pending Verification</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase font-mono text-[10px]">
                <th className="py-2.5 px-3">Batch ID</th>
                <th className="py-2.5 px-3">Botanical & Taxa</th>
                <th className="py-2.5 px-3">Farmer</th>
                <th className="py-2.5 px-3">Farm & Location</th>
                <th className="py-2.5 px-3">Date</th>
                <th className="py-2.5 px-3">Yield</th>
                <th className="py-2.5 px-3">Supply Stage</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/15">
              {filteredBatches.map((b) => (
                <tr key={b.batch_id} className="hover:bg-surface-container-low transition">
                  <td className="py-3 px-3 font-mono font-bold text-secondary">
                    {b.batch_id}
                  </td>
                  <td className="py-3 px-3">
                    <span className="font-semibold text-on-surface block">{b.botanical}</span>
                    <span className="text-[10px] text-outline italic block">{b.scientific_name}</span>
                  </td>
                  <td className="py-3 px-3 font-medium text-on-surface">
                    {b.farmer}
                  </td>
                  <td className="py-3 px-3">
                    <span className="text-on-surface block">{b.farm_name}</span>
                    <span className="text-[10px] text-on-surface-variant block">{b.location}</span>
                  </td>
                  <td className="py-3 px-3 font-mono text-on-surface-variant">
                    {b.harvest_date}
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-on-surface">
                    {b.harvest_qty_kg} kg
                  </td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded font-mono text-[10px] bg-surface-container text-on-surface font-semibold">
                      {b.current_stage}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span
                      className={`px-2 py-0.5 rounded font-mono text-[10px] font-semibold ${
                        b.status === 'Verified'
                          ? 'bg-emerald-100 text-emerald-800'
                          : b.status === 'In Transit'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}
                    >
                      {b.status}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <button
                      onClick={() => onSelectBatchForTrace(b.batch_id)}
                      className="px-2.5 py-1 bg-secondary/10 hover:bg-secondary text-secondary hover:text-white rounded-lg text-xs font-semibold transition flex items-center gap-1 ml-auto"
                    >
                      <span className="material-symbols-outlined text-[14px]">account_tree</span>
                      <span>Trace</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
