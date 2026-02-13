"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { getVessels, getWorkOrders, updateWorkOrder } from "@/lib/api";

const STATUS_TABS = ["All", "Planned", "InProgress", "Completed", "Overdue", "Postponed"];

const STATUS_COLORS: Record<string, string> = {
  Planned: "bg-blue-100 text-blue-700",
  InProgress: "bg-yellow-100 text-yellow-700",
  Completed: "bg-green-100 text-green-700",
  Overdue: "bg-red-100 text-red-700",
  Postponed: "bg-gray-100 text-gray-600",
  Cancelled: "bg-gray-100 text-gray-400",
};

const PRIORITY_ICONS: Record<string, string> = {
  Critical: "🔴",
  High: "🟠",
  Medium: "🔵",
  Low: "⚪",
};

export default function WorkOrdersPage() {
  const { user } = useAuth();
  const [vessels, setVessels] = useState<any[]>([]);
  const [selectedVessel, setSelectedVessel] = useState("");
  const [workOrders, setWorkOrders] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState("All");
  const [loading, setLoading] = useState(true);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.role === "developer";
  const isCrewOrAdmin =
    user?.is_admin || ["admin", "captain", "chief_engineer", "shore_manager", "engineer"].includes(user?.role || "");

  useEffect(() => {
    loadVessels();
  }, [user]);

  useEffect(() => {
    if (selectedVessel) loadWorkOrders();
  }, [selectedVessel]);

  async function loadVessels() {
    try {
      const data = await getVessels();
      let filtered = data;
      if (!isAdmin && user?.vessel_id) {
        filtered = data.filter((v: any) => v.id === user.vessel_id);
      }
      setVessels(filtered);
      if (filtered.length > 0) {
        const uv = user?.vessel_id;
        if (uv && filtered.find((v: any) => v.id === uv)) {
          setSelectedVessel(uv);
        } else {
          setSelectedVessel(filtered[0].id);
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function loadWorkOrders() {
    try {
      const data = await getWorkOrders(`vessel_id=${selectedVessel}`);
      setWorkOrders(data);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleStatusChange(woId: string, newStatus: string) {
    try {
      await updateWorkOrder(woId, { status: newStatus });
      await loadWorkOrders();
    } catch (e: any) {
      alert(e.message || "Failed");
    }
  }

  const filteredOrders = statusFilter === "All"
    ? workOrders
    : workOrders.filter((wo) => {
        if (statusFilter === "Overdue") return wo.is_overdue;
        return wo.status === statusFilter;
      });

  const statusCounts: Record<string, number> = {
    All: workOrders.length,
    Planned: workOrders.filter((w) => w.status === "Planned").length,
    InProgress: workOrders.filter((w) => w.status === "InProgress").length,
    Completed: workOrders.filter((w) => w.status === "Completed").length,
    Overdue: workOrders.filter((w) => w.is_overdue).length,
    Postponed: workOrders.filter((w) => w.status === "Postponed").length,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">
        📋 Work Orders
      </h1>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <select
          value={selectedVessel}
          onChange={(e) => setSelectedVessel(e.target.value)}
          disabled={!isAdmin && vessels.length <= 1}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm disabled:opacity-60"
        >
          {vessels.map((v: any) => (
            <option key={v.id} value={v.id}>{v.name}</option>
          ))}
        </select>
      </div>

      {/* Status Tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {STATUS_TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setStatusFilter(tab)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              statusFilter === tab
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {tab} ({statusCounts[tab] || 0})
          </button>
        ))}
      </div>

      {/* Work Orders List */}
      <div className="space-y-2">
        {filteredOrders.map((wo: any) => (
          <div
            key={wo.id}
            className={`bg-white rounded-xl shadow-sm border p-3 sm:p-4 ${
              wo.is_overdue ? "border-red-200 bg-red-50/30" : "border-gray-200"
            }`}
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-base">{PRIORITY_ICONS[wo.priority] || "🔵"}</span>
                  <h3 className="text-sm font-medium text-gray-800 truncate">{wo.title}</h3>
                  <span className={`px-1.5 py-0.5 text-[10px] rounded font-medium ${
                    wo.is_overdue ? STATUS_COLORS.Overdue : STATUS_COLORS[wo.status] || "bg-gray-100"
                  }`}>
                    {wo.is_overdue ? "OVERDUE" : wo.status}
                  </span>
                  {wo.is_class_related && (
                    <span className="px-1.5 py-0.5 text-[10px] bg-purple-100 text-purple-700 rounded">Class</span>
                  )}
                </div>
                <div className="flex flex-wrap gap-3 mt-1 text-[11px] text-gray-500">
                  <span>[{wo.equipment_code}] {wo.equipment_name}</span>
                  <span>Planned: {wo.planned_date?.slice(0, 10) || "N/A"}</span>
                  <span>Due: {wo.due_date?.slice(0, 10) || "N/A"}</span>
                  {wo.completed_date && <span className="text-green-600">Done: {wo.completed_date?.slice(0, 10)}</span>}
                  {wo.actual_hours && <span>Hours: {wo.actual_hours?.toFixed(1)}h</span>}
                </div>
              </div>

              {/* Actions */}
              {isCrewOrAdmin && wo.status !== "Completed" && wo.status !== "Cancelled" && (
                <div className="flex gap-1 flex-shrink-0">
                  {wo.status === "Planned" && (
                    <button
                      onClick={() => handleStatusChange(wo.id, "InProgress")}
                      className="px-2 py-1 text-[10px] font-medium bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
                    >
                      Start
                    </button>
                  )}
                  {(wo.status === "InProgress" || wo.status === "Planned") && (
                    <button
                      onClick={() => handleStatusChange(wo.id, "Completed")}
                      className="px-2 py-1 text-[10px] font-medium bg-green-100 text-green-700 rounded hover:bg-green-200"
                    >
                      Complete
                    </button>
                  )}
                  {wo.status !== "Postponed" && (
                    <button
                      onClick={() => handleStatusChange(wo.id, "Postponed")}
                      className="px-2 py-1 text-[10px] font-medium bg-gray-100 text-gray-600 rounded hover:bg-gray-200"
                    >
                      Postpone
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {filteredOrders.length === 0 && (
          <div className="text-center py-12 text-gray-400 text-sm">
            No work orders found for this filter.
          </div>
        )}
      </div>

      <div className="mt-3 text-xs text-gray-500">
        Showing {filteredOrders.length} of {workOrders.length} work orders
      </div>
    </div>
  );
}
