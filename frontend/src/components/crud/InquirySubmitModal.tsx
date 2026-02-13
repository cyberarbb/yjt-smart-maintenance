"use client";

import { useState } from "react";
import Modal from "@/components/ui/Modal";
import { createInquiry } from "@/lib/api";
import { useAuth } from "@/lib/auth";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function InquirySubmitModal({ isOpen, onClose, onSuccess }: Props) {
  const { user } = useAuth();
  const [form, setForm] = useState({ subject: "", message: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await createInquiry({
        subject: form.subject,
        message: form.message,
        contact_email: user?.email || "",
      });
      onSuccess();
      onClose();
      setForm({ subject: "", message: "" });
    } catch (err: any) {
      setError(err.message || "Failed to submit");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Submit Inquiry">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>}

        <div className="bg-gray-50 p-3 rounded-lg text-sm text-gray-600">
          Contact email: <span className="font-medium">{user?.email}</span>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Subject *</label>
          <input type="text" required value={form.subject} onChange={e => setForm({...form, subject: e.target.value})}
            placeholder="e.g. Overhaul quote request for MAN NR29/S"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Message *</label>
          <textarea required value={form.message} onChange={e => setForm({...form, message: e.target.value})} rows={5}
            placeholder="Describe your inquiry in detail..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <div className="flex gap-3 pt-2">
          <button type="button" onClick={onClose} className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">Cancel</button>
          <button type="submit" disabled={saving} className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {saving ? "Submitting..." : "Submit Inquiry"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
