
# Importações necessárias
import json
import time
from datetime import datetime

estornos = {}

def gerar_id_estorno():
    # Gera um ID único para cada estorno
    # Usa a data/hora atual para criar um ID único
    agora = datetime.now()
    return f"EST_{agora.strftime('%Y%m%d_%H%M%S')}"

def criar_estorno(valor, cliente_id, motivo=""):
    
    # Gera um ID único para este estorno
    estorno_id = gerar_id_estorno()
    
    # Cria o registro do estorno
    novo_estorno = {
        "id": estorno_id,
        "valor": float(valor),
        "cliente": cliente_id,
        "motivo": motivo,
        "status": "pendente",  # pendente, aprovado, processando, concluido, erro
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "aprovador": "",
        "erro": ""
    }
    
    # Salva no banco de dados
    estornos[estorno_id] = novo_estorno
    
    print(f"✅ Estorno criado: {estorno_id}")
    print(f"   Valor: R$ {valor:.2f}")
    print(f"   Cliente: {cliente_id}")
    
    # Se o valor for pequeno (até R$ 1000), processa automaticamente
    if valor <= 1000:
        print("   💰 Valor baixo - processando automaticamente...")
        processar_estorno(estorno_id)
    else:
        print("   ⚠️  Valor alto - precisa de aprovação!")
    
    return novo_estorno


def aprovar_estorno(estorno_id, aprovador):
    
    # Lista os estornos disponíveis para aprovação
    print("\n📋 ESTORNOS DISPONÍVEIS PARA APROVAÇÃO:")
    print("-" * 50)
    
    estornos_pendentes = [e for e in estornos.values() if e["status"] == "pendente" and e["valor"] > 1000]
    
    if not estornos_pendentes:
        print("📭 Nenhum estorno pendente de aprovação encontrado")
        print("   (Apenas estornos com valor > R$ 1000 precisam de aprovação)")
        return False
    
    for estorno in estornos_pendentes:
        print(f"⏳ {estorno['id']} - R$ {estorno['valor']:.2f} | Cliente: {estorno['cliente']}")
        if estorno["motivo"]:
            print(f"   📝 Motivo: {estorno['motivo']}")
        print(f"   📅 Criado em: {estorno['data_criacao']}")
        print()
    
    # Verifica se o estorno existe
    if estorno_id not in estornos:
        print("❌ Estorno não encontrado!")
        return False
    
    estorno = estornos[estorno_id]
    
    # Verifica se realmente precisa de aprovação
    if estorno["valor"] <= 1000:
        print("ℹ️  Este estorno não precisa de aprovação (valor baixo)")
        return False
    
    # Aprova o estorno
    estorno["status"] = "aprovado"
    estorno["aprovador"] = aprovador
    
    print(f"✅ Estorno {estorno_id} aprovado por {aprovador}")
    print("   🚀 Iniciando processamento...")
    
    # Processa o estorno aprovado
    processar_estorno(estorno_id)
    return True

def rejeitar_estorno(estorno_id, aprovador):
    
    # Verifica se o estorno existe
    if estorno_id not in estornos:
        print("❌ Estorno não encontrado!")
        return False
    
    estorno = estornos[estorno_id]
    
    # Rejeita o estorno
    estorno["status"] = "rejeitado"
    estorno["aprovador"] = aprovador
    
    print(f"❌ Estorno {estorno_id} rejeitado por {aprovador}")
    return True


def processar_estorno(estorno_id):
    
    # Verifica se o estorno existe
    if estorno_id not in estornos:
        print("❌ Estorno não encontrado!")
        return
    
    estorno = estornos[estorno_id]
    
    # Verifica se não foi rejeitado
    if estorno["status"] == "rejeitado":
        print("⚠️  Estorno foi rejeitado - não será processado")
        return
    
    # Muda status para "processando"
    estorno["status"] = "processando"
    print(f"🔄 Processando estorno {estorno_id}...")
    
    # Simula o processamento (como se fosse enviar dinheiro para o banco)
    # Vamos tentar 2 vezes para simular problemas de rede
    for tentativa in range(1, 3):
        print(f"   Tentativa {tentativa}...")
        time.sleep(1)  # Simula tempo de processamento
        
        # Na primeira tentativa, simula um erro
        # Na segunda tentativa, funciona
        if tentativa == 1:
            print("   ❌ Erro temporário (simulado)")
            estorno["erro"] = "Erro de conexão"
        else:
            # Sucesso!
            estorno["status"] = "concluido"
            estorno["erro"] = ""
            print(f"   ✅ Sucesso! Dinheiro enviado para o cliente")
            print(f"   💰 R$ {estorno['valor']:.2f} estornado com sucesso!")
            return
    
    # Se chegou aqui, todas as tentativas falharam
    estorno["status"] = "erro"
    print(f"   ❌ Falha definitiva - estorno não pôde ser processado")


def reprocessar_estorno(estorno_id):
    
    if estorno_id not in estornos:
        print("❌ Estorno não encontrado!")
        return False
    
    estorno = estornos[estorno_id]
    
    if estorno["status"] != "erro":
        print("ℹ️  Este estorno não está com erro - não precisa reprocessar")
        return False
    
    print(f"🔄 Tentando reprocessar estorno {estorno_id}...")
    estorno["erro"] = ""  # Limpa o erro anterior
    processar_estorno(estorno_id)
    return True

def listar_estornos(filtro=None):
    
    # Pega todos os estornos
    todos_estornos = list(estornos.values())
    
    # Se foi pedido um filtro, aplica ele
    if filtro:
        estornos_filtrados = [e for e in todos_estornos if e["status"] == filtro]
    else:
        estornos_filtrados = todos_estornos
    
    # Verifica se tem estornos para mostrar
    if not estornos_filtrados:
        print("📭 Nenhum estorno encontrado")
        return
    
    # Mostra os estornos
    print(f"\n📋 ESTORNOS ({len(estornos_filtrados)}):")
    print("-" * 60)
    
    for estorno in estornos_filtrados:
        # Emoji baseado no status
        emoji_status = {
            "pendente": "⏳",
            "aprovado": "✅", 
            "processando": "🔄",
            "concluido": "✅",
            "rejeitado": "❌",
            "erro": "🚨"
        }.get(estorno["status"], "❓")
        
        print(f"{emoji_status} {estorno['id']}")
        print(f"   💰 R$ {estorno['valor']:.2f} | 👤 {estorno['cliente']}")
        print(f"   📅 {estorno['data_criacao']} | Status: {estorno['status']}")
        
        if estorno["motivo"]:
            print(f"   📝 Motivo: {estorno['motivo']}")
        if estorno["aprovador"]:
            print(f"   👨‍💼 Aprovador: {estorno['aprovador']}")
        if estorno["erro"]:
            print(f"   ❌ Erro: {estorno['erro']}")
        print()

def estatisticas():
    
    total_estornos = len(estornos)
    
    if total_estornos == 0:
        print("📊 Nenhum estorno registrado ainda")
        return
    
    # Conta estornos por status
    contador_status = {}
    valor_total = 0.0
    
    for estorno in estornos.values():
        status = estorno["status"]
        contador_status[status] = contador_status.get(status, 0) + 1
        valor_total += estorno["valor"]
    
    # Mostra as estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print("-" * 30)
    print(f"📦 Total de estornos: {total_estornos}")
    print(f"💰 Valor total: R$ {valor_total:.2f}")
    print("\n📈 Por status:")
    
    for status, quantidade in contador_status.items():
        emoji = {
            "pendente": "⏳",
            "aprovado": "✅", 
            "processando": "🔄",
            "concluido": "✅",
            "rejeitado": "❌",
            "erro": "🚨"
        }.get(status, "❓")
        print(f"   {emoji} {status}: {quantidade}")

def salvar_estornos():
    """
    Salva todos os estornos em um arquivo JSON
    """
    if not estornos:
        print("📭 Nenhum estorno para salvar")
        return
    
    # Cria nome do arquivo com data/hora
    nome_arquivo = f"estornos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Salva no arquivo
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(list(estornos.values()), arquivo, indent=2, ensure_ascii=False)
    
    print(f"💾 Estornos salvos em: {nome_arquivo}")


def demo():
    """
    Demonstra o sistema criando alguns estornos de exemplo
    """
    print("🧪 DEMONSTRAÇÃO DO SISTEMA")
    print("=" * 40)
    
    # Cria estornos de exemplo
    print("\n1️⃣ Criando estorno de valor baixo (processamento automático):")
    criar_estorno(500.0, "CLIENTE001", "Produto defeituoso")
    
    print("\n2️⃣ Criando estorno de valor alto (precisa aprovação):")
    criar_estorno(1500.0, "CLIENTE002", "Cancelamento de pedido")
    
    print("\n3️⃣ Aprovando o estorno de valor alto:")
    # Pega o último estorno criado (que precisa de aprovação)
    ultimo_estorno = list(estornos.keys())[-1]
    aprovar_estorno(ultimo_estorno, "GERENTE_SILVA")
    
    print("\n4️⃣ Listando todos os estornos:")
    listar_estornos()
    
    print("\n5️⃣ Mostrando estatísticas:")
    estatisticas()

def menu():
    """
    Menu principal do sistema - interface para o usuário
    """
    print("🏛️  SISTEMA DE ESTORNO - 2025 - v1.0")
    print("=" * 50)
    print("Este sistema gerencia estornos de dinheiro para clientes")
    print("Valores até R$ 1000 são processados automaticamente")
    print("Valores acima de R$ 1000 precisam de aprovação")
    print("=" * 50)
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. 💰 Criar Novo Estorno")
        print("2. ✅ Aprovar Estorno (valores altos)")
        print("3. ❌ Rejeitar Estorno")
        print("4. 📋 Listar Estornos")
        print("5. 🔄 Reprocessar Estorno com Erro")
        print("6. 📊 Ver Estatísticas")
        print("7. 💾 Salvar em Arquivo")
        print("8. 🧪 Demonstração Automática")
        print("9. 🚪 Sair")
        
        opcao = input("\n👉 Escolha uma opção (1-9): ").strip()
        
        try:
            if opcao == "1":
                print("\n💰 CRIAR NOVO ESTORNO")
                print("-" * 25)
                valor = float(input("💵 Valor do estorno (R$): "))
                cliente = input("👤 ID do cliente: ").strip()
                motivo = input("📝 Motivo (opcional): ").strip()
                criar_estorno(valor, cliente, motivo)
                
            elif opcao == "2":
                print("\n✅ APROVAR ESTORNO")
                print("-" * 20)
                estorno_id = input("🔍 ID do estorno: ").strip()
                aprovador = input("👨‍💼 Seu ID (aprovador): ").strip()
                aprovar_estorno(estorno_id, aprovador)
                
            elif opcao == "3":
                print("\n❌ REJEITAR ESTORNO")
                print("-" * 20)
                estorno_id = input("🔍 ID do estorno: ").strip()
                aprovador = input("👨‍💼 Seu ID (aprovador): ").strip()
                rejeitar_estorno(estorno_id, aprovador)
                
            elif opcao == "4":
                print("\n📋 LISTAR ESTORNOS")
                print("-" * 20)
                print("Filtros disponíveis:")
                print("  - Deixe vazio para ver todos")
                print("  - pendente, aprovado, processando, concluido, rejeitado, erro")
                filtro = input("🔍 Filtro (opcional): ").strip() or None
                listar_estornos(filtro)
                
            elif opcao == "5":
                print("\n🔄 REPROCESSAR ESTORNO")
                print("-" * 25)
                estorno_id = input("🔍 ID do estorno com erro: ").strip()
                reprocessar_estorno(estorno_id)
                
            elif opcao == "6":
                estatisticas()
                
            elif opcao == "7":
                salvar_estornos()
                
            elif opcao == "8":
                demo()
                
            elif opcao == "9":
                print("\n👋 Obrigado por usar o Sistema de Estorno!")
                print("   Até logo! 🚪")
                break
                
            else:
                print("❌ Opção inválida! Escolha um número de 1 a 9.")
                
        except ValueError:
            print("❌ Valor inválido! Verifique se digitou números corretamente.")
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

# ==========================================
# INÍCIO DO PROGRAMA
# ==========================================
if __name__ == "__main__":
    menu()


