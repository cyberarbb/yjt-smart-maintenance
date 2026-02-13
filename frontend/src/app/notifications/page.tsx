"use client";

import { useEffect, useState } from "react";
import { getNotifications, markNotificationRead, markAllNotificationsRead } from "@/lib/api";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState("");

  const types = ["", "info", "warning", "order", "inquiry", "success"];
  const typeLabels: Record<string, string> = {
    "": "All",
    info: "Info",
    warning: "Warning",
    order: "Order",
    inquiry: "Inquiry",
    success: "Success",
  };

  useEffect(() => {
    loadNotifications();
  }, []);

  async function loadNotifications() {
    setLoading(true);
    try {
      const data = await getNotifications();
      setNotifications(data);
    } catch (e) {
      console.error("Failed to load notifications:", e);
    } finally {
      setLoading(false);
    }
  }

  async function handleMarkRead(id: string) {
    try {
      await markNotificationRead(id);
      setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
    } catch {}
  }

  async function handleMarkAllRead() {
    try {
      await markAllNotificationsRead();
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
    } catch {}
  }

  const filtered = typeFilter
    ? notifications.filter(n => n.type === typeFilter)
    : notifications;

  const typeColors: Record<string, string> = {
    info: "bg-blue-100 text-blue-700",
    warning: "bg-amber-100 text-amber-700",
    success: "bg-green-100 text-green-700",
    order: "bg-indigo-100 text-indigo-700",
    inquiry: "bg-purple-100 text-purple-700",
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Notifications</h1>
        <button
          onClick={handleMarkAllRead}
          className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          Mark All as Read
        </button>
      </div>

      {/* Type Filters */}
      <div className="flex gap-2 mb-6">
        {types.map((t) => (
          <button
            key={t || "all"}
            onClick={() => setTypeFilter(t)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              typeFilter === t
                ? "bg-blue-600 text-white"
                : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
            }`}
          >
            {typeLabels[t]}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading...</div>
      ) : (
        <div className="space-y-3">
          {filtered.map((notif) => (
            <div
              key={notif.id}
              className={`bg-white rounded-xl shadow-sm border border-gray-200 p-5 transition-colors ${
                !notif.is_read ? "border-l-4 border-l-blue-500" : ""
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    typeColors[notif.type] || typeColors.info
                  }`}>
                    {notif.type}
                  </span>
                  <div className="flex-1">
                    <h3 className="text-sm font-semibold text-gray-800">{notif.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{notif.message}</p>
                    <p className="text-xs text-gray-400 mt-2">
                      {new Date(notif.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  {!notif.is_read && (
                    <button
                      onClick={() => handleMarkRead(notif.id)}
                      className="px-3 py-1 text-xs font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
                    >
                      Mark Read
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No notifications found
            </div>
          )}
        </div>
      )}
    </div>
  );
}
