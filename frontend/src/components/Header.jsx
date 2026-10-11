import React from 'react';

export default function Header({
  appMode,
  activePage,
  health,
  searchQuery,
  setSearchQuery,
  onOpenCypherModal,
  isRtl,
}) {
  const pageTitles = {
    dashboard: 'Dashboard',
    'farms-and-suppliers': 'Farms & Suppliers',
    'botanical-batches': 'Botanical Batches',
    'supply-chain-explorer': 'Supply Chain Explorer',
    'traceability-search': 'Traceability Search',
    'analytics-and-reports': 'Analytics & Reports',
    'farmer-register': 'Register Harvest',
    'farmer-catalog': 'Botanical Catalog',
    'farmer-batches': 'My Harvest Batches',
    'farmer-voice': 'Voice Assistant',
  };

  return (
    <header
      className={`fixed top-0 ${
        isRtl ? 'right-72 left-0' : 'left-72 right-0'
      } h-16 bg-surface/90 backdrop-blur-md shadow-sm border-b border-outline-variant/30 z-40 flex items-center justify-between px-6`}
    >
      {/* Left: Breadcrumbs & Search */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 font-mono text-xs text-on-surface-variant">
          <span className="material-symbols-outlined text-[16px]">schema</span>
          <span>Botanical Supply Chain</span>
          <span className="text-outline">/</span>
          <span className="text-on-surface font-semibold">
            {pageTitles[activePage] || activePage}
          </span>
        </div>

        <div className="relative flex items-center hidden sm:flex">
          <span className="material-symbols-outlined absolute left-3 text-[18px] text-outline">
            search
          </span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search batch ID, botanical crop, farmer, farm, or location..."
            className="w-80 md:w-96 pl-9 pr-12 py-1.5 h-9 bg-surface-container-low text-on-surface placeholder:text-outline/70 font-body text-xs rounded-lg border border-outline-variant/40 focus:outline-none focus:border-secondary focus:bg-white transition"
          />
          <span className="absolute right-2 px-1.5 py-0.5 bg-surface-container-high rounded font-mono text-[10px] text-on-surface-variant">
            Ctrl+K
          </span>
        </div>
      </div>

      {/* Right: Status & Actions */}
      <div className="flex items-center gap-3">
        {/* Database Status Chip */}
        <div className="flex items-center gap-2 px-3 py-1 bg-surface-container-low rounded-lg border border-outline-variant/30 hidden md:flex">
          <span
            className={`h-2 w-2 rounded-full ${
              health?.database?.connected ? 'bg-emerald-500' : 'bg-amber-500'
            }`}
          ></span>
          <span className="font-mono text-xs text-on-surface font-medium">
            {health?.database?.connected ? 'Neo4j Bolt Active' : 'NetworkX Property Graph'}
          </span>
        </div>

        {/* Export Cypher Query Button */}
        <button
          onClick={onOpenCypherModal}
          className="h-9 px-3 bg-secondary/10 hover:bg-secondary/20 text-secondary border border-secondary/20 rounded-lg font-mono text-xs font-semibold flex items-center gap-1.5 transition"
          title="Download or inspect Cypher graph query script"
        >
          <span className="material-symbols-outlined text-[16px]">terminal</span>
          <span className="hidden lg:inline">Neo4j Cypher</span>
        </button>

        {/* Notifications Icon */}
        <div className="w-8 h-8 rounded-full bg-surface-container-low flex items-center justify-center text-on-surface-variant relative cursor-pointer hover:bg-surface-container">
          <span className="material-symbols-outlined text-[18px]">notifications</span>
          <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-secondary"></span>
        </div>
      </div>
    </header>
  );
}
