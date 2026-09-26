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

  .item-img { width: 60px; height: 60px; border-radius: 10px; background: #e8f5e9; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; overflow: hidden; }
  .item-img img { width: 100%; height: 100%; object-fit: cover; }

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

  /* MODAL */
  #modalOverlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 99999; align-items: flex-end; justify-content: center; }
  #modalOverlay.open { display: flex; }
  #modalOverlay .content { background: #fff; border-radius: 24px 24px 0 0; padding: 20px 20px 40px; width: 100%; max-width: 480px; max-height: 92vh; overflow-y: auto; box-sizing: border-box; animation: slideUp 0.3s ease; }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-handle { width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; margin: 0 auto 16px; }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; color: var(--text-dark); }

  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: #212121; }
  .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; background: #fff; box-sizing: border-box; }
  .form-group textarea { min-height: 70px; resize: vertical; }

  /* IMAGE UPLOAD */
  .image-upload {
    width: 100%; height: 160px;
    border: 2px dashed #e0e0e0;
    border-radius: 14px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 8px; cursor: pointer; background: #fafafa;
    overflow: hidden; position: relative;
  }
  .image-upload:active { background: #f0f0f0; }
  .image-upload input { display: none; }
  .image-upload .label { font-size: 12px; color: #757575; font-weight: 600; }
  .image-upload img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .image-upload .remove-img {
    position: absolute; top: 8px; right: 8px;
    width: 32px; height: 32px;
    background: rgba(0,0,0,0.7); color: #fff;
    border: none; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 2; font-family: inherit; font-size: 14px;
  }
  .img-or-divider { text-align: center; font-size: 11px; color: #9e9e9e; margin: 10px 0; position: relative; }
  .img-or-divider::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: #f0f0f0; }
  .img-or-divider span { background: #fff; padding: 0 10px; position: relative; }

  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: #212121; }
  .modal-btn.confirm { background: #2e7d32; color: #fff; }
  .modal-btn.confirm:disabled { opacity: 0.6; cursor: not-allowed; }

  /* TOAST */
  .toast-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; display: flex; flex-direction: column; gap: 10px; pointer-events: none; width: 340px; max-width: 90vw; }
  .toast { padding: 16px 20px; border-radius: 16px; color: #fff; font-size: 14px; font-weight: 700; box-shadow: 0 10px 30px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 12px; pointer-events: auto; animation: toastIn 0.3s ease; line-height: 1.4; }
  .toast.success { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .toast.error { background: linear-gradient(135deg, #d32f2f, #b71c1c); }
  .toast.warning { background: linear-gradient(135deg, #f57c00, #e65100); }
  .toast.info { background: linear-gradient(135deg, #1976d2, #0d47a1); }
  .toast .toast-icon { font-size: 24px; flex-shrink: 0; }
  .toast .toast-text { flex: 1; min-width: 0; }
  .toast.out { animation: toastOut 0.3s forwards; }
  @keyframes toastIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes toastOut { to { opacity: 0; transform: translateY(-20px); } }
</style>
</head>
<body>

<div class="toast-container" id="toastContainer"></div>

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
      <input type="text" id="userSearch" placeholder="Rechercher..." oninput="loadUsers()">
    </div>
    <div class="list" id="usersList"><div class="empty">Chargement...</div></div>
  </div>

  <div class="tab-content" id="tab-market"><div class="list" id="marketList"><div class="empty">Chargement...</div></div></div>
  <div class="tab-content" id="tab-services"><div class="list" id="servicesList"><div class="empty">Chargement...</div></div></div>
  <div class="tab-content" id="tab-franchises"><div class="list" id="franchisesList"><div class="empty">Chargement...</div></div></div>

  <div class="tab-content" id="tab-formations">
    <div class="list" id="formationsList"><div class="empty">Chargement...</div></div>
    <button class="fab" onclick="openFormationModal()">+</button>
  </div>

  <div class="tab-content" id="tab-paths"><div class="list" id="pathsList"><div class="empty">Chargement...</div></div></div>

  <div style="height: 40px;"></div>
</div>

<!-- MODAL USER -->
<div id="modalOverlay" onclick="if(event.target===this) closeModal()">
  <div class="content" id="modalContent"></div>
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
  let formationImageBase64 = null;

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }

  function showToast(message, type) {
    type = type || 'success';
    const container = document.getElementById('toastContainer');
    const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML = '<div class="toast-icon">' + icons[type] + '</div><div class="toast-text">' + message + '</div>';
    container.appendChild(toast);
    if (navigator.vibrate) navigator.vibrate(type === 'error' ? [30, 50, 30] : 20);
    setTimeout(function() {
      toast.classList.add('out');
      setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
  }

  function closeModal() {
    document.getElementById('modalOverlay').classList.remove('open');
    document.body.style.overflow = '';
    formationImageBase64 = null;
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
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur</div>'; return; }
    const items = r.data.users || [];
    allUsersCache = items;
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun utilisateur</div>'; return; }

    list.innerHTML = items.map(u => {
      return '<div class="item ' + (u.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(u.full_name || 'Sans nom') + (u.is_admin ? ' ⭐' : '') + (u.is_banned ? ' 🚫' : '') + '</div>' +
        '<div class="item-sub">📞 ' + escapeHtml(u.phone || '-') + ' · 📍 ' + escapeHtml(u.country || '-') + '</div>' +
        '<div class="item-sub">🔗 ' + escapeHtml(u.referral_code || '-') + ' · 💰 ' + fmt(u.wallet_balance) + ' F</div>' +
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

    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">Modifier l'utilisateur</div>
      <div class="form-group">
        <label>Nom complet</label>
        <input type="text" id="editName" value="${escapeHtml(u.full_name || '')}">
      </div>
      <div class="form-group">
        <label>Téléphone</label>
        <input type="tel" id="editPhone" value="${escapeHtml(u.phone || '')}">
      </div>
      <div class="form-group">
        <label>Pays (2 lettres)</label>
        <input type="text" id="editCountry" maxlength="2" value="${escapeHtml(u.country || '')}">
      </div>
      <div class="form-group">
        <label>Code parrainage</label>
        <input type="text" id="editReferralCode" value="${escapeHtml(u.referral_code || '')}">
      </div>
      <div class="form-group">
        <label>Note admin</label>
        <textarea id="editAdminNote">${escapeHtml(u.admin_note || '')}</textarea>
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveUser()">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  async function saveUser() {
    const payload = {
      full_name: document.getElementById('editName').value.trim(),
      phone: document.getElementById('editPhone').value.trim(),
      country: document.getElementById('editCountry').value.trim().toUpperCase(),
      referral_code: document.getElementById('editReferralCode').value.trim(),
      admin_note: document.getElementById('editAdminNote').value.trim(),
    };
    const r = await apiCall('/api/admin/content/user/' + editingUserId + '/update', {
      method: 'POST', body: JSON.stringify(payload)
    });
    if (r.ok) {
      closeModal();
      showToast('Utilisateur mis à jour', 'success');
      loadUsers();
    } else {
      showToast(r.data.detail || 'Erreur', 'error');
    }
  }

  function toggleUserBan(uid, isBanned) {
    if (isBanned) {
      apiCall('/api/admin/content/user/' + uid + '/update', {
        method: 'POST', body: JSON.stringify({ is_banned: false })
      }).then(function() { showToast('Utilisateur débanni', 'success'); loadUsers(); });
    } else {
      currentBanAction = { type: 'user', id: uid };
      showBanModal();
    }
  }

  function showBanModal() {
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">Motif du blocage</div>
      <div class="form-group">
        <textarea id="banReason" placeholder="Expliquez..."></textarea>
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" style="background:#d32f2f" onclick="confirmBan()">Bloquer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function confirmBan() {
    const reason = document.getElementById('banReason').value.trim();
    if (currentBanAction.type === 'user') {
      await apiCall('/api/admin/content/user/' + currentBanAction.id + '/update', {
        method: 'POST', body: JSON.stringify({ is_banned: true, admin_note: reason })
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
    closeModal();
    showToast('Bloqué', 'warning');
    currentBanAction = null;
  }

  // ===== MARCHÉ =====
  async function loadMarket() {
    const list = document.getElementById('marketList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/market');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune annonce</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item ' + (i.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(i.user_name || '') + '</div>' +
        '<div class="item-sub">💰 ' + fmt(i.price) + ' F · 📱 ' + escapeHtml(i.whatsapp || '') + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_banned ? 'badge-banned' : 'badge-active') + '">' + (i.is_banned ? 'Banni' : 'Actif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        (i.is_banned ? '' : '<button class="btn-sm btn-warn" onclick="banMarket(\\'' + i.id + '\\')">🚫 Bloquer</button>') +
        '<button class="btn-sm btn-danger" onclick="deleteMarket(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  function banMarket(id) {
    currentBanAction = { type: 'market', id: id };
    showBanModal();
  }

  async function deleteMarket(id) {
    if (!confirm('Supprimer cette annonce ?')) return;
    await apiCall('/api/admin/content/market/' + id, { method: 'DELETE' });
    showToast('Annonce supprimée', 'info');
    loadMarket();
  }

  // ===== SERVICES =====
  async function loadServices() {
    const list = document.getElementById('servicesList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/services');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun service</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item ' + (i.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(i.user_name || '') + '</div>' +
        '<div class="item-sub">💰 ' + fmt(i.price) + ' F · 🎨 ' + escapeHtml(i.category || '') + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_banned ? 'badge-banned' : 'badge-active') + '">' + (i.is_banned ? 'Banni' : 'Actif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        (i.is_banned ? '' : '<button class="btn-sm btn-warn" onclick="banService(\\'' + i.id + '\\')">🚫 Bloquer</button>') +
        '<button class="btn-sm btn-danger" onclick="deleteService(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  function banService(id) {
    currentBanAction = { type: 'service', id: id };
    showBanModal();
  }

  async function deleteService(id) {
    if (!confirm('Supprimer ce service ?')) return;
    await apiCall('/api/admin/content/services/' + id, { method: 'DELETE' });
    showToast('Service supprimé', 'info');
    loadServices();
  }

  // ===== FRANCHISES =====
  async function loadFranchises() {
    const list = document.getElementById('franchisesList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/franchises');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune franchise</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">📍 ' + escapeHtml(i.city || '') + (i.quartier ? ' — ' + escapeHtml(i.quartier) : '') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(i.user_name || '') + '</div>' +
        '<div class="item-sub">💰 ' + fmt(i.price_paid) + ' F · Gains : ' + fmt(i.total_earned) + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_active ? 'badge-active' : 'badge-inactive') + '">' + (i.is_active ? 'Active' : 'Inactive') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-warn" onclick="toggleFranchise(\\'' + i.id + '\\')">' + (i.is_active ? '⏸ Désactiver' : '▶ Activer') + '</button>' +
        '<button class="btn-sm btn-danger" onclick="deleteFranchise(\\'' + i.id + '\\')">🗑</button>' +
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
    showToast('Franchise supprimée', 'info');
    loadFranchises();
  }

  // ===== FORMATIONS =====
  async function loadFormations() {
    const list = document.getElementById('formationsList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/formations');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune formation. Clique +</div>'; return; }

    list.innerHTML = items.map(i => {
      const img = i.cover_url ? '<img src="' + i.cover_url + '" alt="">' : '📚';
      return '<div class="item ' + (i.is_banned ? 'banned' : '') + '">' +
        '<div class="item-header">' +
        '<div class="item-img">' + img + '</div>' +
        '<div style="flex:1;min-width:0;margin-left:10px;">' +
        '<div class="item-title">' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">📚 ' + escapeHtml(i.category || '') + ' · ' + escapeHtml(i.duration || '-') + '</div>' +
        '<div class="item-sub">💰 ' + (i.is_free ? 'GRATUIT' : fmt(i.price) + ' F') + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_published ? 'badge-active' : 'badge-inactive') + '">' + (i.is_published ? 'Publiée' : 'Brouillon') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="editFormation(\\'' + i.id + '\\')">✏️ Modifier</button>' +
        '<button class="btn-sm btn-danger" onclick="deleteFormation(\\'' + i.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  function openFormationModal() {
    editingFormationId = null;
    formationImageBase64 = null;
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">Nouvelle formation</div>

      <div class="form-group">
        <label>Image de couverture</label>
        <label class="image-upload" id="imageUpload">
          <input type="file" accept="image/*" onchange="handleFormationImage(event)">
          <svg id="uploadIcon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#bdbdbd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span class="label" id="uploadLabel">📷 Toucher pour choisir une image</span>
        </label>
      </div>

      <div class="img-or-divider"><span>OU</span></div>

      <div class="form-group">
        <label>Lien d'image (URL)</label>
        <input type="url" id="fCover" placeholder="https://exemple.com/image.jpg" oninput="onUrlChange()">
      </div>

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
        <label>Lien du contenu (vidéo/PDF)</label>
        <input type="url" id="fContentUrl" placeholder="https://...">
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

      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" id="saveFormationBtn" onclick="saveFormation()">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function handleFormationImage(e) {
    const file = e.target.files[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      showToast('Image trop lourde (max 5 MB)', 'error');
      return;
    }
    const reader = new FileReader();
    reader.onload = function(ev) {
      formationImageBase64 = ev.target.result;
      const upload = document.getElementById('imageUpload');
      upload.querySelectorAll('img, .remove-img').forEach(el => el.remove());

      const img = document.createElement('img');
      img.src = formationImageBase64;
      upload.appendChild(img);

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'remove-img';
      btn.innerHTML = '✕';
      btn.onclick = function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        formationImageBase64 = null;
        img.remove();
        btn.remove();
        document.getElementById('uploadIcon').style.display = '';
        document.getElementById('uploadLabel').style.display = '';
      };
      upload.appendChild(btn);

      document.getElementById('uploadIcon').style.display = 'none';
      document.getElementById('uploadLabel').style.display = 'none';
      document.getElementById('fCover').value = '';
    };
    reader.readAsDataURL(file);
  }

  function onUrlChange() {
    const url = document.getElementById('fCover').value.trim();
    if (url) {
      formationImageBase64 = null;
      const upload = document.getElementById('imageUpload');
      upload.querySelectorAll('img, .remove-img').forEach(el => el.remove());
      document.getElementById('uploadIcon').style.display = 'none';
      document.getElementById('uploadLabel').style.display = 'none';

      const img = document.createElement('img');
      img.src = url;
      upload.appendChild(img);
    }
  }

  async function editFormation(id) {
    const r = await apiCall('/api/admin/content/formations');
    const f = (r.data.items || []).find(x => x.id === id);
    if (!f) return;

    editingFormationId = id;
    formationImageBase64 = null;

    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">Modifier la formation</div>

      <div class="form-group">
        <label>Image de couverture</label>
        <label class="image-upload" id="imageUpload">
          <input type="file" accept="image/*" onchange="handleFormationImage(event)">
          ${f.cover_url ? '' : '<svg id="uploadIcon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#bdbdbd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>'}
          <span class="label" id="uploadLabel" style="${f.cover_url ? 'display:none;' : ''}">📷 Toucher pour choisir une image</span>
        </label>
      </div>

      <div class="img-or-divider"><span>OU</span></div>

      <div class="form-group">
        <label>Lien d'image (URL)</label>
        <input type="url" id="fCover" value="${escapeHtml(f.cover_url || '')}" placeholder="https://...">
      </div>

      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="fTitle" value="${escapeHtml(f.title || '')}">
      </div>

      <div class="form-group">
        <label>Description</label>
        <textarea id="fDesc">${escapeHtml(f.description || '')}</textarea>
      </div>

      <div class="form-group">
        <label>Catégorie</label>
        <select id="fCategory">
          <option value="marketing" ${f.category === 'marketing' ? 'selected' : ''}>📣 Marketing</option>
          <option value="business" ${f.category === 'business' ? 'selected' : ''}>💼 Business</option>
          <option value="tech" ${f.category === 'tech' ? 'selected' : ''}>💻 Tech</option>
          <option value="finance" ${f.category === 'finance' ? 'selected' : ''}>💰 Finance</option>
          <option value="créatif" ${f.category === 'créatif' ? 'selected' : ''}>🎨 Créatif</option>
          <option value="développement" ${f.category === 'développement' ? 'selected' : ''}>🚀 Développement</option>
          <option value="autre" ${f.category === 'autre' ? 'selected' : ''}>📦 Autre</option>
        </select>
      </div>

      <div class="form-group">
        <label>Lien du contenu</label>
        <input type="url" id="fContentUrl" value="${escapeHtml(f.content_url || '')}">
      </div>

      <div class="form-group">
        <label>Durée</label>
        <input type="text" id="fDuration" value="${escapeHtml(f.duration || '')}">
      </div>

      <div class="form-group">
        <label>Niveau</label>
        <select id="fLevel">
          <option value="débutant" ${f.level === 'débutant' ? 'selected' : ''}>Débutant</option>
          <option value="intermédiaire" ${f.level === 'intermédiaire' ? 'selected' : ''}>Intermédiaire</option>
          <option value="avancé" ${f.level === 'avancé' ? 'selected' : ''}>Avancé</option>
        </select>
      </div>

      <div class="form-group">
        <label>Prix (FCFA)</label>
        <input type="number" id="fPrice" value="${f.price || 0}" min="0" step="500">
      </div>

      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" id="saveFormationBtn" onclick="saveFormation()">Enregistrer</button>
      </div>
    `;

    // Charger l'image existante
    if (f.cover_url) {
      const upload = document.getElementById('imageUpload');
      const img = document.createElement('img');
      img.src = f.cover_url;
      upload.appendChild(img);
    }

    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
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
      is_free: parseFloat(document.getElementById('fPrice').value) === 0,
      image_base64: formationImageBase64,
    };

    if (!payload.title) { showToast('Titre obligatoire', 'warning'); return; }

    const btn = document.getElementById('saveFormationBtn');
    btn.disabled = true;
    btn.textContent = 'Enregistrement...';

    const url = editingFormationId
      ? '/api/admin/content/formations/' + editingFormationId + '/update'
      : '/api/admin/content/formations/create';

    const r = await apiCall(url, { method: 'POST', body: JSON.stringify(payload) });

    btn.disabled = false;
    btn.textContent = 'Enregistrer';

    if (r.ok) {
      closeModal();
      showToast('Formation enregistrée !', 'success');
      loadFormations();
    } else {
      showToast(r.data.detail || 'Erreur', 'error');
    }
  }

  async function deleteFormation(id) {
    if (!confirm('Supprimer cette formation ?')) return;
    await apiCall('/api/admin/content/formations/' + id, { method: 'DELETE' });
    showToast('Formation supprimée', 'info');
    loadFormations();
  }

  // ===== PARCOURS =====
  async function loadPaths() {
    const list = document.getElementById('pathsList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/content/paths');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur</div>'; return; }
    const items = r.data.items || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun parcours</div>'; return; }

    list.innerHTML = items.map(i => {
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + (i.icon || '📚') + ' ' + escapeHtml(i.title || '') + '</div>' +
        '<div class="item-sub">' + escapeHtml(i.description || '') + '</div>' +
        '<div class="item-sub">💰 +' + fmt(i.reward_per_formation) + ' F/formation · 🏆 +' + fmt(i.bonus_final) + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + (i.is_active ? 'badge-active' : 'badge-inactive') + '">' + (i.is_active ? 'Actif' : 'Inactif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="editPath(\\'' + i.id + '\\')">✏️</button>' +
        '<button class="btn-sm btn-danger" onclick="deletePath(\\'' + i.id + '\\')">🗑</button>' +
        '</div></div>';
    }).join('');
  }

  async function editPath(id) {
    const r = await apiCall('/api/admin/content/paths');
    const p = (r.data.items || []).find(x => x.id === id);
    if (!p) return;

    const newTitle = prompt('Titre :', p.title || '');
    if (newTitle === null) return;
    const newReward = prompt('Récompense/formation :', p.reward_per_formation || 100);
    if (newReward === null) return;
    const newBonus = prompt('Bonus final :', p.bonus_final || 500);
    if (newBonus === null) return;

    await apiCall('/api/admin/content/paths/' + id + '/update', {
      method: 'POST',
      body: JSON.stringify({
        title: newTitle,
        reward_per_formation: parseFloat(newReward) || 0,
        bonus_final: parseFloat(newBonus) || 0,
      })
    });
    showToast('Parcours mis à jour', 'success');
    loadPaths();
  }

  async function deletePath(id) {
    if (!confirm('Supprimer ce parcours ?')) return;
    await apiCall('/api/admin/content/paths/' + id, { method: 'DELETE' });
    showToast('Parcours supprimé', 'info');
    loadPaths();
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

  loadUsers();
</script>
</body>
</html>
"""
)