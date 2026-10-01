# Quadro de agentes

## Objetivo

Construir um quadro local, clonável, em que um card atravessa papéis de agente no Cursor. O diferencial não é um chatbot solto: é o mesmo gesto, repetido, com situação do card, rodada, JSON obrigatório e coluna de destino explícita.

## Stack

- Node.js
- TypeScript
- SQLite (`better-sqlite3`)
- Zod
- Vitest
- uma página estática, sem framework de UI
- Cloud Agents API v1 (`https://api.cursor.com`) no modo live
- cliente mock quando não houver chave

## Microetapas

### Fase 0 — Base

- [ ] **QA.00** Criar `package.json`, TypeScript e Vitest.
  - Pronto quando: `npm install` e `npm test` passam num clone limpo, mesmo que o teste só prove que o runner sobe.
- [ ] **QA.01** Criar `.env.example`.
  - Pronto quando: o exemplo lista `CURSOR_API_KEY`, `AGENT_MODE`, repositório padrão, modelos e `PORT`, sem valor real e sem segredo versionado.
- [ ] **QA.02** Criar o SQLite de `cards` e `rounds`.
  - Pronto quando: um teste cria o banco do zero com as duas tabelas.

### Fase 1 — Telefone e contrato

- [ ] **QA.03** Criar a interface do cliente e o mock.
  - Pronto quando: o mock devolve id de agente e id de run sem rede, e a interface expõe `createAgent`, `createRun`, `getAgent` e `getRun`.
- [ ] **QA.04** Implementar o cliente HTTP live.
  - Pronto quando: um teste com fetch falso cobre o POST de agente, o POST de run, o GET de agente e o GET de run, com autenticação Basic, e cobre erro HTTP.
- [ ] **QA.05** Validar o JSON de cada rodada.
  - Pronto quando: um bloco ` ```json ` ou um objeto JSON puro passa; texto livre falha; existe um schema para negócio, arquiteto, código, plano, classificação e correção.

### Fase 2 — Analista

- [ ] **QA.06** Escrever os prompts em markdown.
  - Pronto quando: há um arquivo por papel e cada um termina pedindo o JSON do contrato daquela rodada.
- [ ] **QA.07** Fazer o serviço escolher prompt, modelo e coluna.
  - Pronto quando: para o analista, quem decide prompt, modelo e coluna de destino é o serviço, não o cliente HTTP.
- [ ] **QA.08** Criar o timer de disparo.
  - Pronto quando: a cada 15 segundos um card `queued` passa a `dispatching` só se ainda estiver `queued`, e dois claims não despacham o mesmo card.
- [ ] **QA.09** Criar o timer de consulta do analista.
  - Pronto quando: run ainda andando não muda o card; erro, cancelamento ou mais de 1 hora grava `failed`; `FINISHED` com JSON válido move o card para Analisadas pela IA; JSON inválido falha sem interpretar texto livre.

### Fase 3 — Chat

- [ ] **QA.10** Continuar a mesma sessão pelo chat.
  - Pronto quando: a mensagem faz `POST /runs` na hora, na sessão do analista, cria outra rodada, e o relatório é substituído quando a consulta termina com JSON válido.

### Fase 4 — Arquiteto

- [ ] **QA.11** Enviar o card para validação de desenvolvimento.
  - Pronto quando: um botão ou arrastar dispara follow-up da sessão do analista, se ela existir; o card não muda de coluna sozinho e só segue depois que uma pessoa aprova.

### Fase 5 — Código e plano de testes

- [ ] **QA.12** Iniciar a implementação.
  - Pronto quando: nasce um agente novo em `mode: "agent"` com `autoCreatePR: true`; o modelo depende da complexidade (baixa, média, alta); branch e `prUrl` são gravados a partir de `git.branches`, não do texto.
- [ ] **QA.13** Gerar o plano de validação.
  - Pronto quando: o follow-up usa a sessão que acabou de programar, em `mode: "plan"`; o card permanece em implementação até o plano existir; JSON válido o move para a fila de implantação.

### Fase 6 — Correção

- [ ] **QA.14** Corrigir depois do teste.
  - Pronto quando: a pessoa marca o que falhou; um agente só de leitura classifica; uma pessoa aprova; o follow-up volta ao agente que programou, ou abre sessão nova com `prUrl` se a sessão anterior não existir.

### Fase 7 — Uso

- [ ] **QA.15** Servir a página do quadro.
  - Pronto quando: uma página mostra as colunas, o detalhe do card, o chat e as ações, lendo `GET /api/board`.
- [ ] **QA.16** Percorrer o fluxo no navegador em modo mock.
  - Pronto quando: um card novo passa por análise, chat, validação, aprovação, implementação, plano e uma falha marcada, até a correção voltar à fila, sem chave de API.
- [ ] **QA.17** Fechar o README no estado real.
  - Pronto quando: o README descreve só o que o código faz, com os comandos que de fato rodam.

## Fora deste roadmap

Colunas de pacote e homologação. Elas não falam com o agente.

Papéis só de leitura usam `mode: "plan"` e não abrem PR. Desenvolvedor e correção usam `mode: "agent"` com `autoCreatePR: true`.

## Resultado que este projeto deve provar

- O mesmo ciclo de disparo e consulta serve a mais de um papel.
- Texto livre não vira decisão de coluna.
- Dá para clonar, configurar e ver o quadro andar em modo mock.
- Com `CURSOR_API_KEY` e um repositório GitHub ligado à conta Cursor, o mesmo código fala com a API live.
