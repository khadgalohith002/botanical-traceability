import React from 'react';

export default function Sidebar({
  appMode,
  setAppMode,
  activePage,
  setActivePage,
  currentLang,
  setCurrentLang,
  languages,
  health,
  t,
  isRtl,
}) {
  const adminNav = [
    { id: 'dashboard', label: 'Dashboard', icon: 'hub' },
    { id: 'farms-and-suppliers', label: 'Farms & Suppliers', icon: 'agriculture' },
    { id: 'botanical-batches', label: 'Botanical Batches', icon: 'potted_plant' },
    { id: 'supply-chain-explorer', label: 'Supply Chain Explorer', icon: 'account_tree' },
    { id: 'traceability-search', label: 'Traceability Search', icon: 'terminal' },
    { id: 'analytics-and-reports', label: 'Analytics & Reports', icon: 'insights' },
  ];

  const farmerNav = [
    { id: 'farmer-register', label: t.farmer_register_harvest || 'Register Harvest', icon: 'add_circle' },
    { id: 'farmer-catalog', label: t.catalog_title || 'Botanical Catalog', icon: 'spa' },
    { id: 'farmer-batches', label: t.farmer_my_batches || 'My Batches', icon: 'inventory_2' },
    { id: 'farmer-voice', label: t.voice_assistant_title || 'Voice Assistant', icon: 'mic' },
  ];

  const navItems = appMode === 'farmer' ? farmerNav : adminNav;

  return (
    <aside
      className={`fixed top-0 h-screen w-72 bg-primary-container z-50 flex flex-col justify-between text-on-primary shadow-lg ${
        isRtl ? 'right-0 border-l border-white/10' : 'left-0 border-r border-white/10'
      }`}
    >
      <div className="flex flex-col overflow-y-auto">
        {/* Brand Header */}
        <div className="h-16 px-4 flex items-center gap-3 bg-primary/30 border-b border-white/5">
          <div className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center text-xl shadow">
            🌿
          </div>
          <div className="flex flex-col">
            <span className="font-headline text-lg font-semibold tracking-tight text-on-primary leading-tight">
              PhytoTrace
            </span>
            <span className="font-mono text-[10px] text-on-primary-container tracking-wider uppercase">
              Property Graph v2.4
            </span>
          </div>
        </div>

        {/* Application Mode Switcher */}
        <div className="p-3">
          <div className="bg-primary/50 p-1 rounded-xl flex items-center gap-1 border border-white/10">
            <button
              onClick={() => {
                setAppMode('farmer');
                setActivePage('farmer-register');
              }}
              className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all ${
                appMode === 'farmer'
                  ? 'bg-secondary text-on-primary shadow'
                  : 'text-on-primary-container hover:text-white'
              }`}
            >
              <span className="material-symbols-outlined text-[16px]">psychiatry</span>
              <span>{t.mode_farmer || 'Farmer Mode'}</span>
            </button>
            <button
              onClick={() => {
                setAppMode('admin');
                setActivePage('dashboard');
              }}
              className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all ${
                appMode === 'admin'
                  ? 'bg-secondary text-on-primary shadow'
                  : 'text-on-primary-container hover:text-white'
              }`}
            >
              <span className="material-symbols-outlined text-[16px]">admin_panel_settings</span>
              <span>{t.mode_admin || 'Admin'}</span>
            </button>
          </div>
        </div>

        {/* Language Selector */}
        <div className="px-4 py-2 flex flex-col gap-1.5">
          <label className="text-[11px] font-mono uppercase tracking-wider text-on-primary-container flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px]">translate</span>
            <span>{t.select_language || 'Language'}</span>
          </label>
          <select
            value={currentLang}
            onChange={(e) => setCurrentLang(e.target.value)}
            className="w-full bg-primary/60 border border-white/10 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-secondary transition cursor-pointer"
          >
            {languages.map((l) => (
              <option key={l.code} value={l.code} className="bg-primary-container text-white">
                {l.native} ({l.name})
              </option>
            ))}
          </select>
        </div>

        {/* Navigation Category Label */}
        <div className="px-4 pt-4 pb-1">
          <span className="font-mono text-[10px] uppercase tracking-wider text-on-primary-container/80">
            {appMode === 'farmer' ? (t.farmer_mode_title || 'Farmer Portal') : 'Provenance Core'}
          </span>
        </div>

        {/* Navigation Items */}
        <nav className="flex flex-col gap-1 px-3 py-1">
          {navItems.map((item) => {
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all text-left ${
                  isActive
                    ? 'bg-secondary text-white font-semibold shadow-sm'
                    : 'text-on-primary-container hover:bg-white/5 hover:text-white'
                }`}
              >
                <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                <span className="truncate">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer / Database Status */}
      <div className="flex flex-col bg-primary/40 border-t border-white/10">
        <div className="p-3 flex flex-col gap-1.5 font-mono text-[11px]">
          <div className="flex items-center justify-between">
            <span className="text-on-primary-container flex items-center gap-1.5">
              <span
                className={`h-2 w-2 rounded-full inline-block ${
                  health?.database?.connected ? 'bg-emerald-400' : 'bg-amber-400'
                }`}
              ></span>
              <span>Neo4j Graph:</span>
            </span>
            <span className="text-white font-medium">
              {health?.database?.connected ? 'Connected' : 'In-Memory'}
            </span>
          </div>

          <div className="text-on-primary-container/70 truncate text-[10px]">
            {health?.database?.uri || 'bolt://localhost:7687'}
          </div>

          <div className="flex items-center justify-between pt-1">
            <span className="text-on-primary-container">Active Batches:</span>
            <span className="text-secondary-fixed font-semibold">
              {health?.total_active_batches ?? 26}
            </span>
          </div>
        </div>

        {/* User Card */}
        <div className="px-3 py-2.5 bg-primary/70 flex items-center justify-between border-t border-white/5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-secondary/80 flex items-center justify-center font-bold text-xs text-white">
              {appMode === 'farmer' ? '👨‍🌾' : '🔬'}
            </div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-white leading-none">
                {appMode === 'farmer' ? 'Farmer Cultivator' : 'Supply Chain Lead'}
              </span>
              <span className="font-mono text-[10px] text-on-primary-container/80 leading-none mt-1">
                {appMode === 'farmer' ? 'Organic Producer' : 'Lead Ontologist'}
              </span>
            </div>
          </div>
          <span className="material-symbols-outlined text-on-primary-container text-[18px]">
            verified
          </span>
        </div>
      </div>
    </aside>
  );
}
