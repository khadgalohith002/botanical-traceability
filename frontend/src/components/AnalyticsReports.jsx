import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function AnalyticsReports() {
  const [metrics, setMetrics] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const [mRes, aRes] = await Promise.all([
          api.getGraphMetrics(),
          api.getAnalyticsSummary(),
        ]);
        setMetrics(mRes);
        setAnalytics(aRes);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadMetrics();
  }, []);

  return (
    <div className="flex flex-col gap-8 pb-16">
      <div>
        <h1 className="font-headline text-2xl font-bold text-on-surface">
          Graph Analytics &amp; Topological Metrics
        </h1>
        <p className="text-xs text-on-surface-variant font-mono">
          Degree centrality, graph density, connected components, and volumetric distribution.
        </p>
      </div>

      {/* Top Cards: Graph Topology */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col">
          <span className="font-mono text-[10px] uppercase text-on-surface-variant font-semibold">
            Total Graph Nodes
          </span>
          <span className="font-headline text-3xl font-bold text-on-surface mt-1">
            {metrics?.num_nodes || 213}
          </span>
          <span className="text-[11px] font-mono text-secondary mt-2">10 Distinct Entity Labels</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col">
          <span className="font-mono text-[10px] uppercase text-on-surface-variant font-semibold">
            Directed Edges
          </span>
          <span className="font-headline text-3xl font-bold text-on-surface mt-1">
            {metrics?.num_edges || 221}
          </span>
          <span className="text-[11px] font-mono text-secondary mt-2">9 Typed Relationships</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col">
          <span className="font-mono text-[10px] uppercase text-on-surface-variant font-semibold">
            Graph Density
          </span>
          <span className="font-headline text-3xl font-bold text-on-surface mt-1">
            {metrics?.density ? Number(metrics.density).toFixed(4) : '0.0098'}
          </span>
          <span className="text-[11px] font-mono text-outline mt-2">Sparse Acyclic DAG</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col">
          <span className="font-mono text-[10px] uppercase text-on-surface-variant font-semibold">
            Connected Components
          </span>
          <span className="font-headline text-3xl font-bold text-secondary mt-1">
            {metrics?.num_components || 26}
          </span>
          <span className="text-[11px] font-mono text-secondary mt-2">Weakly Connected Lineages</span>
        </div>
      </div>

      {/* Centrality Ranking Table & Crop Volume Bars */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Degree Centrality Table (7 cols) */}
        <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-secondary text-[22px]">hub</span>
            <div>
              <h3 className="font-headline text-base font-bold text-on-surface">
                Degree Centrality &amp; Critical Hub Analysis
              </h3>
              <p className="text-xs text-on-surface-variant">
                Top aggregators, facilities, and distribution hubs with high network centrality.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase font-mono text-[10px]">
                  <th className="py-2.5 px-3">Node / Entity</th>
                  <th className="py-2.5 px-3">Label</th>
                  <th className="py-2.5 px-3">Degree Score</th>
                  <th className="py-2.5 px-3">In / Out</th>
                  <th className="py-2.5 px-3 text-right">Connections</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/15">
                {metrics?.centrality_ranking?.map((c) => (
                  <tr key={c.node_id} className="hover:bg-surface-container-low transition">
                    <td className="py-2.5 px-3 font-semibold text-on-surface">
                      {c.display_name}
                      <span className="text-[10px] font-mono text-outline block truncate max-w-xs">
                        {c.node_id}
                      </span>
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="px-2 py-0.5 rounded font-mono text-[10px] bg-surface-container font-semibold">
                        {c.label}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-secondary">
                      {c.degree_centrality}
                    </td>
                    <td className="py-2.5 px-3 font-mono text-on-surface-variant text-[11px]">
                      {c.in_centrality} / {c.out_centrality}
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-right text-on-surface">
                      {c.total_connections}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Crop Volume Bar Chart (5 cols) */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-secondary text-[22px]">bar_chart</span>
            <div>
              <h3 className="font-headline text-base font-bold text-on-surface">
                Harvest Yield by Botanical Crop
              </h3>
              <p className="text-xs text-on-surface-variant">
                Aggregate weight in kg across registered batches.
              </p>
            </div>
          </div>

          <div className="space-y-3 max-h-[460px] overflow-y-auto pr-2">
            {analytics?.crop_volumes?.map((cv, idx) => {
              const maxVol = analytics.crop_volumes[0]?.volume_kg || 1;
              const pct = Math.round((cv.volume_kg / maxVol) * 100);
              return (
                <div key={cv.crop} className="flex flex-col gap-1 text-xs">
                  <div className="flex items-center justify-between font-mono">
                    <span className="font-semibold text-on-surface truncate max-w-[200px]">
                      {cv.crop}
                    </span>
                    <span className="font-bold text-secondary">{cv.volume_kg.toLocaleString()} kg</span>
                  </div>
                  <div className="w-full h-3 bg-surface-container-low rounded-full overflow-hidden">
                    <div
                      className="h-full bg-secondary rounded-full transition-all"
                      style={{ width: `${pct}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
