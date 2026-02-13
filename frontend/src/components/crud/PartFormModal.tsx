"use client";

import { useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { createPart, updatePart } from "@/lib/api";

const BRANDS = ["MAN", "MHI", "KBB", "ABB", "Napier", "OTHER"];
const CATEGORIES = ["Nozzle Ring", "Bearing", "Turbine Blade", "Compressor Wheel", "Shaft", "Seal", "Gasket", "Casing", "Cartridge", "Filter", "Other"];

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  editData?: any;
}

export default function PartFormModal({ isOpen, onClose, onSuccess, editData }: Props) {
  const isEdit = !!editData;
  const [form, setForm] = useState({
    part_number: "",
    name: "",
    brand: "MAN",
    turbo_model: "",
    category: "Nozzle Ring",
    description: "",
    unit_price: 0,
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (editData) {
      setForm({
        part_number: editData.part_number || "",
        name: editData.name || "",
        brand: editData.brand || "MAN",
        turbo_model: editData.turbo_model || "",
        category: editData.category || "Nozzle Ring",
        description: editData.description || "",
        unit_price: editData.unit_price || 0,
      });
    } else {
      setForm({ part_number: "", name: "", brand: "MAN", turbo_model: "", category: "Nozzle Ring", description: "", unit_price: 0 });
    }
    setError("");
  }, [editData, isOpen]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      if (isEdit) {
        await updatePart(editData.id, form);
      } else {
        await createPart(form);
      }
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isEdit ? "Edit Part" : "Add Part"} size="lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>}

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Part Number *</label>
            <input type="text" required value={form.part_number} onChange={e => setForm({...form, part_number: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" disabled={isEdit} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
            <input type="text" required value={form.name} onChange={e => setForm({...form, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Brand *</label>
            <select value={form.brand} onChange={e => setForm({...form, brand: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
              {BRANDS.map(b => <option key={b} value={b}>{b}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Turbo Model *</label>
            <input type="text" required value={form.turbo_model} onChange={e => setForm({...form, turbo_model: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select value={form.category} onChange={e => setForm({...form, category: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
              {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Unit Price (USD)</label>
          <input type="number" step="0.01" min="0" value={form.unit_price} onChange={e => setForm({...form, unit_price: parseFloat(e.target.value) || 0})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea value={form.description} onChange={e => setForm({...form, description: e.target.value})} rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <div className="flex gap-3 pt-2">
          <button type="button" onClick={onClose} className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">Cancel</button>
          <button type="submit" disabled={saving} className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {saving ? "Saving..." : isEdit ? "Update" : "Create"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
