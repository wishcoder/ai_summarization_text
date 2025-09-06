<template>
  <v-container class="pa-0 chat-root" fluid>
    <!-- Header (optional) -->
    <v-sheet class="px-4 py-3 border-b" elevation="0">
      <div class="text-subtitle-1 font-weight-medium">Chat</div>
    </v-sheet>

    <!-- Messages area: grows and scrolls -->
    <v-sheet
      class="messages flex-grow-1 overflow-auto px-3 py-4"
      elevation="0"
      ref="scrollAreaRef"
    >
      <div class="d-flex flex-column" style="gap: 12px;">
        <template v-for="m in messages" :key="m.id">
          <div
            class="d-flex"
            :class="m.sender === 'user' ? 'justify-end' : 'justify-start'"
          >
            <v-sheet
              class="pa-3 rounded-xl bubble"
              :class="m.sender === 'user' ? 'bubble-user' : 'bubble-bot'"
              elevation="1"
              max-width="80%"
            >
              <!-- Render parsed segments; link segments are clickable -->
              <template v-for="(seg, idx) in m.segments" :key="idx">
                <span v-if="seg.type === 'text'">{{ seg.text }}</span>
                <v-btn
                  v-else
                  variant="text"
                  density="compact"
                  class="text-decoration-underline px-0"
                  @click="onLinkClick((seg as LinkSegment).href)"
                >
                  {{ (seg as LinkSegment).text }}
                </v-btn>
              </template>
            </v-sheet>
          </div>
        </template>

        <!-- Typing / busy indicator bubble -->
        <div v-if="busy" class="d-flex justify-start">
          <v-sheet class="pa-3 rounded-xl bubble bubble-bot" elevation="1" max-width="60%">
            <div class="d-flex align-center" style="gap: 10px;">
              <v-progress-circular indeterminate size="18" width="2" />
              <span>Thinking…</span>
            </div>
          </v-sheet>
        </div>
      </div>
    </v-sheet>

    <!-- Sticky input area pinned to bottom -->
    <div class="input-sticky">
      <v-divider />
      <v-progress-linear
        v-if="busy"
        indeterminate
        height="3"
      />
      <v-sheet class="px-3 py-2" elevation="0">
        <v-text-field
          v-model="draft"
          variant="outlined"
          density="comfortable"
          :disabled="busy"
          :placeholder="busy ? 'Please wait…' : 'Type your message…'"
          hide-details
          clearable
          @keydown.enter="trySend"
          class="ma-0"
        >
          <template #append-inner>
            <v-btn
              icon
              :disabled="busy || !canSend"
              @click="trySend"
              :aria-label="'Send message'"
            >
              <v-icon>mdi-send</v-icon>
            </v-btn>
          </template>
        </v-text-field>
      </v-sheet>
    </div>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, computed, nextTick, type Ref } from 'vue';
import { sendQuery, processChatAction } from './Chat';

type Sender = 'user' | 'bot';

type TextSegment = { type: 'text'; text: string };
type LinkSegment = { type: 'link'; text: string; href: string };
type Segment = TextSegment | LinkSegment;

interface ChatMessage {
  id: string;
  sender: Sender;
  raw: string;
  segments: Segment[];
}

export default defineComponent({
  name: 'AssistChat',
  setup() {
    // --- State ---
    const messages = ref<ChatMessage[]>([]);
    const draft = ref<string>('');
    const busy = ref<boolean>(false);
    const scrollAreaRef: Ref<HTMLElement | null> = ref(null);

    const canSend = computed<boolean>(() => draft.value.trim().length > 0 && !busy.value);

    // --- Helpers ---
    function uid(): string {
      return Math.random().toString(36).slice(2, 9);
    }

    function parseAnchorSegments(htmlish: string): Segment[] {
      const container = document.createElement('div');
      container.innerHTML = htmlish;

      const result: Segment[] = [];

      function walk(node: ChildNode) {
        if (node.nodeType === Node.TEXT_NODE) {
          const text = node.textContent ?? '';
          if (text) result.push({ type: 'text', text });
          return;
        }
        if (node.nodeType === Node.ELEMENT_NODE) {
          const el = node as HTMLElement;
          if (el.tagName.toLowerCase() === 'a') {
            const href = el.getAttribute('href') || '';
            const text = el.textContent?.trim() || href || 'link';
            result.push({ type: 'link', text, href });
            return;
          }
          Array.from(node.childNodes).forEach(walk);
        }
      }

      Array.from(container.childNodes).forEach(walk);
      return result.length ? result : [{ type: 'text', text: htmlish }];
    }

    function appendMessage(sender: Sender, raw: string) {
      messages.value.push({
        id: uid(),
        sender,
        raw,
        segments: parseAnchorSegments(raw),
      });
      nextTick(() => {
        const el = scrollAreaRef.value;
        if (el) el.scrollTop = el.scrollHeight;
      });
    }

    function updateResult(response: string) {
      appendMessage('bot', response);
    }

    async function trySend() {
      if (!canSend.value) return;
      const text = draft.value.trim();
      draft.value = '';

      appendMessage('user', text);

      busy.value = true;
      try {
        const response = await sendQuery(text);
        updateResult(response);
      } catch (err) {
        updateResult('Sorry, something went wrong.');
        // eslint-disable-next-line no-console
        console.error(err);
      } finally {
        busy.value = false;
      }
    }

    function onLinkClick(href: string) {
      processChatAction(href);
    }

    return {
      messages,
      draft,
      busy,
      scrollAreaRef,
      canSend,
      trySend,
      onLinkClick,
    };
  },
});
</script>

<style scoped>
/* Ensure the view fills its parent and stays white */
.chat-root {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: #ffffff;
}

/* subtle border helper for header */
.border-b {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

/* Messages list behavior */
.messages {
  /* already flex-grow-1 via class, keep for clarity: */
  flex: 1 1 auto;
  overflow: auto;
}

/* Sticky input at the bottom of the view */
.input-sticky {
  position: sticky;
  bottom: 0;
  background: #ffffff;
  /* keep above the scrolling content */
  z-index: 2;
  /* support iOS safe-area */
  padding-bottom: env(safe-area-inset-bottom);
}

.bubble {
  white-space: pre-wrap;
  word-break: break-word;
}

/* User bubble = silver */
.bubble-user {
  background-color: silver !important;
  color: rgba(0, 0, 0, 0.87);
}

/* Bot bubble = green */
.bubble-bot {
  background-color: #A5D6A7 !important;
  color: rgba(0, 0, 0, 0.87);
}

.text-decoration-underline {
  text-decoration: underline;
}
</style>
