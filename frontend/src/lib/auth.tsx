"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface User {
  id: string;
  email: string;
  full_name: string;
  company: string;
  country: string;
  phone: string;
  preferred_language: string;
  is_active: boolean;
  is_admin: boolean;
  // 역할 시스템
  role?: string;
  vessel_id?: string | null;
  // 네임카드 필드
  namecard_title?: string;
  namecard_department?: string;
  namecard_mobile?: string;
  namecard_fax?: string;
  namecard_address?: string;
  namecard_website?: string;
  namecard_custom_html?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  updateUser: (data: Partial<User>) => Promise<void>;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  company?: string;
  country?: string;
  phone?: string;
  preferred_language?: string;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // 초기 로드: localStorage에서 토큰 복원
  useEffect(() => {
    const saved = localStorage.getItem("yjt_token");
    if (saved) {
      setToken(saved);
      fetchMe(saved).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  async function fetchMe(t: string) {
    try {
      const res = await fetch("/api/auth/me", {
        headers: { Authorization: `Bearer ${t}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
        setToken(t);
      } else {
        localStorage.removeItem("yjt_token");
        setToken(null);
        setUser(null);
      }
    } catch {
      localStorage.removeItem("yjt_token");
      setToken(null);
      setUser(null);
    }
  }

  async function login(email: string, password: string) {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Login failed");
    }
    const data = await res.json();
    localStorage.setItem("yjt_token", data.access_token);
    setToken(data.access_token);
    setUser(data.user);
  }

  async function register(regData: RegisterData) {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(regData),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Registration failed");
    }
    const data = await res.json();
    localStorage.setItem("yjt_token", data.access_token);
    setToken(data.access_token);
    setUser(data.user);
  }

  async function logout() {
    // 백엔드에 로그아웃 기록
    if (token) {
      try {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
        });
      } catch {
        // 로그아웃 기록 실패해도 로컬 세션은 정리
      }
    }
    localStorage.removeItem("yjt_token");
    setToken(null);
    setUser(null);
  }

  async function updateUser(data: Partial<User>) {
    if (!token) return;
    const res = await fetch("/api/auth/me", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
    if (res.ok) {
      const updated = await res.json();
      setUser(updated);
    }
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}
