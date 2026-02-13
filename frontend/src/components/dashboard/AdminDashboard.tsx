"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useI18n } from "@/lib/i18n";
import {
  getInventoryStats, getOrderStats, getLowStock, getOrders,
  getVessels, getOverdueWorkOrders,
} from "@/lib/api";

interface Stats {
  inventory: { total_items: number; low_stock_count: number; total_quantity: number };
  orders: { total: number; pending: number; in_progress: number; completed: number };
  vesselCount: number;
  pmsOverdue: number;
}

export default function AdminDashboard() {
  const { t } = useI18n();
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [lowStock, setLowStock] = useState<any[]>([]);
  const [recentOrders, setRecentOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [invStats, ordStats, low, orders, vessels, overdueWOs] = await Promise.all([
          getInventoryStats(),
          getOrderStats(),
          getLowStock(),
          getOrders("limit=5"),
          getVessels().catch(() => []),
          getOverdueWorkOrders().catch(() => []),
        ]);
        setStats({
          inventory: invStats,
          orders: ordStats,
          vesselCount: vessels.length,
          pmsOverdue: overdueWOs.length,
        });
        setLowStock(low);
        setRecentOrders(orders);
      } catch (e) {
        console.error("Failed to load dashboard:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">{t("nav_dashboard")}</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 mb-6 sm:mb-8">
        <StatCard title={t("total_parts")} value={stats?.inventory.total_items ?? 0} icon="📦" color="bg-blue-500" onClick={() => router.push("/inventory")} />
        <StatCard title={t("low_stock")} value={stats?.inventory.low_stock_count ?? 0} icon="⚠️" color="bg-red-500" onClick={() => router.push("/inventory")} />
        <StatCard title={t("pending_orders") || "Pending Orders"} value={stats?.orders.pending ?? 0} icon="⏳" color="bg-yellow-500" onClick={() => router.push("/orders")} />
        <StatCard title="Vessels" value={stats?.vesselCount ?? 0} icon="🚢" color="bg-cyan-500" onClick={() => router.push("/vessels")} />
        <StatCard title="PMS Overdue" value={stats?.pmsOverdue ?? 0} icon="🔴" color="bg-rose-500" onClick={() => router.push("/work-orders")} />
        <StatCard title={t("completed_orders") || "Completed"} value={stats?.orders.completed ?? 0} icon="✅" color="bg-green-500" onClick={() => router.push("/orders")} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* Low Stock Alerts */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3 sm:mb-4">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800">{t("low_stock")}</h2>
            <button
              onClick={() => router.push("/inventory")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium transition-colors"
            >
              View All →
            </button>
          </div>
          {lowStock.length === 0 ? (
            <p className="text-gray-500 text-sm">No low stock alerts</p>
          ) : (
            <div className="space-y-2 sm:space-y-3">
              {lowStock.slice(0, 5).map((item: any) => (
                <div
                  key={item.id}
                  onClick={() => router.push("/inventory")}
                  className="flex justify-between items-center p-2.5 sm:p-3 bg-red-50 rounded-lg cursor-pointer hover:bg-red-100 transition-colors"
                >
                  <div className="min-w-0 flex-1 mr-3">
                    <p className="text-xs sm:text-sm font-medium text-gray-800 truncate">{item.part_name}</p>
                    <p className="text-[11px] sm:text-xs text-gray-500 truncate">{item.brand} | {item.part_number}</p>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-xs sm:text-sm font-bold text-red-600">{item.quantity} / {item.min_quantity}</p>
                    <p className="text-[11px] sm:text-xs text-gray-500">{item.warehouse}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Orders */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3 sm:mb-4">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800">{t("recent_orders") || "Recent Orders"}</h2>
            <button
              onClick={() => router.push("/orders")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium transition-colors"
            >
              View All →
            </button>
          </div>
          {recentOrders.length === 0 ? (
            <p className="text-gray-500 text-sm">No orders yet</p>
          ) : (
            <div className="space-y-2 sm:space-y-3">
              {recentOrders.map((order: any) => (
                <div
                  key={order.id}
                  onClick={() => router.push("/orders")}
                  className="flex justify-between items-center p-2.5 sm:p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                >
                  <div className="min-w-0 flex-1 mr-3">
                    <p className="text-xs sm:text-sm font-medium text-gray-800 truncate">{order.customer_company}</p>
                    <p className="text-[11px] sm:text-xs text-gray-500 truncate">{order.order_type} | {order.turbo_brand} {order.turbo_model}</p>
                  </div>
                  <StatusBadge status={order.status} />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color, onClick }: { title: string; value: number; icon: string; color: string; onClick?: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-3 sm:p-6 cursor-pointer hover:shadow-md hover:border-gray-300 transition-all active:scale-[0.98]"
    >
      <div className="flex items-center justify-between">
        <div className="min-w-0">
          <p className="text-[11px] sm:text-sm text-gray-500 truncate">{title}</p>
          <p className="text-xl sm:text-3xl font-bold text-gray-800 mt-0.5 sm:mt-1">{value}</p>
        </div>
        <div className={`w-8 h-8 sm:w-12 sm:h-12 ${color} rounded-lg flex items-center justify-center text-sm sm:text-xl flex-shrink-0`}>{icon}</div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    Pending: "bg-yellow-100 text-yellow-800",
    "In Progress": "bg-blue-100 text-blue-800",
    Completed: "bg-green-100 text-green-800",
    Cancelled: "bg-gray-100 text-gray-800",
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status] || "bg-gray-100 text-gray-800"}`}>
      {status}
    </span>
  );
}
