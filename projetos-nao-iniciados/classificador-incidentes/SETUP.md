# Configuração do Cursor — Classificador de Incidentes

## Estrutura esperada

```text
classificador-incidentes/
├── .cursor/rules/
│   ├── 00-project-context.mdc
│   ├── 10-roadmap-executor.mdc
│   └── 20-git-commit.mdc
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
7. **não** criar commit automaticamente — só se você pedir;
8. nunca fazer push automaticamente.

## Prompt inicial recomendado

```text
Leia o ROADMAP.md, o README.md e todas as Project Rules.
Valide a CI.00 contra o estado atual do repositório.
Se o Definition of Done estiver atendido, marque somente a CI.00 como concluída.
Ajuste o README apenas se necessário para refletir fielmente o estado atual do projeto.
Execute as validações.
Não faça commit a menos que eu peça. Não faça push. Não inicie a CI.01.
```

## Prompt padrão para as próximas etapas

```text
Execute a próxima microetapa do ROADMAP.md.
Implemente somente essa etapa, cumpra o Definition of Done, mantenha o README alinhado com o estado real do projeto, execute as validações e atualize o roadmap.
Não faça commit a menos que eu peça. Não faça push. Não inicie a tarefa seguinte.
```
