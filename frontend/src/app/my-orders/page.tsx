"use client";

import { useEffect, useState } from "react";
import { useI18n } from "@/lib/i18n";
import { getMyOrders } from "@/lib/api";

export default function MyOrdersPage() {
  const { t } = useI18n();
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getMyOrders();
        setOrders(data);
      } catch (e) {
        console.error("Failed to load orders:", e);
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
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        {t("nav_my_orders") || "My Orders"}
      </h1>

      {orders.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <p className="text-4xl mb-4">📋</p>
          <p className="text-gray-500">No orders found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {orders.map((order: any) => (
            <div key={order.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex justify-between items-start mb-3">
                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                  {order.order_type}
                </span>
                <StatusBadge status={order.status} />
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <span>🔧</span>
                  <span className="font-medium">{order.turbo_brand} {order.turbo_model}</span>
                </div>
                {order.vessel_name && (
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <span>🚢</span>
                    <span>{order.vessel_name}</span>
                  </div>
                )}
                {order.description && (
                  <p className="text-xs text-gray-500 mt-2">{order.description}</p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  {new Date(order.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
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
