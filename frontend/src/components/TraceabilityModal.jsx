import React from 'react';

export default function TraceabilityModal({
  traceData,
  onClose,
}) {
  if (!traceData) return null;

  const { batch, custody_chain, graph_trace } = traceData;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fadeIn">
      <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-outline-variant/30 overflow-hidden">
        {/* Header */}
        <div className="p-6 bg-gradient-to-r from-primary-container to-secondary/40 text-white flex items-start justify-between border-b border-white/10">
          <div className="flex flex-col gap-1.5">
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-secondary text-white font-mono text-[11px] font-bold tracking-wider uppercase">
                Acyclic Property Graph Trace
              </span>
              <span className="text-white/40">|</span>
              <span className="font-mono text-xs text-white/90">
                {graph_trace?.hop_count || 8} Hops &bull; Deterministic Lineage
              </span>
            </div>
            <h2 className="font-headline text-2xl font-bold tracking-tight flex items-center gap-2">
              <span>{batch?.botanical}</span>
              <span className="text-white/60 font-mono text-lg font-normal">
                [{batch?.batch_id}]
              </span>
            </h2>
            <p className="text-xs text-white/80 font-mono">
              Scientific Name: <span className="italic">{batch?.scientific_name}</span> &bull; Harvest Qty: {batch?.harvest_qty_kg} kg &bull; Origin: {batch?.location}
            </p>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Modal Body: 10-Tier Custody Journey */}
        <div className="p-6 overflow-y-auto flex flex-col gap-6">
          {/* Summary Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 flex flex-col">
              <span className="font-mono text-[10px] text-on-surface-variant uppercase">Current Stage</span>
              <span className="font-headline font-bold text-sm text-on-surface mt-0.5">
                {batch?.current_stage || 'Retailer'}
              </span>
            </div>
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 flex flex-col">
              <span className="font-mono text-[10px] text-on-surface-variant uppercase">Verification Status</span>
              <span
                className={`font-headline font-bold text-sm mt-0.5 ${
                  batch?.status === 'Verified' ? 'text-emerald-700' : 'text-amber-700'
                }`}
              >
                {batch?.status}
              </span>
            </div>
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 flex flex-col">
              <span className="font-mono text-[10px] text-on-surface-variant uppercase">Shortest Path Hops</span>
              <span className="font-headline font-bold text-sm text-secondary mt-0.5">
                {graph_trace?.hop_count || 8} Directed Steps
              </span>
            </div>
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 flex flex-col">
              <span className="font-mono text-[10px] text-on-surface-variant uppercase">Subgraph Nodes</span>
              <span className="font-headline font-bold text-sm text-on-surface mt-0.5">
                {graph_trace?.subgraph_nodes_count || 10} Vertices
              </span>
            </div>
          </div>

          {/* Stepper Timeline */}
          <div>
            <h3 className="font-headline text-base font-bold text-on-surface mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary text-[20px]">linear_scale</span>
              <span>10-Tier Farm-to-Retailer Custody Chain</span>
            </h3>

            <div className="relative pl-6 border-l-2 border-secondary/30 space-y-6">
              {custody_chain?.map((step) => {
                const isVerified = step.status === 'Verified' || step.status === 'Delivered';
                return (
                  <div key={step.tier} className="relative group">
                    {/* Circle Node on Timeline */}
                    <span
                      className={`absolute -left-[31px] top-1 w-6 h-6 rounded-full flex items-center justify-center font-mono text-[10px] font-bold text-white shadow ${
                        isVerified ? 'bg-secondary' : 'bg-amber-500'
                      }`}
                    >
                      {step.tier}
                    </span>

                    {/* Step Card */}
                    <div className="bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/40 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-secondary/60 transition">
                      <div className="flex items-start gap-3">
                        <div className="w-10 h-10 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary">
                          <span className="material-symbols-outlined text-[20px]">{step.icon}</span>
                        </div>
                        <div className="flex flex-col">
                          <span className="font-mono text-[10px] uppercase font-bold text-secondary">
                            Tier {step.tier}: {step.label}
                          </span>
                          <span className="font-headline text-sm font-bold text-on-surface">
                            {step.name || step.batch_id || step.processed_batch_id || step.finished_batch_id}
                          </span>
                          <span className="text-xs text-on-surface-variant mt-0.5">
                            {step.role || step.facility_type || step.hub_type || step.location || step.city || step.scientific_name || `Qty: ${step.harvest_qty_kg} kg`}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 self-start sm:self-center">
                        <span
                          className={`px-2.5 py-1 rounded-full font-mono text-[11px] font-semibold ${
                            isVerified
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {step.status}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-surface-container-low border-t border-outline-variant/30 flex items-center justify-between">
          <span className="font-mono text-xs text-on-surface-variant">
            Acyclic verification verified by NetworkX &amp; Neo4j
          </span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-secondary text-white rounded-lg font-headline text-xs font-semibold hover:bg-secondary/90 transition"
          >
            Close Trace
          </button>
        </div>
      </div>
    </div>
  );
}
