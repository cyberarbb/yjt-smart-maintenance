"use client";

import { useEffect, useState } from "react";
import { getInquiries } from "@/lib/api";

export default function InquiriesPage() {
  const [inquiries, setInquiries] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInquiries();
  }, [filter]);

  async function loadInquiries() {
    setLoading(true);
    try {
      const params = filter ? `resolved=${filter === "resolved"}` : "";
      const data = await getInquiries(params);
      setInquiries(data);
    } catch (e) {
      console.error("Failed to load inquiries:", e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Customer Inquiries</h1>

      <div className="flex gap-2 mb-6">
        {["", "unresolved", "resolved"].map((f) => (
          <button
            key={f || "all"}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? "bg-blue-600 text-white"
                : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
            }`}
          >
            {f === "" ? "All" : f === "resolved" ? "Resolved" : "Unresolved"}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading...</div>
      ) : (
        <div className="space-y-4">
          {inquiries.map((inq) => (
            <div
              key={inq.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
            >
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-base font-semibold text-gray-800">
                      {inq.subject}
                    </h3>
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        inq.is_resolved
                          ? "bg-green-100 text-green-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {inq.is_resolved ? "Resolved" : "Pending"}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{inq.message}</p>
                  <p className="text-xs text-gray-400">
                    Contact: {inq.contact_email}
                  </p>
                </div>
                <div className="text-xs text-gray-400 ml-4">
                  {new Date(inq.created_at).toLocaleDateString()}
                </div>
              </div>
              {inq.response && (
                <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                  <p className="text-xs font-semibold text-blue-600 mb-1">
                    Response:
                  </p>
                  <p className="text-sm text-gray-700">{inq.response}</p>
                </div>
              )}
            </div>
          ))}
          {inquiries.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No inquiries found
            </div>
          )}
        </div>
      )}
    </div>
  );
}
