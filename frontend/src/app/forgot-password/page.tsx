"use client";

import { useState } from "react";
import { useI18n } from "@/lib/i18n";
import Link from "next/link";
import { useRouter } from "next/navigation";

type Step = "email" | "code" | "password";

export default function ForgotPasswordPage() {
  const { t, lang, setLang, languages } = useI18n();
  const router = useRouter();

  const [step, setStep] = useState<Step>("email");
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  // Step 1: 이메일로 인증 코드 발송
  async function handleSendCode(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch("/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, language: lang }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to send code");
      }
      setSuccess(t("code_sent"));
      setStep("code");
    } catch (err: any) {
      setError(err.message || "Error sending code");
    } finally {
      setLoading(false);
    }
  }

  // Step 2: 인증 코드 확인 → Step 3으로
  function handleVerifyCode(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (code.trim().length !== 6) {
      setError("Please enter a 6-digit code");
      return;
    }
    setSuccess("");
    setStep("password");
  }

  // Step 3: 새 비밀번호 설정
  async function handleResetPassword(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (newPassword.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError(t("password_mismatch"));
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code: code.trim(), new_password: newPassword }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to reset password");
      }
      setSuccess(t("password_reset_success"));
      // 2초 후 로그인 페이지로 이동
      setTimeout(() => router.push("/login"), 2000);
    } catch (err: any) {
      setError(err.message || "Error resetting password");
    } finally {
      setLoading(false);
    }
  }

  // 코드 재발송
  async function handleResendCode() {
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const res = await fetch("/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, language: lang }),
      });
      if (res.ok) {
        setSuccess(t("code_sent"));
      }
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
      {/* 언어 선택기 */}
      <div className="fixed top-4 right-4 z-50">
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value)}
          className="bg-white/10 text-white border border-white/20 rounded-lg px-3 py-2 text-sm backdrop-blur-sm cursor-pointer"
        >
          {Object.entries(languages).map(([code, info]) => (
            <option key={code} value={code} className="bg-slate-800">
              {info.native}
            </option>
          ))}
        </select>
      </div>

      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">🚢 YJT Smart</h1>
          <p className="text-blue-300 text-sm">{t("app_title")}</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-1">
            {step === "email" && "🔐"} {t("reset_password")}
          </h2>
          <p className="text-gray-500 text-sm mb-6">{t("forgot_password_subtitle")}</p>

          {/* 스텝 인디케이터 */}
          <div className="flex items-center gap-2 mb-6">
            {["email", "code", "password"].map((s, i) => (
              <div key={s} className="flex items-center gap-2 flex-1">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    step === s
                      ? "bg-blue-600 text-white"
                      : ["email", "code", "password"].indexOf(step) > i
                        ? "bg-green-500 text-white"
                        : "bg-gray-200 text-gray-400"
                  }`}
                >
                  {["email", "code", "password"].indexOf(step) > i ? "✓" : i + 1}
                </div>
                {i < 2 && (
                  <div className={`flex-1 h-0.5 ${["email", "code", "password"].indexOf(step) > i ? "bg-green-500" : "bg-gray-200"}`} />
                )}
              </div>
            ))}
          </div>

          {/* 에러/성공 메시지 */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg text-sm">
              {error}
            </div>
          )}
          {success && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-600 rounded-lg text-sm">
              {success}
            </div>
          )}

          {/* Step 1: 이메일 입력 */}
          {step === "email" && (
            <form onSubmit={handleSendCode} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t("email")}</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="email@company.com"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? "..." : t("send_code")}
              </button>
            </form>
          )}

          {/* Step 2: 인증 코드 입력 */}
          {step === "code" && (
            <form onSubmit={handleVerifyCode} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t("verification_code")}</label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl text-sm text-center tracking-[0.5em] font-mono text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="000000"
                  maxLength={6}
                  required
                />
                <p className="text-xs text-gray-400 mt-1 text-center">{email}</p>
              </div>
              <button
                type="submit"
                disabled={loading || code.length !== 6}
                className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {t("verify")}
              </button>
              <button
                type="button"
                onClick={handleResendCode}
                disabled={loading}
                className="w-full py-2 text-sm text-blue-600 hover:underline disabled:opacity-50"
              >
                {t("resend_code")}
              </button>
            </form>
          )}

          {/* Step 3: 새 비밀번호 설정 */}
          {step === "password" && (
            <form onSubmit={handleResetPassword} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t("new_password")}</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="••••••••"
                  minLength={6}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t("confirm_password")}</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="••••••••"
                  minLength={6}
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? "..." : t("reset_password")}
              </button>
            </form>
          )}

          <p className="mt-6 text-center text-sm text-gray-500">
            <Link href="/login" className="text-blue-600 font-medium hover:underline">
              ← {t("back_to_login")}
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-blue-300/60 mt-6">
          YONGJIN TURBO CO., LTD. • {t("global_service")}
        </p>
      </div>
    </div>
  );
}
