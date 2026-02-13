"use client";

import { useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { updateInquiry, generateInquiryDraft } from "@/lib/api";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  inquiry: any;
}

const LANG_LABELS: Record<string, string> = {
  ko: "🇰🇷 Korean",
  en: "🇺🇸 English",
  zh: "🇨🇳 Chinese",
  ja: "🇯🇵 Japanese",
  ar: "🇸🇦 Arabic",
  es: "🇪🇸 Spanish",
  hi: "🇮🇳 Hindi",
  fr: "🇫🇷 French",
};

export default function InquiryResponseModal({ isOpen, onClose, onSuccess, inquiry }: Props) {
  const [response, setResponse] = useState("");
  const [isResolved, setIsResolved] = useState(false);
  const [sendEmail, setSendEmail] = useState(true);
  const [saving, setSaving] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");
  const [detectedLang, setDetectedLang] = useState("");

  useEffect(() => {
    if (inquiry) {
      setResponse(inquiry.response || "");
      setIsResolved(inquiry.is_resolved || false);
      setSendEmail(true);
      setDetectedLang("");
    }
    setError("");
  }, [inquiry, isOpen]);

  async function handleGenerateDraft() {
    setGenerating(true);
    setError("");
    try {
      const result = await generateInquiryDraft(inquiry.id);
      setResponse(result.draft);
      setDetectedLang(result.detected_language);
    } catch (err: any) {
      setError(err.message || "Failed to generate draft");
    } finally {
      setGenerating(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!response.trim()) {
      setError("Response cannot be empty.");
      return;
    }
    setSaving(true);
    setError("");
    try {
      await updateInquiry(inquiry.id, {
        response,
        is_resolved: isResolved,
        send_email: sendEmail,
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  if (!inquiry) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Respond to Inquiry" size="lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>}

        {/* 문의 원본 */}
        <div className="bg-gray-50 p-4 rounded-lg space-y-2">
          <div className="flex items-start justify-between gap-2">
            <p className="text-sm font-medium text-gray-800">{inquiry.subject}</p>
            {detectedLang && (
              <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-[11px] font-medium rounded-full flex-shrink-0">
                {LANG_LABELS[detectedLang] || detectedLang}
              </span>
            )}
          </div>
          <p className="text-sm text-gray-600 whitespace-pre-wrap">{inquiry.message}</p>
          <div className="flex items-center gap-3 pt-1">
            <p className="text-xs text-gray-400">From: {inquiry.contact_email}</p>
            {inquiry.company_name && (
              <p className="text-xs text-gray-400">| {inquiry.company_name}</p>
            )}
          </div>
        </div>

        {/* AI 초안 생성 버튼 */}
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleGenerateDraft}
            disabled={generating}
            className="px-4 py-2 text-sm font-medium text-purple-700 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 disabled:opacity-50 transition-colors flex items-center gap-2"
          >
            {generating ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Generating AI Draft...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Generate AI Draft
              </>
            )}
          </button>
          <span className="text-xs text-gray-400">
            Auto-detect language & generate response
          </span>
        </div>

        {/* 답변 텍스트 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Response</label>
          <textarea
            value={response}
            onChange={(e) => setResponse(e.target.value)}
            rows={6}
            placeholder="Type your response or use AI draft..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y"
          />
        </div>

        {/* 옵션 체크박스 */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={isResolved}
              onChange={(e) => setIsResolved(e.target.checked)}
              className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700">Mark as resolved</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={sendEmail}
              onChange={(e) => setSendEmail(e.target.checked)}
              className="w-4 h-4 rounded border-gray-300 text-green-600 focus:ring-green-500"
            />
            <div className="flex items-center gap-1.5">
              <span className="text-sm text-gray-700">Send response via email</span>
              <svg className="w-3.5 h-3.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </label>
          {sendEmail && (
            <p className="text-xs text-gray-400 ml-6">
              Email will be sent to {inquiry.contact_email} with your namecard signature.
            </p>
          )}
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
            className="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
          >
            {saving ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Saving...
              </>
            ) : sendEmail ? (
              "Save & Send Email"
            ) : (
              "Save Response"
            )}
          </button>
        </div>
      </form>
    </Modal>
  );
}
