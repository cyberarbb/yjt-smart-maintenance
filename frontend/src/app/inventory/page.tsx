"use client";

import { useEffect, useState } from "react";
import { getParts, deletePart } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import PartFormModal from "@/components/crud/PartFormModal";
import InventoryAdjustModal from "@/components/crud/InventoryAdjustModal";

export default function InventoryPage() {
  const { user } = useAuth();
  const isAdmin = user?.is_admin || user?.role === "developer";

  const [parts, setParts] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [brandFilter, setBrandFilter] = useState("");
  const [loading, setLoading] = useState(true);

  // Modal state
  const [partModalOpen, setPartModalOpen] = useState(false);
  const [editPart, setEditPart] = useState<any>(null);
  const [adjustModal, setAdjustModal] = useState<{ open: boolean; part: any }>({ open: false, part: null });

  const brands = ["", "MAN", "MHI", "KBB", "ABB", "Napier"];

  useEffect(() => {
    loadParts();
  }, [brandFilter]);

  async function loadParts() {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (brandFilter) params.set("brand", brandFilter);
      if (search) params.set("search", search);
      const data = await getParts(params.toString());
      setParts(data);
    } catch (e) {
      console.error("Failed to load parts:", e);
    } finally {
      setLoading(false);
    }
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    loadParts();
  }

  async function handleDelete(part: any) {
    if (!confirm(`Delete "${part.name}"? This cannot be undone.`)) return;
    try {
      await deletePart(part.id);
      loadParts();
    } catch (err: any) {
      alert(err.message || "Failed to delete");
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">Parts Inventory</h1>
        {isAdmin && (
          <button
            onClick={() => { setEditPart(null); setPartModalOpen(true); }}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-600 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-1 sm:gap-2"
          >
            <span className="text-base sm:text-lg leading-none">+</span> Add Part
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-4 mb-4 sm:mb-6">
        <div className="space-y-3 sm:space-y-0 sm:flex sm:flex-wrap sm:gap-4 sm:items-center">
          <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-0">
            <input
              type="text"
              placeholder="Search parts..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 min-w-0 px-3 sm:px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="px-3 sm:px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors flex-shrink-0"
            >
              Search
            </button>
          </form>

          <div className="flex gap-1.5 sm:gap-2 flex-wrap">
            {brands.map((b) => (
              <button
                key={b || "all"}
                onClick={() => setBrandFilter(b)}
                className={`px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                  brandFilter === b
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                {b || "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 모바일: 카드뷰 / 데스크톱: 테이블 */}
      {loading ? (
        <div className="p-8 text-center text-gray-500">Loading...</div>
      ) : (
        <>
          {/* 모바일 카드뷰 */}
          <div className="lg:hidden space-y-3">
            {parts.map((part) => (
              <div key={part.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-800 truncate">{part.name}</p>
                    <p className="text-xs font-mono text-blue-600">{part.part_number}</p>
                  </div>
                  {part.inventory?.is_low_stock ? (
                    <span className="px-2 py-0.5 bg-red-100 text-red-700 rounded-full text-xs font-medium flex-shrink-0">Low</span>
                  ) : (
                    <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded-full text-xs font-medium flex-shrink-0">OK</span>
                  )}
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs text-gray-500 mb-3">
                  <div><span className="text-gray-400">Brand:</span> <span className="font-medium text-gray-700">{part.brand}</span></div>
                  <div><span className="text-gray-400">Model:</span> <span className="font-medium text-gray-700">{part.turbo_model}</span></div>
                  <div><span className="text-gray-400">Price:</span> <span className="font-medium text-gray-700">${part.unit_price?.toLocaleString()}</span></div>
                  <div><span className="text-gray-400">Stock:</span> <span className={`font-bold ${part.inventory?.is_low_stock ? "text-red-600" : "text-gray-800"}`}>{part.inventory?.quantity ?? 0}</span></div>
                </div>
                {isAdmin && (
                  <div className="flex gap-2 pt-2 border-t border-gray-100">
                    <button
                      onClick={() => { setEditPart(part); setPartModalOpen(true); }}
                      className="flex-1 px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors text-center"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => setAdjustModal({ open: true, part })}
                      className="flex-1 px-3 py-1.5 text-xs font-medium text-emerald-600 bg-emerald-50 hover:bg-emerald-100 rounded-lg transition-colors text-center"
                    >
                      Stock
                    </button>
                    <button
                      onClick={() => handleDelete(part)}
                      className="px-3 py-1.5 text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                    >
                      Del
                    </button>
                  </div>
                )}
              </div>
            ))}
            {parts.length === 0 && (
              <div className="text-center py-8 text-gray-500">No parts found</div>
            )}
          </div>

          {/* 데스크톱 테이블 */}
          <div className="hidden lg:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="table-scroll-wrapper">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Part Number</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Name</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Brand</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Model</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Category</th>
                    <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Price (USD)</th>
                    <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Stock</th>
                    <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Status</th>
                    {isAdmin && (
                      <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Actions</th>
                    )}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {parts.map((part) => (
                    <tr key={part.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-mono text-blue-600">{part.part_number}</td>
                      <td className="px-6 py-4 text-sm text-gray-800 font-medium">{part.name}</td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 bg-slate-100 rounded text-xs font-medium text-slate-700">{part.brand}</span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">{part.turbo_model}</td>
                      <td className="px-6 py-4 text-sm text-gray-600">{part.category}</td>
                      <td className="px-6 py-4 text-sm text-gray-800 text-right font-medium">
                        ${part.unit_price?.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-right font-bold">
                        <span className={part.inventory?.is_low_stock ? "text-red-600" : "text-gray-800"}>
                          {part.inventory?.quantity ?? 0}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        {part.inventory?.is_low_stock ? (
                          <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">Low Stock</span>
                        ) : (
                          <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">In Stock</span>
                        )}
                      </td>
                      {isAdmin && (
                        <td className="px-6 py-4 text-center">
                          <div className="flex items-center justify-center gap-1">
                            <button
                              onClick={() => { setEditPart(part); setPartModalOpen(true); }}
                              className="px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50 rounded transition-colors"
                              title="Edit Part"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => setAdjustModal({ open: true, part })}
                              className="px-2 py-1 text-xs font-medium text-emerald-600 hover:bg-emerald-50 rounded transition-colors"
                              title="Adjust Stock"
                            >
                              Stock
                            </button>
                            <button
                              onClick={() => handleDelete(part)}
                              className="px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-50 rounded transition-colors"
                              title="Delete Part"
                            >
                              Del
                            </button>
                          </div>
                        </td>
                      )}
                    </tr>
                  ))}
                  {parts.length === 0 && (
                    <tr>
                      <td colSpan={isAdmin ? 9 : 8} className="px-6 py-8 text-center text-gray-500">
                        No parts found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <div className="mt-3 sm:mt-4 text-xs sm:text-sm text-gray-500">Total: {parts.length} parts</div>

      {/* Modals */}
      <PartFormModal
        isOpen={partModalOpen}
        onClose={() => { setPartModalOpen(false); setEditPart(null); }}
        onSuccess={loadParts}
        editData={editPart}
      />

      {adjustModal.part && (
        <InventoryAdjustModal
          isOpen={adjustModal.open}
          onClose={() => setAdjustModal({ open: false, part: null })}
          onSuccess={loadParts}
          inventoryId={adjustModal.part.inventory?.id || ""}
          partName={adjustModal.part.name}
          currentQty={adjustModal.part.inventory?.quantity ?? 0}
        />
      )}
    </div>
  );
}
