"use client";

import { useI18n } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";

export default function Header() {
  const { t, lang, setLang, languages } = useI18n();
  const { user } = useAuth();

  // 언어별 환영 메시지 포맷 (이름 + 접미사)
  const welcomeText = user
    ? lang === "ko"
      ? `${user.full_name}${t("welcome_user")}`
      : lang === "ja"
        ? `${user.full_name}${t("welcome_user")}`
        : lang === "zh"
          ? `${user.full_name}${t("welcome_user")}`
          : lang === "ar"
            ? `${user.full_name}${t("welcome_user")}`
            : `${user.full_name}${t("welcome_user")}`
    : "";

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
      <div className="flex items-center gap-3">
        <h2 className="text-lg font-semibold text-gray-800">
          {t("app_title")}
        </h2>
        {/* 환영 메시지 */}
        {user && (
          <div className="flex items-center gap-2 ml-4 pl-4 border-l border-gray-200">
            <span className="text-lg">👋</span>
            <span className="text-sm font-medium text-blue-600">
              {welcomeText}
            </span>
          </div>
        )}
      </div>
      <div className="flex items-center gap-4">
        {/* 언어 선택기 */}
        <select
          value={lang}
          onChange={(e) => {
            setLang(e.target.value);
            // 유저 프로필에도 저장
            if (user) {
              fetch("/api/auth/me", {
                method: "PUT",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${localStorage.getItem("yjt_token")}`,
                },
                body: JSON.stringify({ preferred_language: e.target.value }),
              });
            }
          }}
          className="bg-gray-100 border border-gray-200 rounded-lg px-3 py-1.5 text-sm cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {Object.entries(languages).map(([code, info]) => (
            <option key={code} value={code}>
              {info.native}
            </option>
          ))}
        </select>

        <span className="text-sm text-gray-500">
          {t("global_service")}
        </span>

        {/* 유저 아바타 */}
        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
          {user?.full_name?.charAt(0)?.toUpperCase() || "?"}
        </div>
      </div>
    </header>
  );
}
