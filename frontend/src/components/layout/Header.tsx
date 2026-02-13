"use client";

import { useState, useRef, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";
import NotificationDropdown from "@/components/notifications/NotificationDropdown";
import ProfileModal from "@/components/crud/ProfileModal";
import NamecardModal from "@/components/crud/NamecardModal";

export default function Header() {
  const { t, lang, setLang, languages } = useI18n();
  const { user, logout } = useAuth();
  const [avatarOpen, setAvatarOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [namecardOpen, setNamecardOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // 드롭다운 외부 클릭 시 닫기
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setAvatarOpen(false);
      }
    }
    if (avatarOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [avatarOpen]);

  // 언어별 환영 메시지 포맷 (이름 + 접미사)
  const welcomeText = user
    ? `${user.full_name}${t("welcome_user")}`
    : "";

  return (
    <>
      <header className="h-14 lg:h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 pl-14 lg:pl-8 lg:px-8">
        {/* 좌측: 타이틀 + 환영 메시지 */}
        <div className="flex items-center gap-2 lg:gap-3 min-w-0 flex-1">
          <h2 className="text-sm lg:text-lg font-semibold text-gray-800 truncate">
            {t("app_title")}
          </h2>
          {/* 환영 메시지 - 태블릿 이상에서만 */}
          {user && (
            <div className="hidden md:flex items-center gap-2 ml-2 lg:ml-4 pl-2 lg:pl-4 border-l border-gray-200">
              <span className="text-xs lg:text-sm font-medium text-blue-600 truncate">
                {welcomeText}
              </span>
            </div>
          )}
        </div>

        {/* 우측: 알림 + 언어 + 아바타 */}
        <div className="flex items-center gap-1.5 sm:gap-2 lg:gap-3 flex-shrink-0">
          {/* 알림 벨 */}
          <NotificationDropdown />

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
            className="bg-gray-100 border border-gray-200 rounded-lg px-2 py-1 lg:px-3 lg:py-1.5 text-xs lg:text-sm cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {Object.entries(languages).map(([code, info]) => (
              <option key={code} value={code}>
                {info.native}
              </option>
            ))}
          </select>

          {/* Global Service 텍스트 - 데스크톱만 */}
          <span className="hidden lg:inline text-sm text-gray-500">
            {t("global_service")}
          </span>

          {/* 유저 아바타 + 드롭다운 */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setAvatarOpen(!avatarOpen)}
              className="w-7 h-7 lg:w-8 lg:h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs lg:text-sm font-bold flex-shrink-0 hover:bg-blue-700 transition-colors cursor-pointer ring-2 ring-transparent hover:ring-blue-300"
            >
              {user?.full_name?.charAt(0)?.toUpperCase() || "?"}
            </button>

            {/* 드롭다운 메뉴 */}
            {avatarOpen && (
              <div className="absolute right-0 top-full mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 animate-in fade-in zoom-in-95">
                {/* 유저 정보 */}
                <div className="px-4 py-2 border-b border-gray-100">
                  <p className="text-sm font-semibold text-gray-800 truncate">{user?.full_name}</p>
                  <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                  {user?.company && (
                    <p className="text-xs text-gray-400 truncate">{user.company}</p>
                  )}
                </div>

                {/* 메뉴 항목 */}
                <button
                  onClick={() => {
                    setAvatarOpen(false);
                    setProfileOpen(true);
                  }}
                  className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2.5 transition-colors"
                >
                  <span className="text-base">👤</span>
                  {t("my_profile")}
                </button>
                <button
                  onClick={() => {
                    setAvatarOpen(false);
                    setProfileOpen(true);
                    // 약간의 딜레이 후 비밀번호 탭 활성화
                    setTimeout(() => {
                      const pwTab = document.querySelector('[data-tab="password"]') as HTMLElement;
                      if (pwTab) pwTab.click();
                    }, 100);
                  }}
                  className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2.5 transition-colors"
                >
                  <span className="text-base">🔒</span>
                  {t("change_password")}
                </button>

                {/* 네임카드/사인 (관리자/개발자만) */}
                {(user?.is_admin || user?.role === "developer") && (
                  <button
                    onClick={() => {
                      setAvatarOpen(false);
                      setNamecardOpen(true);
                    }}
                    className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2.5 transition-colors"
                  >
                    <span className="text-base">💼</span>
                    Namecard / Signature
                  </button>
                )}

                <div className="border-t border-gray-100 mt-1 pt-1">
                  <button
                    onClick={() => {
                      setAvatarOpen(false);
                      logout();
                    }}
                    className="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2.5 transition-colors"
                  >
                    <span className="text-base">🚪</span>
                    {t("logout")}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* 프로필 모달 */}
      <ProfileModal isOpen={profileOpen} onClose={() => setProfileOpen(false)} />
      {/* 네임카드 모달 */}
      <NamecardModal isOpen={namecardOpen} onClose={() => setNamecardOpen(false)} />
    </>
  );
}
