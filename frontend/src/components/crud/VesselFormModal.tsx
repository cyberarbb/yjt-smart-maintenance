"use client";

import { useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { createVessel, updateVessel } from "@/lib/api";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  editData?: any;
}

const VESSEL_TYPES = [
  "Container Ship",
  "Bulk Carrier",
  "Tanker",
  "LNG Carrier",
  "LPG Carrier",
  "FPSO",
  "Car Carrier",
  "General Cargo",
  "Passenger Ship",
  "Tug Boat",
  "Offshore",
  "Other",
];

const CLASS_SOCIETIES = ["KR", "DNV", "LR", "BV", "ABS", "NK", "CCS", "RINA", "RS", "Other"];

export default function VesselFormModal({ isOpen, onClose, onSuccess, editData }: Props) {
  const [form, setForm] = useState({
    name: "",
    imo_number: "",
    vessel_type: "Container Ship",
    flag: "",
    class_society: "",
    gross_tonnage: "",
    build_year: "",
    owner_company: "",
    manager_company: "",
    description: "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      if (editData) {
        setForm({
          name: editData.name || "",
          imo_number: editData.imo_number || "",
          vessel_type: editData.vessel_type || "Container Ship",
          flag: editData.flag || "",
          class_society: editData.class_society || "",
          gross_tonnage: editData.gross_tonnage?.toString() || "",
          build_year: editData.build_year?.toString() || "",
          owner_company: editData.owner_company || "",
          manager_company: editData.manager_company || "",
          description: editData.description || "",
        });
      } else {
        setForm({
          name: "",
          imo_number: "",
          vessel_type: "Container Ship",
          flag: "",
          class_society: "",
          gross_tonnage: "",
          build_year: "",
          owner_company: "",
          manager_company: "",
          description: "",
        });
      }
      setError("");
    }
  }, [isOpen, editData]);

  function handleChange(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name.trim()) {
      setError("Vessel name is required");
      return;
    }
    setSaving(true);
    setError("");

    const payload = {
      ...form,
      gross_tonnage: form.gross_tonnage ? parseFloat(form.gross_tonnage) : null,
      build_year: form.build_year ? parseInt(form.build_year) : null,
      imo_number: form.imo_number || null,
      flag: form.flag || null,
      class_society: form.class_society || null,
      owner_company: form.owner_company || null,
      manager_company: form.manager_company || null,
      description: form.description || null,
    };

    try {
      if (editData) {
        await updateVessel(editData.id, payload);
      } else {
        await createVessel(payload);
      }
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to save vessel");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={editData ? "Edit Vessel" : "Register New Vessel"} size="lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>
        )}

        {/* 선박명 + IMO */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Vessel Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => handleChange("name", e.target.value)}
              placeholder="e.g. HMM Algeciras"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">IMO Number</label>
            <input
              type="text"
              value={form.imo_number}
              onChange={(e) => handleChange("imo_number", e.target.value)}
              placeholder="e.g. 9863297"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* 선종 + 선급 */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Vessel Type</label>
            <select
              value={form.vessel_type}
              onChange={(e) => handleChange("vessel_type", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {VESSEL_TYPES.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Class Society</label>
            <select
              value={form.class_society}
              onChange={(e) => handleChange("class_society", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Select...</option>
              {CLASS_SOCIETIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>

        {/* 국기 + 총톤수 + 건조년도 */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Flag</label>
            <input
              type="text"
              value={form.flag}
              onChange={(e) => handleChange("flag", e.target.value)}
              placeholder="e.g. Panama"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Gross Tonnage</label>
            <input
              type="number"
              value={form.gross_tonnage}
              onChange={(e) => handleChange("gross_tonnage", e.target.value)}
              placeholder="e.g. 228283"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Build Year</label>
            <input
              type="number"
              value={form.build_year}
              onChange={(e) => handleChange("build_year", e.target.value)}
              placeholder="e.g. 2020"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* 선주 + 관리회사 */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Owner Company</label>
            <input
              type="text"
              value={form.owner_company}
              onChange={(e) => handleChange("owner_company", e.target.value)}
              placeholder="e.g. HMM Co., Ltd."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Manager Company</label>
            <input
              type="text"
              value={form.manager_company}
              onChange={(e) => handleChange("manager_company", e.target.value)}
              placeholder="e.g. HMM Ship Management"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* 비고 */}
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Description</label>
          <textarea
            value={form.description}
            onChange={(e) => handleChange("description", e.target.value)}
            placeholder="Additional notes..."
            rows={2}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          />
        </div>

        {/* 버튼 */}
        <div className="flex gap-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {saving ? "Saving..." : editData ? "Update Vessel" : "Register Vessel"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
