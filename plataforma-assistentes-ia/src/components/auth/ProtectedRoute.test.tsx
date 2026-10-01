import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "./ProtectedRoute";

const auth = vi.hoisted(() => ({
  session: null as { user: { id: string } } | null,
  loading: true,
  signIn: vi.fn(),
  signUp: vi.fn(),
  signOut: vi.fn(),
}));

vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => auth,
}));

function renderAtDashboard() {
  return render(
    <MemoryRouter initialEntries={["/dashboard"]}>
      <Routes>
        <Route path="/auth" element={<div>Tela de login</div>} />
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<div>Área logada</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("ProtectedRoute", () => {
  beforeEach(() => {
    auth.session = null;
    auth.loading = true;
  });

  it("mostra carregando enquanto a sessão não resolve", () => {
    renderAtDashboard();
    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("redireciona para /auth sem sessão", () => {
    auth.loading = false;
    renderAtDashboard();
    expect(screen.getByText("Tela de login")).toBeInTheDocument();
    expect(screen.queryByText("Área logada")).not.toBeInTheDocument();
  });

  it("renderiza a rota interna com sessão", () => {
    auth.loading = false;
    auth.session = { user: { id: "user-1" } };
    renderAtDashboard();
    expect(screen.getByText("Área logada")).toBeInTheDocument();
  });
});
