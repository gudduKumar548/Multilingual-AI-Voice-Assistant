const API_BASE = "http://localhost:8000";

function getToken() {
  return localStorage.getItem("lingua_token");
}

function authHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${getToken()}`,
  };
}

const API = {
  async register(username, email, password) {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });
    return { ok: res.ok, data: await res.json() };
  },

  async login(username, password) {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      body: form,
    });
    return { ok: res.ok, data: await res.json() };
  },

  async sendMessage(message, targetLanguage, conversationId = null) {
    const res = await fetch(`${API_BASE}/api/chat/send`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        message,
        target_language: targetLanguage,
        conversation_id: conversationId,
      }),
    });
    return { ok: res.ok, status: res.status, data: await res.json() };
  },

  async getConversations() {
    const res = await fetch(`${API_BASE}/api/chat/conversations`, {
      headers: authHeaders(),
    });
    return { ok: res.ok, data: await res.json() };
  },

  async getConversationMessages(convId) {
    const res = await fetch(`${API_BASE}/api/chat/messages/${convId}`, {
      headers: authHeaders(),
    });
    return { ok: res.ok, data: await res.json() };
  },

  async deleteConversation(convId) {
    const res = await fetch(`${API_BASE}/api/chat/messages/${convId}`, {
      method: "DELETE",
      headers: authHeaders(),
    });
    return { ok: res.ok };
  },

  async health() {
    try {
      const res = await fetch(`${API_BASE}/health`);
      return res.ok;
    } catch {
      return false;
    }
  },
};
