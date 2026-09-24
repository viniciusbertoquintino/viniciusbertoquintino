/**
 * Configurações globais da aplicação.
 * Fonte única da verdade — qualquer texto que dependa de versão/marca
 * deve importar daqui.
 */
export const appConfig = {
  name: "AI Assistant Platform",
  tagline: "LLMs, RAG & Agents",
  version: "2.1.0",
  channel: "enterprise",
} as const;

export const appFullName = `${appConfig.name} — ${appConfig.tagline}`;
export const appVersionLabel = `v${appConfig.version} ${appConfig.channel}`;
