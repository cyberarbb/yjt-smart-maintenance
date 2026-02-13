"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import {
  getVessels,
  getWorkOrderStats,
  getOverdueWorkOrders,
  getUpcomingWorkOrders,
  getMaintenancePlans,
  updateWorkOrder,
} from "@/lib/api";
import Link from "next/link";

const STATUS_COLORS: Record<string, string> = {
  Planned: "bg-blue-100 text-blue-700",
  InProgress: "bg-yellow-100 text-yellow-700",
  Completed: "bg-green-100 text-green-700",
  Overdue: "bg-red-100 text-red-700",
  Postponed: "bg-gray-100 text-gray-600",
  Cancelled: "bg-gray-100 text-gray-400",
};

const PRIORITY_COLORS: Record<string, string> = {
  Critical: "text-red-600",
  High: "text-orange-600",
  Medium: "text-blue-600",
  Low: "text-gray-500",
};

export default function PMSPage() {
  const { user } = useAuth();
  const [vessels, setVessels] = useState<any[]>([]);
  const [selectedVessel, setSelectedVessel] = useState("");
  const [stats, setStats] = useState<any>(null);
  const [overdue, setOverdue] = useState<any[]>([]);
  const [upcoming, setUpcoming] = useState<any[]>([]);
  const [plans, setPlans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.role === "developer";

  useEffect(() => {
    loadVessels();
  }, [user]);

  useEffect(() => {
    if (selectedVessel) loadPMSData();
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

  async function loadPMSData() {
    try {
      const [s, o, u, p] = await Promise.all([
        getWorkOrderStats(selectedVessel),
        getOverdueWorkOrders(selectedVessel),
        getUpcomingWorkOrders(selectedVessel, 30),
        getMaintenancePlans(selectedVessel),
      ]);
      setStats(s);
      setOverdue(o);
      setUpcoming(u);
      setPlans(p);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleStatusChange(woId: string, newStatus: string) {
    try {
      await updateWorkOrder(woId, { status: newStatus });
      await loadPMSData();
    } catch (e: any) {
      alert(e.message || "Failed to update");
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
          🔧 PMS Dashboard
        </h1>
        <div className="flex gap-3">
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
          <Link
            href="/work-orders"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
          >
            All Work Orders
          </Link>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
            <p className="text-[11px] text-gray-500">Total</p>
            <p className="text-xl font-bold text-gray-800">{stats.total}</p>
          </div>
          <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
            <p className="text-[11px] text-gray-500">Completed</p>
            <p className="text-xl font-bold text-green-600">{stats.completed}</p>
          </div>
          <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
            <p className="text-[11px] text-gray-500">Overdue</p>
            <p className="text-xl font-bold text-red-600">{stats.overdue}</p>
          </div>
          <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
            <p className="text-[11px] text-gray-500">In Progress</p>
            <p className="text-xl font-bold text-yellow-600">{stats.in_progress}</p>
          </div>
          <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
            <p className="text-[11px] text-gray-500">Planned</p>
            <p className="text-xl font-bold text-blue-600">{stats.planned}</p>
          </div>
          <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
            <p className="text-[11px] text-gray-500">Completion</p>
            <p className="text-xl font-bold text-purple-600">{stats.completion_rate}%</p>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-4">
        {/* Overdue */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-red-600 mb-3 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
            Overdue ({overdue.length})
          </h2>
          <div className="space-y-2 max-h-80 overflow-y-auto">
            {overdue.map((wo: any) => (
              <div key={wo.id} className="p-2 rounded-lg border border-red-100 bg-red-50/50">
                <div className="flex justify-between items-start gap-2">
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-medium text-gray-800 truncate">{wo.title}</p>
                    <p className="text-[10px] text-gray-500">[{wo.equipment_code}] Due: {wo.due_date?.slice(0, 10)}</p>
                  </div>
                  <span className={`text-[10px] font-medium ${PRIORITY_COLORS[wo.priority]}`}>{wo.priority}</span>
                </div>
                <div className="flex gap-1 mt-1.5">
                  <button
                    onClick={() => handleStatusChange(wo.id, "InProgress")}
                    className="px-2 py-0.5 text-[10px] bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
                  >
                    Start
                  </button>
                  <button
                    onClick={() => handleStatusChange(wo.id, "Completed")}
                    className="px-2 py-0.5 text-[10px] bg-green-100 text-green-700 rounded hover:bg-green-200"
                  >
                    Complete
                  </button>
                </div>
              </div>
            ))}
            {overdue.length === 0 && (
              <p className="text-center text-gray-400 text-xs py-4">No overdue work orders</p>
            )}
          </div>
        </div>

        {/* Upcoming */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-blue-600 mb-3">
            Upcoming (30 days) - {upcoming.length}
          </h2>
          <div className="space-y-2 max-h-80 overflow-y-auto">
            {upcoming.map((wo: any) => (
              <div key={wo.id} className="p-2 rounded-lg border border-gray-100 hover:bg-gray-50">
                <div className="flex justify-between items-start gap-2">
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-medium text-gray-800 truncate">{wo.title}</p>
                    <p className="text-[10px] text-gray-500">
                      [{wo.equipment_code}] Planned: {wo.planned_date?.slice(0, 10)}
                      {wo.is_class_related && <span className="ml-1 text-purple-500">[Class]</span>}
                    </p>
                  </div>
                  <span className={`px-1.5 py-0.5 text-[10px] rounded ${STATUS_COLORS[wo.status]}`}>{wo.status}</span>
                </div>
              </div>
            ))}
            {upcoming.length === 0 && (
              <p className="text-center text-gray-400 text-xs py-4">No upcoming work orders</p>
            )}
          </div>
        </div>
      </div>

      {/* Maintenance Plans */}
      <div className="mt-4 bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">
          Maintenance Plans ({plans.length})
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-3 py-2 font-medium text-gray-500">Equipment</th>
                <th className="text-left px-3 py-2 font-medium text-gray-500">Plan</th>
                <th className="text-left px-3 py-2 font-medium text-gray-500">Interval</th>
                <th className="text-left px-3 py-2 font-medium text-gray-500">Priority</th>
                <th className="text-left px-3 py-2 font-medium text-gray-500">Next Due</th>
                <th className="text-center px-3 py-2 font-medium text-gray-500">Class</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {plans.slice(0, 20).map((p: any) => {
                const isOverdue = p.next_due_date && new Date(p.next_due_date) < new Date();
                return (
                  <tr key={p.id} className={`hover:bg-gray-50 ${isOverdue ? "bg-red-50/50" : ""}`}>
                    <td className="px-3 py-2 text-gray-700">[{p.equipment_code}] {p.equipment_name}</td>
                    <td className="px-3 py-2 text-gray-800 font-medium">{p.title}</td>
                    <td className="px-3 py-2 text-gray-600">{p.interval_value} {p.interval_unit}</td>
                    <td className="px-3 py-2"><span className={PRIORITY_COLORS[p.priority]}>{p.priority}</span></td>
                    <td className={`px-3 py-2 ${isOverdue ? "text-red-600 font-medium" : "text-gray-600"}`}>
                      {p.next_due_date?.slice(0, 10) || "N/A"}
                    </td>
                    <td className="px-3 py-2 text-center">{p.is_class_related ? "✓" : ""}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
