"use client";

import { useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { sendEmailToCustomer } from "@/lib/api";
import { useAuth } from "@/lib/auth";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  toEmail: string;
  toName?: string;
  toCompany?: string;
}

export default function SendEmailModal({ isOpen, onClose, toEmail, toName, toCompany }: Props) {
  const { user } = useAuth();
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setSubject("");
      setBody("");
      setError("");
      setSuccess(false);
    }
  }, [isOpen]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!subject.trim() || !body.trim()) {
      setError("Subject and message are required.");
      return;
    }
    setSending(true);
    setError("");
    try {
      const result = await sendEmailToCustomer({ to_email: toEmail, subject, body });
      if (result.success) {
        setSuccess(true);
        setTimeout(() => onClose(), 1500);
      } else {
        setError(result.message || "Failed to send email.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to send email.");
    } finally {
      setSending(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Send Email" size="lg">
      {success ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-3">✉️</div>
          <p className="text-lg font-semibold text-green-600">Email Sent!</p>
          <p className="text-sm text-gray-500 mt-1">
            Successfully sent to {toEmail}
          </p>
        </div>
      ) : (
        <form onSubmit={handleSend} className="space-y-4">
          {error && (
            <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>
          )}

          {/* 발신자 정보 */}
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-xs text-blue-600 font-medium mb-1">From</p>
            <p className="text-sm text-gray-800 font-medium">{user?.full_name}</p>
            {user?.company && (
              <p className="text-xs text-gray-500">{user.company}</p>
            )}
            {user?.namecard_title && (
              <p className="text-xs text-gray-500">{user.namecard_title}{user?.namecard_department ? ` | ${user.namecard_department}` : ""}</p>
            )}
          </div>

          {/* 수신자 정보 */}
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-500 font-medium mb-1">To</p>
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-800">{toEmail}</span>
              {toName && (
                <span className="text-xs text-gray-500">
                  ({toName}{toCompany ? ` - ${toCompany}` : ""})
                </span>
              )}
            </div>
          </div>

          {/* 제목 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Subject <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="Email subject..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              autoFocus
            />
          </div>

          {/* 본문 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Message <span className="text-red-500">*</span>
            </label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={8}
              placeholder="Type your message here..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y"
            />
          </div>

          {/* 네임카드 안내 */}
          {(user?.namecard_title || user?.namecard_mobile) && (
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <svg className="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Your namecard signature will be automatically attached.</span>
            </div>
          )}

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
              disabled={sending}
              className="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
            >
              {sending ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Sending...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  Send Email
                </>
              )}
            </button>
          </div>
        </form>
      )}
    </Modal>
  );
}
