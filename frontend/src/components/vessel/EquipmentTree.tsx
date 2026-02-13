"use client";

import { useState } from "react";

interface EquipmentNode {
  id: string;
  vessel_id: string;
  parent_id: string | null;
  equipment_code: string;
  name: string;
  category: string;
  maker?: string;
  model?: string;
  status: string;
  current_running_hours: number;
  overhaul_interval_hours?: number;
  sort_order: number;
  children: EquipmentNode[];
}

const CATEGORY_ICONS: Record<string, string> = {
  "Main Engine": "🔧",
  Generator: "⚡",
  Boiler: "🔥",
  Turbocharger: "🌀",
  Pump: "💧",
  Compressor: "💨",
  "Steering Gear": "🎯",
  "Emergency Generator": "🆘",
  Purifier: "🧹",
  "Heat Exchanger": "🌡️",
  Crane: "🏗️",
  "Fuel System": "⛽",
  "Exhaust System": "💨",
  Other: "📦",
};

const STATUS_COLORS: Record<string, string> = {
  Normal: "bg-green-100 text-green-700",
  Warning: "bg-amber-100 text-amber-700",
  Critical: "bg-red-100 text-red-700",
  Inactive: "bg-gray-100 text-gray-500",
};

function RunningHoursBar({ current, max }: { current: number; max?: number }) {
  if (!max || max <= 0) return null;
  const pct = Math.min((current / max) * 100, 100);
  const color = pct > 90 ? "bg-red-500" : pct > 70 ? "bg-amber-500" : "bg-green-500";

  return (
    <div className="flex items-center gap-2 mt-1">
      <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-[10px] text-gray-500 whitespace-nowrap">
        {current.toLocaleString()}h / {max.toLocaleString()}h
      </span>
    </div>
  );
}

function TreeNode({
  node,
  depth = 0,
  onSelect,
}: {
  node: EquipmentNode;
  depth?: number;
  onSelect: (node: EquipmentNode) => void;
}) {
  const [expanded, setExpanded] = useState(depth < 2);
  const hasChildren = node.children && node.children.length > 0;
  const icon = CATEGORY_ICONS[node.category] || "📦";
  const statusColor = STATUS_COLORS[node.status] || STATUS_COLORS.Normal;

  return (
    <div className={depth > 0 ? "ml-4 sm:ml-6" : ""}>
      <div
        className="flex items-center gap-2 py-1.5 px-2 rounded-lg hover:bg-gray-50 cursor-pointer group transition-colors"
        onClick={() => onSelect(node)}
      >
        {/* Expand/Collapse */}
        {hasChildren ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setExpanded(!expanded);
            }}
            className="w-5 h-5 flex items-center justify-center text-gray-400 hover:text-gray-600 flex-shrink-0"
          >
            <svg
              className={`w-3.5 h-3.5 transition-transform ${expanded ? "rotate-90" : ""}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        ) : (
          <span className="w-5 h-5 flex items-center justify-center text-gray-300 flex-shrink-0">
            <span className="w-1.5 h-1.5 bg-gray-300 rounded-full" />
          </span>
        )}

        {/* Icon + Name */}
        <span className="text-base flex-shrink-0">{icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-medium text-gray-800 truncate">{node.name}</span>
            <span className="text-[10px] text-gray-400 font-mono">{node.equipment_code}</span>
          </div>
          {node.maker && (
            <p className="text-[11px] text-gray-500 truncate">
              {node.maker} {node.model && `- ${node.model}`}
            </p>
          )}
          <RunningHoursBar current={node.current_running_hours} max={node.overhaul_interval_hours || undefined} />
        </div>

        {/* Status Badge */}
        <span className={`px-1.5 py-0.5 text-[10px] font-medium rounded ${statusColor} flex-shrink-0`}>
          {node.status}
        </span>
      </div>

      {/* Children */}
      {hasChildren && expanded && (
        <div className="border-l border-gray-200 ml-2.5">
          {node.children.map((child) => (
            <TreeNode key={child.id} node={child} depth={depth + 1} onSelect={onSelect} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function EquipmentTree({
  tree,
  onSelect,
}: {
  tree: EquipmentNode[];
  onSelect: (node: EquipmentNode) => void;
}) {
  if (!tree || tree.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <p className="text-4xl mb-2">🔧</p>
        <p className="text-sm">No equipment registered yet.</p>
        <p className="text-xs mt-1">Add equipment using the button above.</p>
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {tree.map((node) => (
        <TreeNode key={node.id} node={node} onSelect={onSelect} />
      ))}
    </div>
  );
}
