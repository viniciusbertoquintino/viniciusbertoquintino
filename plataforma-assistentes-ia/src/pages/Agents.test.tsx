import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Agents from "./Agents";

const mutateAsync = vi.hoisted(() => vi.fn());

vi.mock("@/hooks/useAgents", () => ({
  useRunAgent: () => ({ mutateAsync }),
}));

vi.mock("@/hooks/use-toast", () => ({
  toast: vi.fn(),
}));

const agentResult = {
  agentName: "Document Analyst",
  input: "",
  steps: [
    {
      number: 1,
      title: "Análise",
      text: "Resumo do trecho",
      tag: "análise",
      tagVariant: "info" as const,
    },
  ],
  latency: 1.2,
  tokens: 1000,
  executedAt: "agora",
};

describe("Agents", () => {
  beforeEach(() => {
    mutateAsync.mockReset();
    mutateAsync.mockResolvedValue(agentResult);
  });

  it("não executa o agente com input vazio", () => {
    render(<Agents />);
    const executar = screen.getAllByRole("button", { name: "Executar" })[0];
    expect(executar).toBeDisabled();
    fireEvent.click(executar);
    expect(mutateAsync).not.toHaveBeenCalled();
  });

  it("mostra o resultado mockado depois de executar", async () => {
    render(<Agents />);
    fireEvent.change(screen.getByPlaceholderText(/Cole um trecho de documento/), {
      target: { value: "política de reembolso" },
    });
    fireEvent.click(screen.getAllByRole("button", { name: "Executar" })[0]);

    expect(mutateAsync).toHaveBeenCalledWith({
      agent_type: "analyst",
      input_text: "política de reembolso",
    });
    expect(await screen.findByText("Último resultado")).toBeInTheDocument();
    expect(screen.getByText("Resumo do trecho")).toBeInTheDocument();
  });
});
