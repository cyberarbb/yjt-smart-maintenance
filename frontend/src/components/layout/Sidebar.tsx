"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useI18n } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";

export default function Sidebar() {
  const pathname = usePathname();
  const { t } = useI18n();
  const { user, logout } = useAuth();

  const navItems = [
    { href: "/", label: t("nav_dashboard"), icon: "📊" },
    { href: "/inventory", label: t("nav_inventory"), icon: "📦" },
    { href: "/orders", label: t("nav_orders"), icon: "🔧" },
    { href: "/chatbot", label: t("nav_chatbot"), icon: "🤖" },
    { href: "/inquiries", label: t("nav_inquiries"), icon: "📨" },
  ];

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-slate-900 text-white flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-xl font-bold text-blue-400">YJT Smart</h1>
        <p className="text-xs text-slate-400 mt-1">Maintenance Platform</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4">
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
            <p className="text-sm text-white font-medium truncate">{user.full_name}</p>
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
  );
}
