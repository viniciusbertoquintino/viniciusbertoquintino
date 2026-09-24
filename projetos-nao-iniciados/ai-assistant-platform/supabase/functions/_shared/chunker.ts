import { approxTokens } from "./text.ts";

const TARGET_TOKENS = 600;
const MAX_TOKENS = 800;
const OVERLAP_TOKENS = 90; // ~15%

// Split text into semantic chunks of 300-800 tokens, paragraph-aware.
export function chunkText(text: string): { content: string; tokens: number }[] {
  const paragraphs = text.split(/\n{2,}/).map((p) => p.trim()).filter(Boolean);

  // Further split very long paragraphs by sentence
  const blocks: string[] = [];
  for (const p of paragraphs) {
    if (approxTokens(p) > MAX_TOKENS) {
      const sentences = p.split(/(?<=[.!?])\s+/);
      let buf = "";
      for (const s of sentences) {
        if (approxTokens(buf + " " + s) > MAX_TOKENS && buf) {
          blocks.push(buf.trim());
          buf = s;
        } else {
          buf = buf ? buf + " " + s : s;
        }
      }
      if (buf) blocks.push(buf.trim());
    } else {
      blocks.push(p);
    }
  }

  const chunks: { content: string; tokens: number }[] = [];
  let current = "";
  for (const block of blocks) {
    const tentative = current ? current + "\n\n" + block : block;
    if (approxTokens(tentative) > TARGET_TOKENS && current) {
      chunks.push({ content: current, tokens: approxTokens(current) });
      // overlap: keep tail of previous chunk
      const tailWords = current.split(/\s+/).slice(-OVERLAP_TOKENS);
      current = tailWords.join(" ") + "\n\n" + block;
    } else {
      current = tentative;
    }
  }
  if (current.trim()) chunks.push({ content: current, tokens: approxTokens(current) });

  return chunks.length > 0 ? chunks : [{ content: text, tokens: approxTokens(text) }];
}
