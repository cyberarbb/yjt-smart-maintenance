"use client";

import { useEffect, useState } from "react";
import { getInventoryStats, getOrderStats, getLowStock, getOrders } from "@/lib/api";

interface Stats {
  inventory: { total_items: number; low_stock_count: number; total_quantity: number };
  orders: { total: number; pending: number; in_progress: number; completed: number };
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [lowStock, setLowStock] = useState<any[]>([]);
  const [recentOrders, setRecentOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [invStats, ordStats, low, orders] = await Promise.all([
          getInventoryStats(),
          getOrderStats(),
          getLowStock(),
          getOrders("limit=5"),
        ]);
        setStats({ inventory: invStats, orders: ordStats });
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
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Parts"
          value={stats?.inventory.total_items ?? 0}
          icon="📦"
          color="bg-blue-500"
        />
        <StatCard
          title="Low Stock Alerts"
          value={stats?.inventory.low_stock_count ?? 0}
          icon="⚠️"
          color="bg-red-500"
        />
        <StatCard
          title="Pending Orders"
          value={stats?.orders.pending ?? 0}
          icon="⏳"
          color="bg-yellow-500"
        />
        <StatCard
          title="Completed Orders"
          value={stats?.orders.completed ?? 0}
          icon="✅"
          color="bg-green-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Low Stock Alerts */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Low Stock Alerts
          </h2>
          {lowStock.length === 0 ? (
            <p className="text-gray-500 text-sm">No low stock alerts</p>
          ) : (
            <div className="space-y-3">
              {lowStock.slice(0, 5).map((item: any) => (
                <div
                  key={item.id}
                  className="flex justify-between items-center p-3 bg-red-50 rounded-lg"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-800">
                      {item.part_name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {item.brand} | {item.part_number}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold text-red-600">
                      {item.quantity} / {item.min_quantity}
                    </p>
                    <p className="text-xs text-gray-500">{item.warehouse}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Orders */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Recent Service Orders
          </h2>
          {recentOrders.length === 0 ? (
            <p className="text-gray-500 text-sm">No orders yet</p>
          ) : (
            <div className="space-y-3">
              {recentOrders.map((order: any) => (
                <div
                  key={order.id}
                  className="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-800">
                      {order.customer_company}
                    </p>
                    <p className="text-xs text-gray-500">
                      {order.order_type} | {order.turbo_brand} {order.turbo_model}
                    </p>
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

function StatCard({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: number;
  icon: string;
  color: string;
}) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-3xl font-bold text-gray-800 mt-1">{value}</p>
        </div>
        <div
          className={`w-12 h-12 ${color} rounded-lg flex items-center justify-center text-xl`}
        >
          {icon}
        </div>
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
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${
        colors[status] || "bg-gray-100 text-gray-800"
      }`}
    >
      {status}
    </span>
  );
}
