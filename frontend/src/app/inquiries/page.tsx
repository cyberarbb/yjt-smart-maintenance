"use client";

import { useEffect, useState } from "react";
import { getInquiries, getMyInquiries } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import InquirySubmitModal from "@/components/crud/InquirySubmitModal";
import InquiryResponseModal from "@/components/crud/InquiryResponseModal";

export default function InquiriesPage() {
  const { user } = useAuth();
  const isAdmin = user?.is_admin || user?.role === "developer";

  const [inquiries, setInquiries] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>("");
  const [loading, setLoading] = useState(true);

  // Modal state
  const [submitOpen, setSubmitOpen] = useState(false);
  const [responseInquiry, setResponseInquiry] = useState<any>(null);

  useEffect(() => {
    loadInquiries();
  }, [filter, isAdmin]);

  async function loadInquiries() {
    setLoading(true);
    try {
      if (isAdmin) {
        const params = filter ? `resolved=${filter === "resolved"}` : "";
        const data = await getInquiries(params);
        setInquiries(data);
      } else {
        const data = await getMyInquiries();
        setInquiries(data);
      }
    } catch (e) {
      console.error("Failed to load inquiries:", e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
          {isAdmin ? "Customer Inquiries" : "My Inquiries"}
        </h1>
        {!isAdmin && (
          <button
            onClick={() => setSubmitOpen(true)}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-600 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-1 sm:gap-2"
          >
            <span className="text-base sm:text-lg leading-none">+</span> <span className="hidden sm:inline">New</span> Inquiry
          </button>
        )}
      </div>

      {/* Filters - admin only */}
      {isAdmin && (
        <div className="flex gap-1.5 sm:gap-2 mb-4 sm:mb-6">
          {["", "unresolved", "resolved"].map((f) => (
            <button
              key={f || "all"}
              onClick={() => setFilter(f)}
              className={`px-2.5 py-1.5 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                filter === f
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
              }`}
            >
              {f === "" ? "All" : f === "resolved" ? "Resolved" : "Unresolved"}
            </button>
          ))}
        </div>
      )}

      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading...</div>
      ) : (
        <div className="space-y-3 sm:space-y-4">
          {inquiries.map((inq) => (
            <div
              key={inq.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6"
            >
              <div className="flex justify-between items-start gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2 mb-2">
                    <h3 className="text-sm sm:text-base font-semibold text-gray-800">
                      {inq.subject}
                    </h3>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[11px] sm:text-xs font-medium flex-shrink-0 ${
                        inq.is_resolved
                          ? "bg-green-100 text-green-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {inq.is_resolved ? "Resolved" : "Pending"}
                    </span>
                  </div>
                  <p className="text-xs sm:text-sm text-gray-600 mb-2 line-clamp-3">{inq.message}</p>
                  <p className="text-[11px] sm:text-xs text-gray-400">
                    Contact: {inq.contact_email}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-2 flex-shrink-0">
                  <div className="text-[11px] sm:text-xs text-gray-400">
                    {new Date(inq.created_at).toLocaleDateString()}
                  </div>
                  {isAdmin && (
                    <button
                      onClick={() => setResponseInquiry(inq)}
                      className="px-2.5 py-1 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                    >
                      {inq.response ? "Edit" : "Reply"}
                    </button>
                  )}
                </div>
              </div>
              {inq.response && (
                <div className="mt-2 sm:mt-3 p-2 sm:p-3 bg-blue-50 rounded-lg">
                  <p className="text-[11px] sm:text-xs font-semibold text-blue-600 mb-1">Response:</p>
                  <p className="text-xs sm:text-sm text-gray-700">{inq.response}</p>
                </div>
              )}
            </div>
          ))}
          {inquiries.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              {isAdmin ? "No inquiries found" : "You haven't submitted any inquiries yet"}
            </div>
          )}
        </div>
      )}

      {/* Modals */}
      <InquirySubmitModal
        isOpen={submitOpen}
        onClose={() => setSubmitOpen(false)}
        onSuccess={loadInquiries}
      />

      <InquiryResponseModal
        isOpen={!!responseInquiry}
        onClose={() => setResponseInquiry(null)}
        onSuccess={loadInquiries}
        inquiry={responseInquiry}
      />
    </div>
  );
}
