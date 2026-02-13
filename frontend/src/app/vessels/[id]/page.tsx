"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {
  getVessel,
  getEquipmentTree,
  getVesselEquipment,
  deleteEquipment,
} from "@/lib/api";
import EquipmentTree from "@/components/vessel/EquipmentTree";
import EquipmentFormModal from "@/components/crud/EquipmentFormModal";

export default function VesselDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const vesselId = params.id as string;

  const [vessel, setVessel] = useState<any>(null);
  const [tree, setTree] = useState<any[]>([]);
  const [flatEquipment, setFlatEquipment] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEquipment, setSelectedEquipment] = useState<any>(null);
  const [showForm, setShowForm] = useState(false);
  const [editEquipment, setEditEquipment] = useState<any>(null);
  const [detailPanel, setDetailPanel] = useState(false);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.role === "developer";

  async function loadData() {
    try {
      const [vesselData, treeData, flatData] = await Promise.all([
        getVessel(vesselId),
        getEquipmentTree(vesselId),
        getVesselEquipment(vesselId),
      ]);
      setVessel(vesselData);
      setTree(treeData);
      setFlatEquipment(flatData);
    } catch (e) {
      console.error("Failed to load vessel data:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (vesselId) loadData();
  }, [vesselId]);

  function handleSelectEquipment(node: any) {
    setSelectedEquipment(node);
    setDetailPanel(true);
  }

  async function handleDeleteEquipment(eqId: string) {
    if (!confirm("Delete this equipment and all its children?")) return;
    try {
      await deleteEquipment(eqId);
      setDetailPanel(false);
      setSelectedEquipment(null);
      await loadData();
    } catch (e: any) {
      alert(e.message || "Failed to delete");
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!vessel) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-500">Vessel not found</p>
        <button onClick={() => router.push("/vessels")} className="mt-4 text-blue-600 text-sm hover:underline">
          Back to Vessels
        </button>
      </div>
    );
  }

  // Stats
  const totalEquipment = flatEquipment.length;
  const warningCount = flatEquipment.filter((e) => e.status === "Warning").length;
  const criticalCount = flatEquipment.filter((e) => e.status === "Critical").length;
  const categories = [...new Set(flatEquipment.map((e) => e.category))];

  return (
    <div>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <button
              onClick={() => router.push("/vessels")}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
              🚢 {vessel.name}
            </h1>
          </div>
          <div className="flex flex-wrap gap-2 text-xs text-gray-500 ml-7">
            <span>IMO: {vessel.imo_number || "N/A"}</span>
            <span>|</span>
            <span>{vessel.vessel_type}</span>
            <span>|</span>
            <span>Flag: {vessel.flag || "N/A"}</span>
            <span>|</span>
            <span>Class: {vessel.class_society || "N/A"}</span>
          </div>
        </div>

        {isAdmin && (
          <button
            onClick={() => {
              setEditEquipment(null);
              setShowForm(true);
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors whitespace-nowrap"
          >
            + Add Equipment
          </button>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
          <p className="text-[11px] text-gray-500">Total Equipment</p>
          <p className="text-xl font-bold text-gray-800">{totalEquipment}</p>
        </div>
        <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
          <p className="text-[11px] text-gray-500">Categories</p>
          <p className="text-xl font-bold text-blue-600">{categories.length}</p>
        </div>
        <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
          <p className="text-[11px] text-gray-500">Warning</p>
          <p className="text-xl font-bold text-amber-600">{warningCount}</p>
        </div>
        <div className="bg-white rounded-xl p-3 shadow-sm border border-gray-200">
          <p className="text-[11px] text-gray-500">Critical</p>
          <p className="text-xl font-bold text-red-600">{criticalCount}</p>
        </div>
      </div>

      {/* Main Content: Tree + Detail Panel */}
      <div className="flex flex-col lg:flex-row gap-4">
        {/* Equipment Tree */}
        <div className="flex-1 bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-gray-700 mb-3">Equipment Hierarchy</h2>
          <EquipmentTree tree={tree} onSelect={handleSelectEquipment} />
        </div>

        {/* Detail Side Panel */}
        {detailPanel && selectedEquipment && (
          <div className="lg:w-80 bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-sm font-bold text-gray-800">{selectedEquipment.name}</h3>
              <button
                onClick={() => setDetailPanel(false)}
                className="text-gray-400 hover:text-gray-600 text-lg"
              >
                &times;
              </button>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">Code</span>
                <span className="font-mono text-gray-700">{selectedEquipment.equipment_code}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Category</span>
                <span className="text-gray-700">{selectedEquipment.category}</span>
              </div>
              {selectedEquipment.maker && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Maker</span>
                  <span className="text-gray-700">{selectedEquipment.maker}</span>
                </div>
              )}
              {selectedEquipment.model && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Model</span>
                  <span className="text-gray-700">{selectedEquipment.model}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-500">Status</span>
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                    selectedEquipment.status === "Normal"
                      ? "bg-green-100 text-green-700"
                      : selectedEquipment.status === "Warning"
                      ? "bg-amber-100 text-amber-700"
                      : selectedEquipment.status === "Critical"
                      ? "bg-red-100 text-red-700"
                      : "bg-gray-100 text-gray-500"
                  }`}
                >
                  {selectedEquipment.status}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Running Hours</span>
                <span className="text-gray-700">{selectedEquipment.current_running_hours?.toLocaleString() || 0}h</span>
              </div>
              {selectedEquipment.overhaul_interval_hours && (
                <div className="flex justify-between">
                  <span className="text-gray-500">OH Interval</span>
                  <span className="text-gray-700">{selectedEquipment.overhaul_interval_hours?.toLocaleString()}h</span>
                </div>
              )}
            </div>

            {/* Running Hours Progress */}
            {selectedEquipment.overhaul_interval_hours > 0 && (
              <div className="mt-3 p-2 bg-gray-50 rounded-lg">
                <div className="flex justify-between text-[10px] text-gray-500 mb-1">
                  <span>Overhaul Progress</span>
                  <span>
                    {Math.round(
                      (selectedEquipment.current_running_hours / selectedEquipment.overhaul_interval_hours) * 100
                    )}
                    %
                  </span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      selectedEquipment.current_running_hours / selectedEquipment.overhaul_interval_hours > 0.9
                        ? "bg-red-500"
                        : selectedEquipment.current_running_hours / selectedEquipment.overhaul_interval_hours > 0.7
                        ? "bg-amber-500"
                        : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(
                        (selectedEquipment.current_running_hours / selectedEquipment.overhaul_interval_hours) * 100,
                        100
                      )}%`,
                    }}
                  />
                </div>
              </div>
            )}

            {/* Admin Actions */}
            {isAdmin && (
              <div className="mt-4 flex gap-2">
                <button
                  onClick={() => {
                    setEditEquipment(selectedEquipment);
                    setShowForm(true);
                  }}
                  className="flex-1 px-3 py-1.5 text-xs font-medium bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteEquipment(selectedEquipment.id)}
                  className="flex-1 px-3 py-1.5 text-xs font-medium bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"
                >
                  Delete
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Equipment Form Modal */}
      <EquipmentFormModal
        isOpen={showForm}
        onClose={() => {
          setShowForm(false);
          setEditEquipment(null);
        }}
        onSaved={loadData}
        vesselId={vesselId}
        equipment={editEquipment}
        parentEquipment={flatEquipment}
      />
    </div>
  );
}
