"use client";

import { useEffect, useState } from "react";
import { getVessels, deleteVessel } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import VesselFormModal from "@/components/crud/VesselFormModal";
import Link from "next/link";

export default function VesselsPage() {
  return <VesselsContent />;
}

function VesselsContent() {
  const { user } = useAuth();
  const [vessels, setVessels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editVessel, setEditVessel] = useState<any>(null);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.role === "developer";

  useEffect(() => {
    loadVessels();
  }, [user]);

  async function loadVessels() {
    setLoading(true);
    try {
      const data = await getVessels();
      // 비관리자 + vessel_id 배정된 경우 해당 선박만 표시
      if (!isAdmin && user?.vessel_id) {
        setVessels(data.filter((v: any) => v.id === user.vessel_id));
      } else {
        setVessels(data);
      }
    } catch (e) {
      console.error("Failed to load vessels:", e);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(vessel: any) {
    if (!confirm(`Delete vessel "${vessel.name}"? This cannot be undone.`)) return;
    try {
      await deleteVessel(vessel.id);
      loadVessels();
    } catch (err: any) {
      alert(err.message || "Failed to delete");
    }
  }

  const vesselTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      "Container Ship": "🚢",
      "Bulk Carrier": "⛴️",
      "Tanker": "🛢️",
      "LNG Carrier": "🔵",
      "LPG Carrier": "🟣",
      "FPSO": "🏭",
      "Car Carrier": "🚗",
      "Tug Boat": "⚓",
      "Offshore": "🌊",
    };
    return icons[type] || "🚢";
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">🚢 Vessel Management</h1>
        {isAdmin && (
          <button
            onClick={() => { setEditVessel(null); setModalOpen(true); }}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-600 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-1 sm:gap-2"
          >
            <span className="text-base sm:text-lg leading-none">+</span> <span className="hidden sm:inline">Register</span> Vessel
          </button>
        )}
      </div>

      {/* 통계 카드 */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4 sm:mb-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-4">
          <p className="text-[11px] sm:text-xs text-gray-500 font-medium">Total Vessels</p>
          <p className="text-lg sm:text-2xl font-bold text-gray-800 mt-1">{vessels.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-4">
          <p className="text-[11px] sm:text-xs text-gray-500 font-medium">Active</p>
          <p className="text-lg sm:text-2xl font-bold text-green-600 mt-1">
            {vessels.filter((v) => v.is_active).length}
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-4">
          <p className="text-[11px] sm:text-xs text-gray-500 font-medium">Vessel Types</p>
          <p className="text-lg sm:text-2xl font-bold text-blue-600 mt-1">
            {new Set(vessels.map((v) => v.vessel_type)).size}
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-4">
          <p className="text-[11px] sm:text-xs text-gray-500 font-medium">Owners</p>
          <p className="text-lg sm:text-2xl font-bold text-purple-600 mt-1">
            {new Set(vessels.filter((v) => v.owner_company).map((v) => v.owner_company)).size}
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-gray-500">Loading...</div>
      ) : (
        <>
          {/* 모바일 카드뷰 */}
          <div className="lg:hidden space-y-3">
            {vessels.map((v) => (
              <div
                key={v.id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-4"
              >
                <div className="flex justify-between items-start gap-2 mb-2">
                  <div className="min-w-0 flex-1">
                    <Link href={`/vessels/${v.id}`} className="flex items-center gap-2 hover:opacity-80">
                      <span className="text-lg">{vesselTypeIcon(v.vessel_type)}</span>
                      <h3 className="text-sm font-semibold text-blue-700 truncate hover:underline">{v.name}</h3>
                    </Link>
                    <p className="text-xs text-gray-500 mt-0.5">{v.vessel_type}</p>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[11px] font-medium flex-shrink-0 ${
                    v.is_active ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"
                  }`}>
                    {v.is_active ? "Active" : "Inactive"}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px] text-gray-500 mb-3">
                  {v.imo_number && (
                    <div>
                      <span className="text-gray-400">IMO:</span>{" "}
                      <span className="text-gray-600">{v.imo_number}</span>
                    </div>
                  )}
                  {v.flag && (
                    <div>
                      <span className="text-gray-400">Flag:</span>{" "}
                      <span className="text-gray-600">{v.flag}</span>
                    </div>
                  )}
                  {v.class_society && (
                    <div>
                      <span className="text-gray-400">Class:</span>{" "}
                      <span className="text-gray-600">{v.class_society}</span>
                    </div>
                  )}
                  {v.owner_company && (
                    <div>
                      <span className="text-gray-400">Owner:</span>{" "}
                      <span className="text-gray-600 truncate">{v.owner_company}</span>
                    </div>
                  )}
                </div>

                <div className="flex gap-2 pt-2 border-t border-gray-100">
                  <Link
                    href={`/vessels/${v.id}`}
                    className="flex-1 px-2 py-1.5 text-xs font-medium text-green-600 bg-green-50 hover:bg-green-100 rounded-lg transition-colors text-center"
                  >
                    View
                  </Link>
                  {isAdmin && (
                    <>
                      <button
                        onClick={() => { setEditVessel(v); setModalOpen(true); }}
                        className="flex-1 px-2 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors text-center"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(v)}
                        className="flex-1 px-2 py-1.5 text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors text-center"
                      >
                        Delete
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))}
            {vessels.length === 0 && (
              <div className="text-center py-8 text-gray-500 text-sm">
                No vessels registered yet
              </div>
            )}
          </div>

          {/* 데스크톱 테이블뷰 */}
          <div className="hidden lg:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="table-scroll-wrapper">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Vessel</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Type</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">IMO</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Flag / Class</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Owner</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Build Year</th>
                    <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Status</th>
                    <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {vessels.map((v) => (
                    <tr key={v.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4">
                        <Link href={`/vessels/${v.id}`} className="flex items-center gap-2 hover:opacity-80">
                          <span className="text-lg">{vesselTypeIcon(v.vessel_type)}</span>
                          <span className="text-sm font-medium text-blue-700 hover:underline">{v.name}</span>
                        </Link>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">{v.vessel_type}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 font-mono">{v.imo_number || "-"}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-1.5">
                          {v.flag && (
                            <span className="px-2 py-0.5 bg-slate-100 rounded text-xs font-medium text-slate-700">
                              {v.flag}
                            </span>
                          )}
                          {v.class_society && (
                            <span className="px-2 py-0.5 bg-blue-50 rounded text-xs font-medium text-blue-700">
                              {v.class_society}
                            </span>
                          )}
                          {!v.flag && !v.class_society && "-"}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">{v.owner_company || "-"}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 text-center">{v.build_year || "-"}</td>
                      <td className="px-6 py-4 text-center">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          v.is_active ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"
                        }`}>
                          {v.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className="flex items-center justify-center gap-1">
                          <Link
                            href={`/vessels/${v.id}`}
                            className="px-2 py-1 text-xs font-medium text-green-600 hover:bg-green-50 rounded transition-colors"
                          >
                            View
                          </Link>
                          {isAdmin && (
                            <>
                              <button
                                onClick={() => { setEditVessel(v); setModalOpen(true); }}
                                className="px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50 rounded transition-colors"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDelete(v)}
                                className="px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-50 rounded transition-colors"
                              >
                                Delete
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                  {vessels.length === 0 && (
                    <tr>
                      <td colSpan={8} className="px-6 py-8 text-center text-gray-500">
                        No vessels registered yet. Click &quot;Register Vessel&quot; to add one.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <div className="mt-3 sm:mt-4 text-xs sm:text-sm text-gray-500">
        Total: {vessels.length} vessels
      </div>

      <VesselFormModal
        isOpen={modalOpen}
        onClose={() => { setModalOpen(false); setEditVessel(null); }}
        onSuccess={loadVessels}
        editData={editVessel}
      />
    </div>
  );
}
