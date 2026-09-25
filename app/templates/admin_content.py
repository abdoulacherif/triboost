from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ADMIN_CONTENT = (
    HTML_HEAD.format(title="Admin Contenu — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: rgba(255,255,255,0.1); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 16px; font-weight: 800; flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .tabs { display: flex; gap: 6px; padding: 12px 16px 0; overflow-x: auto; scrollbar-width: none; }
  .tabs::-webkit-scrollbar { display: none; }
  .tab { flex-shrink: 0; background: #fff; border: 1.5px solid #e0e0e0; color: #757575; padding: 10px 14px; border-radius: 12px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; white-space: nowrap; }
  .tab.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
  .tab-content { display: none; padding-top: 12px; }
  .tab-content.active { display: block; }

  .search-box { margin: 0 16px 12px; display: flex; align-items: center; gap: 8px; background: #fff; border-radius: 12px; padding: 10px 14px; }
  .search-box input { flex: 1; border: none; outline: none; font-size: 14px; font-family: inherit; background: transparent; }

  .list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .item { background: #fff; border-radius: 14px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .item.banned { opacity: 0.6; border-left: 4px solid #d32f2f; }
  .item-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 8px; }
  .item-title { font-size: 14px; font-weight: 800; color: #212121; flex: 1; min-width: 0; }
  .item-sub { font-size: 11px; color: #757575; margin-top: 2px; }
  .item-badge { font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px; white-space: nowrap; }
  .badge-active { background: #e8f5e9; color: #2e7d32; }
  .badge-inactive { background: #f5f5f5; color: #9e9e9e; }
  .badge-banned { background: #ffebee; color: #d32f2f; }

  .item-actions { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
  .btn-sm { border: none; padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 800; cursor: pointer; font-family: inherit; }
  .btn-edit { background: #e3f2fd; color: #1976d2; }
  .btn-warn { background: #fff3e0; color: #f57c00; }
  .btn-danger { background: #d32f2f; color: #fff; }
  .btn-approve { background: #2e7d32; color: #fff; }
  .btn-sm:active { transform: scale(0.95); }

  .empty { text-align: center; padding: 40px 20px; color: #757575; font-size: 13px; }

  .fab { position: fixed; bottom: calc(30px + var(--safe-bottom)); right: 20px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 8px 24px rgba(46,125,50,0.4); z-index: 90; }
  .fab:active { transform: scale(0.9); }

  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: flex-end; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 20px 20px 0 0; padding: 20px 20px calc(20px + var(--safe-bottom)); max-width: 480px; width: 100%; max-height: 90vh; overflow-y: auto; animation: slideUp 0.3s ease; }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; color: #212121; }
  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: #212121; }
  .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; background: #fff; }
  .form-group textarea { min-height: 70px; resize: vertical; }
  .form-group input:focus, .form-group textarea:focus { border-color: #2e7d32; }
  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: #212121; }
  .modal-btn.confirm { background: #2e7d32; color: #fff; }
  .modal-btn.danger { background: #d32f2f; color: #fff; }

  .switch-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
  .switch-row:last-child { border-bottom: none; }
  .switch-row span { font-size: 13px; font-weight: 600; color: #212121; }
  .switch { width: 44px; height: 26px; background: #e0e0e0; border-radius: 13px; position: relative; cursor: pointer; transition: background 0.2s; flex-shrink: 0; }
  .switch.on { background: #2e7d32; }
  .switch::after { content: ''; position: absolute; top: 3px; left: 3px; width: 20px; height: 20px; background: #fff; border-radius: 50%; transition: transform 0.2s; }
  .switch.on::after { transform: translateX(18px); }

  .debug-panel { position: fixed; bottom: 0; left: 0; right: 0; background: #1a1a1a; color: #0f0; font-family: monospace; font-size: 10px; padding: 10px; max-height: 180px; overflow-y: auto; z-index: 9999; display: none; border-top: 2px solid #0f0; }
  .debug-panel.show { display: block; }
  .debug-panel .line { margin-bottom: 3px; }
  .debug-panel .error { color: #f66; }
  .debug-panel .success { color: #0f0; }
  .debug-toggle { position: fixed; bottom: 100px; right: 16px; width: 44px; height: 44px; border-radius: 50%; background: #1a1a1a; color: #0f0; border: 2px solid #0f0; font-size: 18px; cursor: pointer; z-index: 9998; }
</style>
</head>
<body>

<div class="debug-panel" id="debugPanel">
  <div id="debugLog"></div>
</div>
<button class="debug-toggle" onclick="toggleDebug()">🐛</button>

<div class="app">
  <header class="topbar">
    <a href="/admin" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Modération</div>
    <div class="spacer"></div>
  </header>

  <div class="tabs">
    <button class="tab active" data-tab="users">👤 Users</button>
    <button class="tab" data-tab="market">🛒 Marché</button>
    <button class="tab" data-tab="services">🎨 Affaire</button>
    <button class="tab" data-tab="franchises">🏪 Boost</button>
    <button class="tab" data-tab="formations">📚 Boutique</button>
    <button class="tab" data-tab="paths">🎓 Parcours</button>
  </div>

  <div class="tab-content active" id="tab-users">
    <div class="search-box">
      <input type="text" id="userSearch" placeholder="Rechercher (nom, tél, code)..." oninput="loadUsers()">
    </div>
    <div class="list" id="usersList"><div class="empty">Chargement...</div></div>
  </div>

  <div class="tab-content" id="tab-market">
    <div class="list" id="marketList"><div class="empty">Chargement...</div></div>
  </div>

  <div class="tab-content" id="tab-services">
    <div class="list" id="servicesList"><div class="empty">Chargement...</div></div>
  </div>

  <div class="tab-content" id="tab-franchises">
    <div class="list" id="franchisesList"><div class="empty">Chargement...</div></div>
  </div>

  <div class="tab-content" id="tab-formations">
    <div class="list" id="formationsList"><div class="empty">Chargement...</div></div>
    <button class="fab" onclick="openFormationModal()" title="Nouvelle formation">+</button>
  </div>

  <div class="tab-content" id="tab-paths">
    <div class="list" id="pathsList"><div class="empty">Chargement...</div></div>
  </div>

  <div style="height: 40px;"></div>
</div>

<!-- MODAL USER -->
<div class="modal-overlay" id="userModal">
  <div class="modal-content">
    <div class="modal-title">Modifier l'utilisateur</div>
    <div class="form-group">
      <label>Nom complet</label>
      <input type="text" id="editName">
    </div>
    <div class="form-group">
      <label>Téléphone</label>
      <input type="tel" id="editPhone">
    </div>
    <div class="form-group">
      <label>Pays (2 lettres)</label>
      <input type="text" id="editCountry" maxlength="2" placeholder="Ex: CM">
    </div>
    <div class="form-group">
      <label>Code parrainage</label>
      <input type="text" id="editReferralCode">
    </div>
    <div class="form-group">
      <label>Note admin (visible dans le profil)</label>
      <textarea id="editAdminNote"></textarea>
    </div>
    <div class="switch-row">
      <span>Compte banni</span>
      <div class="switch" id="editBanned" onclick="this.classList.toggle('on')"></div>
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('userModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="saveUser()">Enregistrer</button>
    </div>
  </div>
</div>

<!-- MODAL BAN -->
<div class="modal-overlay" id="banModal">
  <div class="modal-content">
    <div class="modal-title">Motif du blocage</div>
    <div class="form-group">
      <textarea id="banReason" placeholder="Expliquez pourquoi..."></textarea>
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('banModal')">Annuler</button>
      <button class="modal-btn danger" onclick="confirmBan()">Bloquer</button>
    </div>
  </div>
</div>

<!-- MODAL FORMATION -->
<div class="modal-overlay" id="formationModal">
  <div class="modal-content">
    <div class="modal-title" id="formationModalTitle">Nouvelle formation</div>
    <div class="form-group">
      <label>Titre *</label>
      <input type="text" id="fTitle">
    </div>
    <div class="form-group">
      <label>Description</label>
      <textarea id="fDesc"></textarea>
    </div>
    <div class="form-group">
      <label>Catégorie</label>
      <select id="fCategory">
        <option value="marketing">📣 Marketing</option>
        <option value="business">💼 Business</option>
        <option value="tech">💻 Tech</option>
        <option value="finance">💰 Finance</option>
        <option value="créatif">🎨 Créatif</option>
        <option value="développement">🚀 Développement</option>
        <option value="autre" selected>📦 Autre</option>
      </select>
    </div>
    <div class="form-group">
      <label>Image de couverture (URL)</label>
      <input type="url" id="fCover">
    </div>
    <div class="form-group">
      <label>Lien contenu (vidéo/PDF/ressource)</label>
      <input type="url" id="fContentUrl">
    </div>
    <div class="form-group">
      <label>Durée</label>
      <input type="text" id="fDuration" placeholder="Ex: 2h30">
    </div>
    <div class="form-group">
      <label>Niveau</label>
      <select id="fLevel">
        <option value="débutant">Débutant</option>
        <option value="intermédiaire">Intermédiaire</option>
        <option value="avancé">Avancé</option>
      </select>
    </div>
    <div class="form-group">
      <label>Prix (FCFA) — 0 si gratuit</label>
      <input type="number" id="fPrice" value="0" min="0" step="500">
    </div>
    <div class="switch-row">
      <span>Formation gratuite</span>
      <div class="switch" id="fIsFree" onclick="this.classList.toggle('on')"></div>
    </div>
    <div class="switch-row">
      <span>Publiée</span>
      <div class="switch on" id="fIsPublished" onclick="this.classList.toggle('on')"></div>
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('formationModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="saveFormation()">Enregistrer</button>
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

  let editingUserId = null;
  let editingFormationId = null;
  let currentBanAction = null;
  let allUsersCache = [];

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }
  function openModal(id) { document.getElementById(id).classList.add('open'); }
  function toggleDebug() { document.getElementById('debugPanel').classList.toggle('show'); }

  function log(msg, type) {
    const c = document.getElementById('debugLog');
    if (!c) return;
    const cls = type === 'error' ? 'error' : (type === 'success' ? 'success' : '');
    c.innerHTML += '<div class="line ' + cls + '">' + msg + '</div>';
  }

  async function apiCall(url, options) {
    options = options || {};
    try {
      const res = await fetch(url, Object.assign({ headers: headers() }, options));
      const text = await res.text();
      let data;
      try { data = JSON.parse(text); } catch (e) { data = { error: 'Non-JSON' }; }
      return { ok: res.ok, status: res.status, data: data };
    } catch (e) {
      return { ok: false, status: 0, data: { error: e.message } };
    }
  }

  // ===== USERS =====
  async function loadUsers() {
    const list = document.getElementById('usersList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const search = (document.getElementById('userSearch')?.value || '').trim();
    let url = '/api/admin/users';
    if (search) url += '?search=' + encodeURIComponent(search);

    const r = await apiCall(url);
    if (!r.ok) {
      list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + ' : ' + (r.data.detail || '') + '</div>';
      return;
    }
    const items = r.data.users || [];
    allUsersCache = items;
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun utilisateur</div>'; return; }

    list.innerHTML = items.map(u => {
      return '<div class="item ' + (u.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(u.full_name || 'Sans nom') + (u.is_admin ? ' ⭐' : '') + (u.is_banned ? ' 🚫' : '') + '</div>' +
        '<div class="item-sub">📞 ' + escapeHtml(u.phone || '-') + ' · 📍 ' + escapeHtml(u.country || '-') + '</div>' +
        '<div class="item-sub">🔗 ' + escapeHtml(u.referral_code || '-') + ' · 💰 ' + Number(u.wallet_balance || 0).toLocaleString('fr-FR') + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + (u.is_activated ? 'badge-active' : 'badge-inactive') + '">' + (u.is_activated ? '✓' : 'Inactif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="openUserModal(\\'' + u.id + '\\')">✏️ Modifier</button>' +
        '<button class="btn-sm ' + (u.is_banned ? 'btn-approve' : 'btn-danger') + '" onclick="toggleUserBan(\\'' + u.id + '\\', ' + (u.is_banned ? 'true' : 'false') + ')">' + (u.is_banned ? '✓ Débannir' : '🚫 Bannir') + '</button>' +
        '</div></div>';
    }).join('');
  }

  function openUserModal(uid) {
    const u = allUsersCache.find(x => x.id === uid);
    if (!u) return;
    editingUserId = uid;
    document.getElementById('editName').value = u.full_name || '';
    document.getElementById('editPhone').value = u.phone || '';
    document.getElementById('editCountry').value = u.country || '';
    document.getElementById('editReferralCode').value = u.referral_code || '';
    document.getElementById('editAdminNote').value = u.admin_note || '';
    const sw = document.getElementById('editBanned');
    if (u.is_banned) sw.classList.add('on'); else sw.classList.remove('on');
    openModal('userModal');
  }

  async function saveUser() {
    const payload = {
      full_name: document.getElementById('editName').value.trim(),
      phone: document.getElementById('editPhone').value.trim(),
      country: document.getElementById('editCountry').value.trim().toUpperCase(),
      referral_code: document.getElementById('editReferralCode').value.trim(),
      admin_note: document.getElementById('editAdminNote').value.trim(),
      is_banned: document.getElementById('editBanned').classList.contains('on'),
    };
    const r = await apiCall('/api/admin/content/user/' + editingUserId + '/update', {
      method: 'POST', body: JSON.stringify(payload)
    });
    if (r.ok) {
      closeModal('userModal');
      loadUsers();
      alert('✅ Utilisateur mis à jour');
    } else {
      alert('⚠ ' + (r.data.detail || 'Erreur'));
    }
  }

  function toggleUserBan(uid, isBanned) {
    if (isBanned) {
      apiCall('/api/admin/content/user/' + uid + '/update', {
        method: 'POST', body: JSON.stringify({ is_banned: false })
      }).then(() => loadUsers());
    } else {
      currentBanAction = { type: 'user', id: uid };
      document.getElementById('banReason').value = '';
      openModal('banModal');
    }
  }

  // ===== MARCHÉ =====
  async function loadMarket() {
    const list = document.getElementById('marketList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/market');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune annonce</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item ' + (i.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(i.user_name || '') + '</div>' +
        '<div class="item-sub">💰 ' + Number(i.price || 0).toLocaleString('fr-FR') + ' F · 📱 ' + escapeHtml(i.whatsapp || '') + '</div>' +
        '<div class="item-sub">📍 ' + escapeHtml(i.city || '-') + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_banned ? 'badge-banned' : (i.is_active ? 'badge-active' : 'badge-inactive')) + '">' + (i.is_banned ? 'Banni' : (i.is_active ? 'Actif' : 'Inactif')) + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        (i.is_banned ? '' : '<button class="btn-sm btn-warn" onclick="banMarket(\\'' + i.id + '\\')">🚫 Bloquer</button>') +
        '<button class="btn-sm btn-danger" onclick="deleteMarket(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  function banMarket(id) {
    currentBanAction = { type: 'market', id: id };
    document.getElementById('banReason').value = '';
    openModal('banModal');
  }

  async function deleteMarket(id) {
    if (!confirm('Supprimer définitivement cette annonce ?')) return;
    await apiCall('/api/admin/content/market/' + id, { method: 'DELETE' });
    loadMarket();
  }

  // ===== SERVICES =====
  async function loadServices() {
    const list = document.getElementById('servicesList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/services');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun service</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item ' + (i.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(i.user_name || '') + '</div>' +
        '<div class="item-sub">💰 ' + Number(i.price || 0).toLocaleString('fr-FR') + ' F · 🎨 ' + escapeHtml(i.category || '') + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_banned ? 'badge-banned' : (i.is_active ? 'badge-active' : 'badge-inactive')) + '">' + (i.is_banned ? 'Banni' : 'Actif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        (i.is_banned ? '' : '<button class="btn-sm btn-warn" onclick="banService(\\'' + i.id + '\\')">🚫 Bloquer</button>') +
        '<button class="btn-sm btn-danger" onclick="deleteService(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  function banService(id) {
    currentBanAction = { type: 'service', id: id };
    document.getElementById('banReason').value = '';
    openModal('banModal');
  }

  async function deleteService(id) {
    if (!confirm('Supprimer ce service ?')) return;
    await apiCall('/api/admin/content/services/' + id, { method: 'DELETE' });
    loadServices();
  }

  // ===== FRANCHISES =====
  async function loadFranchises() {
    const list = document.getElementById('franchisesList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/franchises');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune franchise</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">📍 ' + escapeHtml(i.city || '') + (i.quartier ? ' — ' + escapeHtml(i.quartier) : '') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(i.user_name || '') + '</div>' +
        '<div class="item-sub">💰 Payé: ' + Number(i.price_paid || 0).toLocaleString('fr-FR') + ' F · Gains: ' + Number(i.total_earned || 0).toLocaleString('fr-FR') + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_active ? 'badge-active' : 'badge-inactive') + '">' + (i.is_active ? 'Active' : 'Inactive') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-warn" onclick="toggleFranchise(\\'' + i.id + '\\')">' + (i.is_active ? '⏸ Désactiver' : '▶ Activer') + '</button>' +
        '<button class="btn-sm btn-danger" onclick="deleteFranchise(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  async function toggleFranchise(id) {
    await apiCall('/api/admin/content/franchises/' + id + '/toggle', { method: 'POST' });
    loadFranchises();
  }

  async function deleteFranchise(id) {
    if (!confirm('Supprimer cette franchise ?')) return;
    await apiCall('/api/admin/content/franchises/' + id, { method: 'DELETE' });
    loadFranchises();
  }

  // ===== FORMATIONS =====
  async function loadFormations() {
    const list = document.getElementById('formationsList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/formations');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune formation. Clique sur + pour en créer.</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item ' + (i.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">📚 ' + escapeHtml(i.category || '') + ' · ' + escapeHtml(i.duration || '-') + ' · ' + escapeHtml(i.level || '') + '</div>' +
        '<div class="item-sub">💰 ' + (i.is_free ? 'GRATUIT' : Number(i.price || 0).toLocaleString('fr-FR') + ' F') + ' · 👁 ' + (i.views || 0) + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_published ? 'badge-active' : 'badge-inactive') + '">' + (i.is_published ? 'Publiée' : 'Brouillon') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="editFormation(\\'' + i.id + '\\')">✏️ Modifier</button>' +
        '<button class="btn-sm ' + (i.is_published ? 'btn-warn' : 'btn-approve') + '" onclick="toggleFormationPublish(\\'' + i.id + '\\', ' + (i.is_published ? 'true' : 'false') + ')">' + (i.is_published ? '⏸' : '▶') + '</button>' +
        '<button class="btn-sm btn-danger" onclick="deleteFormation(\\'' + i.id + '\\')">🗑</button>' +
        '</div></div>';
    }).join('');
  }

  function openFormationModal() {
    editingFormationId = null;
    document.getElementById('formationModalTitle').textContent = 'Nouvelle formation';
    document.getElementById('fTitle').value = '';
    document.getElementById('fDesc').value = '';
    document.getElementById('fCategory').value = 'autre';
    document.getElementById('fCover').value = '';
    document.getElementById('fContentUrl').value = '';
    document.getElementById('fDuration').value = '';
    document.getElementById('fLevel').value = 'débutant';
    document.getElementById('fPrice').value = '0';
    document.getElementById('fIsFree').classList.add('on');
    document.getElementById('fIsPublished').classList.add('on');
    openModal('formationModal');
  }

  async function editFormation(id) {
    const r = await apiCall('/api/admin/content/formations');
    const f = (r.data.items || []).find(x => x.id === id);
    if (!f) return;
    editingFormationId = id;
    document.getElementById('formationModalTitle').textContent = 'Modifier la formation';
    document.getElementById('fTitle').value = f.title || '';
    document.getElementById('fDesc').value = f.description || '';
    document.getElementById('fCategory').value = f.category || 'autre';
    document.getElementById('fCover').value = f.cover_url || '';
    document.getElementById('fContentUrl').value = f.content_url || '';
    document.getElementById('fDuration').value = f.duration || '';
    document.getElementById('fLevel').value = f.level || 'débutant';
    document.getElementById('fPrice').value = f.price || 0;
    if (f.is_free) document.getElementById('fIsFree').classList.add('on');
    else document.getElementById('fIsFree').classList.remove('on');
    if (f.is_published) document.getElementById('fIsPublished').classList.add('on');
    else document.getElementById('fIsPublished').classList.remove('on');
    openModal('formationModal');
  }

  async function saveFormation() {
    const payload = {
      title: document.getElementById('fTitle').value.trim(),
      description: document.getElementById('fDesc').value.trim(),
      category: document.getElementById('fCategory').value,
      cover_url: document.getElementById('fCover').value.trim(),
      content_url: document.getElementById('fContentUrl').value.trim(),
      duration: document.getElementById('fDuration').value.trim(),
      level: document.getElementById('fLevel').value,
      price: parseFloat(document.getElementById('fPrice').value) || 0,
      is_free: document.getElementById('fIsFree').classList.contains('on'),
      is_published: document.getElementById('fIsPublished').classList.contains('on'),
    };
    if (!payload.title) { alert('⚠ Titre obligatoire'); return; }

    const url = editingFormationId
      ? '/api/admin/content/formations/' + editingFormationId + '/update'
      : '/api/admin/content/formations/create';
    const r = await apiCall(url, { method: 'POST', body: JSON.stringify(payload) });
    if (r.ok) {
      closeModal('formationModal');
      loadFormations();
      alert('✅ Formation enregistrée');
    } else {
      alert('⚠ ' + (r.data.detail || 'Erreur'));
    }
  }

  async function toggleFormationPublish(id, isPublished) {
    await apiCall('/api/admin/content/formations/' + id + '/update', {
      method: 'POST', body: JSON.stringify({ is_published: !isPublished })
    });
    loadFormations();
  }

  async function deleteFormation(id) {
    if (!confirm('Supprimer cette formation ?')) return;
    await apiCall('/api/admin/content/formations/' + id, { method: 'DELETE' });
    loadFormations();
  }

  // ===== PARCOURS =====
  async function loadPaths() {
    const list = document.getElementById('pathsList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/paths');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun parcours</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + (i.icon || '📚') + ' ' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">' + escapeHtml(i.description || '') + '</div>' +
        '<div class="item-sub">💰 +' + Number(i.reward_per_formation || 0) + ' F/formation · 🏆 +' + Number(i.bonus_final || 0) + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_active ? 'badge-active' : 'badge-inactive') + '">' + (i.is_active ? 'Actif' : 'Inactif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="editPath(\\'' + i.id + '\\')">✏️ Modifier</button>' +
        '<button class="btn-sm btn-danger" onclick="deletePath(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  async function editPath(id) {
    const r = await apiCall('/api/admin/content/paths');
    const p = (r.data.items || []).find(x => x.id === id);
    if (!p) return;

    const newTitle = prompt('Titre du parcours :', p.title || '');
    if (newTitle === null) return;
    const newReward = prompt('Récompense par formation (FCFA) :', p.reward_per_formation || 100);
    if (newReward === null) return;
    const newBonus = prompt('Bonus final (FCFA) :', p.bonus_final || 500);
    if (newBonus === null) return;

    await apiCall('/api/admin/content/paths/' + id + '/update', {
      method: 'POST',
      body: JSON.stringify({
        title: newTitle,
        reward_per_formation: parseFloat(newReward) || 0,
        bonus_final: parseFloat(newBonus) || 0,
      })
    });
    loadPaths();
    alert('✅ Parcours mis à jour');
  }

  async function deletePath(id) {
    if (!confirm('Supprimer ce parcours ? Les formations liées seront retirées.')) return;
    await apiCall('/api/admin/content/paths/' + id, { method: 'DELETE' });
    loadPaths();
  }

  // ===== BAN =====
  async function confirmBan() {
    const reason = document.getElementById('banReason').value.trim();
    if (!currentBanAction) return;

    if (currentBanAction.type === 'user') {
      await apiCall('/api/admin/content/user/' + currentBanAction.id + '/update', {
        method: 'POST',
        body: JSON.stringify({ is_banned: true, admin_note: reason })
      });
      loadUsers();
    } else if (currentBanAction.type === 'market') {
      await apiCall('/api/admin/content/market/' + currentBanAction.id + '/ban', {
        method: 'POST', body: JSON.stringify({ reason: reason })
      });
      loadMarket();
    } else if (currentBanAction.type === 'service') {
      await apiCall('/api/admin/content/services/' + currentBanAction.id + '/ban', {
        method: 'POST', body: JSON.stringify({ reason: reason })
      });
      loadServices();
    }
    closeModal('banModal');
    currentBanAction = null;
    alert('✅ Bloqué');
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');

      const t = this.dataset.tab;
      if (t === 'users') loadUsers();
      else if (t === 'market') loadMarket();
      else if (t === 'services') loadServices();
      else if (t === 'franchises') loadFranchises();
      else if (t === 'formations') loadFormations();
      else if (t === 'paths') loadPaths();
    });
  });

  // ===== INIT =====
  loadUsers();
</script>
</body>
</html>
"""
)