"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface I18nContextType {
  lang: string;
  dir: "ltr" | "rtl";
  t: (key: string) => string;
  setLang: (lang: string) => void;
  languages: Record<string, { name: string; native: string; dir: string }>;
}

const LANGUAGES: Record<string, { name: string; native: string; dir: string }> = {
  ko: { name: "한국어", native: "한국어", dir: "ltr" },
  en: { name: "English", native: "English", dir: "ltr" },
  zh: { name: "Chinese", native: "中文", dir: "ltr" },
  ja: { name: "Japanese", native: "日本語", dir: "ltr" },
  ar: { name: "Arabic", native: "العربية", dir: "rtl" },
  es: { name: "Spanish", native: "Español", dir: "ltr" },
  hi: { name: "Hindi", native: "हिन्दी", dir: "ltr" },
  fr: { name: "French", native: "Français", dir: "ltr" },
};

const I18nContext = createContext<I18nContextType | null>(null);

export function useI18n() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useI18n must be used within I18nProvider");
  return ctx;
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState("en");
  const [translations, setTranslations] = useState<Record<string, string>>({});
  const dir = LANGUAGES[lang]?.dir === "rtl" ? "rtl" : "ltr";

  // 초기 로드
  useEffect(() => {
    const saved = localStorage.getItem("yjt_lang");
    if (saved && LANGUAGES[saved]) {
      setLangState(saved);
    }
  }, []);

  // 언어 변경 시 번역 로드
  useEffect(() => {
    fetch(`/api/i18n/translations/${lang}`)
      .then((r) => r.json())
      .then((data) => setTranslations(data.translations || {}))
      .catch(() => {});
  }, [lang]);

  function setLang(newLang: string) {
    if (LANGUAGES[newLang]) {
      setLangState(newLang);
      localStorage.setItem("yjt_lang", newLang);
    }
  }

  function t(key: string): string {
    return translations[key] || key;
  }

  return (
    <I18nContext.Provider value={{ lang, dir, t, setLang, languages: LANGUAGES }}>
      {children}
    </I18nContext.Provider>
  );
}
