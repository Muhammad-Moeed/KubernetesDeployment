import en from "./locales/en.json";
import ur from "./locales/ur.json";

export type Locale = "en" | "ur";

const translations = {
  en,
  ur,
};

export function getTranslations(locale: Locale) {
  return translations[locale];
}

export function useTranslations(locale: Locale) {
  const t = translations[locale];

  return {
    t: (key: string) => {
      const keys = key.split(".");
      let value: any = t;
      for (const k of keys) {
        value = value?.[k];
      }
      return value || key;
    },
  };
}
