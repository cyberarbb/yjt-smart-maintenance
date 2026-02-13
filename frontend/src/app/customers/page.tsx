"use client";

import { useEffect, useState } from "react";
import { getCustomers, deleteCustomer } from "@/lib/api";
import AdminGuard from "@/components/layout/AdminGuard";
import CustomerFormModal from "@/components/crud/CustomerFormModal";
import SendEmailModal from "@/components/crud/SendEmailModal";

export default function CustomersPage() {
  return (
    <AdminGuard>
      <CustomersContent />
    </AdminGuard>
  );
}

function CustomersContent() {
  const [customers, setCustomers] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editCustomer, setEditCustomer] = useState<any>(null);

  // Email modal state
  const [emailModalOpen, setEmailModalOpen] = useState(false);
  const [emailTarget, setEmailTarget] = useState<{ email: string; name: string; company: string }>({
    email: "",
    name: "",
    company: "",
  });

  useEffect(() => {
    loadCustomers();
  }, []);

  async function loadCustomers() {
    setLoading(true);
    try {
      const params = search ? `search=${encodeURIComponent(search)}` : "";
      const data = await getCustomers(params);
      setCustomers(data);
    } catch (e) {
      console.error("Failed to load customers:", e);
    } finally {
      setLoading(false);
    }
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    loadCustomers();
  }

  async function handleDelete(customer: any) {
    if (!confirm(`Delete "${customer.company_name}"? This cannot be undone.`)) return;
    try {
      await deleteCustomer(customer.id);
      loadCustomers();
    } catch (err: any) {
      alert(err.message || "Failed to delete");
    }
  }

  function openEmailModal(customer: any) {
    setEmailTarget({
      email: customer.email,
      name: customer.contact_name,
      company: customer.company_name,
    });
    setEmailModalOpen(true);
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">Customer Management</h1>
        <button
          onClick={() => { setEditCustomer(null); setModalOpen(true); }}
          className="px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-600 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-1 sm:gap-2"
        >
          <span className="text-base sm:text-lg leading-none">+</span> <span className="hidden sm:inline">Add</span> Customer
        </button>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-4 mb-4 sm:mb-6">
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            placeholder="Search company, name, email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 min-w-0 px-3 py-2 sm:px-4 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-3 py-2 sm:px-4 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors flex-shrink-0"
          >
            Search
          </button>
        </form>
      </div>

      {loading ? (
        <div className="p-8 text-center text-gray-500">Loading...</div>
      ) : (
        <>
          {/* 모바일 카드뷰 */}
          <div className="lg:hidden space-y-3">
            {customers.map((c) => (
              <div
                key={c.id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-4"
              >
                <div className="flex justify-between items-start gap-2 mb-2">
                  <div className="min-w-0 flex-1">
                    <h3 className="text-sm font-semibold text-gray-800 truncate">{c.company_name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">{c.contact_name}</p>
                  </div>
                  <span className="px-2 py-0.5 bg-slate-100 rounded text-[11px] font-medium text-slate-700 flex-shrink-0">
                    {c.country}
                  </span>
                </div>

                {/* 이메일 - 클릭하면 이메일 모달 열림 */}
                <div className="mb-2">
                  <button
                    onClick={() => openEmailModal(c)}
                    className="text-xs text-blue-600 break-all hover:text-blue-800 hover:underline text-left"
                  >
                    ✉️ {c.email}
                  </button>
                </div>

                {/* 상세 정보 */}
                <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px] text-gray-500 mb-3">
                  {c.phone && (
                    <div>
                      <span className="text-gray-400">Phone:</span>{" "}
                      <span className="text-gray-600">{c.phone}</span>
                    </div>
                  )}
                  {c.vessel_type && (
                    <div>
                      <span className="text-gray-400">Vessel:</span>{" "}
                      <span className="text-gray-600">{c.vessel_type}</span>
                    </div>
                  )}
                </div>

                {/* 액션 버튼 */}
                <div className="flex gap-2 pt-2 border-t border-gray-100">
                  <button
                    onClick={() => openEmailModal(c)}
                    className="flex-1 px-2 py-1.5 text-xs font-medium text-green-600 bg-green-50 hover:bg-green-100 rounded-lg transition-colors text-center flex items-center justify-center gap-1"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    Email
                  </button>
                  <button
                    onClick={() => { setEditCustomer(c); setModalOpen(true); }}
                    className="flex-1 px-2 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors text-center"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(c)}
                    className="flex-1 px-2 py-1.5 text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors text-center"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
            {customers.length === 0 && (
              <div className="text-center py-8 text-gray-500 text-sm">
                No customers found
              </div>
            )}
          </div>

          {/* 데스크톱 테이블뷰 */}
          <div className="hidden lg:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="table-scroll-wrapper">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Company</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Contact</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Email</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Phone</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Country</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Vessel Type</th>
                    <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {customers.map((c) => (
                    <tr key={c.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-gray-800">{c.company_name}</td>
                      <td className="px-6 py-4 text-sm text-gray-700">{c.contact_name}</td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => openEmailModal(c)}
                          className="text-sm text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
                        >
                          <svg className="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                          </svg>
                          {c.email}
                        </button>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">{c.phone || "-"}</td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 bg-slate-100 rounded text-xs font-medium text-slate-700">
                          {c.country}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">{c.vessel_type || "-"}</td>
                      <td className="px-6 py-4 text-center">
                        <div className="flex items-center justify-center gap-1">
                          <button
                            onClick={() => openEmailModal(c)}
                            className="px-2 py-1 text-xs font-medium text-green-600 hover:bg-green-50 rounded transition-colors"
                            title="Send Email"
                          >
                            ✉️
                          </button>
                          <button
                            onClick={() => { setEditCustomer(c); setModalOpen(true); }}
                            className="px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50 rounded transition-colors"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(c)}
                            className="px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-50 rounded transition-colors"
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {customers.length === 0 && (
                    <tr>
                      <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                        No customers found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <div className="mt-3 sm:mt-4 text-xs sm:text-sm text-gray-500">Total: {customers.length} customers</div>

      {/* Customer Form Modal */}
      <CustomerFormModal
        isOpen={modalOpen}
        onClose={() => { setModalOpen(false); setEditCustomer(null); }}
        onSuccess={loadCustomers}
        editData={editCustomer}
      />

      {/* Send Email Modal */}
      <SendEmailModal
        isOpen={emailModalOpen}
        onClose={() => setEmailModalOpen(false)}
        toEmail={emailTarget.email}
        toName={emailTarget.name}
        toCompany={emailTarget.company}
      />
    </div>
  );
}
