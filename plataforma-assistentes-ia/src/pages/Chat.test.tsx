import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Chat from "./Chat";

const chat = vi.hoisted(() => ({
  messages: [] as [],
  send: vi.fn(),
  isSending: false,
  setSessionId: vi.fn(),
  sessionId: null as string | null,
}));

vi.mock("@/hooks/useChat", () => ({
  useChat: () => chat,
}));

vi.mock("@/hooks/useDocuments", () => ({
  useDocuments: () => ({ data: [] }),
}));

function sendButton() {
  const box = screen.getByPlaceholderText("Pergunte sobre seus documentos…");
  const button = box.parentElement?.querySelector("button");
  if (!button) throw new Error("botão de envio não encontrado");
  return button;
}

describe("Chat", () => {
  beforeEach(() => {
    chat.messages = [];
    chat.isSending = false;
    chat.sessionId = null;
    chat.send.mockReset();
    chat.send.mockImplementation(() => {
      chat.isSending = true;
    });
  });

  it("não envia texto em branco", () => {
    render(<Chat />);
    fireEvent.change(screen.getByPlaceholderText("Pergunte sobre seus documentos…"), {
      target: { value: "   " },
    });
    expect(sendButton()).toBeDisabled();
    fireEvent.click(sendButton());
    expect(chat.send).not.toHaveBeenCalled();
  });

  it("coloca a mensagem do usuário na lista ao enviar", () => {
    render(<Chat />);
    fireEvent.change(screen.getByPlaceholderText("Pergunte sobre seus documentos…"), {
      target: { value: "qual a política?" },
    });
    fireEvent.click(sendButton());

    expect(chat.send).toHaveBeenCalledWith("qual a política?");
    expect(screen.getByText("qual a política?")).toBeInTheDocument();
  });
});
