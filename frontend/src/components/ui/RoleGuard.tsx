"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

interface Props {
  children: React.ReactNode;
  allowedRoles: string[];
  fallbackMessage?: string;
}

/**
 * 역할 기반 가드 컴포넌트
 * allowedRoles에 포함된 역할만 접근 가능
 * admin은 항상 허용
 */
export default function RoleGuard({ children, allowedRoles, fallbackMessage }: Props) {
  const { user, loading } = useAuth();
  const router = useRouter();

  const userRole = user?.role || (user?.is_admin ? "admin" : "customer");
  const hasAccess = user?.is_admin || userRole === "developer" || allowedRoles.includes(userRole);

  useEffect(() => {
    if (!loading && user && !hasAccess) {
      // 접근 권한 없으면 대시보드로 리다이렉트
      router.replace("/");
    }
  }, [user, loading, hasAccess, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!hasAccess) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-4xl mb-4">🔒</p>
          <p className="text-gray-500">
            {fallbackMessage || "Access denied - Insufficient permissions"}
          </p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
