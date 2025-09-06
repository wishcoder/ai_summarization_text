// VertexChat.ts
// Reusable functions used by VertexChat.vue

/**
 * Mimic a long-running async operation that returns a response string.
 * The response may contain an HTML anchor tag that the UI should parse.
 */
export async function sendQuery(userText: string): Promise<string> {
  // Simulate latency (e.g., server call)
  await new Promise((resolve) => setTimeout(resolve, 1800));

  const lc = userText.trim().toLowerCase();
  if (!lc) {
    return 'I didn\'t receive any text. Try typing something like <a href="https://vuetifyjs.com">Vuetify Docs</a>.';
  }

  if (lc.includes('docs') || lc.includes('help')) {
    return `Here’s something useful: <a href="https://vuetifyjs.com/en/components/text-fields/">This is hyperlink</a> for text fields.
Also, see <a href="https://vuetifyjs.com/en/components/progress-linear/">progress examples</a>.`;
  }

  if (lc.includes('hello') || lc.includes('hi')) {
    return 'Hello! Want a quick tour? <a href="https://vuetifyjs.com/en/introduction/why-vuetify/">Why Vuetify</a>';
  }

  return `You said: "${userText}". Check <a href="https://vuetifyjs.com/en/components/sheets/">sheets</a> for bubble styling.`;
}

/** Handle link actions from chat bubbles (requirement: log href). */
export function processChatAction(href: string): void {
  // eslint-disable-next-line no-console
  console.log('processChatAction href:', href);
}
