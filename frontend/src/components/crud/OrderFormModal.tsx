"use client";

import { useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { createOrder, updateOrder, getCustomers } from "@/lib/api";

const ORDER_TYPES = ["Overhaul", "Part Supply", "Technical Service"];
const STATUSES = ["Pending", "In Progress", "Completed", "Cancelled"];
const BRANDS = ["MAN", "MHI", "KBB", "ABB", "Napier"];

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  editData?: any;
}

export default function OrderFormModal({ isOpen, onClose, onSuccess, editData }: Props) {
  const isEdit = !!editData;
  const [customers, setCustomers] = useState<any[]>([]);
  const [form, setForm] = useState({
    customer_id: "",
    order_type: "Overhaul",
    turbo_brand: "MAN",
    turbo_model: "",
    vessel_name: "",
    description: "",
    status: "Pending",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      getCustomers().then(setCustomers).catch(() => {});
    }
  }, [isOpen]);

  useEffect(() => {
    if (editData) {
      setForm({
        customer_id: editData.customer_id || "",
        order_type: editData.order_type || "Overhaul",
        turbo_brand: editData.turbo_brand || "MAN",
        turbo_model: editData.turbo_model || "",
        vessel_name: editData.vessel_name || "",
        description: editData.description || "",
        status: editData.status || "Pending",
      });
    } else {
      setForm({ customer_id: "", order_type: "Overhaul", turbo_brand: "MAN", turbo_model: "", vessel_name: "", description: "", status: "Pending" });
    }
    setError("");
  }, [editData, isOpen]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      if (isEdit) {
        await updateOrder(editData.id, form);
      } else {
        await createOrder(form);
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
    <Modal isOpen={isOpen} onClose={onClose} title={isEdit ? "Edit Order" : "Create Order"} size="lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Customer *</label>
          <select required value={form.customer_id} onChange={e => setForm({...form, customer_id: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
            <option value="">Select customer...</option>
            {customers.map((c: any) => <option key={c.id} value={c.id}>{c.company_name} - {c.contact_name}</option>)}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Order Type *</label>
            <select value={form.order_type} onChange={e => setForm({...form, order_type: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
              {ORDER_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          {isEdit && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select value={form.status} onChange={e => setForm({...form, status: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
                {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Turbo Brand</label>
            <select value={form.turbo_brand} onChange={e => setForm({...form, turbo_brand: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
              {BRANDS.map(b => <option key={b} value={b}>{b}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Turbo Model</label>
            <input type="text" value={form.turbo_model} onChange={e => setForm({...form, turbo_model: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Vessel Name</label>
          <input type="text" value={form.vessel_name} onChange={e => setForm({...form, vessel_name: e.target.value})}
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
