"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import {
  getVessels,
  getVesselLatestHours,
  recordRunningHoursBulk,
  getEquipmentHoursHistory,
} from "@/lib/api";

export default function RunningHoursPage() {
  const { user } = useAuth();
  const [vessels, setVessels] = useState<any[]>([]);
  const [selectedVessel, setSelectedVessel] = useState<string>("");
  const [latestHours, setLatestHours] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [inputDate, setInputDate] = useState(new Date().toISOString().split("T")[0]);
  const [inputValues, setInputValues] = useState<Record<string, number>>({});
  const [saving, setSaving] = useState(false);
  const [viewMode, setViewMode] = useState<"input" | "history">("input");
  const [historyEquipment, setHistoryEquipment] = useState<string>("");
  const [historyData, setHistoryData] = useState<any[]>([]);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.role === "developer";
  const isCrewOrAdmin =
    user?.is_admin ||
    ["admin", "captain", "chief_engineer", "shore_manager", "engineer"].includes(user?.role || "");

  useEffect(() => {
    loadVessels();
  }, [user]);

  useEffect(() => {
    if (selectedVessel) loadLatestHours(selectedVessel);
  }, [selectedVessel]);

  async function loadVessels() {
    try {
      const data = await getVessels();
      // 비관리자 + vessel_id 배정된 경우 해당 선박만
      let filtered = data;
      if (!isAdmin && user?.vessel_id) {
        filtered = data.filter((v: any) => v.id === user.vessel_id);
      }
      setVessels(filtered);
      if (filtered.length > 0) {
        // 배정 선박이 있으면 그걸 선택, 아니면 첫번째
        const userVessel = user?.vessel_id;
        if (userVessel && filtered.find((v: any) => v.id === userVessel)) {
          setSelectedVessel(userVessel);
        } else {
          setSelectedVessel(filtered[0].id);
        }
      }
    } catch (e) {
      console.error("Failed to load vessels:", e);
    } finally {
      setLoading(false);
    }
  }

  async function loadLatestHours(vesselId: string) {
    try {
      const data = await getVesselLatestHours(vesselId);
      setLatestHours(data);
      // Initialize input values with 0
      const defaults: Record<string, number> = {};
      data.forEach((eq: any) => {
        defaults[eq.equipment_id] = 0;
      });
      setInputValues(defaults);
    } catch (e) {
      console.error("Failed to load latest hours:", e);
    }
  }

  async function handleBulkRecord() {
    if (!selectedVessel) return;
    setSaving(true);
    try {
      const records = Object.entries(inputValues)
        .filter(([_, hours]) => hours > 0)
        .map(([eqId, hours]) => ({
          equipment_id: eqId,
          recorded_date: inputDate,
          daily_hours: hours,
        }));

      if (records.length === 0) {
        alert("Please enter at least one record");
        return;
      }

      const result = await recordRunningHoursBulk({
        vessel_id: selectedVessel,
        recorded_date: inputDate,
        records,
      });

      alert(`Recorded ${result.recorded} entries for ${inputDate}${result.errors?.length ? `\nErrors: ${result.errors.join(", ")}` : ""}`);
      await loadLatestHours(selectedVessel);
    } catch (e: any) {
      alert(e.message || "Failed to record");
    } finally {
      setSaving(false);
    }
  }

  async function loadHistory(equipmentId: string) {
    setHistoryEquipment(equipmentId);
    try {
      const data = await getEquipmentHoursHistory(equipmentId, 30);
      setHistoryData(data);
    } catch (e) {
      console.error("Failed to load history:", e);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const vesselName = vessels.find((v) => v.id === selectedVessel)?.name || "";

  return (
    <div>
      <h1 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">
        ⏱️ Running Hours Management
      </h1>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-3 mb-4 sm:mb-6">
        <select
          value={selectedVessel}
          onChange={(e) => setSelectedVessel(e.target.value)}
          disabled={!isAdmin && vessels.length <= 1}
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 disabled:opacity-60"
        >
          {vessels.map((v: any) => (
            <option key={v.id} value={v.id}>
              {v.name} ({v.vessel_type})
            </option>
          ))}
        </select>

        <div className="flex gap-2">
          <button
            onClick={() => setViewMode("input")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              viewMode === "input"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            Daily Input
          </button>
          <button
            onClick={() => setViewMode("history")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              viewMode === "history"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            History
          </button>
        </div>
      </div>

      {viewMode === "input" ? (
        /* ── Daily Input Grid ── */
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
            <h2 className="text-sm font-semibold text-gray-700">
              Daily Running Hours - {vesselName}
            </h2>
            <div className="flex items-center gap-3">
              <input
                type="date"
                value={inputDate}
                onChange={(e) => setInputDate(e.target.value)}
                className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
              />
              {isCrewOrAdmin && (
                <button
                  onClick={handleBulkRecord}
                  disabled={saving}
                  className="px-4 py-1.5 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 transition-colors"
                >
                  {saving ? "Saving..." : "Save All"}
                </button>
              )}
            </div>
          </div>

          {/* Equipment grid */}
          <div className="space-y-2">
            {latestHours.map((eq: any) => {
              const pct = eq.overhaul_interval
                ? Math.min((eq.current_hours / eq.overhaul_interval) * 100, 100)
                : 0;
              const barColor =
                pct > 90 ? "bg-red-500" : pct > 70 ? "bg-amber-500" : "bg-green-500";

              return (
                <div
                  key={eq.equipment_id}
                  className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 px-3 rounded-lg hover:bg-gray-50 border border-gray-100"
                >
                  {/* Equipment info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-gray-400">{eq.equipment_code}</span>
                      <span className="text-sm font-medium text-gray-800 truncate">{eq.equipment_name}</span>
                      <span className="text-[10px] px-1.5 py-0.5 bg-gray-100 text-gray-500 rounded">{eq.category}</span>
                    </div>
                    {/* Progress bar */}
                    {eq.overhaul_interval > 0 && (
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden max-w-[200px]">
                          <div className={`h-full ${barColor} rounded-full`} style={{ width: `${pct}%` }} />
                        </div>
                        <span className="text-[10px] text-gray-500">
                          {eq.current_hours.toLocaleString()}h / {eq.overhaul_interval.toLocaleString()}h ({Math.round(pct)}%)
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Input */}
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <span className="text-[10px] text-gray-400 hidden sm:inline">
                      Last: {eq.last_recorded_date || "N/A"}
                    </span>
                    {isCrewOrAdmin ? (
                      <input
                        type="number"
                        min={0}
                        max={24}
                        step={0.5}
                        value={inputValues[eq.equipment_id] || 0}
                        onChange={(e) =>
                          setInputValues({
                            ...inputValues,
                            [eq.equipment_id]: parseFloat(e.target.value) || 0,
                          })
                        }
                        className="w-20 px-2 py-1.5 border border-gray-200 rounded-lg text-sm text-center focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <span className="text-sm font-medium text-gray-600">
                        {eq.daily_hours}h
                      </span>
                    )}
                    <span className="text-xs text-gray-400">h/day</span>
                  </div>
                </div>
              );
            })}

            {latestHours.length === 0 && (
              <div className="text-center py-8 text-gray-400 text-sm">
                No equipment found. Please add equipment to this vessel first.
              </div>
            )}
          </div>
        </div>
      ) : (
        /* ── History View ── */
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row gap-3 mb-4">
            <h2 className="text-sm font-semibold text-gray-700">History (30 days)</h2>
            <select
              value={historyEquipment}
              onChange={(e) => loadHistory(e.target.value)}
              className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select equipment...</option>
              {latestHours.map((eq: any) => (
                <option key={eq.equipment_id} value={eq.equipment_id}>
                  [{eq.equipment_code}] {eq.equipment_name}
                </option>
              ))}
            </select>
          </div>

          {historyData.length > 0 ? (
            <>
              {/* Simple bar chart */}
              <div className="mb-4 overflow-x-auto">
                <div className="flex items-end gap-1 h-32 min-w-[600px]">
                  {historyData.map((d: any, i: number) => {
                    const maxH = Math.max(...historyData.map((x: any) => x.daily_hours), 1);
                    const h = (d.daily_hours / maxH) * 100;
                    return (
                      <div key={i} className="flex-1 flex flex-col items-center gap-0.5">
                        <span className="text-[8px] text-gray-400">{d.daily_hours}h</span>
                        <div
                          className={`w-full rounded-t ${
                            d.daily_hours === 0 ? "bg-gray-200" : d.daily_hours > 22 ? "bg-blue-500" : "bg-blue-400"
                          }`}
                          style={{ height: `${Math.max(h, 2)}%` }}
                        />
                        <span className="text-[7px] text-gray-400 -rotate-45 origin-left whitespace-nowrap">
                          {d.recorded_date.slice(5)}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left px-3 py-2 font-medium text-gray-500">Date</th>
                      <th className="text-right px-3 py-2 font-medium text-gray-500">Daily Hours</th>
                      <th className="text-right px-3 py-2 font-medium text-gray-500">Total Hours</th>
                      <th className="text-left px-3 py-2 font-medium text-gray-500">Note</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {historyData.map((d: any) => (
                      <tr key={d.id} className="hover:bg-gray-50">
                        <td className="px-3 py-2 text-gray-700">{d.recorded_date}</td>
                        <td className="px-3 py-2 text-right font-medium text-gray-800">{d.daily_hours}h</td>
                        <td className="px-3 py-2 text-right text-gray-600">{d.total_hours?.toLocaleString()}h</td>
                        <td className="px-3 py-2 text-gray-500">{d.note || ""}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="text-center py-8 text-gray-400 text-sm">
              {historyEquipment ? "No history data found" : "Select equipment to view history"}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
