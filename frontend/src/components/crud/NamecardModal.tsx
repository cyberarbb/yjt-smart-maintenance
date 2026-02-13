"use client";

import { useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { useAuth } from "@/lib/auth";
import { updateMyProfile } from "@/lib/api";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function NamecardModal({ isOpen, onClose }: Props) {
  const { user, updateUser } = useAuth();
  const [form, setForm] = useState({
    namecard_title: "",
    namecard_department: "",
    namecard_mobile: "",
    namecard_fax: "",
    namecard_address: "",
    namecard_website: "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (user && isOpen) {
      setForm({
        namecard_title: user.namecard_title || "",
        namecard_department: user.namecard_department || "",
        namecard_mobile: user.namecard_mobile || "",
        namecard_fax: user.namecard_fax || "",
        namecard_address: user.namecard_address || "",
        namecard_website: user.namecard_website || "",
      });
      setError("");
      setSuccess(false);
    }
  }, [user, isOpen]);

  function handleChange(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await updateMyProfile(form);
      await updateUser(form);
      setSuccess(true);
      setTimeout(() => onClose(), 1200);
    } catch (err: any) {
      setError(err.message || "Failed to save namecard.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Namecard / Email Signature" size="lg">
      {success ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-3">💼</div>
          <p className="text-lg font-semibold text-green-600">Namecard Saved!</p>
          <p className="text-sm text-gray-500 mt-1">
            Your email signature has been updated.
          </p>
        </div>
      ) : (
        <form onSubmit={handleSave} className="space-y-4">
          {error && (
            <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>
          )}

          {/* 기본 정보 (읽기 전용) */}
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-500 font-medium mb-1">Basic Info (from profile)</p>
            <p className="text-sm font-medium text-gray-800">{user?.full_name}</p>
            <p className="text-xs text-gray-500">{user?.email}{user?.company ? ` | ${user.company}` : ""}</p>
          </div>

          {/* 직책 & 부서 */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Title / Position</label>
              <input
                type="text"
                value={form.namecard_title}
                onChange={(e) => handleChange("namecard_title", e.target.value)}
                placeholder="e.g. Sales Manager"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Department</label>
              <input
                type="text"
                value={form.namecard_department}
                onChange={(e) => handleChange("namecard_department", e.target.value)}
                placeholder="e.g. Sales Department"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* 연락처 */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Mobile</label>
              <input
                type="tel"
                value={form.namecard_mobile}
                onChange={(e) => handleChange("namecard_mobile", e.target.value)}
                placeholder="e.g. +82-10-1234-5678"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Fax</label>
              <input
                type="tel"
                value={form.namecard_fax}
                onChange={(e) => handleChange("namecard_fax", e.target.value)}
                placeholder="e.g. +82-51-123-4567"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* 주소 */}
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Address</label>
            <input
              type="text"
              value={form.namecard_address}
              onChange={(e) => handleChange("namecard_address", e.target.value)}
              placeholder="e.g. 123, Centum-ro, Haeundae-gu, Busan, Korea"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 웹사이트 */}
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Website</label>
            <input
              type="url"
              value={form.namecard_website}
              onChange={(e) => handleChange("namecard_website", e.target.value)}
              placeholder="e.g. https://www.yongjinturbo.com"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 미리보기 */}
          <div>
            <p className="text-xs font-medium text-gray-600 mb-2">Email Signature Preview</p>
            <div className="border border-gray-200 rounded-lg p-4 bg-white">
              <div style={{ borderTop: "2px solid #2563eb", paddingTop: "12px" }}>
                <p className="text-sm font-bold text-gray-800 m-0">{user?.full_name}</p>
                {(form.namecard_title || form.namecard_department) && (
                  <p className="text-xs text-blue-600 font-medium mt-0.5">
                    {[form.namecard_title, form.namecard_department].filter(Boolean).join(" | ")}
                  </p>
                )}
                {user?.company && (
                  <p className="text-xs text-gray-600 font-semibold mt-0.5">{user.company}</p>
                )}
                <div className="mt-1.5 text-[11px] text-gray-400 space-y-0.5">
                  {(user?.phone || form.namecard_mobile || form.namecard_fax) && (
                    <p className="m-0">
                      {[
                        user?.phone ? `Tel: ${user.phone}` : "",
                        form.namecard_mobile ? `Mobile: ${form.namecard_mobile}` : "",
                        form.namecard_fax ? `Fax: ${form.namecard_fax}` : "",
                      ]
                        .filter(Boolean)
                        .join(" | ")}
                    </p>
                  )}
                  <p className="m-0">Email: {user?.email}</p>
                  {form.namecard_address && <p className="m-0">{form.namecard_address}</p>}
                  {form.namecard_website && (
                    <p className="m-0 text-blue-600">{form.namecard_website}</p>
                  )}
                </div>
              </div>
            </div>
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
              {saving ? "Saving..." : "Save Namecard"}
            </button>
          </div>
        </form>
      )}
    </Modal>
  );
}
