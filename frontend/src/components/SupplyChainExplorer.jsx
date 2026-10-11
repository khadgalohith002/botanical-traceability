import React, { useState } from 'react';
import InteractiveGraph from './InteractiveGraph';

export default function SupplyChainExplorer({
  graphData,
  batches,
  onSelectBatchForTrace,
}) {
  const [selectedBatchId, setSelectedBatchId] = useState(batches[0]?.batch_id || '');

  return (
    <div className="flex flex-col gap-6 pb-16">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-headline text-2xl font-bold text-on-surface">
            Supply Chain Graph Explorer
          </h1>
          <p className="text-xs text-on-surface-variant font-mono">
            Interactive topological visualization powered by NetworkX &amp; Neo4j.
          </p>
        </div>

        {/* Highlight batch selector */}
        <div className="flex items-center gap-2 bg-white p-2 rounded-xl border border-outline-variant/30 shadow-sm text-xs font-mono">
          <span className="text-secondary font-bold">Highlight Path:</span>
          <select
            value={selectedBatchId}
            onChange={(e) => setSelectedBatchId(e.target.value)}
            className="bg-surface-container-low px-3 py-1.5 rounded-lg border border-outline-variant/30 text-on-surface focus:outline-none cursor-pointer"
          >
            {batches.map((b) => (
              <option key={b.batch_id} value={b.batch_id}>
                {b.batch_id} — {b.botanical} ({b.farmer})
              </option>
            ))}
          </select>
          {selectedBatchId && (
            <button
              onClick={() => onSelectBatchForTrace(selectedBatchId)}
              className="px-3 py-1.5 bg-secondary text-white rounded-lg font-semibold hover:bg-secondary/90 transition flex items-center gap-1"
            >
              <span className="material-symbols-outlined text-[14px]">timeline</span>
              <span>Inspect</span>
            </button>
          )}
        </div>
      </div>

      {/* Graph Visualizer */}
      <InteractiveGraph
        graphData={graphData}
        highlightBatchId={selectedBatchId}
        onSelectBatchForTrace={onSelectBatchForTrace}
      />

      {/* 10-Tier Architectural Topology Reference */}
      <div className="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-4">
        <h3 className="font-headline text-base font-bold text-on-surface">
          PhytoTrace Graph Schema &amp; Node Hierarchy
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 font-mono text-xs">
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#1B4332] font-bold block mb-1">1. Farmer</span>
            <span className="text-on-surface-variant text-[11px]">(:Farmer) Cultivator</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#2D6A4F] font-bold block mb-1">2. Farm</span>
            <span className="text-on-surface-variant text-[11px]">(:Farm) Geographic plot</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#52B788] font-bold block mb-1">3. Botanical</span>
            <span className="text-on-surface-variant text-[11px]">(:Botanical) Taxa &amp; genus</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#0284C7] font-bold block mb-1">4. HarvestBatch</span>
            <span className="text-on-surface-variant text-[11px]">(:HarvestBatch) Yield mass</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#7C3AED] font-bold block mb-1">5. Processor</span>
            <span className="text-on-surface-variant text-[11px]">(:Processor) Extraction unit</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#6366F1] font-bold block mb-1">6. ProcessedBatch</span>
            <span className="text-on-surface-variant text-[11px]">(:ProcessedBatch) Extract lot</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#D97706] font-bold block mb-1">7. Manufacturer</span>
            <span className="text-on-surface-variant text-[11px]">(:Manufacturer) Formulation</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#F59E0B] font-bold block mb-1">8. FinishedLot</span>
            <span className="text-on-surface-variant text-[11px]">(:FinishedLot) Packaging</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#0D9488] font-bold block mb-1">9. Distributor</span>
            <span className="text-on-surface-variant text-[11px]">(:Distributor) Logistics depot</span>
          </div>
          <div className="p-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
            <span className="text-[#334155] font-bold block mb-1">10. Retailer</span>
            <span className="text-on-surface-variant text-[11px]">(:Retailer) Dispensary</span>
          </div>
        </div>
      </div>
    </div>
  );
}
