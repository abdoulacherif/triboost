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

  .admin-badge { display: inline-block; background: var(--gold); color: #212121; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; margin-left: 6px; }

  /* Stats */
  .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 16px; }
  .stat-card { background: #fff; border-radius: 16px; padding: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); position: relative; overflow: hidden; }
  .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--green); }
  .stat-card.gold::before { background: var(--gold); }
  .stat-card.orange::before { background: var(--orange); }
  .stat-card.red::before { background: var(--red); }
  .stat-label { font-size: 10px; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  .stat-value { font-size: 20px; font-weight: 900; color: var(--text-dark); }

  /* Tabs */
  .tabs { display: flex; gap: 6px; padding: 0 16px; margin-bottom: 16px; overflow-x: auto; scrollbar-width: none; }
  .tabs::-webkit-scrollbar { display: none; }
  .tab { flex-shrink: 0; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 10px 14px; border-radius: 12px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; white-space: nowrap; }
  .tab.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* Search */
  .search-box { margin: 0 16px 12px; display: flex; align-items: center; gap: 8px; background: #fff; border-radius: 12px; padding: 10px 14px; }
  .search-box input { flex: 1; border: none; outline: none; font-size: 14px; font-family: inherit; background: transparent; }

  /* Filter chips */
  .filter-row { display: flex; gap: 6px; padding: 0 16px 12px; overflow-x: auto; scrollbar-width: none; }
  .filter-row::-webkit-scrollbar { display: none; }
  .f-chip { flex-shrink: 0; background: #fff; border: 1.5px solid var(--border); padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; cursor: pointer; font-family: inherit; color: var(--text-muted); }
  .f-chip.active { background: var(--green); color: #fff; border-color: var(--green); }

  /* List items */
  .list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .item { background: #fff; border-radius: 14px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .item-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 8px; }
  .item-title { font-size: 14px; font-weight: 800; color: var(--text-dark); flex: 1; min-width: 0; }
  .item-sub { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
  .item-badge { font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px; white-space: nowrap; }
  .badge-pending { background: #fff3e0; color: #e65100; }
  .badge-approved, .badge-completed { background: var(--green-light); color: var(--green); }
  .badge-rejected, .badge-failed { background: var(--red-light); color: var(--red); }
  .badge-active { background: var(--green-light); color: var(--green); }
  .badge-inactive { background: #f5f5f5; color: #9e9e9e; }
  .badge-admin { background: var(--gold-light); color: #f9a825; }

  .item-actions { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
  .btn-sm { border: none; padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 800; cursor: pointer; font-family: inherit; display: flex; align-items: center; gap: 4px; }
  .btn-approve { background: var(--green); color: #fff; }
  .btn-reject { background: var(--red-light); color: var(--red); }
  .btn-edit { background: var(--blue-light); color: var(--blue); }
  .btn-warn { background: var(--orange-light); color: var(--orange); }
  .btn-gold { background: var(--gold-light); color: #f9a825; }
  .btn-sm:active { transform: scale(0.95); }

  .empty { text-align: center; padding: 40px 20px; color: var(--text-muted); font-size: 13px; }

  /* Modal */
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: center; justify-content: center; padding: 20px; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 20px; padding: 24px; max-width: 340px; width: 100%; animation: scaleIn 0.3s ease; }
  @keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .modal-content input, .modal-content textarea { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; margin-bottom: 12px; outline: none; }
  .modal-content textarea { min-height: 80px; resize: vertical; }
  .modal-actions { display: flex; gap: 8px; margin-top: 12px; }
  .modal-btn { flex: 1; padding: 12px; border-radius: 10px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: var(--text-dark); }
  .modal-btn.confirm { background: var(--green); color: #fff; }

  .info-line { display: flex; justify-content: space-between; padding: 6px 0; font-size: 12px; border-bottom: 1px solid #f5f5f5; }
  .info-line span:first-child { color: var(--text-muted); }
  .info-line span:last-child { font-weight: 700; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </a>
    <div class="page-title">Admin <span class="admin-badge">PANEL</span></div>
    <div class="spacer"></div>
  </header>

  <div class="stats-grid" id="statsGrid">
    <div class="stat-card"><div class="stat-label">Utilisateurs</div><div class="stat-value" id="statUsers">-</div></div>
    <div class="stat-card gold"><div class="stat-label">Activés</div><div class="stat-value" id="statActivated">-</div></div>
    <div class="stat-card orange"><div class="stat-label">Tâches en attente</div><div class="stat-value" id="statTasks">-</div></div>
    <div class="stat-card red"><div class="stat-label">Retraits en attente</div><div class="stat-value" id="statWithdrawals">-</div></div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="users">👥 Utilisateurs</button>
    <button class="tab" data-tab="referrals">🌳 Parrainage</button>
    <button class="tab" data-tab="tasks">✅ Tâches</button>
    <button class="tab" data-tab="withdrawals">💸 Retraits</button>
    <button class="tab" data-tab="recharges">💰 Recharges</button>
  </div>

  <!-- UTILISATEURS -->
  <div class="tab-content active" id="tab-users">
    <div class="search-box">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9e9e9e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" id="userSearch" placeholder="Rechercher nom, email, téléphone..." oninput="filterUsers()">
    </div>
    <div class="filter-row">
      <button class="f-chip active" data-filter="all" onclick="setUserFilter(this, 'all')">Tous</button>
      <button class="f-chip" data-filter="activated" onclick="setUserFilter(this, 'activated')">Activés</button>
      <button class="f-chip" data-filter="inactive" onclick="setUserFilter(this, 'inactive')">Non activés</button>
      <button class="f-chip" data-filter="admin" onclick="setUserFilter(this, 'admin')">Admins</button>
    </div>
    <div class="list" id="usersList"><div class="empty">Chargement...</div></div>
  </div>

  <!-- PARRAINAGE -->
  <div class="tab-content" id="tab-referrals">
    <div class="list" id="referralsList"><div class="empty">Chargement...</div></div>
  </div>

  <!-- TÂCHES -->
  <div class="tab-content" id="tab-tasks">
    <div class="filter-row">
      <button class="f-chip active" data-tstatus="pending" onclick="setTaskFilter(this, 'pending')">En attente</button>
      <button class="f-chip" data-tstatus="approved" onclick="setTaskFilter(this, 'approved')">Approuvées</button>
      <button class="f-chip" data-tstatus="rejected" onclick="setTaskFilter(this, 'rejected')">Rejetées</button>
      <button class="f-chip" data-tstatus="all" onclick="setTaskFilter(this, 'all')">Toutes</button>
    </div>
    <div class="list" id="tasksList"><div class="empty">Chargement...</div></div>
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
    <div id="balanceInfo"></div>
    <input type="number" id="balanceInput" placeholder="Nouveau solde (FCFA)" step="100">
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
    <textarea id="rejectNote" placeholder="Expliquez la raison..."></textarea>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('rejectModal')">Annuler</button>
      <button class="modal-btn confirm" style="background:#d32f2f" onclick="confirmReject()">Rejeter</button>
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
  let taskFilter = 'pending';
  let withdrawFilter = 'pending';
  let rechargeFilter = 'pending';
  let currentAction = null;

  // ===== HEADERS =====
  function headers() {
    return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' };
  }

  // ===== STATS =====
  async function loadStats() {
    try {
      const res = await fetch('/api/admin/stats', { headers: headers() });
      if (res.status === 403) {
        document.body.innerHTML = '<div style="padding:60px 20px;text-align:center;"><h1 style="color:#d32f2f;">Accès refusé</h1><p>Cette page est réservée aux administrateurs.</p><a href="/dashboard" style="color:#2e7d32;">Retour</a></div>';
        return;
      }
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
        (u.referral_code || '').toLowerCase().includes(search)
      );
    }

    if (filtered.length === 0) {
      list.innerHTML = '<div class="empty">Aucun utilisateur</div>';
      return;
    }

    list.innerHTML = filtered.slice(0, 100).map(u => {
      const initials = (u.full_name || 'U').charAt(0).toUpperCase();
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
    document.getElementById('balanceModalTitle').textContent = 'Solde de ' + (name || 'cet utilisateur');
    document.getElementById('balanceInput').value = current;
    document.getElementById('balanceInfo').innerHTML =
      '<div class="info-line"><span>Solde actuel</span><span>' + Number(current).toLocaleString('fr-FR') + ' F</span></div>';
    document.getElementById('balanceModal').classList.add('open');
  }

  async function saveBalance() {
    const newBal = parseFloat(document.getElementById('balanceInput').value) || 0;
    try {
      const res = await fetch('/api/admin/users/' + currentAction + '/balance', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ balance: newBal })
      });
      if (!res.ok) throw new Error('Erreur');
      closeModal('balanceModal');
      loadUsers();
      alert('✅ Solde mis à jour');
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== ACTIVATION =====
  async function toggleActivation(uid) {
    if (!confirm('Changer le statut d\\'activation de cet utilisateur ?')) return;
    try {
      const res = await fetch('/api/admin/users/' + uid + '/toggle-activation', {
        method: 'POST', headers: headers()
      });
      if (!res.ok) throw new Error('Erreur');
      loadUsers();
      loadStats();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  // ===== REFERRALS =====
  async function loadReferrals() {
    const list = document.getElementById('referralsList');
    try {
      const res = await fetch('/api/admin/referrals', { headers: headers() });
      const data = await res.json();
      const refs = data.referrals || [];

      // Grouper par parrain
      const referrers = {};
      refs.forEach(r => {
        if (r.referrer) {
          const rid = r.referrer.id;
          if (!referrers[rid]) referrers[rid] = { referrer: r.referrer, filleuls: [] };
          referrers[rid].filleuls.push(r.user);
        }
      });

      const arr = Object.values(referrers).sort((a, b) => b.filleuls.length - a.filleuls.length);

      if (arr.length === 0) {
        list.innerHTML = '<div class="empty">Aucun parrainage enregistré</div>';
        return;
      }

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
          '</div>' +
          '</div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  // ===== TASKS =====
  async function loadTasks() {
    const list = document.getElementById('tasksList');
    try {
      const res = await fetch('/api/admin/tasks?status=' + taskFilter, { headers: headers() });
      const data = await res.json();
      const items = data.tasks || [];

      if (items.length === 0) {
        list.innerHTML = '<div class="empty">Aucune tâche ' + taskFilter + '</div>';
        return;
      }

      list.innerHTML = items.map(t => {
        const statusBadge = t.status === 'pending' ? 'badge-pending' : (t.status === 'approved' ? 'badge-approved' : 'badge-rejected');
        const statusLabel = t.status === 'pending' ? '⏳ En attente' : (t.status === 'approved' ? '✓ Approuvée' : '✗ Rejetée');
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
          '<span class="item-badge ' + statusBadge + '">' + statusLabel + '</span>' +
          '</div>' +
          (t.status === 'pending' ? '<div class="item-actions">' +
            '<button class="btn-sm btn-approve" onclick="reviewTask(\\'' + t.id + '\\', \\'approved\\')">✓ Approuver</button>' +
            '<button class="btn-sm btn-reject" onclick="openRejectTask(\\'' + t.id + '\\')">✗ Rejeter</button>' +
            '</div>' : '') +
          '</div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function setTaskFilter(el, f) {
    taskFilter = f;
    document.querySelectorAll('#tab-tasks .f-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    loadTasks();
  }

  async function reviewTask(id, status, note) {
    note = note || '';
    try {
      const res = await fetch('/api/admin/tasks/' + id + '/review', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ status: status, note: note })
      });
      if (!res.ok) throw new Error('Erreur');
      loadTasks();
      loadStats();
    } catch (e) { alert('⚠ ' + e.message); }
  }

  function openRejectTask(id) {
    currentAction = { type: 'task', id: id };
    document.getElementById('rejectNote').value = '';
    document.getElementById('rejectModal').classList.add('open');
  }

  // ===== WITHDRAWALS =====
  async function loadWithdrawals() {
    const list = document.getElementById('withdrawalsList');
    try {
      const res = await fetch('/api/admin/withdrawals?status=' + withdrawFilter, { headers: headers() });
      const data = await res.json();
      const items = data.withdrawals || [];

      if (items.length === 0) {
        list.innerHTML = '<div class="empty">Aucun retrait ' + withdrawFilter + '</div>';
        return;
      }

      list.innerHTML = items.map(w => {
        const statusBadge = w.status === 'pending' ? 'badge-pending' : (w.status === 'completed' ? 'badge-completed' : 'badge-rejected');
        const statusLabel = {pending: '⏳', processing: '🔄', completed: '✓', rejected: '✗'}[w.status] || w.status;
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">💸 ' + Number(w.amount).toLocaleString('fr-FR') + ' F</div>' +
          '<div class="item-sub">👤 ' + escapeHtml(w.full_name || 'User') + ' · ' + escapeHtml(w.user_name || '') + '</div>' +
          '<div class="item-sub">📱 ' + escapeHtml(w.operator || '') + ' · ' + escapeHtml(w.phone || '') + '</div>' +
          '<div class="item-sub">🌍 ' + escapeHtml(w.country || '') + ' · 📅 ' + formatDate(w.created_at) + '</div>' +
          '</div>' +
          '<span class="item-badge ' + statusBadge + '">' + statusLabel + '</span>' +
          '</div>' +
          (w.status === 'pending' ? '<div class="item-actions">' +
            '<button class="btn-sm btn-approve" onclick="reviewWithdrawal(\\'' + w.id + '\\', \\'completed\\')">✓ Valider</button>' +
            '<button class="btn-sm btn-reject" onclick="reviewWithdrawal(\\'' + w.id + '\\', \\'rejected\\')">✗ Rejeter</button>' +
            '</div>' : '') +
          '</div>';
      }).join('');
    } catch (e) { list.innerHTML = '<div class="empty">Erreur</div>'; }
  }

  function setWithdrawFilter(el, f) {
    withdrawFilter = f;
    document.querySelectorAll('#tab-withdrawals .f-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    loadWithdrawals();
  }

  async function reviewWithdrawal(id, status) {
    if (status === 'rejected') {
      currentAction = { type: 'withdrawal', id: id };
      document.getElementById('rejectNote').value = '';
      document.getElementById('rejectModal').classList.add('open');
      return;
    }
    if (!confirm('Valider ce retrait ? Le montant sera déduit définitivement.')) return;
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

  // ===== RECHARGES =====
  async function loadRecharges() {
    const list = document.getElementById('rechargesList');
    try {
      const res = await fetch('/api/admin/recharges?status=' + rechargeFilter, { headers: headers() });
      const data = await res.json();
      const items = data.recharges || [];

      if (items.length === 0) {
        list.innerHTML = '<div class="empty">Aucune recharge ' + rechargeFilter + '</div>';
        return;
      }

      list.innerHTML = items.map(r => {
        const statusBadge = r.status === 'pending' ? 'badge-pending' : (r.status === 'completed' ? 'badge-completed' : 'badge-failed');
        return '<div class="item">' +
          '<div class="item-header">' +
          '<div style="flex:1;min-width:0;">' +
          '<div class="item-title">💰 ' + Number(r.amount).toLocaleString('fr-FR') + ' F</div>' +
          '<div class="item-sub">👤 ' + escapeHtml(r.full_name || '') + ' · ' + escapeHtml(r.user_name || '') + '</div>' +
          '<div class="item-sub">📱 ' + escapeHtml(r.operator || '') + ' · ' + escapeHtml(r.phone || '') + '</div>' +
          '<div class="item-sub">📅 ' + formatDate(r.created_at) + '</div>' +
          '</div>' +
          '<span class="item-badge ' + statusBadge + '">' + r.status + '</span>' +
          '</div>' +
          (r.status === 'pending' ? '<div class="item-actions">' +
            '<button class="btn-sm btn-approve" onclick="confirmRecharge(\\'' + r.id + '\\')">✓ Valider manuellement</button>' +
            '</div>' : '') +
          '</div>';
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
    if (!confirm('Valider cette recharge ? Le montant sera crédité au wallet de l\\'utilisateur.')) return;
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

  // ===== REJECT MODAL =====
  async function confirmReject() {
    const note = document.getElementById('rejectNote').value.trim();
    if (!currentAction) return;

    try {
      if (currentAction.type === 'task') {
        await reviewTask(currentAction.id, 'rejected', note);
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

  // ===== HELPERS =====
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return d.toLocaleDateString('fr-FR') + ' ' + d.toLocaleTimeString('fr-FR', {hour:'2-digit', minute:'2-digit'});
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      if (this.dataset.tab === 'referrals') loadReferrals();
      if (this.dataset.tab === 'tasks') loadTasks();
      if (this.dataset.tab === 'withdrawals') loadWithdrawals();
      if (this.dataset.tab === 'recharges') loadRecharges();
    });
  });

  // ===== INIT =====
  (async function() {
    await loadStats();
    loadUsers();
  })();
</script>
</body>
</html>
"""
)