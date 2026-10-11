import React, { useState, useMemo } from 'react';

export default function InteractiveGraph({
  graphData,
  highlightBatchId,
  onSelectBatchForTrace,
}) {
  const [selectedNode, setSelectedNode] = useState(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const nodes = graphData?.nodes || [];
  const edges = graphData?.edges || [];

  // Coordinate scaling to SVG canvas (width 1100, height 500)
  const { scaledNodes, nodeMap } = useMemo(() => {
    if (!nodes.length) return { scaledNodes: [], nodeMap: new Map() };

    // Find min/max coordinates
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    nodes.forEach((n) => {
      if (n.x < minX) minX = n.x;
      if (n.x > maxX) maxX = n.x;
      if (n.y < minY) minY = n.y;
      if (n.y > maxY) maxY = n.y;
    });

    const rangeX = maxX - minX || 1;
    const rangeY = maxY - minY || 1;
    const width = 1000;
    const height = 440;
    const paddingX = 60;
    const paddingY = 40;

    const map = new Map();
    const result = nodes.map((n) => {
      const cx = paddingX + ((n.x - minX) / rangeX) * (width - paddingX * 2);
      const cy = paddingY + ((n.y - minY) / rangeY) * (height - paddingY * 2);
      const scaled = { ...n, cx, cy };
      map.set(n.id, scaled);
      return scaled;
    });

    return { scaledNodes: result, nodeMap: map };
  }, [nodes]);

  // Pan handlers
  const handleMouseDown = (e) => {
    if (e.target.tagName === 'svg' || e.target.tagName === 'rect') {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
    }
  };

  const handleMouseUp = () => setIsDragging(false);

  return (
    <div className="bg-white rounded-2xl border border-outline-variant/40 shadow-sm overflow-hidden flex flex-col">
      {/* Graph Toolbar */}
      <div className="px-6 py-4 border-b border-outline-variant/20 flex flex-wrap items-center justify-between gap-4 bg-surface-container-lowest">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary text-[22px]">account_tree</span>
          <div>
            <h3 className="font-headline text-base font-bold text-on-surface leading-tight">
              Interactive Property Graph Network
            </h3>
            <span className="font-mono text-[11px] text-on-surface-variant">
              {nodes.length} Nodes &bull; {edges.length} Relationships &bull; 10 Custody Tiers
            </span>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-3 text-[11px] font-mono">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#1B4332]"></span> Farmer
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#2D6A4F]"></span> Farm
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#52B788]"></span> Botanical
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#0284C7]"></span> Batch
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#7C3AED]"></span> Facility
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#334155]"></span> Retailer
          </span>
        </div>

        {/* Zoom Controls */}
        <div className="flex items-center gap-1 bg-surface-container-low p-1 rounded-lg border border-outline-variant/30">
          <button
            onClick={() => setZoom((z) => Math.min(z + 0.2, 2.5))}
            className="p-1 hover:bg-white rounded text-on-surface-variant hover:text-on-surface"
            title="Zoom In"
          >
            <span className="material-symbols-outlined text-[18px]">zoom_in</span>
          </button>
          <button
            onClick={() => setZoom((z) => Math.max(z - 0.2, 0.5))}
            className="p-1 hover:bg-white rounded text-on-surface-variant hover:text-on-surface"
            title="Zoom Out"
          >
            <span className="material-symbols-outlined text-[18px]">zoom_out</span>
          </button>
          <button
            onClick={() => {
              setZoom(1);
              setPan({ x: 0, y: 0 });
            }}
            className="p-1 hover:bg-white rounded text-on-surface-variant hover:text-on-surface"
            title="Reset View"
          >
            <span className="material-symbols-outlined text-[18px]">restart_alt</span>
          </button>
        </div>
      </div>

      {/* Main Graph SVG Canvas */}
      <div
        className="relative h-[480px] bg-slate-50/60 overflow-hidden cursor-grab active:cursor-grabbing select-none"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      >
        <svg
          className="w-full h-full"
          viewBox="0 0 1000 440"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            <marker
              id="arrowhead"
              markerWidth="7"
              markerHeight="5"
              refX="16"
              refY="2.5"
              orient="auto"
            >
              <polygon points="0 0, 7 2.5, 0 5" fill="#94A3B8" />
            </marker>
            <marker
              id="arrowhead-highlight"
              markerWidth="8"
              markerHeight="6"
              refX="18"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="#26734D" />
            </marker>
          </defs>

          <g
            transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}
            style={{ transformOrigin: 'center center' }}
          >
            {/* Edges */}
            {edges.map((e, idx) => {
              const u = nodeMap.get(e.source);
              const v = nodeMap.get(e.target);
              if (!u || !v) return null;

              const isHl = e.highlighted;
              return (
                <line
                  key={`${e.source}-${e.target}-${idx}`}
                  x1={u.cx}
                  y1={u.cy}
                  x2={v.cx}
                  y2={v.cy}
                  stroke={isHl ? '#26734D' : '#CBD5E1'}
                  strokeWidth={isHl ? 3 : 1.2}
                  strokeDasharray={isHl ? 'none' : 'none'}
                  markerEnd={isHl ? 'url(#arrowhead-highlight)' : 'url(#arrowhead)'}
                  className="transition-all"
                />
              );
            })}

            {/* Nodes */}
            {scaledNodes.map((n) => {
              const isHl = n.highlighted;
              const isSelected = selectedNode?.id === n.id;
              const radius = isHl ? 14 : (n.size ? n.size / 2 : 10);

              return (
                <g
                  key={n.id}
                  transform={`translate(${n.cx}, ${n.cy})`}
                  className="cursor-pointer group"
                  onClick={() => setSelectedNode(n)}
                >
                  {/* Halo pulse for highlighted */}
                  {isHl && (
                    <circle
                      r={radius + 6}
                      fill="#26734D"
                      opacity="0.25"
                      className="animate-ping"
                    />
                  )}

                  {/* Outer selection ring */}
                  {isSelected && (
                    <circle
                      r={radius + 4}
                      fill="none"
                      stroke="#111c2d"
                      strokeWidth="2"
                    />
                  )}

                  {/* Node Body */}
                  <circle
                    r={radius}
                    fill={n.color || '#2D6A4F'}
                    stroke={isHl ? '#26734D' : '#ffffff'}
                    strokeWidth={isHl ? 2.5 : 1.5}
                    className="transition-all hover:scale-125"
                  />

                  {/* Node Label Text */}
                  <text
                    y={radius + 12}
                    textAnchor="middle"
                    className="font-mono text-[9px] fill-slate-700 pointer-events-none select-none font-medium"
                  >
                    {n.display_name?.slice(0, 14)}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>

        {/* Selected Node Details Card Float */}
        {selectedNode && (
          <div className="absolute bottom-4 right-4 bg-white/95 backdrop-blur-md p-4 rounded-xl border border-outline-variant/40 shadow-xl max-w-sm animate-fadeIn z-10 text-xs">
            <div className="flex items-center justify-between border-b border-outline-variant/20 pb-2 mb-2">
              <span className="font-mono font-bold text-secondary uppercase">
                {selectedNode.label}
              </span>
              <button
                onClick={() => setSelectedNode(null)}
                className="text-outline hover:text-on-surface"
              >
                &times;
              </button>
            </div>
            <h4 className="font-headline font-bold text-on-surface text-sm mb-1">
              {selectedNode.display_name}
            </h4>
            <div className="space-y-1 font-mono text-[11px] text-on-surface-variant max-h-36 overflow-y-auto">
              <div><strong className="text-on-surface">Node ID:</strong> {selectedNode.id}</div>
              {selectedNode.metadata &&
                Object.entries(selectedNode.metadata).map(([k, v]) => (
                  <div key={k}>
                    <strong className="text-on-surface capitalize">{k.replace('_', ' ')}:</strong> {String(v)}
                  </div>
                ))}
            </div>
            {selectedNode.label === 'HarvestBatch' && (
              <button
                onClick={() => onSelectBatchForTrace(selectedNode.id)}
                className="mt-3 w-full py-1.5 bg-secondary text-white rounded-lg font-mono text-xs font-semibold hover:bg-secondary/90 transition flex items-center justify-center gap-1"
              >
                <span className="material-symbols-outlined text-[14px]">timeline</span>
                <span>Trace Full Custody Journey</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
