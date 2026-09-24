function tokens(text: string): Set<string> {
  return new Set(
    text
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, " ")
      .split(/\s+/)
      .filter((w) => w.length > 3)
  );
}

// Jaccard overlap between answer tokens and the union of context chunks.
export function overlapScore(answer: string, contexts: string[]): number {
  const a = tokens(answer);
  const c = tokens(contexts.join(" "));
  if (a.size === 0 || c.size === 0) return 0;
  let inter = 0;
  for (const w of a) if (c.has(w)) inter++;
  const union = new Set([...a, ...c]).size;
  return union === 0 ? 0 : Number((inter / union).toFixed(4));
}
