"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {
  getEquipment,
  getEquipmentHoursHistory,
  getEquipmentHoursChart,
  getWorkOrders,
} from "@/lib/api";

const STATUS_COLORS: Record<string, string> = {
  Normal: "bg-green-100 text-green-700",
  Warning: "bg-yellow-100 text-yellow-700",
  Critical: "bg-red-100 text-red-700",
};

const WO_STATUS_COLORS: Record<string, string> = {
  Planned: "bg-blue-100 text-blue-700",
  InProgress: "bg-yellow-100 text-yellow-700",
  Completed: "bg-green-100 text-green-700",
  Overdue: "bg-red-100 text-red-700",
  Postponed: "bg-gray-100 text-gray-600",
};

export default function EquipmentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const router = useRouter();
  const [equipment, setEquipment] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [workOrders, setWorkOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) loadData();
  }, [id]);

  async function loadData() {
    try {
      const eq = await getEquipment(id);
      setEquipment(eq);

      const [hist, chart, wos] = await Promise.all([
        getEquipmentHoursHistory(id, 30).catch(() => []),
        getEquipmentHoursChart(id, 30).catch(() => []),
        getWorkOrders(`vessel_id=${eq.vessel_id}`).catch(() => []),
      ]);
      setHistory(hist);
      setChartData(chart);
      // Filter work orders for this equipment
      setWorkOrders(wos.filter((wo: any) => wo.equipment_id === id));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!equipment) {
    return <div className="text-center py-12 text-gray-500">Equipment not found</div>;
  }

  const overhaulProgress = equipment.overhaul_interval_hours
    ? Math.min(100, Math.round((equipment.current_running_hours / equipment.overhaul_interval_hours) * 100))
    : null;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-3 mb-4 sm:mb-6">
        <button
          onClick={() => router.back()}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          ←
        </button>
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
            {equipment.name}
          </h1>
          <p className="text-sm text-gray-500">
            [{equipment.equipment_code}] {equipment.category}
          </p>
        </div>
        <span className={`px-2 py-1 text-xs rounded font-medium ${STATUS_COLORS[equipment.status] || "bg-gray-100"}`}>
          {equipment.status}
        </span>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <InfoCard label="Maker" value={equipment.maker || "N/A"} />
        <InfoCard label="Model" value={equipment.model || "N/A"} />
        <InfoCard label="Serial No." value={equipment.serial_number || "N/A"} />
        <InfoCard label="Category" value={equipment.category} />
        {equipment.rated_power && (
          <InfoCard label="Rated Power" value={`${equipment.rated_power} kW`} />
        )}
        {equipment.rated_rpm && (
          <InfoCard label="Rated RPM" value={`${equipment.rated_rpm}`} />
        )}
        <InfoCard
          label="Running Hours"
          value={`${equipment.current_running_hours?.toLocaleString() || 0}h`}
        />
        {equipment.overhaul_interval_hours && (
          <InfoCard
            label="Overhaul Interval"
            value={`${equipment.overhaul_interval_hours?.toLocaleString()}h`}
          />
        )}
      </div>

      {/* Overhaul Progress */}
      {overhaulProgress !== null && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6 mb-6">
          <h2 className="text-sm sm:text-lg font-semibold text-gray-800 mb-3">
            Overhaul Progress
          </h2>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className={`h-4 rounded-full transition-all ${
                    overhaulProgress >= 100
                      ? "bg-red-500"
                      : overhaulProgress >= 85
                      ? "bg-yellow-500"
                      : "bg-green-500"
                  }`}
                  style={{ width: `${overhaulProgress}%` }}
                />
              </div>
            </div>
            <span className="text-lg font-bold text-gray-800 min-w-[60px] text-right">
              {overhaulProgress}%
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {equipment.current_running_hours?.toLocaleString()}h / {equipment.overhaul_interval_hours?.toLocaleString()}h
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* Running Hours Chart */}
        {chartData.length > 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800 mb-3">
              ⏱️ Running Hours (30 days)
            </h2>
            <div className="flex items-end gap-0.5 h-32">
              {chartData.map((d: any, i: number) => {
                const maxH = Math.max(...chartData.map((c: any) => c.daily_hours || 0), 1);
                const h = ((d.daily_hours || 0) / maxH) * 100;
                return (
                  <div
                    key={i}
                    className="flex-1 bg-blue-400 rounded-t hover:bg-blue-500 transition-colors"
                    style={{ height: `${h}%`, minHeight: d.daily_hours > 0 ? "2px" : "0" }}
                    title={`${d.date}: ${d.daily_hours}h`}
                  />
                );
              })}
            </div>
            <div className="flex justify-between mt-1 text-[10px] text-gray-400">
              <span>{chartData[0]?.date?.slice(5)}</span>
              <span>{chartData[chartData.length - 1]?.date?.slice(5)}</span>
            </div>
          </div>
        )}

        {/* Maintenance History (Work Orders) */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <h2 className="text-sm sm:text-lg font-semibold text-gray-800 mb-3">
            🔧 Maintenance History ({workOrders.length})
          </h2>
          {workOrders.length === 0 ? (
            <p className="text-gray-500 text-sm py-4 text-center">No work orders</p>
          ) : (
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {workOrders.map((wo: any) => (
                <div
                  key={wo.id}
                  className="p-2.5 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-2">
                    <h3 className="text-xs sm:text-sm font-medium text-gray-800 truncate flex-1">
                      {wo.title}
                    </h3>
                    <span className={`px-1.5 py-0.5 text-[10px] rounded font-medium ${
                      wo.is_overdue ? WO_STATUS_COLORS.Overdue : WO_STATUS_COLORS[wo.status] || "bg-gray-100"
                    }`}>
                      {wo.is_overdue ? "OVERDUE" : wo.status}
                    </span>
                  </div>
                  <div className="flex gap-3 mt-1 text-[11px] text-gray-500">
                    <span>Planned: {wo.planned_date?.slice(0, 10) || "N/A"}</span>
                    {wo.completed_date && (
                      <span className="text-green-600">Done: {wo.completed_date?.slice(0, 10)}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function InfoCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3">
      <p className="text-[11px] text-gray-500">{label}</p>
      <p className="text-sm font-medium text-gray-800 mt-0.5 truncate">{value}</p>
    </div>
  );
}
