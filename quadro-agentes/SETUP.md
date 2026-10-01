# Configuração do Cursor — Quadro de agentes

As rules ficam nesta pasta. O Git é o da raiz do perfil, não um repositório dentro de `quadro-agentes/`.

Estrutura:

```text
quadro-agentes/
├── .cursor/
│   └── rules/
│       ├── 00-project-context.mdc
│       ├── 10-roadmap-executor.mdc
│       └── 20-git-commit.mdc
├── README.md
├── ROADMAP.md
└── SETUP.md
```

Não há rule de commit automático. O `production-rag` commita sozinho porque tem Git próprio. Aqui um commit automático misturaria arquivos de outras pastas do perfil.

## Comportamento esperado

As rules instruem o Cursor a:

1. ler `ROADMAP.md` e `README.md`;
2. selecionar somente uma microetapa por vez;
3. implementar apenas o escopo necessário;
4. atualizar o README quando a mudança afetar o que um leitor novo precisa saber;
5. validar o "Pronto quando";
6. marcar apenas a tarefa validada no roadmap;
7. não criar commit, a menos que isso seja pedido;
8. se o commit for pedido, usar Conventional Commits com corpo em português e depois em inglês, e não fazer push.

## Prompt inicial recomendado

```text
Leia o ROADMAP.md, o README.md e todas as Project Rules desta pasta.
Execute somente a QA.00.
Cumpra o Definition of Done, mantenha o README alinhado com o estado real do projeto e execute as validações.
Não faça commit a menos que eu peça. Não faça push. Não inicie a QA.01.
```

## Prompt padrão para as próximas etapas

```text
Execute a próxima microetapa do ROADMAP.md.
Implemente somente essa etapa, cumpra o Definition of Done, mantenha o README alinhado com o estado real do projeto, execute as validações e atualize o roadmap.
Não faça commit a menos que eu peça. Não faça push. Não inicie a tarefa seguinte.
```
