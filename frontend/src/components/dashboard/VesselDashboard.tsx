"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {
  getVessels,
  getWorkOrderStats,
  getOverdueWorkOrders,
  getUpcomingWorkOrders,
  getVesselLatestHours,
} from "@/lib/api";

interface VesselInfo {
  id: string;
  name: string;
  vessel_type: string;
}

export default function VesselDashboard() {
  const { user } = useAuth();
  const router = useRouter();
  const [vessels, setVessels] = useState<VesselInfo[]>([]);
  const [selectedVessel, setSelectedVessel] = useState("");
  const [stats, setStats] = useState<any>(null);
  const [overdue, setOverdue] = useState<any[]>([]);
  const [upcoming, setUpcoming] = useState<any[]>([]);
  const [latestHours, setLatestHours] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.role === "developer";

  useEffect(() => {
    loadVessels();
  }, [user]);

  useEffect(() => {
    if (selectedVessel) loadVesselData();
  }, [selectedVessel]);

  async function loadVessels() {
    try {
      const data = await getVessels();
      // 비관리자 + vessel_id 배정 시 해당 선박만
      let filtered = data;
      if (!isAdmin && user?.vessel_id) {
        filtered = data.filter((v: any) => v.id === user.vessel_id);
      }
      setVessels(filtered);
      const userVessel = user?.vessel_id;
      if (userVessel && filtered.find((v: any) => v.id === userVessel)) {
        setSelectedVessel(userVessel);
      } else if (filtered.length > 0) {
        setSelectedVessel(filtered[0].id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function loadVesselData() {
    try {
      const [s, o, u, h] = await Promise.all([
        getWorkOrderStats(selectedVessel),
        getOverdueWorkOrders(selectedVessel),
        getUpcomingWorkOrders(selectedVessel, 14),
        getVesselLatestHours(selectedVessel),
      ]);
      setStats(s);
      setOverdue(o);
      setUpcoming(u);
      setLatestHours(h);
    } catch (e) {
      console.error(e);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const vesselName = vessels.find((v) => v.id === selectedVessel)?.name || "Select Vessel";

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
          🚢 Vessel Dashboard
        </h1>
        <select
          value={selectedVessel}
          onChange={(e) => setSelectedVessel(e.target.value)}
          disabled={!isAdmin && vessels.length <= 1}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white disabled:opacity-60"
        >
          {vessels.map((v) => (
            <option key={v.id} value={v.id}>
              {v.name}
            </option>
          ))}
        </select>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6">
        <StatCard
          title="Total W/O"
          value={stats?.total ?? 0}
          icon="📋"
          color="bg-blue-500"
          onClick={() => router.push("/work-orders")}
        />
        <StatCard
          title="Completed"
          value={stats?.completed ?? 0}
          icon="✅"
          color="bg-green-500"
          onClick={() => router.push("/work-orders")}
        />
        <StatCard
          title="Overdue"
          value={stats?.overdue ?? 0}
          icon="🔴"
          color="bg-red-500"
          onClick={() => router.push("/work-orders")}
        />
        <StatCard
          title="Completion"
          value={`${stats?.completion_rate ?? 0}%`}
          icon="📊"
          color="bg-purple-500"
          onClick={() => router.push("/pms")}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* Overdue Work Orders */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm sm:text-lg font-semibold text-red-600">
              ⚠️ Overdue ({overdue.length})
            </h2>
            <button
              onClick={() => router.push("/work-orders")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium"
            >
              View All →
            </button>
          </div>
          {overdue.length === 0 ? (
            <p className="text-gray-500 text-sm py-4 text-center">
              No overdue work orders
            </p>
          ) : (
            <div className="space-y-2">
              {overdue.slice(0, 5).map((wo: any) => (
                <div
                  key={wo.id}
                  className="p-2.5 bg-red-50 rounded-lg border border-red-100"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-sm">
                      {wo.priority === "Critical"
                        ? "🔴"
                        : wo.priority === "High"
                        ? "🟠"
                        : "🔵"}
                    </span>
                    <p className="text-xs sm:text-sm font-medium text-gray-800 truncate">
                      {wo.title}
                    </p>
                  </div>
                  <div className="flex gap-3 mt-1 text-[11px] text-gray-500">
                    <span>{wo.equipment_name}</span>
                    <span>Due: {wo.due_date?.slice(0, 10)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Upcoming Work Orders */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800">
              📅 Upcoming (14 days)
            </h2>
            <button
              onClick={() => router.push("/pms")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium"
            >
              View PMS →
            </button>
          </div>
          {upcoming.length === 0 ? (
            <p className="text-gray-500 text-sm py-4 text-center">
              No upcoming work orders
            </p>
          ) : (
            <div className="space-y-2">
              {upcoming.slice(0, 5).map((wo: any) => (
                <div
                  key={wo.id}
                  className="p-2.5 bg-yellow-50 rounded-lg border border-yellow-100"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-sm">
                      {wo.priority === "Critical"
                        ? "🔴"
                        : wo.priority === "High"
                        ? "🟠"
                        : "🔵"}
                    </span>
                    <p className="text-xs sm:text-sm font-medium text-gray-800 truncate">
                      {wo.title}
                    </p>
                  </div>
                  <div className="flex gap-3 mt-1 text-[11px] text-gray-500">
                    <span>{wo.equipment_name}</span>
                    <span>Due: {wo.due_date?.slice(0, 10)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Running Hours Summary */}
      {latestHours.length > 0 && (
        <div className="mt-4 sm:mt-6 bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800">
              ⏱️ Equipment Running Hours
            </h2>
            <button
              onClick={() => router.push("/running-hours")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium"
            >
              Record Hours →
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {latestHours.slice(0, 6).map((item: any) => (
              <div
                key={item.equipment_id}
                className="p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center justify-between">
                  <p className="text-xs font-medium text-gray-800 truncate">
                    {item.equipment_name}
                  </p>
                  <span
                    className={`px-1.5 py-0.5 text-[10px] rounded font-medium ${
                      item.status === "Critical"
                        ? "bg-red-100 text-red-700"
                        : item.status === "Warning"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-green-100 text-green-700"
                    }`}
                  >
                    {item.status || "Normal"}
                  </span>
                </div>
                <p className="text-lg font-bold text-gray-800 mt-1">
                  {item.total_hours?.toLocaleString() || 0}h
                </p>
                {item.overhaul_interval_hours && (
                  <div className="mt-1">
                    <div className="flex justify-between text-[10px] text-gray-500">
                      <span>Progress</span>
                      <span>
                        {Math.min(
                          100,
                          Math.round(
                            (item.total_hours / item.overhaul_interval_hours) *
                              100
                          )
                        )}
                        %
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5 mt-0.5">
                      <div
                        className={`h-1.5 rounded-full ${
                          item.total_hours / item.overhaul_interval_hours >= 1
                            ? "bg-red-500"
                            : item.total_hours /
                                item.overhaul_interval_hours >=
                              0.85
                            ? "bg-yellow-500"
                            : "bg-green-500"
                        }`}
                        style={{
                          width: `${Math.min(
                            100,
                            (item.total_hours / item.overhaul_interval_hours) *
                              100
                          )}%`,
                        }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({
  title,
  value,
  icon,
  color,
  onClick,
}: {
  title: string;
  value: number | string;
  icon: string;
  color: string;
  onClick?: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-6 cursor-pointer hover:shadow-md hover:border-gray-300 transition-all active:scale-[0.98]"
    >
      <div className="flex items-center justify-between">
        <div className="min-w-0">
          <p className="text-[11px] sm:text-sm text-gray-500 truncate">
            {title}
          </p>
          <p className="text-xl sm:text-3xl font-bold text-gray-800 mt-0.5 sm:mt-1">
            {value}
          </p>
        </div>
        <div
          className={`w-8 h-8 sm:w-12 sm:h-12 ${color} rounded-lg flex items-center justify-center text-sm sm:text-xl flex-shrink-0`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}
