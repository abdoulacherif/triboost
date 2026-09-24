from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_AFFAIRE = (
    HTML_HEAD.format(title="Affaire — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
    --blue: #1976d2;
    --blue-light: #e3f2fd;
    --purple: #7b1fa2;
    --purple-light: #f3e5f5;
  }
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(100px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; position: relative; }

  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .inactive-banner { display: none; margin: 12px 16px; background: linear-gradient(135deg, #fff3e0, #ffe0b2); border: 1.5px solid #ffb74d; border-radius: 16px; padding: 12px 14px; align-items: center; gap: 10px; }
  .inactive-banner.show { display: flex; }
  .inactive-banner .icon { width: 36px; height: 36px; border-radius: 10px; background: #ffe0b2; color: #e65100; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .inactive-banner .text { flex: 1; min-width: 0; }
  .inactive-banner .title { font-size: 12px; font-weight: 800; color: #e65100; }
  .inactive-banner .desc { font-size: 10px; color: #bf360c; }
  .inactive-banner .action { background: #e65100; color: #fff; border: none; padding: 6px 10px; border-radius: 8px; font-size: 10px; font-weight: 700; cursor: pointer; flex-shrink: 0; }

  .hero { margin: 16px; background: linear-gradient(135deg, var(--green), var(--green-dark)); border-radius: 20px; padding: 20px; color: #fff; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3); }
  .hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .hero::after { content: ''; position: absolute; bottom: -40px; left: -40px; width: 120px; height: 120px; background: rgba(251, 192, 45, 0.2); border-radius: 50%; }
  .hero-content { position: relative; z-index: 2; }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 6px; }
  .hero-sub { font-size: 13px; opacity: 0.9; line-height: 1.5; }

  .tabs { display: flex; gap: 8px; padding: 0 16px; margin-bottom: 16px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; transition: all 0.2s; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25); }

  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .cat-chips { display: flex; gap: 8px; overflow-x: auto; padding: 0 16px 14px; scrollbar-width: none; }
  .cat-chips::-webkit-scrollbar { display: none; }
  .cat-chip { flex-shrink: 0; background: #fff; color: var(--text-muted); border: 1.5px solid var(--border); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; font-family: inherit; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
  .cat-chip.active { background: var(--green); color: #fff; border-color: var(--green); }

  .services-list { padding: 0 16px; display: flex; flex-direction: column; gap: 12px; }

  .service-card { background: #fff; border-radius: 18px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); animation: fadeIn 0.3s ease-out; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
  .sc-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 10px; }
  .sc-avatar { width: 48px; height: 48px; border-radius: 12px; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
  .sc-info { flex: 1; min-width: 0; }
  .sc-title { font-size: 14px; font-weight: 800; color: var(--text-dark); margin-bottom: 4px; line-height: 1.3; }
  .sc-cat { font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 6px; background: var(--purple-light); color: var(--purple); text-transform: uppercase; letter-spacing: 0.5px; }
  .sc-price { font-size: 18px; font-weight: 900; color: var(--green); white-space: nowrap; flex-shrink: 0; }
  .sc-desc { font-size: 12px; color: var(--text-muted); line-height: 1.5; margin-bottom: 12px; }
  .sc-footer { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
  .sc-meta { font-size: 11px; font-weight: 700; color: var(--text-muted); }
  .sc-btn { background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; border: none; padding: 10px 20px; border-radius: 12px; font-weight: 800; font-size: 13px; font-family: inherit; cursor: pointer; transition: transform 0.15s; text-decoration: none; display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3); }
  .sc-btn:active { transform: scale(0.95); }

  .reseller-hero { margin: 0 16px 16px; background: linear-gradient(135deg, var(--gold), #f9a825); border-radius: 20px; padding: 24px 20px; color: #212121; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(251, 192, 45, 0.3); }
  .reseller-hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.2); border-radius: 50%; }
  .reseller-hero h2 { font-size: 20px; font-weight: 900; margin-bottom: 8px; position: relative; z-index: 2; }
  .reseller-hero p { font-size: 13px; line-height: 1.5; position: relative; z-index: 2; margin-bottom: 16px; }
  .reseller-hero .btn { background: #212121; color: #fff; border: none; padding: 14px 20px; border-radius: 14px; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; width: 100%; position: relative; z-index: 2; box-shadow: 0 4px 14px rgba(0,0,0,0.2); }
  .reseller-hero .btn:active { transform: scale(0.98); }

  .reseller-stats { margin: 0 16px 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .rs-card { background: #fff; border-radius: 16px; padding: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.04); position: relative; overflow: hidden; }
  .rs-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--gold); }
  .rs-value { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 4px; }
  .rs-label { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

  .code-card { margin: 0 16px 16px; background: linear-gradient(135deg, #1a1a1a, #333); border-radius: 20px; padding: 20px; color: #fff; position: relative; overflow: hidden; }
  .code-card .label { font-size: 11px; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .code-card .code { font-size: 24px; font-family: 'Courier New', monospace; font-weight: 900; color: var(--gold); letter-spacing: 2px; margin-bottom: 14px; }
  .code-card .link-box { display: flex; gap: 8px; }
  .code-card input { flex: 1; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; padding: 10px 14px; color: #fff; font-size: 12px; outline: none; min-width: 0; }
  .code-card button { background: var(--gold); color: #212121; border: none; padding: 10px 16px; border-radius: 10px; font-weight: 800; font-size: 12px; cursor: pointer; font-family: inherit; white-space: nowrap; }

  .section-title { font-size: 15px; font-weight: 800; margin: 20px 16px 12px; color: var(--text-dark); display: flex; align-items: center; justify-content: space-between; }
  .section-title .right { font-size: 12px; color: var(--text-muted); font-weight: 600; }

  .sales-list { padding: 0 16px; display: flex; flex-direction: column; gap: 10px; }
  .sale-item { background: #fff; border-radius: 14px; padding: 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .sale-icon { width: 44px; height: 44px; border-radius: 12px; background: var(--gold-light); color: #f9a825; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
  .sale-info { flex: 1; min-width: 0; }
  .sale-title { font-size: 13px; font-weight: 700; color: var(--text-dark); margin-bottom: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .sale-date { font-size: 11px; color: var(--text-muted); }
  .sale-amount { font-size: 15px; font-weight: 900; color: var(--green); }

  .empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }
  .empty-state .icon { width: 64px; height: 64px; margin: 0 auto 12px; border-radius: 50%; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; }
  .empty-state h3 { font-size: 14px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  .fab { position: fixed; bottom: calc(30px + var(--safe-bottom)); right: 20px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(46, 125, 50, 0.4); z-index: 90; transition: transform 0.15s; }
  .fab:active { transform: scale(0.9); }

  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: flex-end; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal-content { width: 100%; max-width: 480px; background: #fff; border-radius: 24px 24px 0 0; max-height: 92vh; overflow-y: auto; padding: 20px 20px calc(20px + var(--safe-bottom)); animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-handle { width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; margin: 0 auto 16px; }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
  .modal-close { width: 32px; height: 32px; border-radius: 50%; background: #f5f5f5; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: var(--text-muted); }

  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: var(--text-dark); }
  .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px 14px; border: 1.5px solid var(--border); border-radius: 12px; font-size: 15px; font-family: inherit; color: var(--text-dark); outline: none; transition: border-color 0.2s; background: #fff; -webkit-appearance: none; }
  .form-group textarea { min-height: 80px; resize: vertical; }
  .form-group input:focus, .form-group textarea:focus, .form-group select:focus { border-color: var(--green); }
  .form-group select { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23757575' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>"); background-repeat: no-repeat; background-position: right 14px center; padding-right: 38px; }

  .modal-actions { display: flex; gap: 10px; margin-top: 20px; }
  .btn-cancel { flex: 1; background: #f5f5f5; color: var(--text-dark); border: none; padding: 14px; border-radius: 12px; font-weight: 700; font-size: 14px; font-family: inherit; cursor: pointer; }
  .btn-submit { flex: 2; background: var(--green); color: #fff; border: none; padding: 14px; border-radius: 12px; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }
  .btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

  .spinner { width: 18px; height: 18px; border: 2.5px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .skel-card { background: #fff; border-radius: 18px; padding: 16px; animation: pulse 1.4s infinite; }
  .skel-line { height: 12px; background: #f0f0f0; border-radius: 6px; margin-bottom: 10px; }
  .skel-line.short { width: 60%; }
  .skel-line.tiny { width: 40%; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </a>
    <div class="page-title">Affaire</div>
    <div class="spacer"></div>
  </header>

  <div class="inactive-banner" id="inactiveBanner">
    <div class="icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
    </div>
    <div class="text">
      <div class="title">Lecture seule</div>
      <div class="desc">Activez pour publier et vendre</div>
    </div>
    <button class="action" onclick="location.href='/activation'">Activer</button>
  </div>

  <div class="hero">
    <div class="hero-content">
      <div class="hero-title">💼 Développez votre business</div>
      <div class="hero-sub">Vendez vos services digitaux et devenez revendeur officiel TriBoost.</div>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="services">
      <span class="icon">🎨</span>
      Services
    </button>
    <button class="tab" data-tab="reseller">
      <span class="icon">🏆</span>
      Revendeur
    </button>
  </div>

  <!-- TAB SERVICES -->
  <div class="tab-content active" id="tab-services">
    <div class="cat-chips" id="catChips">
      <button class="cat-chip active" data-cat="tous">Tous</button>
      <button class="cat-chip" data-cat="design">🎨 Design</button>
      <button class="cat-chip" data-cat="dev">💻 Dev</button>
      <button class="cat-chip" data-cat="redaction">✍️ Rédaction</button>
      <button class="cat-chip" data-cat="video">🎬 Vidéo</button>
      <button class="cat-chip" data-cat="marketing">📣 Marketing</button>
      <button class="cat-chip" data-cat="autre">📦 Autre</button>
    </div>

    <div class="services-list" id="servicesList">
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div><div class="skel-line tiny"></div></div>
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div><div class="skel-line tiny"></div></div>
    </div>
  </div>

  <!-- TAB REVENDEUR -->
  <div class="tab-content" id="tab-reseller">
    <div id="resellerContent">
      <div class="skel-card" style="margin: 0 16px;"><div class="skel-line"></div><div class="skel-line short"></div></div>
    </div>
  </div>

  <button class="fab" id="fabAdd" onclick="openAddService()" aria-label="Ajouter un service">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
  </button>
</div>

<!-- MODAL AJOUT SERVICE -->
<div class="modal-overlay" id="addServiceModal" onclick="if(event.target===this) closeAddService()">
  <div class="modal-content">
    <div class="modal-handle"></div>
    <div class="modal-title">
      <span>Publier un service</span>
      <button class="modal-close" onclick="closeAddService()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>
    <div id="addError" class="alert error" style="display:none;"></div>
    <form id="addServiceForm" onsubmit="submitService(event)">
      <div class="form-group">
        <label>Titre du service *</label>
        <input type="text" id="svcTitle" required maxlength="80" placeholder="Ex : Création de logo professionnel">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="svcDesc" maxlength="300" placeholder="Décrivez votre service..."></textarea>
      </div>
      <div class="form-group">
        <label>Catégorie</label>
        <select id="svcCategory">
          <option value="design">🎨 Design</option>
          <option value="dev">💻 Développement</option>
          <option value="redaction">✍️ Rédaction</option>
          <option value="video">🎬 Vidéo</option>
          <option value="marketing">📣 Marketing</option>
          <option value="autre" selected>📦 Autre</option>
        </select>
      </div>
      <div class="form-group">
        <label>Prix (FCFA) *</label>
        <input type="number" id="svcPrice" required min="500" step="500" placeholder="Ex : 5000">
      </div>
      <div class="form-group">
        <label>Délai de livraison</label>
        <input type="text" id="svcDelay" maxlength="30" placeholder="Ex : 3 jours" value="3 jours">
      </div>
      <div class="form-group">
        <label>Lien portfolio (optionnel)</label>
        <input type="url" id="svcPortfolio" placeholder="https://...">
      </div>
      <div class="modal-actions">
        <button type="button" class="btn-cancel" onclick="closeAddService()">Annuler</button>
        <button type="submit" class="btn-submit" id="addBtn"><span>Publier</span></button>
      </div>
    </form>
  </div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) window.location.href = '/login';

  let isActivated = false;
  let currentCategory = 'tous';

  // ===== PROFIL =====
  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      const raw = data.profile?.is_activated;
      isActivated = (raw === true || raw === "true" || raw === 1 || raw === "1");
      if (!isActivated) document.getElementById('inactiveBanner').classList.add('show');
    } catch (e) {}
  }

  // ===== SERVICES =====
  async function loadServices(category = 'tous', search = '') {
    const list = document.getElementById('servicesList');
    list.innerHTML = '<div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div></div>';
    try {
      let url = '/api/affaires/services?t=' + Date.now();
      if (category && category !== 'tous') url += '&category=' + category;
      if (search) url += '&search=' + encodeURIComponent(search);

      const res = await fetch(url);
      const data = await res.json();
      if (!data.success || !data.services || data.services.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">🎨</div><h3>Aucun service</h3><p>Soyez le premier à proposer un service !</p></div>';
        return;
      }
      list.innerHTML = data.services.map(s => renderService(s)).join('');
    } catch (err) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3><p>' + err.message + '</p></div>';
    }
  }

  function renderService(s) {
    const price = Number(s.price || 0).toLocaleString('fr-FR');
    const catIcons = { design: '🎨', dev: '💻', redaction: '✍️', video: '🎬', marketing: '📣', autre: '📦' };
    const icon = catIcons[s.category] || '📦';
    const isMine = s.user_id === userId;
    return `
      <div class="service-card">
        <div class="sc-header">
          <div class="sc-avatar">${icon}</div>
          <div class="sc-info">
            <div class="sc-title">${escapeHtml(s.title)}</div>
            <span class="sc-cat">${escapeHtml(s.category)}</span>
          </div>
          <div class="sc-price">${price} F</div>
        </div>
        ${s.description ? `<div class="sc-desc">${escapeHtml(s.description)}</div>` : ''}
        <div class="sc-footer">
          <div class="sc-meta">⏱ ${escapeHtml(s.delivery_time || 'N/A')}${isMine ? ' · ✓ Mon service' : ''}</div>
          ${!isMine ? `<a href="https://wa.me/?text=${encodeURIComponent('Bonjour, je suis intéressé par votre service : ' + s.title)}" target="_blank" class="sc-btn">Contacter</a>` : ''}
        </div>
      </div>
    `;
  }

  // ===== REVENDEUR =====
  async function loadReseller() {
    const content = document.getElementById('resellerContent');
    try {
      const res = await fetch('/api/affaires/reseller/me?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();
      const r = data.reseller;

      if (!r) {
        content.innerHTML = `
          <div class="reseller-hero">
            <h2>🏆 Devenez revendeur TriBoost</h2>
            <p>Vendez les formations TriBoost en votre nom et gagnez <strong>30%</strong> de commission sur chaque vente.</p>
            <button class="btn" onclick="becomeReseller()">Devenir revendeur gratuitement</button>
          </div>
          <div style="padding: 0 16px;">
            <div class="section-title" style="margin-left: 0; margin-right: 0;"><span>💡 Comment ça marche ?</span></div>
            <div style="background: #fff; border-radius: 16px; padding: 16px; font-size: 13px; line-height: 1.8; color: var(--text-dark);">
              1. Cliquez sur "Devenir revendeur"<br>
              2. Recevez votre code unique<br>
              3. Partagez vos formations à votre réseau<br>
              4. Gagnez 30% sur chaque vente<br>
              5. Retirez vos gains dans votre wallet
            </div>
          </div>
        `;
        return;
      }

      // Charger les ventes
      let salesHTML = '';
      try {
        const salesRes = await fetch('/api/affaires/reseller/sales?t=' + Date.now(), {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        const salesData = await salesRes.json();
        const sales = salesData.sales || [];

        if (sales.length === 0) {
          salesHTML = '<div class="empty-state"><div class="icon">💰</div><h3>Aucune vente</h3><p>Partagez vos formations pour commencer.</p></div>';
        } else {
          salesHTML = sales.map(sale => `
            <div class="sale-item">
              <div class="sale-icon">💰</div>
              <div class="sale-info">
                <div class="sale-title">${escapeHtml(sale.formations?.title || 'Formation')}</div>
                <div class="sale-date">${formatDate(sale.created_at)}</div>
              </div>
              <div class="sale-amount">+${Number(sale.commission).toLocaleString('fr-FR')} F</div>
            </div>
          `).join('');
        }
      } catch (e) {}

      const baseUrl = window.location.origin;
      const refLink = baseUrl + '/register?reseller=' + r.reseller_code;

      content.innerHTML = `
        <div class="reseller-stats">
          <div class="rs-card">
            <div class="rs-value">${r.total_sales || 0}</div>
            <div class="rs-label">Ventes</div>
          </div>
          <div class="rs-card">
            <div class="rs-value">${Number(r.total_earned || 0).toLocaleString('fr-FR')} F</div>
            <div class="rs-label">Gains</div>
          </div>
        </div>

        <div class="code-card">
          <div class="label">Votre code revendeur</div>
          <div class="code">${escapeHtml(r.reseller_code)}</div>
          <div class="link-box">
            <input type="text" id="refLinkInput" value="${refLink}" readonly>
            <button onclick="copyRefLink()">Copier</button>
          </div>
        </div>

        <div class="section-title"><span>💰 Mes ventes</span><span class="right">${(salesData?.sales || []).length}</span></div>
        <div class="sales-list">${salesHTML}</div>
        <div style="height: 32px;"></div>
      `;
    } catch (err) {
      content.innerHTML = '<div class="empty-state"><h3>Erreur</h3><p>' + err.message + '</p></div>';
    }
  }

  async function becomeReseller() {
    if (!isActivated) { showInactiveToast(); return; }
    if (!confirm('Devenir revendeur TriBoost ? C\\'est gratuit.')) return;

    try {
      const res = await fetch('/api/affaires/reseller/become', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      vibrate(20);
      showToast('🎉 Vous êtes maintenant revendeur !');
      loadReseller();
    } catch (err) {
      alert('⚠ ' + err.message);
    }
  }

  function copyRefLink() {
    const input = document.getElementById('refLinkInput');
    if (!input) return;
    navigator.clipboard.writeText(input.value).then(() => {
      showToast('✅ Lien copié !');
    });
  }

  // ===== MODAL =====
  function openAddService() {
    if (!isActivated) { showInactiveToast(); return; }
    document.getElementById('addServiceModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeAddService() {
    document.getElementById('addServiceModal').classList.remove('open');
    document.body.style.overflow = '';
    document.getElementById('addServiceForm').reset();
  }

  async function submitService(e) {
    e.preventDefault();
    const btn = document.getElementById('addBtn');
    const errEl = document.getElementById('addError');
    errEl.style.display = 'none';

    const payload = {
      title: document.getElementById('svcTitle').value.trim(),
      description: document.getElementById('svcDesc').value.trim(),
      category: document.getElementById('svcCategory').value,
      price: parseFloat(document.getElementById('svcPrice').value) || 0,
      delivery_time: document.getElementById('svcDelay').value.trim() || '3 jours',
      portfolio_url: document.getElementById('svcPortfolio').value.trim(),
    };

    if (!payload.title || payload.price <= 0) {
      errEl.textContent = '⚠ Titre et prix valides requis';
      errEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/affaires/services', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      vibrate(20);
      closeAddService();
      showToast('✅ Service publié !');
      loadServices(currentCategory);
    } catch (err) {
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.innerHTML = '<span>Publier</span>';
    }
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      document.getElementById('fabAdd').style.display = this.dataset.tab === 'services' ? 'flex' : 'none';
      vibrate(5);
    });
  });

  // ===== CATÉGORIES =====
  document.querySelectorAll('.cat-chip').forEach(chip => {
    chip.addEventListener('click', function() {
      document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      currentCategory = this.dataset.cat;
      vibrate(5);
      loadServices(currentCategory);
    });
  });

  // ===== HELPERS =====
  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  }
  function formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const diff = (Date.now() - d) / 1000;
    if (diff < 3600) return Math.floor(diff / 60) + ' min';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h';
    if (diff < 604800) return Math.floor(diff / 86400) + 'j';
    return d.toLocaleDateString('fr-FR');
  }

  function showInactiveToast() {
    vibrate([20, 40, 20]);
    const old = document.getElementById('inactiveToast');
    if (old) old.remove();
    const t = document.createElement('div');
    t.id = 'inactiveToast';
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#e65100,#bf360c);color:#fff;padding:16px 20px;border-radius:16px;font-size:13px;font-weight:600;z-index:10000;box-shadow:0 10px 30px rgba(230,81,0,0.5);max-width:340px;text-align:center;line-height:1.5;';
    t.innerHTML = '<div style="font-size:24px;margin-bottom:6px;">🔒</div><div><strong>Compte non activé</strong></div><div style="font-size:12px;opacity:0.9;margin-top:4px;">Activez pour 3 600 FCFA</div><button onclick="location.href=\\'/activation\\'" style="margin-top:12px;background:#fff;color:#e65100;border:none;padding:10px 20px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;font-family:inherit;width:100%;">Activer maintenant</button>';
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 5000);
  }

  function showToast(msg) {
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#2e7d32,#1b5e20);color:#fff;padding:14px 20px;border-radius:14px;font-size:13px;font-weight:700;z-index:10001;box-shadow:0 8px 24px rgba(0,0,0,0.3);max-width:340px;text-align:center;';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  // ===== INIT =====
  (async () => {
    await loadProfile();
    loadServices();
    loadReseller();
  })();
</script>
</body>
</html>
"""
)