"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/layout/Sidebar";
import { getActivityLogs, getOnlineUsers } from "@/lib/api";

export default function ActivityLogPage() {
  const { user, loading: authLoading } = useAuth();
  const { t } = useI18n();
  const router = useRouter();

  const [logs, setLogs] = useState<any[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all"); // all, login, logout, login_failed
  const [page, setPage] = useState(0);
  const [searchEmail, setSearchEmail] = useState("");
  const LIMIT = 50;

  // 개발자 체크
  const isDeveloper = user?.role === "developer";
  useEffect(() => {
    if (!authLoading && (!user || !isDeveloper)) {
      router.push("/");
    }
  }, [user, authLoading, router, isDeveloper]);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const action = filter === "all" ? undefined : filter;
      const [logsData, onlineData] = await Promise.all([
        getActivityLogs(action, LIMIT, page * LIMIT),
        getOnlineUsers(),
      ]);
      setLogs(logsData.logs);
      setTotal(logsData.total);
      setOnlineUsers(onlineData);
    } catch (err) {
      console.error("Failed to load activity logs:", err);
    } finally {
      setLoading(false);
    }
  }, [filter, page]);

  useEffect(() => {
    if (isDeveloper) {
      fetchData();
    }
  }, [user, fetchData]);

  // 자동 새로고침 (30초)
  useEffect(() => {
    if (!isDeveloper) return;
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [user, fetchData]);

  const totalPages = Math.ceil(total / LIMIT);

  const getActionBadge = (action: string) => {
    switch (action) {
      case "login":
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-700">
            🟢 Login
          </span>
        );
      case "logout":
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700">
            🔴 Logout
          </span>
        );
      case "login_failed":
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-700">
            ⚠️ Failed
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-600">
            {action}
          </span>
        );
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return "-";
    const d = new Date(dateStr);
    return d.toLocaleString("ko-KR", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const filteredLogs = searchEmail
    ? logs.filter(
        (log) =>
          log.user_email.toLowerCase().includes(searchEmail.toLowerCase()) ||
          log.user_name.toLowerCase().includes(searchEmail.toLowerCase())
      )
    : logs;

  if (authLoading) return null;
  if (!isDeveloper) return null;

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 lg:ml-64 p-4 lg:p-8">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">📋 Activity Log</h1>
          <p className="text-sm text-gray-500 mt-1">
            User login/logout activity monitoring (Auto-refresh: 30s)
          </p>
        </div>

        {/* Online Users Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
          <h2 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            Currently Online ({onlineUsers.length})
          </h2>
          {onlineUsers.length === 0 ? (
            <p className="text-sm text-gray-400">No users currently online</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {onlineUsers.map((u) => (
                <div
                  key={u.user_id}
                  className="flex items-center gap-2 bg-green-50 border border-green-200 rounded-lg px-3 py-2"
                >
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <div>
                    <p className="text-sm font-medium text-gray-800">{u.user_name}</p>
                    <p className="text-xs text-gray-500">{u.user_email}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Stats Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <p className="text-xs text-gray-500">Total Records</p>
            <p className="text-2xl font-bold text-gray-900">{total}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <p className="text-xs text-gray-500">Online Users</p>
            <p className="text-2xl font-bold text-green-600">{onlineUsers.length}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <p className="text-xs text-gray-500">Current Page</p>
            <p className="text-2xl font-bold text-blue-600">
              {totalPages > 0 ? page + 1 : 0} / {totalPages}
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <p className="text-xs text-gray-500">Showing</p>
            <p className="text-2xl font-bold text-gray-700">{filteredLogs.length}</p>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex flex-col sm:flex-row gap-3">
            {/* Action Filter */}
            <div className="flex gap-2">
              {[
                { value: "all", label: "All" },
                { value: "login", label: "🟢 Login" },
                { value: "logout", label: "🔴 Logout" },
                { value: "login_failed", label: "⚠️ Failed" },
              ].map((f) => (
                <button
                  key={f.value}
                  onClick={() => {
                    setFilter(f.value);
                    setPage(0);
                  }}
                  className={`px-3 py-1.5 text-xs rounded-lg font-medium transition-colors ${
                    filter === f.value
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
            {/* Search */}
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search by email or name..."
                value={searchEmail}
                onChange={(e) => setSearchEmail(e.target.value)}
                className="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            {/* Refresh */}
            <button
              onClick={fetchData}
              className="px-3 py-1.5 text-xs bg-gray-100 text-gray-600 hover:bg-gray-200 rounded-lg font-medium transition-colors"
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Logs Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-3"></div>
              <p className="text-sm text-gray-500">Loading activity logs...</p>
            </div>
          ) : filteredLogs.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-4xl mb-3">📋</p>
              <p className="text-sm text-gray-500">No activity logs found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Time</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">User</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Action</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600 hidden md:table-cell">
                      IP Address
                    </th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600 hidden lg:table-cell">
                      Details
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filteredLogs.map((log) => (
                    <tr
                      key={log.id}
                      className="hover:bg-gray-50 transition-colors"
                    >
                      <td className="px-4 py-3 text-xs text-gray-500 whitespace-nowrap">
                        {formatDate(log.created_at)}
                      </td>
                      <td className="px-4 py-3">
                        <p className="font-medium text-gray-800 text-sm">{log.user_name}</p>
                        <p className="text-xs text-gray-400">{log.user_email}</p>
                      </td>
                      <td className="px-4 py-3">{getActionBadge(log.action)}</td>
                      <td className="px-4 py-3 text-xs text-gray-500 hidden md:table-cell">
                        {log.ip_address || "-"}
                      </td>
                      <td className="px-4 py-3 text-xs text-gray-500 hidden lg:table-cell max-w-xs truncate">
                        {log.details || "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 bg-gray-50">
              <button
                onClick={() => setPage(Math.max(0, page - 1))}
                disabled={page === 0}
                className="px-3 py-1.5 text-xs bg-white border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                ← Previous
              </button>
              <span className="text-xs text-gray-500">
                Page {page + 1} of {totalPages} ({total} records)
              </span>
              <button
                onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
                disabled={page >= totalPages - 1}
                className="px-3 py-1.5 text-xs bg-white border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Next →
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
