import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

export function ProtectedRoute() {
  const { session, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#0a0e1a] text-[#8ba3c7] font-mono text-sm">
        Carregando...
      </div>
    );
  }

  if (!session) return <Navigate to="/auth" replace />;
  return <Outlet />;
}
