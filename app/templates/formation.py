from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_FORMATION = (
    HTML_HEAD.format(title="Formation — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
  }
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .hero { margin: 16px; background: linear-gradient(135deg, var(--green), var(--green-dark)); border-radius: 20px; padding: 20px; color: #fff; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3); }
  .hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 6px; }
  .hero-sub { font-size: 13px; opacity: 0.9; line-height: 1.5; }

  .tabs { display: flex; gap: 8px; padding: 0 16px; margin-bottom: 16px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* ===== PARCOURS ===== */
  .paths-list { padding: 0 16px; display: flex; flex-direction: column; gap: 14px; }
  .path-card { background: #fff; border-radius: 20px; padding: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); position: relative; overflow: hidden; }
  .path-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; }
  .path-card.green::before { background: linear-gradient(90deg, #2e7d32, #4caf50); }
  .path-card.gold::before { background: linear-gradient(90deg, #fbc02d, #f57c00); }
  .path-card.orange::before { background: linear-gradient(90deg, #f57c00, #e65100); }
  .path-card.purple::before { background: linear-gradient(90deg, #7b1fa2, #9c27b0); }

  .path-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
  .path-icon { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; background: var(--green-light); }
  .path-card.gold .path-icon { background: #fff8e1; }
  .path-card.orange .path-icon { background: #fff3e0; }
  .path-card.purple .path-icon { background: #f3e5f5; }

  .path-info { flex: 1; min-width: 0; }
  .path-title { font-size: 16px; font-weight: 800; color: var(--text-dark); margin-bottom: 2px; }
  .path-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4; }

  .path-progress { margin-top: 12px; }
  .progress-bar { background: #f0f0f0; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 6px; }
  .progress-fill { height: 100%; background: linear-gradient(90deg, #2e7d32, #fbc02d); border-radius: 4px; transition: width 0.4s ease; }
  .path-stats { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); font-weight: 600; }

  .path-reward { background: linear-gradient(135deg, #fff8e1, #fffde7); border-radius: 12px; padding: 10px 12px; margin-top: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; }
  .path-reward .label { color: #6d4c00; font-weight: 700; }
  .path-reward .value { color: #f57c00; font-weight: 900; font-size: 14px; }

  .path-btn { width: 100%; background: var(--green); color: #fff; border: none; padding: 12px; border-radius: 12px; font-weight: 800; font-size: 13px; font-family: inherit; cursor: pointer; margin-top: 12px; }
  .path-btn.completed { background: #f5f5f5; color: var(--text-muted); cursor: default; }

  /* ===== FORMATION DANS PARCOURS ===== */
  .formation-item { background: #fafafa; border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 10px; margin-top: 8px; }
  .fi-check { width: 28px; height: 28px; border-radius: 50%; border: 2px solid #e0e0e0; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 14px; }
  .fi-check.done { background: var(--green); border-color: var(--green); color: #fff; }
  .fi-info { flex: 1; min-width: 0; }
  .fi-title { font-size: 13px; font-weight: 700; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .fi-meta { font-size: 10px; color: var(--text-muted); margin-top: 2px; }
  .fi-action { background: var(--green-light); color: var(--green); border: none; padding: 6px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; font-family: inherit; cursor: pointer; flex-shrink: 0; }
  .fi-action.done { background: var(--green); color: #fff; }
  .fi-action:disabled { opacity: 0.5; cursor: not-allowed; }

  /* ===== CERTIFICATS ===== */
  .certs-list { padding: 0 16px; display: flex; flex-direction: column; gap: 12px; }
  .cert-card { background: linear-gradient(135deg, #fff, #fafafa); border: 2px dashed var(--gold); border-radius: 18px; padding: 20px; text-align: center; position: relative; overflow: hidden; }
  .cert-card::before { content: '★'; position: absolute; top: 10px; left: 12px; color: var(--gold); font-size: 20px; opacity: 0.4; }
  .cert-card::after { content: '★'; position: absolute; top: 10px; right: 12px; color: var(--gold); font-size: 20px; opacity: 0.4; }
  .cert-type { font-size: 10px; font-weight: 800; color: var(--gold); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .cert-title { font-size: 15px; font-weight: 900; color: var(--text-dark); margin-bottom: 8px; line-height: 1.3; }
  .cert-name { font-size: 13px; color: var(--text-muted); margin-bottom: 12px; font-style: italic; }
  .cert-code { background: #f5f5f5; padding: 4px 10px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 10px; color: var(--text-muted); margin-bottom: 12px; display: inline-block; }
  .cert-share { display: flex; gap: 8px; }
  .cert-share button { flex: 1; background: var(--green); color: #fff; border: none; padding: 10px; border-radius: 10px; font-weight: 700; font-size: 12px; font-family: inherit; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px; }
  .cert-share button.wa { background: #25D366; }

  /* ===== EMPTY ===== */
  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
  .empty-state .icon { width: 80px; height: 80px; margin: 0 auto 16px; border-radius: 50%; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; font-size: 36px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  .skel-card { background: #fff; border-radius: 20px; padding: 18px; animation: pulse 1.4s infinite; }
  .skel-line { height: 12px; background: #f0f0f0; border-radius: 6px; margin-bottom: 10px; }
  .skel-line.short { width: 60%; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }

  /* Modal */
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: center; justify-content: center; padding: 20px; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 20px; padding: 24px; max-width: 340px; width: 100%; text-align: center; animation: scaleIn 0.3s ease; }
  @keyframes scaleIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  .modal-icon { font-size: 60px; margin-bottom: 12px; }
  .modal-title { font-size: 20px; font-weight: 900; color: var(--green); margin-bottom: 8px; }
  .modal-text { font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 20px; }
  .modal-btn { background: var(--green); color: #fff; border: none; padding: 14px; border-radius: 12px; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; width: 100%; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Formation</div>
    <div class="spacer"></div>
  </header>

  <div class="hero">
    <div class="hero-title">📚 Progressez et gagnez</div>
    <div class="hero-sub">Terminez les formations, débloquez des certificats et recevez des récompenses.</div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="paths"><span class="icon">🎯</span>Parcours</button>
    <button class="tab" data-tab="certificates"><span class="icon">📜</span>Certificats</button>
  </div>

  <div class="tab-content active" id="tab-paths">
    <div class="paths-list" id="pathsList">
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div></div>
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div></div>
    </div>
  </div>

  <div class="tab-content" id="tab-certificates">
    <div class="certs-list" id="certsList">
      <div class="empty-state">
        <div class="icon">📜</div>
        <h3>Aucun certificat</h3>
        <p>Terminez vos premières formations pour les débloquer.</p>
      </div>
    </div>
  </div>

  <div style="height: 32px;"></div>
</div>

<div class="modal-overlay" id="successModal">
  <div class="modal-content">
    <div class="modal-icon">🎉</div>
    <div class="modal-title" id="modalTitle">Félicitations !</div>
    <div class="modal-text" id="modalText"></div>
    <button class="modal-btn" onclick="closeModal()">Continuer</button>
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
  let allPaths = [];

  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), { headers: { 'Authorization': 'Bearer ' + token } });
      if (!res.ok) return;
      const data = await res.json();
      const raw = data.profile?.is_activated;
      isActivated = (raw === true || raw === "true" || raw === 1 || raw === "1");
    } catch (e) {}
  }

  async function loadPaths() {
    const list = document.getElementById('pathsList');
    try {
      const res = await fetch('/api/formations/paths?t=' + Date.now(), { headers: { 'Authorization': 'Bearer ' + token } });
      const data = await res.json();
      allPaths = data.paths || [];
      if (allPaths.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">🎯</div><h3>Aucun parcours</h3><p>Revenez plus tard, de nouveaux parcours arrivent.</p></div>';
        return;
      }
      list.innerHTML = allPaths.map(function(p) { return renderPath(p); }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur de chargement</h3></div>';
    }
  }

  function renderPath(p) {
    const total = p.total_formations || 0;
    const done = p.completed_count || 0;
    const percent = total > 0 ? Math.round((done / total) * 100) : 0;
    const isCompleted = p.is_completed || false;

    const formationsHTML = (p.formations || []).map(function(f) {
      const isDone = (p.completed_ids || []).indexOf(f.id) !== -1;
      return '<div class="formation-item">' +
        '<div class="fi-check ' + (isDone ? 'done' : '') + '">' + (isDone ? '✓' : '') + '</div>' +
        '<div class="fi-info">' +
        '<div class="fi-title">' + (f.title || 'Formation') + '</div>' +
        '<div class="fi-meta">' + (f.duration || '') + (f.duration && f.category ? ' · ' : '') + (f.category || '') + '</div>' +
        '</div>' +
        '<button class="fi-action ' + (isDone ? 'done' : '') + '" onclick="completeFormation(\\'' + f.id + '\\')" ' + (isDone ? 'disabled' : '') + '>' + (isDone ? '✓' : 'Terminer') + '</button>' +
        '</div>';
    }).join('');

    return '<div class="path-card ' + (p.color || 'green') + '">' +
      '<div class="path-header">' +
      '<div class="path-icon">' + (p.icon || '📚') + '</div>' +
      '<div class="path-info">' +
      '<div class="path-title">' + (p.title || '') + '</div>' +
      '<div class="path-desc">' + (p.description || '') + '</div>' +
      '</div>' +
      '</div>' +
      '<div class="path-progress">' +
      '<div class="progress-bar"><div class="progress-fill" style="width:' + percent + '%"></div></div>' +
      '<div class="path-stats"><span>' + done + '/' + total + ' formations</span><span>' + percent + '%</span></div>' +
      '</div>' +
      '<div class="path-reward">' +
      '<span class="label">💰 Récompense : ' + Number(p.reward_per_formation || 0) + ' F / formation</span>' +
      '</div>' +
      '<div class="path-reward">' +
      '<span class="label">🏆 Bonus final : </span>' +
      '<span class="value">' + Number(p.bonus_final || 0) + ' F</span>' +
      '</div>' +
      formationsHTML +
      (isCompleted ? '<button class="path-btn completed">✓ Parcours terminé</button>' : '') +
      '</div>';
  }

  async function completeFormation(formationId) {
    if (!isActivated) {
      alert('⚠ Activez votre compte pour recevoir les récompenses.');
      window.location.href = '/activation';
      return;
    }

    if (!confirm('Marquer cette formation comme terminée ?\\n\\nVous recevrez une récompense.')) return;

    try {
      const res = await fetch('/api/formations/complete/' + formationId, {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Erreur');

      const r = data.result;
      if (!r.success) {
        alert(r.message || 'Erreur');
        return;
      }

      if (navigator.vibrate) navigator.vibrate([20, 40, 20]);

      let msg = '🎉 +' + Number(r.reward).toLocaleString('fr-FR') + ' F crédités !';
      if (r.path_completed) {
        msg += '\\n\\n🏆 PARCOURS TERMINÉ !\\nBonus : +' + Number(r.bonus).toLocaleString('fr-FR') + ' F';
      }

      document.getElementById('modalTitle').textContent = r.path_completed ? '🏆 Parcours terminé !' : '🎉 Félicitations !';
      document.getElementById('modalText').innerHTML = msg.replace(/\\n/g, '<br>');
      document.getElementById('successModal').classList.add('open');

      setTimeout(function() {
        loadPaths();
        loadCertificates();
      }, 500);

    } catch (err) {
      alert('⚠ ' + err.message);
    }
  }

  async function loadCertificates() {
    const list = document.getElementById('certsList');
    try {
      const res = await fetch('/api/formations/certificates?t=' + Date.now(), { headers: { 'Authorization': 'Bearer ' + token } });
      const data = await res.json();
      const certs = data.certificates || [];

      if (certs.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">📜</div><h3>Aucun certificat</h3><p>Terminez vos premières formations pour les débloquer.</p></div>';
        return;
      }

      list.innerHTML = certs.map(function(c) {
        return '<div class="cert-card">' +
          '<div class="cert-type">' + (c.type === 'parcours' ? '🏆 Parcours complet' : '🎓 Certificat') + '</div>' +
          '<div class="cert-title">' + (c.title || '') + '</div>' +
          '<div class="cert-name">' + (c.full_name || '') + '</div>' +
          '<div class="cert-code">' + (c.code || '') + '</div>' +
          '<div class="cert-share">' +
          '<button onclick="copyCert(\\'' + c.code + '\\', \\'' + (c.title || '').replace(/'/g, '') + '\\')">📋 Copier</button>' +
          '<button class="wa" onclick="shareWhatsapp(\\'' + c.code + '\\', \\'' + (c.title || '').replace(/'/g, '') + '\\')">💬 WhatsApp</button>' +
          '</div>' +
          '</div>';
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  function copyCert(code, title) {
    const text = '🏆 Certificat TriBoost\\n\\n' + title + '\\nCode : ' + code + '\\n\\nVérifié sur triboost.vercel.app';
    navigator.clipboard.writeText(text).then(function() {
      alert('✅ Certificat copié !');
    });
  }

  function shareWhatsapp(code, title) {
    const text = encodeURIComponent('🏆 J\\'ai obtenu un certificat TriBoost !\\n\\n' + title + '\\nCode : ' + code);
    window.open('https://wa.me/?text=' + text, '_blank');
  }

  function closeModal() {
    document.getElementById('successModal').classList.remove('open');
  }

  document.querySelectorAll('.tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
      document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      if (this.dataset.tab === 'certificates') loadCertificates();
    });
  });

  (async function() {
    await loadProfile();
    loadPaths();
  })();
</script>
</body>
</html>
"""
)