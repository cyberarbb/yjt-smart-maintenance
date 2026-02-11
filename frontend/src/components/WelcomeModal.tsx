"use client";

import { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { useAuth } from "@/lib/auth";

const BRANDS = [
  { name: "MAN Energy Solutions", color: "bg-blue-100 text-blue-800" },
  { name: "MHI (Mitsubishi)", color: "bg-red-100 text-red-800" },
  { name: "KBB", color: "bg-green-100 text-green-800" },
  { name: "ABB", color: "bg-orange-100 text-orange-800" },
  { name: "Napier", color: "bg-purple-100 text-purple-800" },
];

const GUIDE_ITEMS = [
  { icon: "📊", key: "welcome_modal_guide_dashboard" },
  { icon: "📦", key: "welcome_modal_guide_inventory" },
  { icon: "🤖", key: "welcome_modal_guide_chatbot" },
  { icon: "🔧", key: "welcome_modal_guide_orders" },
];

export default function WelcomeModal() {
  const { t } = useI18n();
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [dontShowAgain, setDontShowAgain] = useState(false);

  useEffect(() => {
    // 유저가 로그인한 후에만 체크
    if (!user) return;

    const dismissed = localStorage.getItem("yjt_welcome_dismissed");
    if (!dismissed) {
      // 약간의 딜레이 후 팝업 표시 (페이지 로드 완료 후)
      const timer = setTimeout(() => setIsOpen(true), 500);
      return () => clearTimeout(timer);
    }
  }, [user]);

  function handleClose() {
    if (dontShowAgain) {
      localStorage.setItem("yjt_welcome_dismissed", "true");
    }
    setIsOpen(false);
  }

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={handleClose}
      />

      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto animate-in">
        {/* 헤더 - 그라데이션 배경 */}
        <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 rounded-t-2xl px-8 py-6 text-white">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
              🚢
            </div>
            <div>
              <h2 className="text-xl font-bold">{t("welcome_modal_title")}</h2>
              <p className="text-blue-200 text-sm">YONGJIN TURBO Co., Ltd.</p>
            </div>
          </div>
        </div>

        <div className="px-8 py-6 space-y-6">
          {/* 회사 소개 섹션 */}
          <div>
            <h3 className="text-base font-bold text-gray-800 flex items-center gap-2 mb-3">
              <span className="w-7 h-7 bg-blue-100 rounded-lg flex items-center justify-center text-sm">🏢</span>
              {t("welcome_modal_about")}
            </h3>
            <p className="text-sm text-gray-600 leading-relaxed mb-2">
              {t("welcome_modal_desc1")}
            </p>
            <p className="text-sm text-gray-600 leading-relaxed">
              {t("welcome_modal_desc2")}
            </p>

            {/* 핵심 수치 카드 */}
            <div className="grid grid-cols-3 gap-3 mt-4">
              <div className="bg-blue-50 rounded-xl p-3 text-center">
                <p className="text-2xl font-bold text-blue-600">31</p>
                <p className="text-xs text-gray-500 mt-1">Countries</p>
              </div>
              <div className="bg-green-50 rounded-xl p-3 text-center">
                <p className="text-2xl font-bold text-green-600">1,990+</p>
                <p className="text-xs text-gray-500 mt-1">Overhauls/Year</p>
              </div>
              <div className="bg-purple-50 rounded-xl p-3 text-center">
                <p className="text-2xl font-bold text-purple-600">$17M</p>
                <p className="text-xs text-gray-500 mt-1">Parts Inventory</p>
              </div>
            </div>
          </div>

          {/* 지원 브랜드 */}
          <div>
            <h3 className="text-base font-bold text-gray-800 flex items-center gap-2 mb-3">
              <span className="w-7 h-7 bg-orange-100 rounded-lg flex items-center justify-center text-sm">⚙️</span>
              {t("welcome_modal_brands")}
            </h3>
            <div className="flex flex-wrap gap-2">
              {BRANDS.map((brand) => (
                <span
                  key={brand.name}
                  className={`px-3 py-1.5 rounded-full text-xs font-semibold ${brand.color}`}
                >
                  {brand.name}
                </span>
              ))}
            </div>
          </div>

          {/* 사용법 가이드 */}
          <div>
            <h3 className="text-base font-bold text-gray-800 flex items-center gap-2 mb-3">
              <span className="w-7 h-7 bg-green-100 rounded-lg flex items-center justify-center text-sm">📖</span>
              {t("welcome_modal_guide_title")}
            </h3>
            <div className="space-y-2">
              {GUIDE_ITEMS.map((item) => (
                <div
                  key={item.key}
                  className="flex items-start gap-3 p-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
                >
                  <span className="text-xl mt-0.5">{item.icon}</span>
                  <p className="text-sm text-gray-700 leading-relaxed">
                    {t(item.key)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* 다시 보지 않기 체크박스 + 닫기 버튼 */}
          <div className="flex items-center justify-between pt-2 border-t border-gray-100">
            <label className="flex items-center gap-2 cursor-pointer group">
              <input
                type="checkbox"
                checked={dontShowAgain}
                onChange={(e) => setDontShowAgain(e.target.checked)}
                className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-xs text-gray-500 group-hover:text-gray-700">
                {t("welcome_modal_dont_show")}
              </span>
            </label>

            <button
              onClick={handleClose}
              className="px-8 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold text-sm hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300"
            >
              {t("welcome_modal_close")} →
            </button>
          </div>
        </div>
      </div>

      <style jsx>{`
        .animate-in {
          animation: modalIn 0.3s ease-out;
        }
        @keyframes modalIn {
          from {
            opacity: 0;
            transform: scale(0.95) translateY(10px);
          }
          to {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
