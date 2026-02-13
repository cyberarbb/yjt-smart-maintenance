"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { getMyOrders, getMyInquiries } from "@/lib/api";
import Link from "next/link";

export default function CustomerDashboard() {
  const { user } = useAuth();
  const { t } = useI18n();
  const router = useRouter();
  const [myOrders, setMyOrders] = useState<any[]>([]);
  const [myInquiries, setMyInquiries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [orders, inquiries] = await Promise.all([
          getMyOrders(),
          getMyInquiries(),
        ]);
        setMyOrders(orders);
        setMyInquiries(inquiries);
      } catch (e) {
        console.error("Failed to load customer dashboard:", e);
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
      <h1 className="text-xl sm:text-2xl font-bold text-gray-800 mb-1 sm:mb-2">
        {t("nav_dashboard")}
      </h1>
      <p className="text-sm sm:text-base text-gray-500 mb-4 sm:mb-6">
        {user?.full_name}{t("welcome_user")?.includes("{name}") ? "" : ", "}{t("welcome_user")?.replace("{name}", "") || "Welcome!"}
      </p>

      {/* Quick Actions */}
      <div className="grid grid-cols-3 gap-2 sm:gap-4 mb-6 sm:mb-8">
        <Link href="/chatbot" className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl p-3 sm:p-6 hover:shadow-lg transition-shadow active:scale-[0.98]">
          <span className="text-xl sm:text-3xl mb-1 sm:mb-2 block">🤖</span>
          <h3 className="text-xs sm:text-base font-semibold">{t("nav_chatbot")}</h3>
          <p className="text-[10px] sm:text-sm text-blue-100 mt-0.5 sm:mt-1 hidden sm:block">Ask about parts, overhaul, pricing</p>
        </Link>
        <Link href="/my-orders" className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl p-3 sm:p-6 hover:shadow-lg transition-shadow active:scale-[0.98]">
          <span className="text-xl sm:text-3xl mb-1 sm:mb-2 block">📋</span>
          <h3 className="text-xs sm:text-base font-semibold">{t("nav_my_orders") || "My Orders"}</h3>
          <p className="text-[10px] sm:text-sm text-green-100 mt-0.5 sm:mt-1 hidden sm:block">Track your service orders</p>
        </Link>
        <Link href="/inquiries" className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-xl p-3 sm:p-6 hover:shadow-lg transition-shadow active:scale-[0.98]">
          <span className="text-xl sm:text-3xl mb-1 sm:mb-2 block">📨</span>
          <h3 className="text-xs sm:text-base font-semibold">{t("nav_inquiries")}</h3>
          <p className="text-[10px] sm:text-sm text-purple-100 mt-0.5 sm:mt-1 hidden sm:block">Submit or track inquiries</p>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* My Recent Orders */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3 sm:mb-4">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800">
              {t("nav_my_orders") || "My Orders"} ({myOrders.length})
            </h2>
            <button
              onClick={() => router.push("/my-orders")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium transition-colors"
            >
              View All →
            </button>
          </div>
          {myOrders.length === 0 ? (
            <p className="text-gray-500 text-sm">No orders yet</p>
          ) : (
            <div className="space-y-2 sm:space-y-3">
              {myOrders.slice(0, 5).map((order: any) => (
                <div
                  key={order.id}
                  onClick={() => router.push("/my-orders")}
                  className="flex justify-between items-center p-2.5 sm:p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                >
                  <div className="min-w-0 flex-1 mr-3">
                    <p className="text-xs sm:text-sm font-medium text-gray-800 truncate">{order.order_type}</p>
                    <p className="text-[11px] sm:text-xs text-gray-500 truncate">{order.turbo_brand} {order.turbo_model} {order.vessel_name ? `| ${order.vessel_name}` : ""}</p>
                  </div>
                  <StatusBadge status={order.status} />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* My Recent Inquiries */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-3 sm:mb-4">
            <h2 className="text-sm sm:text-lg font-semibold text-gray-800">
              {t("nav_inquiries")} ({myInquiries.length})
            </h2>
            <button
              onClick={() => router.push("/inquiries")}
              className="text-[11px] sm:text-xs text-blue-600 hover:text-blue-800 font-medium transition-colors"
            >
              View All →
            </button>
          </div>
          {myInquiries.length === 0 ? (
            <p className="text-gray-500 text-sm">No inquiries yet</p>
          ) : (
            <div className="space-y-2 sm:space-y-3">
              {myInquiries.slice(0, 5).map((inq: any) => (
                <div
                  key={inq.id}
                  onClick={() => router.push("/inquiries")}
                  className="p-2.5 sm:p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                >
                  <div className="flex justify-between items-start gap-2">
                    <p className="text-xs sm:text-sm font-medium text-gray-800 truncate min-w-0 flex-1">{inq.subject}</p>
                    <span className={`px-2 py-0.5 rounded-full text-[11px] sm:text-xs font-medium flex-shrink-0 ${inq.is_resolved ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}`}>
                      {inq.is_resolved ? "Resolved" : "Pending"}
                    </span>
                  </div>
                  {inq.response && (
                    <p className="text-[11px] sm:text-xs text-blue-600 mt-1 truncate">Reply: {inq.response}</p>
                  )}
                </div>
              ))}
            </div>
          )}
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
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status] || "bg-gray-100 text-gray-800"}`}>
      {status}
    </span>
  );
}
