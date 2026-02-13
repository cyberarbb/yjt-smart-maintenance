"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AdminGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  const hasAccess = user?.is_admin || user?.role === "developer";

  useEffect(() => {
    if (!loading && user && !hasAccess) {
      router.replace("/");
    }
  }, [user, loading, router, hasAccess]);

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
          <p className="text-gray-500">Access denied - Admin only</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
