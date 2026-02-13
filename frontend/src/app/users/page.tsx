"use client";

import { useEffect, useState } from "react";
import { useI18n } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";
import DeveloperGuard from "@/components/layout/DeveloperGuard";
import { getUsers, toggleUserAdmin, updateUserRole, updateUserVessel, getVessels } from "@/lib/api";

export default function UsersPage() {
  return (
    <DeveloperGuard>
      <UsersContent />
    </DeveloperGuard>
  );
}

const ROLE_LABELS: Record<string, { label: string; color: string }> = {
  developer: { label: "Developer", color: "bg-red-100 text-red-800" },
  admin: { label: "Admin", color: "bg-blue-100 text-blue-800" },
  captain: { label: "Captain", color: "bg-amber-100 text-amber-800" },
  chief_engineer: { label: "Chief Engineer", color: "bg-green-100 text-green-800" },
  shore_manager: { label: "Shore Manager", color: "bg-purple-100 text-purple-800" },
  engineer: { label: "Engineer", color: "bg-teal-100 text-teal-800" },
  customer: { label: "Customer", color: "bg-gray-100 text-gray-800" },
};

function UsersContent() {
  const { t } = useI18n();
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState<any[]>([]);
  const [vessels, setVessels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const isDeveloper = currentUser?.role === "developer";

  // 비밀번호 확인 모달 상태
  const [pwModal, setPwModal] = useState<{
    open: boolean;
    type: "toggle_admin" | "role_admin" | "role_developer";
    userId: string;
    userName: string;
    currentAdmin: boolean;
  } | null>(null);
  const [adminPw, setAdminPw] = useState("");
  const [pwError, setPwError] = useState("");
  const [pwLoading, setPwLoading] = useState(false);

  async function loadData() {
    try {
      const [usersData, vesselsData] = await Promise.all([getUsers(), getVessels()]);
      setUsers(usersData);
      setVessels(vesselsData);
    } catch (e) {
      console.error("Failed to load data:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  // 역할 드롭다운에 표시할 옵션 (developer는 developer 사용자만 볼 수 있음)
  const getRoleOptions = () => {
    if (isDeveloper) {
      return Object.entries(ROLE_LABELS);
    }
    return Object.entries(ROLE_LABELS).filter(([val]) => val !== "developer");
  };

  async function handleRoleChange(userId: string, role: string) {
    const targetUser = users.find((u) => u.id === userId);
    // developer 역할로 변경 시 비밀번호 확인 모달
    if (role === "developer") {
      setPwModal({
        open: true,
        type: "role_developer",
        userId,
        userName: targetUser?.full_name || "",
        currentAdmin: false,
      });
      setAdminPw("");
      setPwError("");
      return;
    }
    // admin 역할로 변경 시 비밀번호 확인 모달
    if (role === "admin") {
      setPwModal({
        open: true,
        type: "role_admin",
        userId,
        userName: targetUser?.full_name || "",
        currentAdmin: false,
      });
      setAdminPw("");
      setPwError("");
      return;
    }
    try {
      await updateUserRole(userId, role);
      await loadData();
    } catch (e: any) {
      alert(e.message || "Failed to change role");
    }
  }

  async function handleVesselChange(userId: string, vesselId: string) {
    try {
      await updateUserVessel(userId, vesselId || null);
      await loadData();
    } catch (e: any) {
      alert(e.message || "Failed to assign vessel");
    }
  }

  async function handleToggleAdmin(userId: string) {
    const targetUser = users.find((u) => u.id === userId);
    setPwModal({
      open: true,
      type: "toggle_admin",
      userId,
      userName: targetUser?.full_name || "",
      currentAdmin: targetUser?.is_admin || false,
    });
    setAdminPw("");
    setPwError("");
  }

  async function handlePwConfirm() {
    if (!pwModal || !adminPw.trim()) {
      setPwError("Please enter your password");
      return;
    }
    setPwLoading(true);
    setPwError("");
    try {
      if (pwModal.type === "toggle_admin") {
        await toggleUserAdmin(pwModal.userId, adminPw);
      } else if (pwModal.type === "role_admin") {
        await updateUserRole(pwModal.userId, "admin", adminPw);
      } else if (pwModal.type === "role_developer") {
        await updateUserRole(pwModal.userId, "developer", adminPw);
      }
      await loadData();
      setPwModal(null);
      setAdminPw("");
    } catch (e: any) {
      const msg = e.message || "Failed";
      if (msg.includes("password")) {
        setPwError("Incorrect password. Please try again.");
      } else {
        setPwError(msg);
      }
    } finally {
      setPwLoading(false);
    }
  }

  const vesselName = (vesselId: string | null) => {
    if (!vesselId) return "-";
    const v = vessels.find((v: any) => v.id === vesselId);
    return v ? v.name : "-";
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const roleOptions = getRoleOptions();

  return (
    <div>
      <h1 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">
        {t("nav_users") || "User Management"}
      </h1>

      {/* 모바일 카드뷰 */}
      <div className="lg:hidden space-y-3">
        {users.map((u: any) => {
          const roleInfo = ROLE_LABELS[u.role || "customer"] || ROLE_LABELS.customer;
          const isTargetDeveloper = u.role === "developer";
          return (
            <div key={u.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <div className="flex justify-between items-start gap-2 mb-2">
                <div className="min-w-0 flex-1">
                  <h3 className="text-sm font-semibold text-gray-800 truncate">{u.full_name}</h3>
                  <p className="text-xs text-gray-500 mt-0.5">{u.email}</p>
                </div>
                <span className={`px-2 py-0.5 rounded text-[11px] font-medium flex-shrink-0 ${roleInfo.color}`}>
                  {roleInfo.label}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px] text-gray-500 mb-3">
                {u.company && <div><span className="text-gray-400">Company:</span> {u.company}</div>}
                {u.country && <div><span className="text-gray-400">Country:</span> {u.country}</div>}
                <div><span className="text-gray-400">Vessel:</span> {vesselName(u.vessel_id)}</div>
              </div>

              {/* 역할 변경 */}
              <div className="space-y-2 pt-2 border-t border-gray-100">
                <div className="flex gap-2 items-center">
                  <label className="text-[11px] text-gray-500 w-12 flex-shrink-0">Role:</label>
                  <select
                    value={u.role || "customer"}
                    onChange={(e) => handleRoleChange(u.id, e.target.value)}
                    disabled={isTargetDeveloper && !isDeveloper}
                    className="flex-1 px-2 py-1 border border-gray-200 rounded text-xs focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {roleOptions.map(([val, info]) => (
                      <option key={val} value={val}>{info.label}</option>
                    ))}
                  </select>
                </div>
                <div className="flex gap-2 items-center">
                  <label className="text-[11px] text-gray-500 w-12 flex-shrink-0">Vessel:</label>
                  <select
                    value={u.vessel_id || ""}
                    onChange={(e) => handleVesselChange(u.id, e.target.value)}
                    className="flex-1 px-2 py-1 border border-gray-200 rounded text-xs focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="">Not assigned</option>
                    {vessels.map((v: any) => (
                      <option key={v.id} value={v.id}>{v.name}</option>
                    ))}
                  </select>
                </div>
                {/* developer는 admin 토글 대상이 아님 */}
                {!isTargetDeveloper && (
                  <button
                    onClick={() => handleToggleAdmin(u.id)}
                    className={`w-full px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                      u.is_admin
                        ? "bg-red-50 text-red-600 hover:bg-red-100"
                        : "bg-blue-50 text-blue-600 hover:bg-blue-100"
                    }`}
                  >
                    {u.is_admin ? "🔒 Remove Admin" : "🔑 Make Admin"}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* 데스크톱 테이블뷰 */}
      <div className="hidden lg:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="table-scroll-wrapper">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Name</th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Email</th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Company</th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Role</th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Assigned Vessel</th>
                <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase">Admin</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {users.map((u: any) => {
                const roleInfo = ROLE_LABELS[u.role || "customer"] || ROLE_LABELS.customer;
                const isTargetDeveloper = u.role === "developer";
                return (
                  <tr key={u.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{u.full_name}</p>
                        <p className="text-xs text-gray-500">{u.country || ""}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{u.email}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{u.company || "-"}</td>
                    <td className="px-6 py-4">
                      <select
                        value={u.role || "customer"}
                        onChange={(e) => handleRoleChange(u.id, e.target.value)}
                        disabled={isTargetDeveloper && !isDeveloper}
                        className={`px-2 py-1 rounded text-xs font-medium border-0 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${roleInfo.color}`}
                      >
                        {roleOptions.map(([val, info]) => (
                          <option key={val} value={val}>{info.label}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-6 py-4">
                      <select
                        value={u.vessel_id || ""}
                        onChange={(e) => handleVesselChange(u.id, e.target.value)}
                        className="px-2 py-1 border border-gray-200 rounded text-xs focus:ring-1 focus:ring-blue-500"
                      >
                        <option value="">Not assigned</option>
                        {vessels.map((v: any) => (
                          <option key={v.id} value={v.id}>{v.name}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {/* developer는 admin 토글 대상이 아님 */}
                      {isTargetDeveloper ? (
                        <span className="text-xs text-gray-400">-</span>
                      ) : (
                        <button
                          onClick={() => handleToggleAdmin(u.id)}
                          className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                            u.is_admin
                              ? "bg-red-50 text-red-600 hover:bg-red-100"
                              : "bg-blue-50 text-blue-600 hover:bg-blue-100"
                          }`}
                        >
                          {u.is_admin ? "🔒 Remove Admin" : "🔑 Make Admin"}
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-3 sm:mt-4 text-xs sm:text-sm text-gray-500">
        Total: {users.length} users
      </div>

      {/* 비밀번호 확인 모달 */}
      {pwModal?.open && (
        <div className="fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center text-xl">
                🔐
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">Password Required</h3>
                <p className="text-xs text-gray-500">Security verification for privilege change</p>
              </div>
            </div>

            <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 mb-4">
              <p className="text-sm text-amber-800">
                {pwModal.type === "toggle_admin"
                  ? pwModal.currentAdmin
                    ? `Remove admin privileges from "${pwModal.userName}"?`
                    : `Grant admin privileges to "${pwModal.userName}"?`
                  : pwModal.type === "role_developer"
                  ? `Grant developer role to "${pwModal.userName}"?`
                  : `Grant admin role to "${pwModal.userName}"?`}
              </p>
              <p className="text-xs text-amber-600 mt-1">
                Please enter your password to confirm this action.
              </p>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={adminPw}
                onChange={(e) => {
                  setAdminPw(e.target.value);
                  setPwError("");
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handlePwConfirm();
                }}
                placeholder="Enter your password..."
                autoFocus
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {pwError && (
                <p className="mt-1.5 text-xs text-red-600 flex items-center gap-1">
                  <span>⚠️</span> {pwError}
                </p>
              )}
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => {
                  setPwModal(null);
                  setAdminPw("");
                  setPwError("");
                }}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handlePwConfirm}
                disabled={pwLoading || !adminPw.trim()}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                {pwLoading ? "Verifying..." : "Confirm"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
