"use client";

import { useEffect, useState } from "react";
import { getOrders } from "@/lib/api";

export default function OrdersPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(true);

  const statuses = ["", "Pending", "In Progress", "Completed", "Cancelled"];

  useEffect(() => {
    loadOrders();
  }, [statusFilter]);

  async function loadOrders() {
    setLoading(true);
    try {
      const params = statusFilter ? `status=${encodeURIComponent(statusFilter)}` : "";
      const data = await getOrders(params);
      setOrders(data);
    } catch (e) {
      console.error("Failed to load orders:", e);
    } finally {
      setLoading(false);
    }
  }

  const statusColors: Record<string, string> = {
    Pending: "bg-yellow-100 text-yellow-800",
    "In Progress": "bg-blue-100 text-blue-800",
    Completed: "bg-green-100 text-green-800",
    Cancelled: "bg-gray-100 text-gray-800",
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Service Orders</h1>

      {/* Filters */}
      <div className="flex gap-2 mb-6">
        {statuses.map((s) => (
          <button
            key={s || "all"}
            onClick={() => setStatusFilter(s)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              statusFilter === s
                ? "bg-blue-600 text-white"
                : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
            }`}
          >
            {s || "All"}
          </button>
        ))}
      </div>

      {/* Orders List */}
      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading...</div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-800">
                      {order.customer_company}
                    </h3>
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        statusColors[order.status] || "bg-gray-100"
                      }`}
                    >
                      {order.status}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                    <div>
                      <span className="text-gray-400">Type:</span>{" "}
                      <span className="font-medium">{order.order_type}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Turbo:</span>{" "}
                      <span className="font-medium">
                        {order.turbo_brand} {order.turbo_model}
                      </span>
                    </div>
                    {order.vessel_name && (
                      <div>
                        <span className="text-gray-400">Vessel:</span>{" "}
                        <span className="font-medium">{order.vessel_name}</span>
                      </div>
                    )}
                    <div>
                      <span className="text-gray-400">Contact:</span>{" "}
                      <span className="font-medium">{order.customer_name}</span>
                    </div>
                  </div>
                  {order.description && (
                    <p className="mt-3 text-sm text-gray-500">
                      {order.description}
                    </p>
                  )}
                </div>
                <div className="text-right text-xs text-gray-400 ml-4">
                  {new Date(order.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
          {orders.length === 0 && (
            <div className="text-center py-8 text-gray-500">No orders found</div>
          )}
        </div>
      )}
    </div>
  );
}
