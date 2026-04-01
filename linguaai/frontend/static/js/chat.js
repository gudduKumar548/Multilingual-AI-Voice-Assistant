let currentConvId = null;

function getTargetLang() {
  return document.getElementById("lang-select").value;
}

function autoResize(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 120) + "px";
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function addMessage(role, text, meta = "") {
  document.getElementById("empty-state")?.remove();
  const wrap = document.createElement("div");
  wrap.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = `msg-avatar ${role === "user" ? "user" : "ai"}`;
  avatar.textContent = role === "user" ? "👤" : "🌍";
  const bubble = document.createElement("div");
  bubble.className = `msg-bubble ${role === "user" ? "user" : "ai"}`;
  bubble.textContent = text;
  if (meta) {
    const m = document.createElement("div");
    m.className = "msg-meta";
    m.textContent = meta;
    bubble.appendChild(m);
  }
  wrap.appendChild(avatar);
  wrap.appendChild(bubble);
  document.getElementById("chat-messages").appendChild(wrap);
  document.getElementById("chat-messages").scrollTop = 99999;
}

function addTyping() {
  const wrap = document.createElement("div");
  wrap.className = "message ai";
  wrap.id = "typing-wrap";
  const av = document.createElement("div");
  av.className = "msg-avatar ai";
  av.textContent = "🌍";
  const bub = document.createElement("div");
  bub.className = "msg-bubble ai";
  bub.innerHTML =
    '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
  wrap.appendChild(av);
  wrap.appendChild(bub);
  document.getElementById("chat-messages").appendChild(wrap);
  document.getElementById("chat-messages").scrollTop = 99999;
}

function removeTyping() {
  document.getElementById("typing-wrap")?.remove();
}

function showEmptyState() {
  document.getElementById("chat-messages").innerHTML = `
    <div class="empty-state" id="empty-state">
      <div class="empty-icon">🌍</div>
      <h2>Start a conversation</h2>
      <p>Type or speak in any language. LinguaAI responds using Groq AI.</p>
      <div class="lang-chips">
        <span class="chip">🇮🇳 Hindi</span><span class="chip">🇮🇳 Punjabi</span>
        <span class="chip">🇪🇸 Spanish</span><span class="chip">🇯🇵 Japanese</span>
        <span class="chip">+ more</span>
      </div>
    </div>`;
}

// ── Conversations ──
async function loadConversations() {
  const token = localStorage.getItem("lingua_token");
  if (!token) return;
  try {
    const { ok, data } = await API.getConversations();
    if (!ok) return;
    renderConversationList(data.conversations);
  } catch {}
}

function renderConversationList(conversations) {
  const list = document.getElementById("history-list");
  list.innerHTML = "";
  if (!conversations || conversations.length === 0) {
    list.innerHTML =
      '<div style="font-size:0.75rem;color:var(--muted)">No conversations yet</div>';
    return;
  }
  conversations.forEach((conv) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.style.cssText =
      "display:flex;align-items:center;justify-content:space-between;gap:6px;cursor:pointer;";
    if (conv.id === currentConvId) {
      item.style.borderColor = "var(--accent)";
      item.style.color = "var(--text)";
    }
    const title = document.createElement("span");
    title.style.cssText =
      "overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;";
    title.textContent = conv.title;
    const del = document.createElement("span");
    del.textContent = "🗑";
    del.style.cssText =
      "cursor:pointer;opacity:0.4;font-size:0.7rem;flex-shrink:0;";
    del.onclick = (e) => {
      e.stopPropagation();
      deleteConversation(conv.id);
    };
    del.onmouseover = () => (del.style.opacity = "1");
    del.onmouseout = () => (del.style.opacity = "0.4");
    item.appendChild(title);
    item.appendChild(del);
    item.onclick = () => openConversation(conv.id);
    list.appendChild(item);
  });
}

async function openConversation(convId) {
  currentConvId = convId;
  const token = localStorage.getItem("lingua_token");
  try {
    const { ok, data } = await API.getConversationMessages(convId);
    if (!ok) return;
    if (data.conversation.language) {
      document.getElementById("lang-select").value = data.conversation.language;
    }
    document.getElementById("chat-messages").innerHTML = "";
    if (data.messages.length === 0) {
      showEmptyState();
    } else {
      data.messages.forEach((m) => {
        addMessage("user", m.user_msg);
        addMessage("ai", m.ai_reply, "🌐 " + m.language + " · Groq AI");
      });
    }
    loadConversations();
  } catch {}
}

async function deleteConversation(convId) {
  try {
    await API.deleteConversation(convId);
    if (currentConvId === convId) {
      currentConvId = null;
      showEmptyState();
    }
    loadConversations();
  } catch {}
}

function newChat() {
  currentConvId = null;
  showEmptyState();
  document.getElementById("lang-select").value = "en";
  loadConversations();
}

// ── Send Message ──
async function sendMessage(textOverride) {
  const input = document.getElementById("chat-input");
  const text = textOverride || input.value.trim();
  if (!text) return;

  const token = localStorage.getItem("lingua_token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  input.value = "";
  autoResize(input);
  document.getElementById("send-btn").disabled = true;

  const lang = getTargetLang();
  addMessage("user", text);
  addTyping();

  try {
    const { ok, status, data } = await API.sendMessage(
      text,
      lang,
      currentConvId,
    );
    removeTyping();

    if (status === 401) {
      localStorage.removeItem("lingua_token");
      localStorage.removeItem("lingua_user");
      window.location.href = "login.html";
      return;
    }
    if (!ok) {
      addMessage("ai", "⚠️ " + (data.detail || "Something went wrong."));
    } else {
      addMessage("ai", data.reply, "🌐 " + lang + " · Groq AI");
      currentConvId = data.conversation_id;
      speakText(data.reply, lang);
      loadConversations();
    }
  } catch {
    removeTyping();
    addMessage(
      "ai",
      "⚠️ Cannot reach backend. Make sure it is running on port 8000.",
    );
  }

  document.getElementById("send-btn").disabled = false;
}

async function checkBackendStatus() {
  try {
    const res = await fetch("http://localhost:8000/health");
    const dot = document.getElementById("backend-dot");
    const label = document.getElementById("backend-status");
    if (res.ok) {
      dot.className = "status-dot green";
      label.textContent = "Backend connected";
    } else {
      dot.className = "status-dot red";
      label.textContent = "Backend offline";
    }
  } catch {
    document.getElementById("backend-dot").className = "status-dot red";
    document.getElementById("backend-status").textContent = "Backend offline";
  }
}

window.addEventListener("load", loadConversations);
