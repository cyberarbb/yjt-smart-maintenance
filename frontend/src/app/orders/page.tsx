"use client";

import { useEffect, useState } from "react";
import { getOrders } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import OrderFormModal from "@/components/crud/OrderFormModal";

export default function OrdersPage() {
  const { user } = useAuth();
  const isAdmin = user?.is_admin || user?.role === "developer";

  const [orders, setOrders] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(true);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editOrder, setEditOrder] = useState<any>(null);

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
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800">Service Orders</h1>
        {isAdmin && (
          <button
            onClick={() => { setEditOrder(null); setModalOpen(true); }}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-600 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-1 sm:gap-2"
          >
            <span className="text-base sm:text-lg leading-none">+</span> <span className="hidden sm:inline">Create</span> Order
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="flex gap-1.5 sm:gap-2 mb-4 sm:mb-6 flex-wrap">
        {statuses.map((s) => (
          <button
            key={s || "all"}
            onClick={() => setStatusFilter(s)}
            className={`px-2.5 py-1.5 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
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
        <div className="space-y-3 sm:space-y-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2 mb-2">
                    <h3 className="text-sm sm:text-lg font-semibold text-gray-800 truncate">
                      {order.customer_company}
                    </h3>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[11px] sm:text-xs font-medium flex-shrink-0 ${
                        statusColors[order.status] || "bg-gray-100"
                      }`}
                    >
                      {order.status}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 sm:gap-4 text-xs sm:text-sm text-gray-600">
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
                    <p className="mt-2 sm:mt-3 text-xs sm:text-sm text-gray-500 line-clamp-2">{order.description}</p>
                  )}
                </div>
                <div className="flex flex-col items-end gap-2 flex-shrink-0">
                  <div className="text-[11px] sm:text-xs text-gray-400">
                    {new Date(order.created_at).toLocaleDateString()}
                  </div>
                  {isAdmin && (
                    <button
                      onClick={() => { setEditOrder(order); setModalOpen(true); }}
                      className="px-2.5 py-1 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                    >
                      Edit
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
          {orders.length === 0 && (
            <div className="text-center py-8 text-gray-500">No orders found</div>
          )}
        </div>
      )}

      {/* Modal */}
      <OrderFormModal
        isOpen={modalOpen}
        onClose={() => { setModalOpen(false); setEditOrder(null); }}
        onSuccess={loadOrders}
        editData={editOrder}
      />
    </div>
  );
}
