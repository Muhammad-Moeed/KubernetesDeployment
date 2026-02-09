"use client";

import { useTheme } from "@/providers/theme-provider";
import { useAuth } from "@/contexts/auth-context";
import { useI18n } from "@/contexts/i18n-context";

export function Header() {
  const { theme, toggleTheme } = useTheme();
  const { user } = useAuth();
  const { locale, setLocale, t } = useI18n();

  const toggleLanguage = () => {
    setLocale(locale === "en" ? "ur" : "en");
  };

  return (
    <header className="h-16 bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800 flex items-center justify-end px-6">
      <div className="flex items-center gap-2">
        {/* Theme Toggle */}
        <IconButton onClick={toggleTheme} label={t("settings.theme")}>
          {theme === "light" ? <SunIcon /> : <MoonIcon />}
        </IconButton>

        {/* Language Switch */}
        <button
          onClick={toggleLanguage}
          className="h-9 px-3 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
          aria-label={t("settings.language")}
        >
          {locale === "en" ? "اردو" : "EN"}
        </button>

        {/* User Info */}
        <div className="flex items-center gap-3 pl-2 border-l border-gray-200 dark:border-gray-800">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              {user?.name || "User"}
            </p>
            <p className="text-xs text-gray-500">Active</p>
          </div>

          <div className="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center font-semibold">
            {user?.name?.[0]?.toUpperCase() || "U"}
          </div>
        </div>
      </div>
    </header>
  );
}

/* ================= Small UI Components ================= */
function IconButton({
  children,
  onClick,
  label,
}: {
  children: React.ReactNode;
  onClick: () => void;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className="h-9 w-9 rounded-lg flex items-center justify-center bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
    >
      {children}
    </button>
  );
}

/* ================= Icons ================= */
function SunIcon() {
  return <span className="text-lg">☀️</span>;
}
function MoonIcon() {
  return <span className="text-lg">🌙</span>;
}
