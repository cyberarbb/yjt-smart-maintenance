const API_BASE = "/api";

/**
 * 공통 API 호출 함수
 * - JWT Authorization 헤더 자동 포함
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

  // JWT 토큰 자동 포함
  const token = typeof window !== "undefined"
    ? localStorage.getItem("yjt_token")
    : null;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Connection: "keep-alive",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers,
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

// ── Parts ──
export const getParts = (params?: string) =>
  fetchAPI<any[]>(`/parts${params ? `?${params}` : ""}`);

export const getPartBrands = () => fetchAPI<string[]>("/parts/brands/list");
export const getPartCategories = () => fetchAPI<string[]>("/parts/categories/list");

export const createPart = (data: any) =>
  fetchAPI<any>("/parts", { method: "POST", body: JSON.stringify(data) });

export const updatePart = (id: string, data: any) =>
  fetchAPI<any>(`/parts/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const deletePart = (id: string) =>
  fetchAPI<any>(`/parts/${id}`, { method: "DELETE" });

// ── Inventory ──
export const getInventory = (params?: string) =>
  fetchAPI<any[]>(`/inventory${params ? `?${params}` : ""}`);

export const getLowStock = () => fetchAPI<any[]>("/inventory/low-stock");
export const getInventoryStats = () => fetchAPI<any>("/inventory/stats");

export const updateInventory = (id: string, data: any) =>
  fetchAPI<any>(`/inventory/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const adjustInventory = (id: string, data: any) =>
  fetchAPI<any>(`/inventory/${id}/adjust`, { method: "POST", body: JSON.stringify(data) });

// ── Customers ──
export const getCustomers = (params?: string) =>
  fetchAPI<any[]>(`/customers${params ? `?${params}` : ""}`);

export const createCustomer = (data: any) =>
  fetchAPI<any>("/customers", { method: "POST", body: JSON.stringify(data) });

export const updateCustomer = (id: string, data: any) =>
  fetchAPI<any>(`/customers/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const deleteCustomer = (id: string) =>
  fetchAPI<any>(`/customers/${id}`, { method: "DELETE" });

// ── Orders ──
export const getOrders = (params?: string) =>
  fetchAPI<any[]>(`/orders${params ? `?${params}` : ""}`);

export const getMyOrders = () =>
  fetchAPI<any[]>("/orders/my-orders");

export const getOrderStats = () => fetchAPI<any>("/orders/stats");

export const createOrder = (data: any) =>
  fetchAPI<any>("/orders", { method: "POST", body: JSON.stringify(data) });

export const updateOrder = (id: string, data: any) =>
  fetchAPI<any>(`/orders/${id}`, { method: "PUT", body: JSON.stringify(data) });

// ── Inquiries ──
export const getInquiries = (params?: string) =>
  fetchAPI<any[]>(`/inquiries${params ? `?${params}` : ""}`);

export const getMyInquiries = () =>
  fetchAPI<any[]>("/inquiries/my-inquiries");

export const createInquiry = (data: any) =>
  fetchAPI<any>("/inquiries", { method: "POST", body: JSON.stringify(data) });

export const updateInquiry = (id: string, data: any) =>
  fetchAPI<any>(`/inquiries/${id}`, { method: "PUT", body: JSON.stringify(data) });

// ── Users (Admin) ──
export const getUsers = () => fetchAPI<any[]>("/auth/users");

export const toggleUserAdmin = (userId: string, adminPassword: string) =>
  fetchAPI<any>(`/auth/users/${userId}/toggle-admin`, {
    method: "PUT",
    body: JSON.stringify({ admin_password: adminPassword }),
  });

// ── Notifications ──
export const getNotifications = () => fetchAPI<any[]>("/notifications");

export const getUnreadCount = () =>
  fetchAPI<{ count: number }>("/notifications/unread-count");

export const markNotificationRead = (id: string) =>
  fetchAPI<any>(`/notifications/${id}/read`, { method: "PUT" });

export const markAllNotificationsRead = () =>
  fetchAPI<any>("/notifications/read-all", { method: "PUT" });

// ── Analytics ──
export const getInventoryByBrand = () => fetchAPI<any[]>("/analytics/inventory-by-brand");
export const getOrderStatusDist = () => fetchAPI<any[]>("/analytics/order-status-distribution");
export const getMonthlyOrders = () => fetchAPI<any[]>("/analytics/monthly-orders");
export const getInventoryValue = () => fetchAPI<any[]>("/analytics/inventory-value-by-brand");
export const getLowStockSummary = () => fetchAPI<any[]>("/analytics/low-stock-summary");

// ── Chatbot (타임아웃 60초 - LLM 응답 대기, 다국어 지원) ──
export const sendChatMessage = (message: string, history: any[], language: string = "ko") =>
  fetchAPI<{ response: string }>("/chat", {
    method: "POST",
    body: JSON.stringify({ message, history, language }),
    timeout: CHAT_TIMEOUT,
  });

// ── Sync ──
export const syncToSheets = () =>
  fetchAPI<any>("/sync/sheets", { method: "POST", timeout: 30_000 });

// ── Email (관리자 전용) ──
export const sendEmailToCustomer = (data: { to_email: string; subject: string; body: string }) =>
  fetchAPI<any>("/email/send", { method: "POST", body: JSON.stringify(data) });

// ── Inquiry AI Draft ──
export const generateInquiryDraft = (inquiryId: string) =>
  fetchAPI<{ draft: string; detected_language: string }>("/inquiries/generate-draft", {
    method: "POST",
    body: JSON.stringify({ inquiry_id: inquiryId }),
    timeout: CHAT_TIMEOUT,
  });

// ── User Profile (네임카드 포함) ──
export const updateMyProfile = (data: any) =>
  fetchAPI<any>("/auth/me", { method: "PUT", body: JSON.stringify(data) });

// ── Vessels (Phase 3) ──
export const getVessels = (params?: string) =>
  fetchAPI<any[]>(`/vessels${params ? `?${params}` : ""}`);

export const getVesselSummaries = () => fetchAPI<any[]>("/vessels/summary");

export const getVessel = (id: string) => fetchAPI<any>(`/vessels/${id}`);

export const createVessel = (data: any) =>
  fetchAPI<any>("/vessels", { method: "POST", body: JSON.stringify(data) });

export const updateVessel = (id: string, data: any) =>
  fetchAPI<any>(`/vessels/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const deleteVessel = (id: string) =>
  fetchAPI<any>(`/vessels/${id}`, { method: "DELETE" });

export const getVesselTypes = () => fetchAPI<string[]>("/vessels/types");

// ── User Role/Vessel Assignment (Admin) ──
export const updateUserRole = (userId: string, role: string, adminPassword?: string) =>
  fetchAPI<any>(`/auth/users/${userId}/role`, {
    method: "PUT",
    body: JSON.stringify({ role, ...(adminPassword ? { admin_password: adminPassword } : {}) }),
  });

export const updateUserVessel = (userId: string, vesselId: string | null) =>
  fetchAPI<any>(`/auth/users/${userId}/vessel`, { method: "PUT", body: JSON.stringify({ vessel_id: vesselId }) });

export const getAvailableRoles = () => fetchAPI<any[]>("/auth/roles");

// ── Equipment (Phase 3 Batch 2) ──
export const getEquipmentTree = (vesselId: string) =>
  fetchAPI<any[]>(`/vessels/${vesselId}/equipment-tree`);

export const getVesselEquipment = (vesselId: string, category?: string) =>
  fetchAPI<any[]>(`/vessels/${vesselId}/equipment${category ? `?category=${category}` : ""}`);

export const getEquipmentBrief = (vesselId?: string) =>
  fetchAPI<any[]>(`/equipment/brief${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const getEquipmentCategories = () =>
  fetchAPI<string[]>("/equipment/categories");

export const getEquipment = (id: string) => fetchAPI<any>(`/equipment/${id}`);

export const createEquipment = (data: any) =>
  fetchAPI<any>("/equipment", { method: "POST", body: JSON.stringify(data) });

export const updateEquipment = (id: string, data: any) =>
  fetchAPI<any>(`/equipment/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const deleteEquipment = (id: string) =>
  fetchAPI<any>(`/equipment/${id}`, { method: "DELETE" });

// ── Running Hours (Phase 3 Batch 3) ──
export const recordRunningHours = (data: any) =>
  fetchAPI<any>("/running-hours/record", { method: "POST", body: JSON.stringify(data) });

export const recordRunningHoursBulk = (data: any) =>
  fetchAPI<any>("/running-hours/record/bulk", { method: "POST", body: JSON.stringify(data) });

export const getVesselLatestHours = (vesselId: string) =>
  fetchAPI<any[]>(`/running-hours/vessel/${vesselId}/latest`);

export const getEquipmentHoursHistory = (equipmentId: string, days: number = 30) =>
  fetchAPI<any[]>(`/running-hours/equipment/${equipmentId}/history?days=${days}`);

export const getEquipmentHoursChart = (equipmentId: string, days: number = 30) =>
  fetchAPI<any[]>(`/running-hours/equipment/${equipmentId}/chart?days=${days}`);

// ── PMS (Phase 3 Batch 4) ──
export const getMaintenancePlans = (vesselId?: string) =>
  fetchAPI<any[]>(`/pms/plans${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const createMaintenancePlan = (data: any) =>
  fetchAPI<any>("/pms/plans", { method: "POST", body: JSON.stringify(data) });

export const updateMaintenancePlan = (id: string, data: any) =>
  fetchAPI<any>(`/pms/plans/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const getWorkOrders = (params?: string) =>
  fetchAPI<any[]>(`/pms/work-orders${params ? `?${params}` : ""}`);

export const getWorkOrderStats = (vesselId?: string) =>
  fetchAPI<any>(`/pms/work-orders/stats${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const getWorkOrderCalendar = (vesselId: string, year?: number, month?: number) => {
  const params = new URLSearchParams({ vessel_id: vesselId });
  if (year) params.set("year", String(year));
  if (month) params.set("month", String(month));
  return fetchAPI<any[]>(`/pms/work-orders/calendar?${params}`);
};

export const getOverdueWorkOrders = (vesselId?: string) =>
  fetchAPI<any[]>(`/pms/work-orders/overdue${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const getUpcomingWorkOrders = (vesselId?: string, days: number = 30) =>
  fetchAPI<any[]>(`/pms/work-orders/upcoming?days=${days}${vesselId ? `&vessel_id=${vesselId}` : ""}`);

export const createWorkOrder = (data: any) =>
  fetchAPI<any>("/pms/work-orders", { method: "POST", body: JSON.stringify(data) });

export const updateWorkOrder = (id: string, data: any) =>
  fetchAPI<any>(`/pms/work-orders/${id}`, { method: "PUT", body: JSON.stringify(data) });

// ── PMS Analytics (Phase 3 Batch 5) ──
export const getPMSCompletionRate = (vesselId?: string) =>
  fetchAPI<any[]>(`/analytics/pms-completion-rate${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const getWODistribution = (vesselId?: string) =>
  fetchAPI<any[]>(`/analytics/work-order-distribution${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const getEquipmentReliability = (vesselId?: string) =>
  fetchAPI<any[]>(`/analytics/equipment-reliability${vesselId ? `?vessel_id=${vesselId}` : ""}`);

export const getVesselSummaryAnalytics = () =>
  fetchAPI<any[]>("/analytics/vessel-summary");

// ── Activity Log (Admin) ──
export const getActivityLogs = (action?: string, limit: number = 100, offset: number = 0) => {
  const params = new URLSearchParams();
  if (action) params.set("action", action);
  params.set("limit", String(limit));
  params.set("offset", String(offset));
  return fetchAPI<{ total: number; logs: any[] }>(`/activity-log/logs?${params}`);
};

export const getOnlineUsers = () => fetchAPI<any[]>("/activity-log/online");

// ── Health ──
export const healthCheck = () => fetchAPI<{ status: string }>("/health");
