"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import enTranslations from "@/lib/locales/en.json";
import urTranslations from "@/lib/locales/ur.json";

type Locale = "en" | "ur";

interface I18nContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string) => string;
  dir: "ltr" | "rtl";
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

const translations = {
  en: enTranslations,
  ur: urTranslations,
};

// Helper to get nested translation value
function getNestedValue(obj: any, path: string): string {
  const keys = path.split(".");
  let value = obj;
  for (const key of keys) {
    value = value?.[key];
    if (value === undefined) return path; // Return key if not found
  }
  return value;
}

// Cookie helpers
function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(";").shift() || null;
  return null;
}

function setCookie(name: string, value: string, days: number = 365) {
  if (typeof document === "undefined") return;
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("en");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Load locale from cookie or default to "en"
    const savedLocale = getCookie("locale") as Locale | null;
    const initialLocale = savedLocale || "en";
    setLocaleState(initialLocale);

    // Set document direction and lang
    const dir = initialLocale === "ur" ? "rtl" : "ltr";
    if (typeof document !== "undefined") {
      document.documentElement.dir = dir;
      document.documentElement.lang = initialLocale;
    }
  }, []);

  const setLocale = (newLocale: Locale) => {
    setLocaleState(newLocale);
    setCookie("locale", newLocale);

    // Update document direction and lang
    const dir = newLocale === "ur" ? "rtl" : "ltr";
    if (typeof document !== "undefined") {
      document.documentElement.dir = dir;
      document.documentElement.lang = newLocale;
    }
  };

  const t = (key: string): string => {
    return getNestedValue(translations[locale], key);
  };

  const dir = locale === "ur" ? "rtl" : "ltr";

  // Always render children, even during SSR
  return (
    <I18nContext.Provider value={{ locale, setLocale, t, dir }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (context === undefined) {
    // Return default values for SSR
    return {
      locale: "en" as Locale,
      setLocale: () => {},
      t: (key: string) => key,
      dir: "ltr" as const,
    };
  }
  return context;
}
