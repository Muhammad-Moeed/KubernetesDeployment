"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import { useI18n } from "@/contexts/i18n-context";

export function Sidebar() {
  const pathname = usePathname();
  const { logout } = useAuth();
  const { t, dir } = useI18n();
  const [collapsed, setCollapsed] = useState(false);

  const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: "🏠" }, // New Dashboard item
    { href: "/tasks", label: t("nav.tasks"), icon: "📋" },
    { href: "/settings", label: t("nav.settings"), icon: "⚙️" },
  ];

  const isActive = (href: string) =>
    pathname === href || pathname.startsWith(href + "/");

  const handleLogout = async () => {
    await logout();
    window.location.href = "/";
  };

  // Arrow rotation for left-right chevron
  const arrowRotation = collapsed
    ? dir === "rtl"
      ? "rotate-180"
      : "rotate-0"
    : dir === "rtl"
    ? "rotate-0"
    : "rotate-180";

  return (
    <aside
      className={`h-screen bg-white dark:bg-gray-950 flex flex-col transition-all duration-300 border-gray-200 dark:border-gray-800 ${
        collapsed ? "w-20" : "w-64"
      } ${dir === "rtl" ? "border-l" : "border-r"}`}
    >
      {/* ===== Brand + Toggle ===== */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center font-bold text-lg">
            L
          </div>
          {!collapsed && (
            <div>
              <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
                {t("common.appName")}
              </h1>
              <p className="text-xs text-gray-500">Dashboard</p>
            </div>
          )}
        </div>

        {/* Toggle Button */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="h-9 w-9 flex items-center justify-center rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition"
          aria-label="Toggle Sidebar"
        >
          <span
            className={`inline-block w-2.5 h-2.5 border-t-2 border-r-2 border-gray-600 dark:border-gray-300 transform transition-transform duration-300 ${arrowRotation}`}
          />
        </button>
      </div>

      {/* ===== Navigation ===== */}
      <nav className="flex-1 px-2 py-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const active = isActive(item.href);

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`relative flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium ${
                    active
                      ? "bg-primary text-white shadow"
                      : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                  }`}
                >
                  {active && (
                    <span className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 bg-white rounded-r" />
                  )}
                  <span className="text-xl">{item.icon}</span>
                  {!collapsed && (
                    <span className={active ? "font-semibold" : "font-medium"}>
                      {item.label}
                    </span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* ===== Logout ===== */}
      <div className="p-3 border-t border-gray-200 dark:border-gray-800">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
        >
          <span className="text-xl">🔒</span>
          {!collapsed && <span>{t("nav.logout")}</span>}
        </button>
      </div>
    </aside>
  );
}
