"use client";

import { useState, useEffect } from "react";
import { createEquipment, updateEquipment } from "@/lib/api";

const EQUIPMENT_CATEGORIES = [
  "Main Engine", "Generator", "Boiler", "Turbocharger", "Pump",
  "Compressor", "Steering Gear", "Emergency Generator", "Purifier",
  "Heat Exchanger", "Crane", "Fuel System", "Exhaust System", "Other",
];

interface EquipmentFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSaved: () => void;
  vesselId: string;
  equipment?: any; // null for create
  parentEquipment?: any[]; // available parent options
}

export default function EquipmentFormModal({
  isOpen,
  onClose,
  onSaved,
  vesselId,
  equipment,
  parentEquipment = [],
}: EquipmentFormModalProps) {
  const [form, setForm] = useState({
    equipment_code: "",
    name: "",
    category: "Main Engine",
    parent_id: "",
    maker: "",
    model: "",
    serial_number: "",
    rated_power: "",
    rated_rpm: "",
    initial_running_hours: 0,
    current_running_hours: 0,
    overhaul_interval_hours: "",
    description: "",
    sort_order: 0,
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (equipment) {
      setForm({
        equipment_code: equipment.equipment_code || "",
        name: equipment.name || "",
        category: equipment.category || "Main Engine",
        parent_id: equipment.parent_id || "",
        maker: equipment.maker || "",
        model: equipment.model || "",
        serial_number: equipment.serial_number || "",
        rated_power: equipment.rated_power || "",
        rated_rpm: equipment.rated_rpm || "",
        initial_running_hours: equipment.initial_running_hours || 0,
        current_running_hours: equipment.current_running_hours || 0,
        overhaul_interval_hours: equipment.overhaul_interval_hours || "",
        description: equipment.description || "",
        sort_order: equipment.sort_order || 0,
      });
    } else {
      setForm({
        equipment_code: "",
        name: "",
        category: "Main Engine",
        parent_id: "",
        maker: "",
        model: "",
        serial_number: "",
        rated_power: "",
        rated_rpm: "",
        initial_running_hours: 0,
        current_running_hours: 0,
        overhaul_interval_hours: "",
        description: "",
        sort_order: 0,
      });
    }
  }, [equipment, isOpen]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      const payload: any = {
        ...form,
        vessel_id: vesselId,
        parent_id: form.parent_id || null,
        overhaul_interval_hours: form.overhaul_interval_hours ? Number(form.overhaul_interval_hours) : null,
      };

      if (equipment) {
        delete payload.vessel_id;
        await updateEquipment(equipment.id, payload);
      } else {
        await createEquipment(payload);
      }
      onSaved();
      onClose();
    } catch (err: any) {
      alert(err.message || "Failed to save equipment");
    } finally {
      setSaving(false);
    }
  }

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-xl">
        <div className="sticky top-0 bg-white px-6 py-4 border-b border-gray-200 rounded-t-2xl">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-bold text-gray-800">
              {equipment ? "Edit Equipment" : "Add Equipment"}
            </h2>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl">&times;</button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Equipment Code *</label>
              <input
                type="text"
                required
                value={form.equipment_code}
                onChange={(e) => setForm({ ...form, equipment_code: e.target.value })}
                placeholder="e.g. ME-001"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Category *</label>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
              >
                {EQUIPMENT_CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Name *</label>
            <input
              type="text"
              required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="e.g. Main Engine #1"
              className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Parent Equipment</label>
            <select
              value={form.parent_id}
              onChange={(e) => setForm({ ...form, parent_id: e.target.value })}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
            >
              <option value="">None (Top Level)</option>
              {parentEquipment
                .filter((p) => p.id !== equipment?.id)
                .map((p: any) => (
                  <option key={p.id} value={p.id}>
                    [{p.equipment_code}] {p.name}
                  </option>
                ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Maker</label>
              <input
                type="text"
                value={form.maker}
                onChange={(e) => setForm({ ...form, maker: e.target.value })}
                placeholder="e.g. MAN Energy Solutions"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Model</label>
              <input
                type="text"
                value={form.model}
                onChange={(e) => setForm({ ...form, model: e.target.value })}
                placeholder="e.g. 8S80ME-C9.2"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Rated Power</label>
              <input
                type="text"
                value={form.rated_power}
                onChange={(e) => setForm({ ...form, rated_power: e.target.value })}
                placeholder="e.g. 68,640 kW"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Rated RPM</label>
              <input
                type="text"
                value={form.rated_rpm}
                onChange={(e) => setForm({ ...form, rated_rpm: e.target.value })}
                placeholder="e.g. 80 RPM"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Initial Hours</label>
              <input
                type="number"
                value={form.initial_running_hours}
                onChange={(e) => setForm({ ...form, initial_running_hours: Number(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Current Hours</label>
              <input
                type="number"
                value={form.current_running_hours}
                onChange={(e) => setForm({ ...form, current_running_hours: Number(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">OH Interval</label>
              <input
                type="number"
                value={form.overhaul_interval_hours}
                onChange={(e) => setForm({ ...form, overhaul_interval_hours: e.target.value })}
                placeholder="e.g. 24000"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Description</label>
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              rows={2}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2.5 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? "Saving..." : equipment ? "Update" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
