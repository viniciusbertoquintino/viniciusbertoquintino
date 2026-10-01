import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import AuthPage from "./Auth";

const auth = vi.hoisted(() => ({
  session: null,
  loading: false,
  signIn: vi.fn(),
  signUp: vi.fn(),
  signOut: vi.fn(),
}));

const toast = vi.hoisted(() => ({
  error: vi.fn(),
  success: vi.fn(),
}));

vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => auth,
}));

vi.mock("sonner", () => ({
  toast,
}));

function renderAuth() {
  return render(
    <MemoryRouter>
      <AuthPage />
    </MemoryRouter>,
  );
}

describe("Auth", () => {
  beforeEach(() => {
    auth.session = null;
    auth.loading = false;
    auth.signIn.mockReset();
    auth.signUp.mockReset();
    toast.error.mockReset();
    toast.success.mockReset();
  });

  it("não chama signUp quando a senha tem menos de 6 caracteres", () => {
    renderAuth();
    fireEvent.mouseDown(screen.getByRole("tab", { name: "Criar conta" }));
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "a@b.co" } });
    fireEvent.change(screen.getByLabelText("Senha (mín. 6 caracteres)"), { target: { value: "12345" } });
    fireEvent.submit(screen.getByRole("button", { name: "Criar conta" }).closest("form")!);

    expect(auth.signUp).not.toHaveBeenCalled();
    expect(toast.error).toHaveBeenCalledWith("A senha precisa ter pelo menos 6 caracteres");
  });

  it("traduz credenciais inválidas no login", async () => {
    auth.signIn.mockResolvedValue({ error: new Error("Invalid login credentials") });
    renderAuth();
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "a@b.co" } });
    fireEvent.change(screen.getByLabelText("Senha"), { target: { value: "secret1" } });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith("Credenciais inválidas");
    });
    expect(auth.signIn).toHaveBeenCalledWith("a@b.co", "secret1");
  });
});
