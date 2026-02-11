"use client";

import { useEffect, useState } from "react";
import { getParts } from "@/lib/api";

export default function InventoryPage() {
  const [parts, setParts] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [brandFilter, setBrandFilter] = useState("");
  const [loading, setLoading] = useState(true);

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

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Parts Inventory</h1>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex flex-wrap gap-4 items-center">
          <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-[300px]">
            <input
              type="text"
              placeholder="Search by name, part number, or model..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors"
            >
              Search
            </button>
          </form>

          <div className="flex gap-2">
            {brands.map((b) => (
              <button
                key={b || "all"}
                onClick={() => setBrandFilter(b)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
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

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading...</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Part Number
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Name
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Brand
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Model
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Category
                </th>
                <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Price (USD)
                </th>
                <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Stock
                </th>
                <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {parts.map((part) => (
                <tr key={part.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm font-mono text-blue-600">
                    {part.part_number}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-800 font-medium">
                    {part.name}
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-slate-100 rounded text-xs font-medium text-slate-700">
                      {part.brand}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {part.turbo_model}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {part.category}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-800 text-right font-medium">
                    ${part.unit_price?.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-right font-bold">
                    <span
                      className={
                        part.inventory?.is_low_stock
                          ? "text-red-600"
                          : "text-gray-800"
                      }
                    >
                      {part.inventory?.quantity ?? 0}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    {part.inventory?.is_low_stock ? (
                      <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                        Low Stock
                      </span>
                    ) : (
                      <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                        In Stock
                      </span>
                    )}
                  </td>
                </tr>
              ))}
              {parts.length === 0 && (
                <tr>
                  <td colSpan={8} className="px-6 py-8 text-center text-gray-500">
                    No parts found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      <div className="mt-4 text-sm text-gray-500">
        Total: {parts.length} parts
      </div>
    </div>
  );
}
