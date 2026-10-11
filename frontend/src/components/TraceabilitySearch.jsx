import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function TraceabilitySearch({
  batches,
  initialBatchId = '',
}) {
  const [selectedBatchId, setSelectedBatchId] = useState(initialBatchId || (batches[0]?.batch_id || ''));
  const [traceData, setTraceData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (selectedBatchId) {
      loadTrace(selectedBatchId);
    }
  }, [selectedBatchId]);

  const loadTrace = async (bId) => {
    setLoading(true);
    setError('');
    try {
      const data = await api.traceBatch(bId);
      setTraceData(data);
    } catch (err) {
      setError(err.message || 'Failed to retrieve batch trace');
      setTraceData(null);
    } finally {
      setLoading(false);
    }
  };

  const batch = traceData?.batch;
  const custodyChain = traceData?.custody_chain || [];
  const graphTrace = traceData?.graph_trace;

  return (
    <div className="flex flex-col gap-6 pb-16">
      {/* Search Console Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-headline text-2xl font-bold text-on-surface">
            Deterministic Traceability Search
          </h1>
          <p className="text-xs text-on-surface-variant font-mono">
            Verify acyclic property graph custody from origin cultivator to retail dispensary.
          </p>
        </div>

        {/* Quick Batch Selector */}
        <div className="flex items-center gap-2 bg-white p-2 rounded-xl border border-outline-variant/30 shadow-sm text-xs font-mono">
          <span className="text-secondary font-bold">Select Batch:</span>
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
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center gap-2">
          <span className="material-symbols-outlined text-[18px]">error</span>
          <span>{error}</span>
        </div>
      )}

      {loading && (
        <div className="p-12 text-center text-on-surface-variant font-mono text-xs">
          Traversing property graph and computing shortest path...
        </div>
      )}

      {batch && !loading && (
        <>
          {/* Batch Summary Card */}
          <div className="bg-gradient-to-r from-primary-container via-primary-container/95 to-secondary/30 rounded-2xl p-6 text-white shadow-md flex flex-col md:flex-row md:items-center justify-between gap-6 border border-white/10">
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-secondary text-white font-mono text-[11px] font-bold uppercase tracking-wider">
                  Verified Batch
                </span>
                <span className="text-white/40">|</span>
                <span className="font-mono text-xs text-white/90">
                  {batch.batch_id}
                </span>
              </div>
              <h2 className="font-headline text-2xl md:text-3xl font-bold tracking-tight">
                {batch.botanical} &bull; <span className="font-normal italic text-lg text-white/90">{batch.scientific_name}</span>
              </h2>
              <div className="flex flex-wrap items-center gap-4 text-xs text-white/80 font-mono mt-1">
                <span>Variety: <strong className="text-white">{batch.variety}</strong></span>
                <span>Origin: <strong className="text-white">{batch.location}</strong></span>
                <span>Harvest Qty: <strong className="text-white">{batch.harvest_qty_kg} kg</strong></span>
                <span>Current Stage: <strong className="text-secondary-fixed">{batch.current_stage}</strong></span>
              </div>
            </div>

            <div className="flex flex-col items-end gap-1 bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/15">
              <span className="font-mono text-[11px] text-white/70 uppercase">Topological Hops</span>
              <span className="font-headline text-3xl font-bold text-white leading-none">
                {graphTrace?.hop_count || 8}
              </span>
              <span className="text-[10px] text-white/80 font-mono">Directed Edges</span>
            </div>
          </div>

          {/* 10-Tier Custody Journey */}
          <div className="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-6">
            <div className="flex items-center justify-between border-b border-outline-variant/20 pb-4">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-secondary text-[24px]">verified</span>
                <div>
                  <h3 className="font-headline text-lg font-bold text-on-surface">
                    10-Tier Farm-to-Retailer Custody Pathway
                  </h3>
                  <span className="text-xs text-on-surface-variant font-mono">
                    Deterministic graph traversal validated by NetworkX
                  </span>
                </div>
              </div>

              <span className="px-3 py-1 bg-emerald-50 text-emerald-800 rounded-full font-mono text-xs font-semibold">
                {batch.status}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {custodyChain.map((step) => {
                const isVerified = step.status === 'Verified' || step.status === 'Delivered';
                return (
                  <div
                    key={step.tier}
                    className="p-4 rounded-xl border border-outline-variant/30 bg-surface-container-lowest flex items-start gap-3 hover:border-secondary transition shadow-sm"
                  >
                    <div className="w-10 h-10 rounded-xl bg-surface-container-low flex items-center justify-center text-secondary shrink-0 font-mono font-bold text-xs">
                      {step.tier}
                    </div>
                    <div className="flex flex-col flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-[10px] uppercase font-bold text-secondary">
                          {step.label}
                        </span>
                        <span
                          className={`px-2 py-0.5 rounded font-mono text-[10px] font-semibold ${
                            isVerified
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {step.status}
                        </span>
                      </div>
                      <span className="font-headline font-bold text-sm text-on-surface mt-0.5">
                        {step.name || step.batch_id || step.processed_batch_id || step.finished_batch_id}
                      </span>
                      <span className="text-xs text-on-surface-variant mt-1">
                        {step.role || step.facility_type || step.hub_type || step.location || step.city || step.scientific_name || `Qty: ${step.harvest_qty_kg} kg`}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
