
import json
import time
import uuid
from datetime import datetime


# "Banco de dados" em memória (dicionário)
estornos = {}


def gerar_request_id():
    return f"REQ_{uuid.uuid4().hex[:6].upper()}"


def criar_estorno(request_id, amount, customer_id, reason=""):
    if request_id in estornos:
        print("[IDEMPOTENCIA] Estorno já existe, retornando existente.")
        return estornos[request_id]

    estorno = {
        "request_id": request_id,
        "amount": float(amount),
        "customer_id": customer_id,
        "reason": reason,
        "status": "pending",
        "retry_count": 0,
        "error": "",
        "approver": "",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    estornos[request_id] = estorno
    print(f"[CRIADO] {request_id} - R$ {amount:.2f}")

    # Processamento automático para valores <= 1000
    if amount <= 1000:
        processar_estorno(request_id)
    else:
        print("[APROVACAO] Valor > R$ 1000, precisa de aprovação")
    return estorno


def aprovar_estorno(request_id, approver):
    e = estornos.get(request_id)
    if not e:
        print("[ERRO] Estorno não encontrado")
        return False
    if e["amount"] <= 1000:
        print("[AVISO] Não precisa aprovação")
        return False
    e["status"] = "approved"
    e["approver"] = approver
    print(f"[APROVADO] {request_id} por {approver}")
    processar_estorno(request_id)
    return True


def rejeitar_estorno(request_id, approver):
    e = estornos.get(request_id)
    if not e:
        print("[ERRO] Estorno não encontrado")
        return False
    e["status"] = "rejected"
    e["approver"] = approver
    print(f"[REJEITADO] {request_id} por {approver}")
    return True


def processar_estorno(request_id):
    e = estornos.get(request_id)
    if not e:
        print("[ERRO] Estorno não encontrado")
        return
    if e["status"] in ("rejected",):
        print("[AVISO] Estorno rejeitado, não será processado")
        return

    e["status"] = "processing"
    print(f"[PROCESSANDO] {request_id}")
    # Simples: tentar até 2 vezes, sem aleatoriedade
    for tentativa in range(1, 3):
        try:
            e["retry_count"] = tentativa
            time.sleep(0.3 * tentativa)
            # Sucesso na segunda tentativa para simular retry
            if tentativa < 2:
                raise Exception("Erro temporário")
            e["status"] = "completed"
            e["error"] = ""
            print(f"[SUCESSO] {request_id} completado!")
            return
        except Exception as exc:
            e["error"] = str(exc)
            print(f"[ERRO] Tentativa {tentativa} falhou: {exc}")

    e["status"] = "dlq"
    print(f"[DLQ] {request_id} enviado para DLQ")


def reprocessar_dlq(request_id):
    e = estornos.get(request_id)
    if not e or e["status"] != "dlq":
        print("[ERRO] Item não está na DLQ")
        return False
    e["retry_count"] = 0
    e["error"] = ""
    processar_estorno(request_id)
    return True


def listar_estornos(filtro=None):
    dados = list(estornos.values())
    if filtro:
        dados = [x for x in dados if x["status"] == filtro]
    if not dados:
        print("Nenhum estorno encontrado")
        return
    print(f"\nESTORNOS ({len(dados)}):")
    for e in dados:
        print(f"- {e['request_id']} | R$ {e['amount']:.2f} | {e['status']}")
        if e["retry_count"]:
            print(f"  tentativas: {e['retry_count']}")
        if e["error"]:
            print(f"  erro: {e['error']}")


def estatisticas():
    total = len(estornos)
    if total == 0:
        print("Nenhum estorno registrado")
        return
    por_status = {}
    valor_total = 0.0
    for e in estornos.values():
        por_status[e["status"]] = por_status.get(e["status"], 0) + 1
        valor_total += e["amount"]
    print("\nESTATISTICAS:")
    print(f"Total: {total} | Valor: R$ {valor_total:.2f}")
    for s, c in por_status.items():
        print(f"{s}: {c}")


def exportar_json(filename=None):
    if not filename:
        filename = f"estornos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(list(estornos.values()), f, indent=2, ensure_ascii=False)
    print(f"[EXPORT] Salvo em {filename}")


def demo():
    print("DEMO - Versão Iniciante\n")
    criar_estorno("REQ001", 500.0, "CUST123", "Produto defeituoso")
    criar_estorno("REQ002", 1500.0, "CUST456", "Cancelamento")
    aprovar_estorno("REQ002", "GERENTE01")
    criar_estorno("REQ001", 500.0, "CUST123", "Duplicado")
    listar_estornos()
    estatisticas()
    exportar_json()


def menu():
    while True:
        print("   🏛️  SISTEMA DE ESTORNO")
        print("="*50)
        print("1. 💰 Criar Estorno")
        print("2. ✅ Aprovar Estorno") 
        print("3. ❌ Rejeitar Estorno")
        print("4. 📋 Listar Estornos")
        print("5. 🚨 Gerenciar DLQ")
        print("6. 📊 Estatísticas")
        print("7. 💾 Exportar JSON")
        print("8. 🧪 Demo Automático")
        print("9. 🚪 Sair")
        opcao = input("Escolha (1-9): ").strip()

        try:
            if opcao == "1":
                rid = input("Request ID (vazio=auto): ").strip() or gerar_request_id()
                amount = float(input("Valor R$: "))
                cid = input("Customer ID: ").strip()
                reason = input("Motivo (opcional): ").strip()
                criar_estorno(rid, amount, cid, reason)
            elif opcao == "2":
                rid = input("Request ID: ").strip()
                approver = input("Seu ID: ").strip()
                aprovar_estorno(rid, approver)
            elif opcao == "3":
                rid = input("Request ID: ").strip()
                approver = input("Seu ID: ").strip()
                rejeitar_estorno(rid, approver)
            elif opcao == "4":
                print("Filtros: vazio=Todos | pending | completed | dlq | rejected | approved | processing")
                filtro = input("Filtro: ").strip() or None
                listar_estornos(filtro)
            elif opcao == "5":
                rid = input("Request ID na DLQ: ").strip()
                reprocessar_dlq(rid)
            elif opcao == "6":
                estatisticas()
            elif opcao == "7":
                exportar_json()
            elif opcao == "8":
                demo()
            elif opcao == "9":
                print("Até logo!")
                break
            else:
                print("Opção inválida!")
        except ValueError:
            print("Valor inválido!")
        except KeyboardInterrupt:
            print("\nEncerrado pelo usuário.")
            break


if __name__ == "__main__":
    menu()


