"use client";

import { useEffect, useState } from "react";
import AdminGuard from "@/components/layout/AdminGuard";
import {
  getInventoryByBrand,
  getOrderStatusDist,
  getMonthlyOrders,
  getInventoryValue,
  getLowStockSummary,
  syncToSheets,
} from "@/lib/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  LineChart,
  Line,
} from "recharts";

const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"];

export default function AnalyticsPage() {
  return (
    <AdminGuard>
      <AnalyticsContent />
    </AdminGuard>
  );
}

function AnalyticsContent() {
  const [inventoryByBrand, setInventoryByBrand] = useState<any[]>([]);
  const [orderStatus, setOrderStatus] = useState<any[]>([]);
  const [monthlyOrders, setMonthlyOrders] = useState<any[]>([]);
  const [inventoryValue, setInventoryValue] = useState<any[]>([]);
  const [lowStock, setLowStock] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  useEffect(() => {
    loadAllData();
  }, []);

  async function loadAllData() {
    setLoading(true);
    try {
      const [ib, os, mo, iv, ls] = await Promise.all([
        getInventoryByBrand(),
        getOrderStatusDist(),
        getMonthlyOrders(),
        getInventoryValue(),
        getLowStockSummary(),
      ]);
      setInventoryByBrand(ib);
      setOrderStatus(os);
      setMonthlyOrders(mo);
      setInventoryValue(iv);
      setLowStock(ls);
    } catch (e) {
      console.error("Failed to load analytics:", e);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12 text-gray-500">Loading analytics...</div>
    );
  }

  return (
    <div className="print-content">
      {/* Header with buttons */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">Analytics Dashboard</h1>
        <div className="print-hide flex items-center gap-2 sm:gap-3">
          <button
            onClick={async () => {
              setSyncing(true);
              try {
                const res = await syncToSheets();
                alert(`Google Sheets Sync Complete!\nParts: ${res.parts}, Orders: ${res.orders}, Customers: ${res.customers}, Inquiries: ${res.inquiries}`);
              } catch (e: any) {
                alert(e.message || "Sync failed");
              } finally {
                setSyncing(false);
              }
            }}
            disabled={syncing}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-green-600 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-green-700 transition-colors flex items-center gap-1.5 sm:gap-2 disabled:opacity-50"
          >
            <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            {syncing ? "..." : "Sync"}
          </button>
          <button
            onClick={() => window.print()}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-gray-800 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-gray-900 transition-colors flex items-center gap-1.5 sm:gap-2"
          >
            <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            <span className="hidden sm:inline">Export</span>
          </button>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-4 sm:mb-6">
        {/* Inventory by Brand */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <h3 className="text-sm sm:text-base font-semibold text-gray-800 mb-3 sm:mb-4">Inventory by Brand</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={inventoryByBrand}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="brand" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} width={35} />
              <Tooltip />
              <Bar dataKey="quantity" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Order Status Distribution */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <h3 className="text-sm sm:text-base font-semibold text-gray-800 mb-3 sm:mb-4">Order Status</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={orderStatus}
                cx="50%"
                cy="50%"
                outerRadius={75}
                fill="#8884d8"
                dataKey="count"
                nameKey="status"
                label={((props: any) => `${props.value}`) as any}
              >
                {orderStatus.map((_, idx) => (
                  <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Monthly Orders Trend */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <h3 className="text-sm sm:text-base font-semibold text-gray-800 mb-3 sm:mb-4">Monthly Orders</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={monthlyOrders}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} allowDecimals={false} width={30} />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Inventory Value by Brand */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <h3 className="text-sm sm:text-base font-semibold text-gray-800 mb-3 sm:mb-4">Inventory Value (USD)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={inventoryValue}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="brand" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} width={45} />
              <Tooltip formatter={((value: any) => [`$${Number(value).toLocaleString()}`, "Value"]) as any} />
              <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Low Stock Summary - 모바일: 카드, 데스크톱: 테이블 */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
          <h3 className="text-sm sm:text-base font-semibold text-gray-800">Low Stock Summary</h3>
        </div>
        {lowStock.length === 0 ? (
          <div className="p-6 text-center text-sm text-gray-500">
            All parts are adequately stocked
          </div>
        ) : (
          <>
            {/* 모바일 카드뷰 */}
            <div className="lg:hidden p-3 space-y-2">
              {lowStock.map((item, idx) => (
                <div key={idx} className="p-3 bg-red-50 rounded-lg">
                  <div className="flex justify-between items-start mb-1">
                    <div className="min-w-0">
                      <p className="text-xs font-medium text-gray-800 truncate">{item.name}</p>
                      <p className="text-[11px] font-mono text-blue-600">{item.part_number}</p>
                    </div>
                    <span className="px-2 py-0.5 bg-red-100 text-red-700 rounded-full text-[11px] font-medium flex-shrink-0">
                      -{item.min_quantity - item.quantity}
                    </span>
                  </div>
                  <div className="flex gap-3 text-[11px] text-gray-500">
                    <span>{item.brand}</span>
                    <span>Stock: <strong className="text-red-600">{item.quantity}</strong>/{item.min_quantity}</span>
                  </div>
                </div>
              ))}
            </div>
            {/* 데스크톱 테이블 */}
            <div className="hidden lg:block table-scroll-wrapper">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Part Number</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Name</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Brand</th>
                    <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Current</th>
                    <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Minimum</th>
                    <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Deficit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {lowStock.map((item, idx) => (
                    <tr key={idx} className="hover:bg-red-50 transition-colors">
                      <td className="px-6 py-3 text-sm font-mono text-blue-600">{item.part_number}</td>
                      <td className="px-6 py-3 text-sm text-gray-800 font-medium">{item.name}</td>
                      <td className="px-6 py-3">
                        <span className="px-2 py-1 bg-slate-100 rounded text-xs font-medium text-slate-700">{item.brand}</span>
                      </td>
                      <td className="px-6 py-3 text-sm text-right font-bold text-red-600">{item.quantity}</td>
                      <td className="px-6 py-3 text-sm text-right text-gray-600">{item.min_quantity}</td>
                      <td className="px-6 py-3 text-center">
                        <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                          -{item.min_quantity - item.quantity}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
