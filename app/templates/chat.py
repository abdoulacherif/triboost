from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_CHAT = (
    HTML_HEAD.format(title="Chat — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }

  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .tabs { display: flex; gap: 8px; padding: 0 16px 12px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 13px; font-weight: 700; font-family: inherit; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 4px; position: relative; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); }
  .tab .badge-count { position: absolute; top: 6px; right: 8px; background: #d32f2f; color: #fff; font-size: 10px; padding: 1px 5px; border-radius: 8px; font-weight: 800; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* CHAT */
  .chat-container { display: flex; flex-direction: column; height: calc(100vh - 220px); min-height: 400px; }
  .contacts-list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; overflow-y: auto; flex: 1; }
  .contact-item { background: #fff; border-radius: 14px; padding: 12px; display: flex; align-items: center; gap: 12px; cursor: pointer; transition: transform 0.15s; }
  .contact-item:active { transform: scale(0.98); }
  .contact-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; flex-shrink: 0; position: relative; }
  .contact-avatar .online { position: absolute; bottom: 0; right: 0; width: 12px; height: 12px; border-radius: 50%; background: #4caf50; border: 2px solid #fff; }
  .contact-info { flex: 1; min-width: 0; }
  .contact-name { font-size: 14px; font-weight: 700; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .contact-last { font-size: 12px; color: var(--text-muted); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .contact-badge { background: var(--green-light); color: var(--green); font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 6px; }

  /* CONVERSATION */
  .conv-header { padding: 12px 16px; background: #fff; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border); }
  .conv-back { width: 36px; height: 36px; border-radius: 50%; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }
  .conv-info { flex: 1; }
  .conv-name { font-size: 15px; font-weight: 800; color: var(--text-dark); }
  .conv-sub { font-size: 11px; color: var(--text-muted); }

  .messages-area { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 8px; background: #f5f5f5; }
  .msg-bubble { max-width: 75%; padding: 10px 14px; border-radius: 16px; font-size: 13px; line-height: 1.4; word-break: break-word; }
  .msg-bubble.sent { align-self: flex-end; background: var(--green); color: #fff; border-bottom-right-radius: 4px; }
  .msg-bubble.received { align-self: flex-start; background: #fff; color: var(--text-dark); border-bottom-left-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .msg-time { font-size: 9px; opacity: 0.7; margin-top: 4px; }
  .msg-bubble.sent .msg-time { color: rgba(255,255,255,0.8); }

  .msg-input-area { padding: 12px 16px; background: #fff; display: flex; gap: 8px; border-top: 1px solid var(--border); }
  .msg-input-area input { flex: 1; border: 1.5px solid var(--border); border-radius: 22px; padding: 12px 16px; font-size: 14px; font-family: inherit; outline: none; }
  .msg-input-area input:focus { border-color: var(--green); }
  .msg-send-btn { width: 44px; height: 44px; border-radius: 50%; background: var(--green); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }

  .empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 50px; margin-bottom: 12px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  /* SUPPORT */
  .support-container { padding: 0 16px; }
  .btn-new-ticket { width: 100%; background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; border: none; padding: 16px; border-radius: 14px; font-weight: 800; font-size: 15px; font-family: inherit; cursor: pointer; margin-bottom: 16px; box-shadow: 0 4px 14px rgba(46,125,50,0.3); }

  .ticket-item { background: #fff; border-radius: 14px; padding: 14px; margin-bottom: 10px; cursor: pointer; border-left: 4px solid #e0e0e0; }
  .ticket-item.open { border-left-color: #f57c00; }
  .ticket-item.answered { border-left-color: #2e7d32; }
  .ticket-item.closed { border-left-color: #9e9e9e; opacity: 0.7; }
  .ticket-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; }
  .ticket-subject { font-size: 14px; font-weight: 800; color: var(--text-dark); flex: 1; }
  .ticket-status { font-size: 9px; font-weight: 800; padding: 3px 8px; border-radius: 6px; text-transform: uppercase; }
  .ticket-status.open { background: #fff3e0; color: #e65100; }
  .ticket-status.answered { background: #e8f5e9; color: #2e7d32; }
  .ticket-status.closed { background: #f5f5f5; color: #9e9e9e; }
  .ticket-message { font-size: 12px; color: var(--text-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .ticket-date { font-size: 10px; color: var(--text-muted); margin-top: 6px; }

  /* Modal */
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: flex-end; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 20px 20px 0 0; padding: 20px 20px calc(20px + var(--safe-bottom)); max-width: 480px; width: 100%; max-height: 90vh; overflow-y: auto; animation: slideUp 0.3s ease; }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; }
  .form-group input, .form-group textarea { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; }
  .form-group textarea { min-height: 100px; resize: vertical; }
  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: var(--text-dark); }
  .modal-btn.confirm { background: var(--green); color: #fff; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Chat</div>
    <div class="spacer"></div>
  </header>

  <div class="tabs">
    <button class="tab active" data-tab="messages"><span class="icon">💬</span>Messages</button>
    <button class="tab" data-tab="support"><span class="icon">🎫</span>Support</button>
  </div>

  <!-- MESSAGES -->
  <div class="tab-content active" id="tab-messages">
    <div class="chat-container" id="chatContainer">
      <div class="contacts-list" id="contactsList">
        <div class="empty-state"><div class="icon">💬</div><h3>Chargement...</h3></div>
      </div>
    </div>
  </div>

  <!-- SUPPORT -->
  <div class="tab-content" id="tab-support">
    <div class="support-container">
      <button class="btn-new-ticket" onclick="openTicketModal()">🎫 Nouveau ticket</button>
      <div id="ticketsList">
        <div class="empty-state"><div class="icon">🎫</div><h3>Chargement...</h3></div>
      </div>
    </div>
  </div>

  <div style="height: 20px;"></div>
</div>

<!-- MODAL NOUVEAU TICKET -->
<div class="modal-overlay" id="ticketModal">
  <div class="modal-content">
    <div class="modal-title">🎫 Contacter le support</div>
    <div class="form-group">
      <label>Sujet *</label>
      <input type="text" id="ticketSubject" placeholder="Ex: Problème avec mon retrait" maxlength="100">
    </div>
    <div class="form-group">
      <label>Message *</label>
      <textarea id="ticketMessage" placeholder="Explique ton problème en détail..." maxlength="1000"></textarea>
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('ticketModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="submitTicket()">Envoyer</button>
    </div>
  </div>
</div>

<!-- MODAL DÉTAIL TICKET -->
<div class="modal-overlay" id="ticketDetailModal">
  <div class="modal-content">
    <div class="modal-title" id="detailSubject">Ticket</div>
    <div style="background: #f5f5f5; padding: 12px; border-radius: 10px; margin-bottom: 12px; font-size: 13px; line-height: 1.5;" id="detailMessage"></div>
    <div id="detailReply" style="display: none;">
      <div style="font-size: 12px; font-weight: 700; color: var(--green); margin-bottom: 6px;">📩 Réponse du support</div>
      <div style="background: var(--green-light); padding: 12px; border-radius: 10px; font-size: 13px; line-height: 1.5; color: var(--text-dark);" id="detailReplyText"></div>
    </div>
    <div class="modal-actions">
      <button class="modal-btn confirm" onclick="closeModal('ticketDetailModal')">Fermer</button>
    </div>
  </div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  let currentContactId = null;
  let currentContactName = '';

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }
  function openModal(id) { document.getElementById(id).classList.add('open'); }
  function timeAgo(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const diff = (Date.now() - d) / 1000;
    if (diff < 60) return 'à l\\'instant';
    if (diff < 3600) return Math.floor(diff / 60) + ' min';
    if (diff < 86400) return Math.floor(diff / 3600) + ' h';
    if (diff < 604800) return Math.floor(diff / 86400) + ' j';
    return d.toLocaleDateString('fr-FR');
  }
  function timeShort(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return d.getHours().toString().padStart(2, '0') + ':' + d.getMinutes().toString().padStart(2, '0');
  }

  // ===== CONTACTS (filleuls) =====
  async function loadContacts() {
    const list = document.getElementById('contactsList');
    try {
      const res = await fetch('/api/chat/contacts', { headers: headers() });
      const data = await res.json();
      const contacts = data.contacts || [];

      if (contacts.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">👥</div><h3>Aucun filleul</h3><p>Invitez des personnes pour pouvoir leur envoyer des messages.</p></div>';
        return;
      }

      list.innerHTML = contacts.map(c => {
        const initial = (c.full_name || 'U').charAt(0).toUpperCase();
        const last = c.last_message ? escapeHtml(c.last_message) : 'Démarrer la conversation';
        const date = c.last_date ? ' · ' + timeAgo(c.last_date) : '';
        return '<div class="contact-item" onclick="openConversation(\\'' + c.id + '\\', \\'' + (c.full_name || '').replace(/'/g, '') + '\\')">' +
          '<div class="contact-avatar">' + initial + (c.is_activated ? '<div class="online"></div>' : '') + '</div>' +
          '<div class="contact-info">' +
          '<div class="contact-name">' + escapeHtml(c.full_name || 'Sans nom') + '</div>' +
          '<div class="contact-last">' + last + date + '</div>' +
          '</div>' +
          '<span class="contact-badge">' + (c.is_activated ? '✓' : 'En attente') + '</span>' +
          '</div>';
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  // ===== CONVERSATION =====
  async function openConversation(contactId, contactName) {
    currentContactId = contactId;
    currentContactName = contactName;

    const container = document.getElementById('chatContainer');
    container.innerHTML = `
      <div class="conv-header">
        <button class="conv-back" onclick="closeConversation()">←</button>
        <div class="conv-info">
          <div class="conv-name">${escapeHtml(contactName)}</div>
          <div class="conv-sub">Filleul direct</div>
        </div>
      </div>
      <div class="messages-area" id="messagesArea">
        <div class="empty-state"><p>Chargement...</p></div>
      </div>
      <div class="msg-input-area">
        <input type="text" id="msgInput" placeholder="Écrire un message..." onkeypress="if(event.key==='Enter') sendMessage()">
        <button class="msg-send-btn" onclick="sendMessage()">➤</button>
      </div>
    `;

    await loadMessages();
  }

  async function loadMessages() {
    try {
      const res = await fetch('/api/chat/conversation/' + currentContactId, { headers: headers() });
      const data = await res.json();
      const messages = data.messages || [];
      const area = document.getElementById('messagesArea');

      if (messages.length === 0) {
        area.innerHTML = '<div class="empty-state"><div class="icon">💬</div><p>Aucun message. Envoyez le premier !</p></div>';
        return;
      }

      area.innerHTML = messages.map(m => {
        const isSent = m.sender_id === userId;
        return '<div class="msg-bubble ' + (isSent ? 'sent' : 'received') + '">' +
          escapeHtml(m.message) +
          '<div class="msg-time">' + timeShort(m.created_at) + '</div>' +
          '</div>';
      }).join('');

      area.scrollTop = area.scrollHeight;
    } catch (e) {
      console.error(e);
    }
  }

  async function sendMessage() {
    const input = document.getElementById('msgInput');
    const message = input.value.trim();
    if (!message) return;
    input.value = '';

    try {
      const res = await fetch('/api/chat/send', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ receiver_id: currentContactId, message: message })
      });
      if (!res.ok) throw new Error('Erreur');
      await loadMessages();
    } catch (e) {
      alert('⚠ Impossible d\\'envoyer le message');
    }
  }

  function closeConversation() {
    currentContactId = null;
    const container = document.getElementById('chatContainer');
    container.innerHTML = '<div class="contacts-list" id="contactsList"><div class="empty-state"><p>Chargement...</p></div></div>';
    loadContacts();
  }

  // ===== SUPPORT =====
  async function loadTickets() {
    const list = document.getElementById('ticketsList');
    try {
      const res = await fetch('/api/chat/support/tickets', { headers: headers() });
      const data = await res.json();
      const tickets = data.tickets || [];

      if (tickets.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">🎫</div><h3>Aucun ticket</h3><p>Créez un ticket pour contacter le support.</p></div>';
        return;
      }

      list.innerHTML = tickets.map(t => {
        return '<div class="ticket-item ' + t.status + '" onclick="openTicket(\\'' + t.id + '\\')">' +
          '<div class="ticket-header">' +
          '<div class="ticket-subject">' + escapeHtml(t.subject || '') + '</div>' +
          '<span class="ticket-status ' + t.status + '">' + t.status + '</span>' +
          '</div>' +
          '<div class="ticket-message">' + escapeHtml(t.message || '') + '</div>' +
          '<div class="ticket-date">📅 ' + timeAgo(t.created_at) + '</div>' +
          '</div>';
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  function openTicketModal() {
    document.getElementById('ticketSubject').value = '';
    document.getElementById('ticketMessage').value = '';
    openModal('ticketModal');
  }

  async function submitTicket() {
    const subject = document.getElementById('ticketSubject').value.trim();
    const message = document.getElementById('ticketMessage').value.trim();

    if (!subject || !message) {
      alert('⚠ Sujet et message obligatoires');
      return;
    }

    try {
      const res = await fetch('/api/chat/support/tickets', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ subject: subject, message: message })
      });
      if (!res.ok) throw new Error('Erreur');
      closeModal('ticketModal');
      loadTickets();
      alert('✅ Ticket envoyé ! Réponse sous 24h.');
    } catch (e) {
      alert('⚠ Erreur');
    }
  }

  let ticketsCache = [];
  async function openTicket(ticketId) {
    try {
      const res = await fetch('/api/chat/support/tickets', { headers: headers() });
      const data = await res.json();
      const ticket = (data.tickets || []).find(t => t.id === ticketId);
      if (!ticket) return;

      document.getElementById('detailSubject').textContent = ticket.subject;
      document.getElementById('detailMessage').textContent = ticket.message;

      const replyDiv = document.getElementById('detailReply');
      if (ticket.admin_reply) {
        document.getElementById('detailReplyText').textContent = ticket.admin_reply;
        replyDiv.style.display = 'block';
      } else {
        replyDiv.style.display = 'none';
      }

      openModal('ticketDetailModal');
    } catch (e) {}
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      if (this.dataset.tab === 'support') loadTickets();
    });
  });

  // ===== INIT =====
  loadContacts();
</script>
</body>
</html>
"""
)