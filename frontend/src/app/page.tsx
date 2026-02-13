"use client";

import { useAuth } from "@/lib/auth";
import AdminDashboard from "@/components/dashboard/AdminDashboard";
import CustomerDashboard from "@/components/dashboard/CustomerDashboard";
import VesselDashboard from "@/components/dashboard/VesselDashboard";

export default function Dashboard() {
  const { user } = useAuth();

  const userRole = user?.role || (user?.is_admin ? "admin" : "customer");

  // Developer/Admin: full admin dashboard
  if (user?.is_admin || userRole === "admin" || userRole === "developer") {
    return <AdminDashboard />;
  }

  // Vessel crew: vessel-focused dashboard
  if (["captain", "chief_engineer", "shore_manager", "engineer"].includes(userRole)) {
    return <VesselDashboard />;
  }

  // Customer: customer dashboard
  return <CustomerDashboard />;
}
