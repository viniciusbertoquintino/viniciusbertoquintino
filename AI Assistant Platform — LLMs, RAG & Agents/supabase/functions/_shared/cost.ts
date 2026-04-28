// USD per 1M tokens
const PRICING = {
  "text-embedding-3-small": { input: 0.02, output: 0 },
  "gpt-4o-mini": { input: 0.15, output: 0.6 },
} as const;

export function estimateCost(model: keyof typeof PRICING, promptTokens: number, completionTokens = 0): number {
  const p = PRICING[model] ?? { input: 0, output: 0 };
  return (promptTokens * p.input + completionTokens * p.output) / 1_000_000;
}
