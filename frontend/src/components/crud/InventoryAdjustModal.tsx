"use client";

import { useState } from "react";
import Modal from "@/components/ui/Modal";
import { adjustInventory } from "@/lib/api";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  inventoryId: string;
  partName: string;
  currentQty: number;
}

export default function InventoryAdjustModal({ isOpen, onClose, onSuccess, inventoryId, partName, currentQty }: Props) {
  const [adjustment, setAdjustment] = useState(0);
  const [reason, setReason] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (adjustment === 0) return;
    setSaving(true);
    setError("");
    try {
      await adjustInventory(inventoryId, { adjustment, reason });
      onSuccess();
      onClose();
      setAdjustment(0);
      setReason("");
    } catch (err: any) {
      setError(err.message || "Failed to adjust");
    } finally {
      setSaving(false);
    }
  }

  const newQty = currentQty + adjustment;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Adjust Stock" size="sm">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>}

        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-sm font-medium text-gray-800">{partName}</p>
          <p className="text-xs text-gray-500">Current stock: {currentQty}</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Adjustment (+/-)</label>
          <input type="number" value={adjustment} onChange={e => setAdjustment(parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          <p className={`text-xs mt-1 ${newQty < 0 ? "text-red-500" : "text-gray-500"}`}>
            New quantity: {newQty}
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Reason</label>
          <input type="text" value={reason} onChange={e => setReason(e.target.value)} placeholder="e.g. Incoming shipment, Used for overhaul"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <div className="flex gap-3 pt-2">
          <button type="button" onClick={onClose} className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">Cancel</button>
          <button type="submit" disabled={saving || newQty < 0} className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {saving ? "Saving..." : "Adjust"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
