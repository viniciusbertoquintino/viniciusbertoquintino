# Configuração do Cursor — Production RAG

Copie o conteúdo deste pacote para a raiz do repositório `production-rag`.

Estrutura esperada:

```text
production-rag/
├── .cursor/
│   └── rules/
│       ├── 00-project-context.mdc
│       ├── 10-roadmap-executor.mdc
│       └── 20-git-autocommit.mdc
├── README.md
├── ROADMAP.md
└── SETUP.md
```

## Comportamento esperado

As rules instruem o Cursor a:

1. ler `ROADMAP.md` e `README.md`;
2. selecionar somente uma microetapa por vez;
3. implementar apenas o escopo necessário;
4. atualizar o README quando a mudança afetar documentação pública;
5. validar a implementação;
6. marcar apenas a tarefa concluída no roadmap;
7. criar um único Conventional Commit;
8. nunca fazer push automaticamente.

## Prompt inicial recomendado

```text
Leia o ROADMAP.md, o README.md e todas as Project Rules.
Valide a P1.00 contra o estado atual do repositório.
Se o Definition of Done estiver atendido, marque somente a P1.00 como concluída.
Ajuste o README apenas se necessário para refletir fielmente o estado atual do projeto.
Execute as validações e crie o commit automático seguindo a Git Rule.
Não faça push e não inicie a P1.01.
```

## Prompt padrão para as próximas etapas

```text
Execute a próxima microetapa do ROADMAP.md.
Implemente somente essa etapa, cumpra o Definition of Done, mantenha o README alinhado com o estado real do projeto, execute as validações, atualize o roadmap e faça o commit.
Não faça push e não inicie a tarefa seguinte.
```
