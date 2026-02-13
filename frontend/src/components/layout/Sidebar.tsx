"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useI18n } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";
import { useState, useEffect } from "react";

export default function Sidebar() {
  const pathname = usePathname();
  const { t } = useI18n();
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);


  // 라우트 변경 시 사이드바 닫기
  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  // 사이드바 열릴 때 body 스크롤 막기
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  const userRole = user?.role || (user?.is_admin ? "admin" : "customer");

  // 공통 메뉴 (모든 인증 사용자)
  const commonItems = [
    { href: "/", label: t("nav_dashboard"), icon: "📊" },
    { href: "/chatbot", label: t("nav_chatbot"), icon: "🤖" },
    { href: "/inquiries", label: t("nav_inquiries"), icon: "📨" },
  ];

  // 선박 관리 섹션 (관리자 + 선박 관련 역할)
  const vesselItems = [
    { href: "/vessels", label: "Vessels", icon: "🚢" },
    { href: "/running-hours", label: "Running Hours", icon: "⏱️" },
    { href: "/pms", label: "PMS", icon: "🔧" },
    { href: "/work-orders", label: "Work Orders", icon: "📋" },
  ];

  // 관리자 전용 메뉴
  const adminItems = [
    { href: "/inventory", label: t("nav_inventory"), icon: "📦" },
    { href: "/orders", label: t("nav_orders"), icon: "🔧" },
    { href: "/customers", label: t("nav_customers") || "Customers", icon: "👥" },
    { href: "/analytics", label: t("nav_analytics") || "Analytics", icon: "📈" },
  ];

  // 선장/기관장 메뉴 (본선)
  const vesselCrewItems = [
    { href: "/my-orders", label: t("nav_my_orders") || "My Orders", icon: "📋" },
  ];

  // 고객 전용 메뉴
  const customerItems = [
    { href: "/my-orders", label: t("nav_my_orders") || "My Orders", icon: "📋" },
  ];

  // 개발자 전용 메뉴
  const developerItems = [
    { href: "/users", label: t("nav_users") || "Users", icon: "⚙️" },
    { href: "/activity-log", label: "Activity Log", icon: "📋" },
  ];

  const isDeveloper = userRole === "developer";

  // 역할별 메뉴 구성
  const getNavItems = () => {
    if (isDeveloper || user?.is_admin || userRole === "admin") {
      const items = [...commonItems, ...vesselItems, ...adminItems];
      if (isDeveloper) {
        items.push(...developerItems);
      }
      return items;
    }
    if (["captain", "chief_engineer", "shore_manager", "engineer"].includes(userRole)) {
      return [...commonItems, ...vesselItems, ...vesselCrewItems];
    }
    return [...commonItems, ...customerItems];
  };

  const navItems = getNavItems();

  return (
    <>
      {/* 모바일 햄버거 버튼 */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed top-3 left-3 z-[60] lg:hidden p-2 bg-slate-900 text-white rounded-lg shadow-lg hover:bg-slate-800 transition-colors"
        aria-label="Open menu"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* 모바일 오버레이 */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-[70] lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* 사이드바 본체 */}
      <aside
        className={`
          fixed left-0 top-0 h-full w-64 bg-slate-900 text-white flex flex-col
          transition-transform duration-300 ease-in-out
          z-[80]
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
          lg:translate-x-0
        `}
      >
        {/* Logo + 모바일 닫기 버튼 */}
        <div className="p-6 border-b border-slate-700 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-blue-400">YJT Smart</h1>
            <p className="text-xs text-slate-400 mt-1">Vessel Management</p>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden p-1 text-slate-400 hover:text-white transition-colors"
            aria-label="Close menu"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-6 py-3 text-sm transition-colors ${
                  isActive
                    ? "bg-blue-600/20 text-blue-400 border-r-2 border-blue-400"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* User Info + Logout */}
        <div className="p-4 border-t border-slate-700">
          {user && (
            <div className="mb-3">
              <div className="flex items-center gap-2">
                <p className="text-sm text-white font-medium truncate">{user.full_name}</p>
                <span className={`px-1.5 py-0.5 text-[10px] text-white rounded font-medium ${
                  userRole === "developer" ? "bg-red-600" :
                  userRole === "admin" ? "bg-blue-600" :
                  userRole === "captain" ? "bg-amber-600" :
                  userRole === "chief_engineer" ? "bg-green-600" :
                  userRole === "shore_manager" ? "bg-purple-600" :
                  userRole === "engineer" ? "bg-teal-600" :
                  "bg-slate-600"
                }`}>
                  {userRole === "developer" ? "Dev" :
                   userRole === "admin" ? "Admin" :
                   userRole === "captain" ? "Captain" :
                   userRole === "chief_engineer" ? "C/E" :
                   userRole === "shore_manager" ? "Shore" :
                   userRole === "engineer" ? "Eng" :
                   "Customer"}
                </span>
              </div>
              <p className="text-xs text-slate-400 truncate">{user.email}</p>
              {user.company && (
                <p className="text-xs text-slate-500 truncate">{user.company}</p>
              )}
            </div>
          )}
          <button
            onClick={logout}
            className="w-full text-left text-xs text-slate-400 hover:text-red-400 transition-colors flex items-center gap-2"
          >
            <span>🚪</span> {t("logout")}
          </button>
        </div>
      </aside>

    </>
  );
}
