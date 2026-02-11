const API_BASE = "/api";

/**
 * 공통 API 호출 함수
 * - AbortController로 요청 타임아웃 관리 (CLOSE_WAIT 방지)
 * - keep-alive 헤더로 커넥션 재사용
 * - 응답 실패 시 에러 핸들링
 */
const DEFAULT_TIMEOUT = 15_000;     // 일반 API 15초
const CHAT_TIMEOUT = 60_000;        // 챗봇 API 60초 (LLM 응답 대기)

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit & { timeout?: number },
): Promise<T> {
  const { timeout = DEFAULT_TIMEOUT, ...fetchOptions } = options || {};

  // AbortController: 타임아웃 시 요청 강제 취소 → 커넥션이 CLOSE_WAIT에 빠지지 않음
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        Connection: "keep-alive",     // 커넥션 재사용 요청
      },
      signal: controller.signal,
      ...fetchOptions,
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || `HTTP ${res.status}`);
    }
    return res.json();
  } catch (err: any) {
    if (err.name === "AbortError") {
      throw new Error("Request timed out. Please try again.");
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

// Parts
export const getParts = (params?: string) =>
  fetchAPI<any[]>(`/parts/${params ? `?${params}` : ""}`);

export const getPartBrands = () => fetchAPI<string[]>("/parts/brands/list");
export const getPartCategories = () => fetchAPI<string[]>("/parts/categories/list");

// Inventory
export const getInventory = (params?: string) =>
  fetchAPI<any[]>(`/inventory/${params ? `?${params}` : ""}`);

export const getLowStock = () => fetchAPI<any[]>("/inventory/low-stock");
export const getInventoryStats = () => fetchAPI<any>("/inventory/stats");

// Orders
export const getOrders = (params?: string) =>
  fetchAPI<any[]>(`/orders/${params ? `?${params}` : ""}`);

export const getOrderStats = () => fetchAPI<any>("/orders/stats");

// Inquiries
export const getInquiries = (params?: string) =>
  fetchAPI<any[]>(`/inquiries/${params ? `?${params}` : ""}`);

// Chatbot (타임아웃 60초 - LLM 응답 대기, 다국어 지원)
export const sendChatMessage = (message: string, history: any[], language: string = "ko") =>
  fetchAPI<{ response: string }>("/chat/", {
    method: "POST",
    body: JSON.stringify({ message, history, language }),
    timeout: CHAT_TIMEOUT,
  });

// Health
export const healthCheck = () => fetchAPI<{ status: string }>("/health");
