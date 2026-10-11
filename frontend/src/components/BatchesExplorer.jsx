import React, { useState } from 'react';

export default function BatchesExplorer({
  batches,
  crops,
  onSelectBatchForTrace,
}) {
  const [search, setSearch] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('ALL');
  const [selectedStage, setSelectedStage] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState('ALL');

  const filteredBatches = batches.filter((b) => {
    const s = search.toLowerCase();
    const matchSearch =
      !s ||
      b.batch_id.toLowerCase().includes(s) ||
      b.botanical.toLowerCase().includes(s) ||
      b.farmer.toLowerCase().includes(s) ||
      b.farm_name.toLowerCase().includes(s) ||
      b.location.toLowerCase().includes(s);

    const matchCrop = selectedCrop === 'ALL' || b.crop_id === selectedCrop;
    const matchStage = selectedStage === 'ALL' || b.current_stage === selectedStage;
    const matchStatus = selectedStatus === 'ALL' || b.status === selectedStatus;

    return matchSearch && matchCrop && matchStage && matchStatus;
  });

  // Export CSV
  const exportCSV = () => {
    const headers = ['Batch ID', 'Crop', 'Taxa', 'Farmer', 'Farm', 'Location', 'Date', 'Yield (kg)', 'Stage', 'Status'];
    const rows = filteredBatches.map((b) => [
      b.batch_id,
      b.botanical,
      b.scientific_name,
      b.farmer,
      b.farm_name,
      b.location,
      b.harvest_date,
      b.harvest_qty_kg,
      b.current_stage,
      b.status,
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((r) => r.map((cell) => `"${cell}"`).join(','))].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `phytotrace_batches_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex flex-col gap-6 pb-16">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-headline text-2xl font-bold text-on-surface">
            Botanical Batches Explorer
          </h1>
          <p className="text-xs text-on-surface-variant font-mono">
            Filterable master registry with full multi-hop property graph metadata.
          </p>
        </div>

        <button
          onClick={exportCSV}
          className="flex items-center gap-1.5 px-3.5 py-1.5 bg-surface-container-low hover:bg-surface-container border border-outline-variant/30 text-on-surface rounded-lg font-mono text-xs font-semibold transition"
        >
          <span className="material-symbols-outlined text-[16px]">file_download</span>
          <span>Export CSV ({filteredBatches.length})</span>
        </button>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-2xl border border-outline-variant/30 flex flex-wrap items-center gap-3">
        {/* Search */}
        <div className="flex-1 min-w-[220px] flex items-center gap-2 px-3 py-1.5 bg-surface-container-low rounded-lg border border-outline-variant/30 text-xs">
          <span className="material-symbols-outlined text-outline text-[16px]">search</span>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search batch ID, botanical, farmer, farm, or location..."
            className="w-full bg-transparent focus:outline-none text-on-surface"
          />
        </div>

        {/* Crop Select */}
        <select
          value={selectedCrop}
          onChange={(e) => setSelectedCrop(e.target.value)}
          className="h-9 px-2.5 bg-surface-container-low border border-outline-variant/30 rounded-lg text-xs text-on-surface font-mono cursor-pointer"
        >
          <option value="ALL">All Crops ({crops.length})</option>
          {crops.map((c) => (
            <option key={c.id} value={c.id}>
              {c.common_name} ({c.id})
            </option>
          ))}
        </select>

        {/* Stage Select */}
        <select
          value={selectedStage}
          onChange={(e) => setSelectedStage(e.target.value)}
          className="h-9 px-2.5 bg-surface-container-low border border-outline-variant/30 rounded-lg text-xs text-on-surface font-mono cursor-pointer"
        >
          <option value="ALL">All Stages</option>
          <option value="Harvest Batch">Harvest Batch</option>
          <option value="Processor">Processor</option>
          <option value="Manufacturer">Manufacturer</option>
          <option value="Distributor">Distributor</option>
          <option value="Retailer">Retailer</option>
        </select>

        {/* Status Select */}
        <select
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
          className="h-9 px-2.5 bg-surface-container-low border border-outline-variant/30 rounded-lg text-xs text-on-surface font-mono cursor-pointer"
        >
          <option value="ALL">All Statuses</option>
          <option value="Verified">Verified</option>
          <option value="In Transit">In Transit</option>
          <option value="Pending Verification">Pending Verification</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl border border-outline-variant/40 shadow-sm overflow-hidden p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase font-mono text-[10px]">
                <th className="py-2.5 px-3">Batch ID</th>
                <th className="py-2.5 px-3">Botanical Crop</th>
                <th className="py-2.5 px-3">Farmer</th>
                <th className="py-2.5 px-3">Farm Plot</th>
                <th className="py-2.5 px-3">Harvest Date</th>
                <th className="py-2.5 px-3">Weight</th>
                <th className="py-2.5 px-3">Facility / Partner</th>
                <th className="py-2.5 px-3">Stage</th>
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
                  <td className="py-3 px-3 text-on-surface-variant text-[11px]">
                    {b.processor || b.manufacturer}
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
