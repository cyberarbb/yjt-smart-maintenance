"use client";

import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import WelcomeModal from "@/components/WelcomeModal";

// 인증 불필요한 경로 (로그인/회원가입)
const PUBLIC_PATHS = ["/login", "/register"];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const { dir } = useI18n();
  const pathname = usePathname();
  const router = useRouter();

  const isPublicPath = PUBLIC_PATHS.includes(pathname);

  useEffect(() => {
    if (!loading && !user && !isPublicPath) {
      router.replace("/login");
    }
  }, [user, loading, isPublicPath, router]);

  // 로딩 중
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 text-sm">Loading...</p>
        </div>
      </div>
    );
  }

  // 공개 페이지 (로그인/가입) - 사이드바 없이 렌더링
  if (isPublicPath) {
    return <div dir={dir}>{children}</div>;
  }

  // 인증 안 됨 - /login으로 리디렉션 대기
  if (!user) {
    return null;
  }

  // ✅ 인증됨 - 사이드바 + 헤더와 함께 렌더링
  return (
    <div dir={dir}>
      <WelcomeModal />
      <Sidebar />
      <div className={dir === "rtl" ? "mr-64" : "ml-64"}>
        <Header />
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
}
