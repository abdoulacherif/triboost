from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ADMIN = (
    HTML_HEAD.format(title="Admin — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
    --blue: #1976d2;
    --blue-light: #e3f2fd;
  }
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: rgba(255,255,255,0.1); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; flex: 1; text-align: center; }
  .spacer { width: 40px; }
  .admin-badge { display: inline-block; background: #fbc02d; color: #212121; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; margin-left: 6px; }

  .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 16px; }
  .stat-card { background: #fff; border-radius: 16px; padding: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); position: relative; overflow: hidden; }
  .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #2e7d32; }
  .stat-card.gold::before { background: #fbc02d; }
  .stat-card.orange::before { background: #f57c00; }
  .stat-card.red::before { background: #d32f2f; }
  .stat-label { font-size: 10px; color: #757575; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  .stat-value { font-size: 20px; font-weight: 900; color: #212121; }

  .tabs { display: flex; gap: 6px; padding: 0 16px; margin-bottom: 16px; overflow-x: auto; scrollbar-width: none; }
  .tabs::-webkit-scrollbar { display: none; }
  .tab { flex-shrink: 0; background: #fff; border: 1.5px solid #e0e0e0; color: #757575; padding: 10px 14px; border-radius: 12px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; white-space: nowrap; }
  .tab.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .search-box { margin: 0 16px 12px; display: flex; align-items: center; gap: 8px; background: #fff; border-radius: 12px; padding: 10px 14px; }
  .search-box input { flex: 1; border: none; outline: none; font-size: 14px; font-family: inherit; background: transparent; }

  .filter-row { display: flex; gap: 6px; padding: 0 16px 12px; overflow-x: auto; scrollbar-width: none; }
  .filter-row::-webkit-scrollbar { display: none; }
  .f-chip { flex-shrink: 0; background: #fff; border: 1.5px solid #e0e0e0; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; cursor: pointer; font-family: inherit; color: #757575; }
  .f-chip.active { background: #2e7d32; color: #fff; border-color: #2e7d32; }

  .list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .item { background: #fff; border-radius: 14px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .item-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 8px; }
  .item-title { font-size: 14px; font-weight: 800; color: #212121; flex: 1; min-width: 0; }
  .item-sub { font-size: 11px; color: #757575; margin-top: 2px; }
  .item-badge { font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px; white-space: nowrap; }
  .badge-pending { background: #fff3e0; color: #e65100; }
  .badge-approved, .badge-completed { background: #e8f5e9; color: #2e7d32; }
  .badge-rejected, .badge-failed { background: #ffebee; color: #d32f2f; }
  .badge-active { background: #e8f5e9; color: #2e7d32; }
  .badge-inactive { background: #f5f5f5; color: #9e9e9e; }
  .badge-admin { background: #fff8e1; color: #f9a825; }

  .item-actions { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
  .btn-sm { border: none; padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 800; cursor: pointer; font-family: inherit; }
  .btn-approve { background: #2e7d32; color: #fff; }
  .btn-reject { background: #ffebee; color: #d32f2f; }
  .btn-edit { background: #e3f2fd; color: #1976d2; }
  .btn-warn { background: #fff3e0; color: #f57c00; }
  .btn-gold { background: #fff8e1; color: #f9a825; }
  .btn-danger { background: #d32f2f; color: #fff; }
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
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Admin <span class="admin-badge">PANEL</span></div>
    <div class="spacer"></div>
  </header>

  <div class="stats-grid">
    <div class="stat-card"><div class="stat-label">Utilisateurs</div><div class="stat-value" id="statUsers">-</div></div>
    <div class="stat-card gold"><div class="stat-label">Activés</div><div class="stat-value" id="statActivated">-</div></div>
    <div class="stat-card orange"><div class="stat-label">Tâches en attente</div><div class="stat-value" id="statTasks">-</div></div>
    <div class="stat-card red"><div class="stat-label">Retraits en attente</div><div class="stat-value" id="statWithdrawals">-</div></div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="users">👥 Users</button>
    <button class="tab" data-tab="referrals">🌳 Parrainage</button>
    <button class="tab" data-tab="submissions">✅ Soumissions</button>
    <button class="tab" data-tab="tasks">📋 Tâches</button>
    <button class="tab" data-tab="withdrawals">💸 Retraits</button>
    <button class="tab" data-tab="recharges">💰 Recharges</button>
  </div>

  <!-- USERS -->
  <div class="tab-content active" id="tab-users">
    <div class="search-box">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9e9e9e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" id="userSearch" placeholder="Rechercher..." oninput="filterUsers()">
    </div>
    <div class="filter-row">
      <button class="f-chip active" data-filter="all" onclick="setUserFilter(this, 'all')">Tous</button>
      <button class="f-chip" data-filter="activated" onclick="setUserFilter(this, 'activated')">Activés</button>
      <button class="f-chip" data-filter="inactive" onclick="setUserFilter(this, 'inactive')">Non activés</button>
      <button class="f-chip" data-filter="admin" onclick="setUserFilter(this, 'admin')">Admins</button>
    </div>
    <div class="list" id="usersList"><div class="empty">Chargement...</div></div>
  </div>

  <!-- REFERRALS -->
  <div class="tab-content" id="tab-referrals">
    <div class="list" id="referralsList"><div class="empty">Chargement...</div></div>
  </div>

  <!-- SOUMISSIONS -->
  <div class="tab-content" id="tab-submissions">
    <div class="filter-row">
      <button class="f-chip active" data-sstatus="pending" onclick="setSubFilter(this, 'pending')">En attente</button>
      <button class="f-chip" data-sstatus="approved" onclick="setSubFilter(this, 'approved')">Approuvées</button>
      <button class="f-chip" data-sstatus="rejected" onclick="setSubFilter(this, 'rejected')">Rejetées</button>
      <button class="f-chip" data-sstatus="all" onclick="setSubFilter(this, 'all')">Toutes</button>
    </div>
    <div class="list" id="submissionsList"><div class="empty">Chargement...</div></div>
  </div>

  <!-- TÂCHES (catalogue) -->
  <div class="tab-content" id="tab-tasks">
    <div class="list" id="tasksList"><div class="empty">Chargement...</div></div>
    <button class="fab" onclick="openTaskModal()" title="Nouvelle tâche">+</button>
  </div>

  <!-- RETRAITS -->
  <div class="tab-content" id="tab-withdrawals">
    <div class="filter-row">
      <button class="f-chip active" data-wstatus="pending" onclick="setWithdrawFilter(this, 'pending')">En attente</button>
      <button class="f-chip" data-wstatus="completed" onclick="setWithdrawFilter(this, 'completed')">Validés</button>
      <button class="f-chip" data-wstatus="rejected" onclick="setWithdrawFilter(this, 'rejected')">Rejetés</button>
      <button class="f-chip" data-wstatus="all" onclick="setWithdrawFilter(this, 'all')">Tous</button>
    </div>
    <div class="list" id="withdrawalsList"><div class="empty">Chargement...</div></div>
  </div>

  <!-- RECHARGES -->
  <div class="tab-content" id="tab-recharges">
    <div class="filter-row">
      <button class="f-chip active" data-rstatus="pending" onclick="setRechargeFilter(this, 'pending')">En attente</button>
      <button class="f-chip" data-rstatus="completed" onclick="setRechargeFilter(this, 'completed')">Validées</button>
      <button class="f-chip" data-rstatus="all" onclick="setRechargeFilter(this, 'all')">Toutes</button>
    </div>
    <div class="list" id="rechargesList"><div class="empty">Chargement...</div></div>
  </div>

  <div style="height: 40px;"></div>
</div>

<!-- MODAL SOLDE -->
<div class="modal-overlay" id="balanceModal">
  <div class="modal-content">
    <div class="modal-title" id="balanceModalTitle">Modifier le solde</div>
    <div class="form-group">
      <label>Nouveau solde (FCFA)</label>
      <input type="number" id="balanceInput" step="100">
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('balanceModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="saveBalance()">Enregistrer</button>
    </div>
  </div>
</div>

<!-- MODAL REJET -->
<div class="modal-overlay" id="rejectModal">
  <div class="modal-content">
    <div class="modal-title">Motif du rejet</div>
    <div class="form-group">
      <textarea id="rejectNote" placeholder="Expliquez..."></textarea>
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('rejectModal')">Annuler</button>
      <button class="modal-btn danger" onclick="confirmReject()">Rejeter</button>
    </div>
  </div>
</div>

<!-- MODAL TÂCHE (créer/modifier) -->
<div class="modal-overlay" id="taskModal">
  <div class="modal-content">
    <div class="modal-title" id="taskModalTitle">Nouvelle tâche</div>
    <div class="form-group">
      <label>Icône (emoji)</label>
      <input type="text" id="taskIcon" placeholder="🎯" value="🎯" maxlength="4">
    </div>
    <div class="form-group">
      <label>Titre *</label>
      <input type="text" id="taskTitle" placeholder="Ex: Vidéo TikTok">
    </div>
    <div class="form-group">
      <label>Description courte</label>
      <textarea id="taskDesc" placeholder="Ex: Fais une vidéo de 30s..."></textarea>
    </div>
    <div class="form-group">
      <label>Instructions détaillées</label>
      <textarea id="taskInstructions" placeholder="1. Étape 1...&#10;2. Étape 2..."></textarea>
    </div>
    <div class="form-group">
      <label>Réseau suggéré</label>
      <input type="text" id="taskNetwork" placeholder="Ex: TikTok">
    </div>
    <div class="form-group">
      <label>Récompense (FCFA) *</label>
      <input type="number" id="taskReward" value="300" min="50" step="50">
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('taskModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="saveTask()">Enregistrer</button>
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

  let allUsers = [];
  let userFilter = 'all';
  let subFilter = 'pending';
  let withdrawFilter = 'pending';
  let rechargeFilter = 'pending';
  let currentAction = null;
  let editingTaskId = null;

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function formatDate(iso) { if (!iso) return ''; const d = new Date(iso); return d.toLocaleDateString('fr-FR') + ' ' + d.toLocaleTimeString('fr-FR', {hour:'2-digit', minute:'2-digit'}); }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }
  function openModal(id) { document.getElementById(id).classList.add('open'); }

  // ===== STATS =====
  async function loadStats() {
    try {
      const res = await fetch('/api/admin/stats', { headers: headers() });
      if (res.status === 403) {
        document.body.innerHTML = '<div style="padding:60px 20px;text-align:center;"><h1 style="color:#d32f2f;">Accès refusé</h1><p>Réservé aux admins.</p><a href="/dashboard" style="color:#2e7d32;">Retour</a></div>';
        return;
      }
      if (!res.ok) return;
      const data = await res.json();
      document.getElementById('statUsers').textContent = data.stats.total_users || 0;
      document.getElementById('statActivated').textContent = data.stats.activated_users || 0;
      document.getElementById('statTasks').textContent = data.stats.tasks_pending || 0;
      document.getElementById('statWithdrawals').textContent = data.stats.withdrawals_pending || 0;
    } catch (e) { console.error(e); }
  }

  // ===== USERS =====
  async function loadUsers() {
    const list = document.getElementById('usersList');
    try {
      const res = await fetch('/api/admin/users', { headers: headers() });
      const data = await res.json();
      allUsers = data.users || [];
      renderUsers();
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function renderUsers() {
    const list = document.getElementById('usersList');
    const search = (document.getElementById('userSearch')?.value || '').toLowerCase();
    let filtered = allUsers;
    if (userFilter === 'activated') filtered = filtered.filter(u => u.is_activated);
    else if (userFilter === 'inactive') filtered = filtered.filter(u => !u.is_activated);
    else if (userFilter === 'admin') filtered = filtered.filter(u => u.is_admin);

    if (search) {
      filtered = filtered.filter(u =>
        (u.full_name || '').toLowerCase().includes(search) ||
        (u.email || '').toLowerCase().includes(search) ||
        (u.phone || '').toLowerCase().includes(search) ||
        (u.referral_code || '').toLowerCase().includes(search));
    }

    if (filtered.length === 0) { list.innerHTML = '<div class="empty">Aucun utilisateur</div>'; return; }

    list.innerHTML = filtered.slice(0, 100).map(u => {
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(u.full_name || 'Sans nom') + (u.is_admin ? ' <span class="badge-admin" style="padding:1px 6px;font-size:9px;border-radius:4px;">ADMIN</span>' : '') + '</div>' +
        '<div class="item-sub">' + escapeHtml(u.email || '') + '</div>' +
        '<div class="item-sub">📞 ' + escapeHtml(u.phone || '-') + ' · 📍 ' + escapeHtml(u.country || '-') + '</div>' +
        '<div class="item-sub">🔗 ' + escapeHtml(u.referral_code || '-') + ' · 💰 ' + Number(u.wallet_balance || 0).toLocaleString('fr-FR') + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + (u.is_activated ? 'badge-active' : 'badge-inactive') + '">' + (u.is_activated ? '✓ Activé' : 'Inactif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="openBalance(\\'' + u.id + '\\', \\'' + (u.full_name || '').replace(/'/g, '') + '\\', ' + (u.wallet_balance || 0) + ')">💰 Solde</button>' +
        '<button class="btn-sm ' + (u.is_activated ? 'btn-warn' : 'btn-approve') + '" onclick="toggleActivation(\\'' + u.id + '\\')">' + (u.is_activated ? '⏸ Désactiver' : '✓ Activer') + '</button>' +
        '</div>' +
        '</div>';
    }).join('');
  }

  function filterUsers() { renderUsers(); }
  function setUserFilter(el, f) {
    userFilter = f;
    document.querySelectorAll('#tab-users .f-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    renderUsers();
  }

  // ===== BALANCE =====
  function openBalance(uid, name, current) {
    currentAction = uid;
    document.getElementById('balanceModalTitle').textContent = 'Solde de ' + (name || 'User');
    document.getElementById('balanceInput').value = current;
    openModal('balanceModal');
  }

  async function saveBalance() {
    const newBal = parseFloat(document.getElementById('balanceInput').value) || 0;
    try {
      const res = await fetch('/api/admin/users/' + currentAction + '/balance', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ balance: newBal })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      closeModal('balanceModal');
      loadUsers();
      alert('✅ Solde mis à jour');
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== ACTIVATION =====
  async function toggleActivation(uid) {
    if (!confirm('Changer le statut ? Si tu actives, les commissions seront distribuées aux parrains.')) return;
    try {
      const res = await fetch('/api/admin/users/' + uid + '/toggle-activation', {
        method: 'POST', headers: headers()
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      loadUsers();
      loadStats();
      alert('✅ ' + (data.result?.message || 'Statut modifié'));
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== REFERRALS =====
  async function loadReferrals() {
    const list = document.getElementById('referralsList');
    try {
      const res = await fetch('/api/admin/referrals', { headers: headers() });
      const data = await res.json();
      const refs = data.referrals || [];
      const referrers = {};
      refs.forEach(r => {
        if (r.referrer) {
          const rid = r.referrer.id;
          if (!referrers[rid]) referrers[rid] = { referrer: r.referrer, filleuls: [] };
          referrers[rid].filleuls.push(r.user);
        }
      });
      const arr = Object.values(referrers).sort((a, b) => b.filleuls.length - a.filleuls.length);
      if (arr.length === 0) { list.innerHTML = '<div class="empty">Aucun parrainage</div>'; return; }
      list.innerHTML = arr.slice(0, 100).map(r => {
        const activated = r.filleuls.filter(f => f.is_activated).length;
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">🌳 ' + escapeHtml(r.referrer.full_name || 'Sans nom') + '</div>' +
          '<div class="item-sub">Code : ' + escapeHtml(r.referrer.referral_code || '-') + '</div>' +
          '<div class="item-sub">' + r.filleuls.length + ' filleul(s) · ' + activated + ' activé(s)</div>' +
          '</div>' +
          '<span class="item-badge badge-active">' + r.filleuls.length + '</span>' +
          '</div>' +
          '<div style="margin-top:10px;padding-top:10px;border-top:1px solid #f5f5f5;font-size:11px;color:#757575;">' +
          r.filleuls.slice(0, 5).map(f => '• ' + escapeHtml(f.full_name || 'Inconnu') + ' ' + (f.is_activated ? '✓' : '⏳')).join('<br>') +
          (r.filleuls.length > 5 ? '<br>... et ' + (r.filleuls.length - 5) + ' autres' : '') +
          '</div></div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  // ===== SOUMISSIONS DE TÂCHES =====
  async function loadSubmissions() {
    const list = document.getElementById('submissionsList');
    try {
      const res = await fetch('/api/admin/tasks?status=' + subFilter, { headers: headers() });
      const data = await res.json();
      const items = data.tasks || [];
      if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune soumission</div>'; return; }
      list.innerHTML = items.map(t => {
        const badge = t.status === 'pending' ? 'badge-pending' : (t.status === 'approved' ? 'badge-approved' : 'badge-rejected');
        const label = t.status === 'pending' ? '⏳ En attente' : (t.status === 'approved' ? '✓ Approuvée' : '✗ Rejetée');
        const taskInfo = t.tasks || {};
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">' + (taskInfo.icon || '🎯') + ' ' + escapeHtml(taskInfo.title || 'Tâche') + '</div>' +
          '<div class="item-sub">👤 ' + escapeHtml(t.user_name || 'User') + '</div>' +
          '<div class="item-sub">📱 ' + escapeHtml(t.network || '-') + ' · 💰 ' + Number(t.reward).toLocaleString('fr-FR') + ' F</div>' +
          '<div class="item-sub"><a href="' + escapeHtml(t.proof_url || '#') + '" target="_blank" style="color:#1976d2;">🔗 Voir la preuve</a></div>' +
          (t.comment ? '<div class="item-sub">💬 ' + escapeHtml(t.comment) + '</div>' : '') +
          '</div>' +
          '<span class="item-badge ' + badge + '">' + label + '</span>' +
          '</div>' +
          '<div class="item-actions">' +
          (t.status === 'pending' ? 
            '<button class="btn-sm btn-approve" onclick="reviewSub(\\'' + t.id + '\\', \\'approved\\')">✓ Approuver</button>' +
            '<button class="btn-sm btn-reject" onclick="openRejectSub(\\'' + t.id + '\\')">✗ Rejeter</button>' :
            '') +
          '<button class="btn-sm btn-danger" onclick="deleteSub(\\'' + t.id + '\\')">🗑 Supprimer</button>' +
          '</div></div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function setSubFilter(el, f) {
    subFilter = f;
    document.querySelectorAll('#tab-submissions .f-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    loadSubmissions();
  }

  async function reviewSub(id, status, note) {
    note = note || '';
    try {
      const res = await fetch('/api/admin/tasks/' + id + '/review', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ status: status, note: note })
      });
      if (!res.ok) throw new Error('Erreur');
      loadSubmissions();
      loadStats();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  function openRejectSub(id) {
    currentAction = { type: 'submission', id: id };
    document.getElementById('rejectNote').value = '';
    openModal('rejectModal');
  }

  async function deleteSub(id) {
    if (!confirm('Supprimer définitivement cette soumission ?')) return;
    try {
      const res = await fetch('/api/admin/submissions/' + id, { method: 'DELETE', headers: headers() });
      if (!res.ok) throw new Error('Erreur');
      loadSubmissions();
      loadStats();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== TÂCHES (catalogue) =====
  async function loadTasks() {
    const list = document.getElementById('tasksList');
    try {
      const res = await fetch('/api/admin/tasks-all', { headers: headers() });
      const data = await res.json();
      const items = data.tasks || [];
      if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune tâche. Clique sur + pour en créer.</div>'; return; }
      list.innerHTML = items.map(t => {
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">' + (t.icon || '🎯') + ' ' + escapeHtml(t.title || '') + '</div>' +
          '<div class="item-sub">' + escapeHtml(t.description || '') + '</div>' +
          '<div class="item-sub">💰 ' + Number(t.reward || 0).toLocaleString('fr-FR') + ' F · 📱 ' + escapeHtml(t.network_hint || '-') + '</div>' +
          '</div>' +
          '<span class="item-badge ' + (t.is_active ? 'badge-active' : 'badge-inactive') + '">' + (t.is_active ? 'Active' : 'Inactive') + '</span>' +
          '</div>' +
          '<div class="item-actions">' +
          '<button class="btn-sm btn-edit" onclick="editTask(\\'' + t.id + '\\')">✏️ Modifier</button>' +
          '<button class="btn-sm ' + (t.is_active ? 'btn-warn' : 'btn-approve') + '" onclick="toggleTask(\\'' + t.id + '\\', ' + t.is_active + ')">' + (t.is_active ? '⏸ Désactiver' : '▶ Activer') + '</button>' +
          '<button class="btn-sm btn-danger" onclick="deleteTask(\\'' + t.id + '\\')">🗑 Supprimer</button>' +
          '</div></div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function openTaskModal() {
    editingTaskId = null;
    document.getElementById('taskModalTitle').textContent = 'Nouvelle tâche';
    document.getElementById('taskIcon').value = '🎯';
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDesc').value = '';
    document.getElementById('taskInstructions').value = '';
    document.getElementById('taskNetwork').value = '';
    document.getElementById('taskReward').value = '300';
    openModal('taskModal');
  }

  async function editTask(id) {
    try {
      const res = await fetch('/api/admin/tasks-all', { headers: headers() });
      const data = await res.json();
      const t = (data.tasks || []).find(x => x.id === id);
      if (!t) return;
      editingTaskId = id;
      document.getElementById('taskModalTitle').textContent = 'Modifier la tâche';
      document.getElementById('taskIcon').value = t.icon || '🎯';
      document.getElementById('taskTitle').value = t.title || '';
      document.getElementById('taskDesc').value = t.description || '';
      document.getElementById('taskInstructions').value = t.instructions || '';
      document.getElementById('taskNetwork').value = t.network_hint || '';
      document.getElementById('taskReward').value = t.reward || 300;
      openModal('taskModal');
    } catch (e) { alert('⚠ Erreur'); }
  }

  async function saveTask() {
    const payload = {
      icon: document.getElementById('taskIcon').value || '🎯',
      title: document.getElementById('taskTitle').value.trim(),
      description: document.getElementById('taskDesc').value.trim(),
      instructions: document.getElementById('taskInstructions').value.trim(),
      network_hint: document.getElementById('taskNetwork').value.trim(),
      reward: parseFloat(document.getElementById('taskReward').value) || 0,
    };

    if (!payload.title || payload.reward <= 0) { alert('⚠ Titre et récompense obligatoires'); return; }

    try {
      const url = editingTaskId ? '/api/admin/tasks/' + editingTaskId + '/update' : '/api/admin/tasks/create';
      const res = await fetch(url, {
        method: 'POST', headers: headers(),
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      closeModal('taskModal');
      loadTasks();
      alert('✅ Tâche enregistrée');
    } catch (e) { alert('⚠ ' + e.message); }
  }

  async function toggleTask(id, isActive) {
    try {
      const res = await fetch('/api/admin/tasks/' + id + '/update', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ is_active: !isActive })
      });
      if (!res.ok) throw new Error('Erreur');
      loadTasks();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  async function deleteTask(id) {
    if (!confirm('Supprimer cette tâche ? Les soumissions associées seront aussi supprimées.')) return;
    try {
      const res = await fetch('/api/admin/tasks/' + id, { method: 'DELETE', headers: headers() });
      if (!res.ok) throw new Error('Erreur');
      loadTasks();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== RETRAITS =====
  async function loadWithdrawals() {
    const list = document.getElementById('withdrawalsList');
    try {
      const res = await fetch('/api/admin/withdrawals?status=' + withdrawFilter, { headers: headers() });
      const data = await res.json();
      const items = data.withdrawals || [];
      if (items.length === 0) { list.innerHTML = '<div class="empty">Aucun retrait</div>'; return; }
      list.innerHTML = items.map(w => {
        const badge = w.status === 'pending' ? 'badge-pending' : (w.status === 'completed' ? 'badge-completed' : 'badge-rejected');
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">💸 ' + Number(w.amount).toLocaleString('fr-FR') + ' F</div>' +
          '<div class="item-sub">👤 ' + escapeHtml(w.full_name || '') + ' · ' + escapeHtml(w.user_name || '') + '</div>' +
          '<div class="item-sub">📱 ' + escapeHtml(w.operator || '') + ' · ' + escapeHtml(w.phone || '') + '</div>' +
          '<div class="item-sub">🌍 ' + escapeHtml(w.country || '') + ' · 📅 ' + formatDate(w.created_at) + '</div>' +
          '</div>' +
          '<span class="item-badge ' + badge + '">' + w.status + '</span>' +
          '</div>' +
          '<div class="item-actions">' +
          (w.status === 'pending' ? 
            '<button class="btn-sm btn-approve" onclick="reviewWithdraw(\\'' + w.id + '\\', \\'completed\\')">✓ Valider</button>' +
            '<button class="btn-sm btn-reject" onclick="reviewWithdraw(\\'' + w.id + '\\', \\'rejected\\')">✗ Rejeter</button>' : '') +
          '<button class="btn-sm btn-danger" onclick="deleteWithdraw(\\'' + w.id + '\\')">🗑</button>' +
          '</div></div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function setWithdrawFilter(el, f) {
    withdrawFilter = f;
    document.querySelectorAll('#tab-withdrawals .f-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    loadWithdrawals();
  }

  async function reviewWithdraw(id, status) {
    if (status === 'rejected') {
      currentAction = { type: 'withdrawal', id: id };
      document.getElementById('rejectNote').value = '';
      openModal('rejectModal');
      return;
    }
    if (!confirm('Valider ce retrait ?')) return;
    try {
      const res = await fetch('/api/admin/withdrawals/' + id + '/review', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ status: status, note: '' })
      });
      if (!res.ok) throw new Error('Erreur');
      loadWithdrawals();
      loadStats();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  async function deleteWithdraw(id) {
    if (!confirm('Supprimer ce retrait de l\\'historique ?')) return;
    try {
      const res = await fetch('/api/admin/withdrawals/' + id, { method: 'DELETE', headers: headers() });
      if (!res.ok) throw new Error('Erreur');
      loadWithdrawals();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== RECHARGES =====
  async function loadRecharges() {
    const list = document.getElementById('rechargesList');
    try {
      const res = await fetch('/api/admin/recharges?status=' + rechargeFilter, { headers: headers() });
      const data = await res.json();
      const items = data.recharges || [];
      if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune recharge</div>'; return; }
      list.innerHTML = items.map(r => {
        const badge = r.status === 'pending' ? 'badge-pending' : (r.status === 'completed' ? 'badge-completed' : 'badge-failed');
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">💰 ' + Number(r.amount).toLocaleString('fr-FR') + ' F</div>' +
          '<div class="item-sub">👤 ' + escapeHtml(r.full_name || '') + ' · ' + escapeHtml(r.user_name || '') + '</div>' +
          '<div class="item-sub">📱 ' + escapeHtml(r.operator || '') + ' · ' + escapeHtml(r.phone || '') + '</div>' +
          '<div class="item-sub">📅 ' + formatDate(r.created_at) + '</div>' +
          '</div>' +
          '<span class="item-badge ' + badge + '">' + r.status + '</span>' +
          '</div>' +
          '<div class="item-actions">' +
          (r.status === 'pending' ? 
            '<button class="btn-sm btn-approve" onclick="confirmRecharge(\\'' + r.id + '\\')">✓ Valider</button>' : '') +
          '<button class="btn-sm btn-danger" onclick="deleteRecharge(\\'' + r.id + '\\')">🗑</button>' +
          '</div></div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function setRechargeFilter(el, f) {
    rechargeFilter = f;
    document.querySelectorAll('#tab-recharges .f-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    loadRecharges();
  }

  async function confirmRecharge(id) {
    if (!confirm('Valider cette recharge manuellement ?')) return;
    try {
      const res = await fetch('/api/admin/recharges/' + id + '/confirm', {
        method: 'POST', headers: headers()
      });
      if (!res.ok) throw new Error('Erreur');
      loadRecharges();
      loadStats();
      alert('✅ Recharge validée');
    } catch (e) { alert('⚠ ' + e.message); }
  }

  async function deleteRecharge(id) {
    if (!confirm('Supprimer cette recharge ?')) return;
    try {
      const res = await fetch('/api/admin/recharges/' + id, { method: 'DELETE', headers: headers() });
      if (!res.ok) throw new Error('Erreur');
      loadRecharges();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== REJECT MODAL =====
  async function confirmReject() {
    const note = document.getElementById('rejectNote').value.trim();
    if (!currentAction) return;
    try {
      if (currentAction.type === 'submission') {
        await reviewSub(currentAction.id, 'rejected', note);
      } else if (currentAction.type === 'withdrawal') {
        await fetch('/api/admin/withdrawals/' + currentAction.id + '/review', {
          method: 'POST', headers: headers(),
          body: JSON.stringify({ status: 'rejected', note: note })
        });
        loadWithdrawals();
        loadStats();
      }
      closeModal('rejectModal');
      currentAction = null;
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      if (this.dataset.tab === 'referrals') loadReferrals();
      if (this.dataset.tab === 'submissions') loadSubmissions();
      if (this.dataset.tab === 'tasks') loadTasks();
      if (this.dataset.tab === 'withdrawals') loadWithdrawals();
      if (this.dataset.tab === 'recharges') loadRecharges();
    });
  });

  (async function() {
    await loadStats();
    loadUsers();
  })();
</script>
</body>
</html>
"""
)