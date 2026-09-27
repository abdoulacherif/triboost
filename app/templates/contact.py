from app.templates.shared import CSS_COMMUN, HTML_HEAD


HTML_CONTACT = (
    HTML_HEAD.format(title="Contact — TriBoost")
    + CSS_COMMUN
    + """
<style>
  .app {
    width: 100%; max-width: 480px;
    background: #fff; min-height: 100vh;
    padding-bottom: calc(40px + var(--safe-bottom));
    padding-top: var(--safe-top);
  }

  /* ===== TOPBAR ===== */
  .topbar {
    display: flex; align-items: center; gap: 12px;
    padding: 16px 20px;
  }
  .back-btn {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--green-light); color: var(--green);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .back-btn:active { transform: scale(0.92); }
  .topbar h1 { font-size: 18px; font-weight: 800; }

  /* ===== BANNIÈRE INACTIF ===== */
  .inactive-banner {
    display: none;
    margin: 0 20px 16px;
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border: 1.5px solid #ffb74d;
    border-radius: 16px;
    padding: 14px 16px;
    align-items: center; gap: 12px;
  }
  .inactive-banner.show { display: flex; }
  .inactive-banner .icon {
    width: 40px; height: 40px; border-radius: 12px;
    background: #ffe0b2; color: #e65100;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .inactive-banner .text { flex: 1; min-width: 0; }
  .inactive-banner .title { font-size: 13px; font-weight: 800; color: #e65100; margin-bottom: 2px; }
  .inactive-banner .desc { font-size: 11px; color: #bf360c; }
  .inactive-banner .action {
    background: #e65100; color: #fff;
    border: none; padding: 8px 12px;
    border-radius: 10px; font-size: 11px; font-weight: 700;
    cursor: pointer; flex-shrink: 0;
  }

  /* ===== HERO ===== */
  .contact-hero { text-align: center; padding: 12px 24px 20px; }
  .contact-hero-icon {
    width: 68px; height: 68px; border-radius: 50%;
    background: var(--green-light); color: var(--green);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 14px;
  }
  .contact-hero h2 { font-size: 18px; font-weight: 800; margin-bottom: 6px; }
  .contact-hero p { font-size: 13px; color: #757575; line-height: 1.5; }

  /* ===== LISTE CONTACTS ===== */
  .contacts-list { display: flex; flex-direction: column; gap: 14px; padding: 0 20px; }
  .contact-card {
    display: flex; align-items: center; gap: 14px;
    background: #fff; border: 1px solid var(--border);
    border-radius: 18px; padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }
  .contact-card-icon {
    width: 48px; height: 48px; border-radius: 14px;
    background: #e7f9ee; color: #25D366;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .contact-card-text { flex: 1; min-width: 0; }
  .contact-card-text .title { font-size: 15px; font-weight: 700; }
  .contact-card-text .desc {
    font-size: 12px; color: #757575; margin-top: 2px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .contact-actions { display: flex; flex-direction: column; gap: 6px; flex-shrink: 0; }
  .mini-btn {
    font-size: 11px; font-weight: 700;
    padding: 8px 12px; border-radius: 10px;
    border: none; cursor: pointer;
    font-family: inherit; white-space: nowrap;
  }
  .mini-btn:active { transform: scale(0.95); }
  .mini-btn-green { background: #25D366; color: #fff; }
  .mini-btn-outline { background: #f5f5f5; color: #616161; }

  .empty-state {
    text-align: center; padding: 30px 20px; color: #9e9e9e; font-size: 13px;
  }

  .download-all-wrap { padding: 0 20px 16px; }
  .download-all-btn {
    display: flex; align-items: center; justify-content: center; gap: 8px;
    width: 100%; background: #f5f5f5; color: #212121;
    border: none; padding: 13px; border-radius: 14px;
    font-weight: 700; font-size: 13px; cursor: pointer;
    font-family: inherit;
  }
  .download-all-btn:active { transform: scale(0.98); }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <button class="back-btn" onclick="window.location.href='/dashboard'" aria-label="Retour">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    <h1>Contact</h1>
  </header>

  <!-- BANNIÈRE INACTIF -->
  <div class="inactive-banner" id="inactiveBanner">
    <div class="icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
      </svg>
    </div>
    <div class="text">
      <div class="title">Compte non activé</div>
      <div class="desc">Activez votre compte pour contacter ou télécharger</div>
    </div>
    <button class="action" onclick="location.href='/activation'">Activer</button>
  </div>

  <div class="contact-hero">
    <div class="contact-hero-icon">
      <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
    </div>
    <h2>Nos contacts</h2>
    <p>Contactez directement l'un de nos représentants ou téléchargez sa fiche contact.</p>
  </div>

  <div class="download-all-wrap">
    <button class="download-all-btn" onclick="handleDownloadAll()">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="7 10 12 15 17 10"></polyline>
        <line x1="12" y1="15" x2="12" y2="3"></line>
      </svg>
      Télécharger tous les contacts
    </button>
  </div>

  <div class="contacts-list" id="contactsList"></div>
</div>

<script>
  // ===== LISTE DES CONTACTS (chargée depuis la base de données) =====
  let CONTACTS = [];

  async function loadContacts() {
    try {
      const res = await fetch('/api/contacts');
      if (!res.ok) throw new Error('Erreur chargement contacts');
      const data = await res.json();
      CONTACTS = data.contacts || [];
    } catch (err) {
      console.error('Erreur contacts:', err);
      CONTACTS = [];
    }
    renderContacts();
  }

  // ===== AUTH / ACTIVATION =====
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) {
    window.location.href = '/login';
  }

  let isActivated = false;

  async function loadActivationStatus() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (res.status === 401) {
        localStorage.clear();
        window.location.href = '/login';
        return;
      }
      if (!res.ok) { updateActivationUI(false); return; }
      const data = await res.json();
      const raw = data.profile.is_activated;
      isActivated = (raw === true || raw === "true" || raw === 1 || raw === "1");
      updateActivationUI(isActivated);
    } catch (err) {
      console.error('Erreur profil:', err);
      updateActivationUI(false);
    }
  }

  function updateActivationUI(activated) {
    const banner = document.getElementById('inactiveBanner');
    if (activated) banner.classList.remove('show');
    else banner.classList.add('show');
  }

  // ===== RENDU DES CONTACTS =====
  function renderContacts() {
    const container = document.getElementById('contactsList');
    if (!CONTACTS.length) {
      container.innerHTML = '<div class="empty-state">Aucun contact disponible pour le moment.</div>';
      return;
    }
    container.innerHTML = CONTACTS.map((c, i) => `
      <div class="contact-card">
        <div class="contact-card-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M17.6 6.32A7.85 7.85 0 0 0 12.05 4a7.94 7.94 0 0 0-6.9 11.9L4 20l4.2-1.1a7.9 7.9 0 0 0 3.85 1h.01a7.94 7.94 0 0 0 5.54-13.58zM12.06 18.4h-.01a6.5 6.5 0 0 1-3.32-.91l-.24-.14-2.47.65.66-2.41-.16-.25a6.53 6.53 0 1 1 5.54 3.06zm3.6-4.9c-.2-.1-1.17-.58-1.35-.64-.18-.07-.32-.1-.45.1-.13.2-.51.64-.63.77-.12.13-.23.15-.43.05a5.4 5.4 0 0 1-1.6-.99 6 6 0 0 1-1.1-1.37c-.12-.2 0-.31.09-.4.09-.09.2-.24.3-.36.1-.12.13-.2.2-.33.07-.13.03-.25-.02-.35-.05-.1-.45-1.08-.62-1.48-.16-.39-.33-.34-.45-.34h-.38c-.13 0-.35.05-.53.25-.18.2-.7.68-.7 1.66 0 .98.72 1.93.82 2.06.1.13 1.4 2.14 3.4 3 .47.2.84.32 1.13.42.47.15.9.13 1.24.08.38-.06 1.17-.48 1.33-.94.16-.46.16-.86.11-.94-.05-.08-.18-.13-.38-.23z"/></svg>
        </div>
        <div class="contact-card-text">
          <div class="title">${c.name}</div>
        </div>
        <div class="contact-actions">
          <button class="mini-btn mini-btn-green" onclick="handleContact(${i})">Contacter</button>
          <button class="mini-btn mini-btn-outline" onclick="handleDownload(${i})">Télécharger</button>
        </div>
      </div>
    `).join('');
  }

  // ===== ACTIONS (bloquées si non activé) =====
  function handleContact(i) {
    if (!isActivated) { showInactiveToast(); return; }
    const c = CONTACTS[i];
    window.open('https://wa.me/' + c.phone.replace(/[^0-9]/g, ''), '_blank');
  }

  function handleDownload(i) {
    if (!isActivated) { showInactiveToast(); return; }
    const c = CONTACTS[i];
    const vcard = 'BEGIN:VCARD\\nVERSION:3.0\\nFN:' + c.name +
      (c.business ? '\\nORG:' + c.business : '') +
      '\\nTEL;TYPE=CELL:' + c.phone +
      (c.city ? '\\nADR:;;' + c.city + ';' + (c.country || '') + ';;;' : '') +
      '\\nEND:VCARD';
    const blob = new Blob([vcard], { type: 'text/vcard' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = c.name.replace(/\\s+/g, '_') + '.vcf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function handleDownloadAll() {
    if (!isActivated) { showInactiveToast(); return; }
    if (!CONTACTS.length) return;
    const vcard = CONTACTS.map((c) =>
      'BEGIN:VCARD\\nVERSION:3.0\\nFN:' + c.name +
      (c.business ? '\\nORG:' + c.business : '') +
      '\\nTEL;TYPE=CELL:' + c.phone +
      (c.city ? '\\nADR:;;' + c.city + ';' + (c.country || '') + ';;;' : '') +
      '\\nEND:VCARD'
    ).join('\\n');
    const blob = new Blob([vcard], { type: 'text/vcard' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contacts_triboost.vcf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function showInactiveToast() {
    if (navigator.vibrate) navigator.vibrate([20, 40, 20]);
    const old = document.getElementById('inactiveToast');
    if (old) old.remove();

    const toast = document.createElement('div');
    toast.id = 'inactiveToast';
    toast.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: linear-gradient(135deg, #e65100, #bf360c);
      color: #fff; padding: 16px 20px; border-radius: 16px;
      font-size: 13px; font-weight: 600;
      box-shadow: 0 10px 30px rgba(230, 81, 0, 0.5);
      z-index: 10000; max-width: 340px; text-align: center; line-height: 1.5;
    `;
    toast.innerHTML = `
      <div style="font-size:24px; margin-bottom:6px;">🔒</div>
      <div><strong>Compte non activé</strong></div>
      <div style="font-size:12px; opacity:0.9; margin-top:4px;">
        Activez votre compte pour utiliser cette fonctionnalité
      </div>
      <button onclick="location.href='/activation'" style="
        margin-top:12px; background:#fff; color:#e65100;
        border:none; padding:10px 20px; border-radius:10px;
        font-weight:800; font-size:13px; cursor:pointer;
        font-family:inherit; width:100%;
      ">Activer maintenant</button>
      <button onclick="this.parentElement.remove()" style="
        margin-top:6px; background:transparent; color:#fff;
        border:1px solid rgba(255,255,255,0.4);
        padding:8px 20px; border-radius:10px;
        font-weight:600; font-size:12px; cursor:pointer;
        font-family:inherit; width:100%;
      ">Plus tard</button>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast?.remove(), 6000);
  }

  // ===== INIT =====
  loadContacts();
  loadActivationStatus();
</script>

</body>
</html>
"""
)
