from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_FORMATION = (
    HTML_HEAD.format(title="Formation — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { display: block !important; background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; margin: 0 auto; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .hero { margin: 16px; background: linear-gradient(135deg, var(--green), var(--green-dark)); border-radius: 20px; padding: 20px; color: #fff; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(46,125,50,0.3); }
  .hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .hero::after { content: ''; position: absolute; bottom: -40px; left: -40px; width: 120px; height: 120px; background: rgba(251,192,45,0.2); border-radius: 50%; }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 6px; position: relative; z-index: 2; }
  .hero-sub { font-size: 13px; opacity: 0.9; line-height: 1.5; position: relative; z-index: 2; }

  .tabs { display: flex; gap: 8px; padding: 0 16px; margin-bottom: 16px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .paths-list { padding: 0 16px; display: flex; flex-direction: column; gap: 14px; }
  .path-card { background: #fff; border-radius: 20px; padding: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); position: relative; overflow: hidden; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s; text-decoration: none; color: inherit; display: block; animation: slideIn 0.3s ease-out backwards; }
  .path-card:active { transform: scale(0.98); }
  .path-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
  .path-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; }
  .path-card.green::before { background: linear-gradient(90deg, #2e7d32, #4caf50); }
  .path-card.gold::before { background: linear-gradient(90deg, #fbc02d, #f57c00); }
  .path-card.orange::before { background: linear-gradient(90deg, #f57c00, #e65100); }
  .path-card.purple::before { background: linear-gradient(90deg, #7b1fa2, #9c27b0); }
  .path-card:nth-child(1) { animation-delay: 0.05s; }
  .path-card:nth-child(2) { animation-delay: 0.1s; }
  .path-card:nth-child(3) { animation-delay: 0.15s; }
  .path-card:nth-child(4) { animation-delay: 0.2s; }
  @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

  .path-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
  .path-icon { width: 56px; height: 56px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; flex-shrink: 0; background: var(--green-light); }
  .path-card.gold .path-icon { background: #fff8e1; }
  .path-card.orange .path-icon { background: #fff3e0; }
  .path-card.purple .path-icon { background: #f3e5f5; }
  .path-info { flex: 1; min-width: 0; }
  .path-title { font-size: 16px; font-weight: 800; color: var(--text-dark); margin-bottom: 4px; }
  .path-desc { font-size: 12px; color: var(--text-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

  .path-meta { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
  .meta-chip { background: #f5f5f5; color: var(--text-muted); font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 8px; text-transform: uppercase; }

  .path-progress { margin-top: 12px; }
  .progress-bar { background: #f0f0f0; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 6px; }
  .progress-fill { height: 100%; background: linear-gradient(90deg, #2e7d32, #fbc02d); border-radius: 4px; transition: width 0.4s ease; }
  .path-stats { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); font-weight: 600; }

  .path-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 14px; border-top: 1px solid #f5f5f5; }
  .price-tag { font-size: 16px; font-weight: 900; color: var(--green); }
  .price-tag.free { background: var(--green-light); color: var(--green); padding: 4px 10px; border-radius: 8px; font-size: 12px; }
  .action-btn { background: var(--green); color: #fff; border: none; padding: 10px 16px; border-radius: 12px; font-weight: 800; font-size: 12px; font-family: inherit; cursor: pointer; display: flex; align-items: center; gap: 4px; }
  .action-btn.continue { background: var(--gold); color: #212121; }
  .action-btn.locked { background: #f5f5f5; color: #9e9e9e; }

  .badge-unlocked { position: absolute; top: 14px; right: 14px; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; font-size: 10px; font-weight: 900; padding: 4px 10px; border-radius: 8px; letter-spacing: 0.5px; }

  /* CERTIFICATS */
  .certs-list { padding: 0 16px; display: flex; flex-direction: column; gap: 12px; }
  .cert-card { background: linear-gradient(135deg, #fff, #fafafa); border: 2px dashed var(--gold); border-radius: 18px; padding: 20px; text-align: center; position: relative; overflow: hidden; animation: slideIn 0.3s ease-out; }
  .cert-card::before { content: '★'; position: absolute; top: 10px; left: 12px; color: var(--gold); font-size: 20px; opacity: 0.4; }
  .cert-card::after { content: '★'; position: absolute; top: 10px; right: 12px; color: var(--gold); font-size: 20px; opacity: 0.4; }
  .cert-type { font-size: 10px; font-weight: 800; color: var(--gold); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .cert-title { font-size: 15px; font-weight: 900; color: var(--text-dark); margin-bottom: 8px; line-height: 1.3; }
  .cert-name { font-size: 13px; color: var(--text-muted); margin-bottom: 12px; font-style: italic; }
  .cert-code { background: #f5f5f5; padding: 4px 10px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 10px; color: var(--text-muted); margin-bottom: 12px; display: inline-block; }
  .cert-share { display: flex; gap: 8px; }
  .cert-share button { flex: 1; background: var(--green); color: #fff; border: none; padding: 10px; border-radius: 10px; font-weight: 700; font-size: 12px; font-family: inherit; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px; }
  .cert-share button.wa { background: #25D366; }

  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
  .empty-state .icon { width: 80px; height: 80px; margin: 0 auto 16px; border-radius: 50%; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; font-size: 36px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  .skel-card { background: #fff; border-radius: 20px; padding: 18px; animation: pulse 1.4s infinite; }
  .skel-line { height: 12px; background: #f0f0f0; border-radius: 6px; margin-bottom: 10px; }
  .skel-line.short { width: 60%; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }

  @media (min-width: 768px) {
    body { background: linear-gradient(135deg, #f0f4f0, #e8f5e9); padding: 20px 0; }
    .app { max-width: 900px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); overflow: hidden; }
    .paths-list { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .hero-title { font-size: 28px; }
  }
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
    <div class="hero-sub">Débloquez un parcours, faites une leçon par jour, répondez aux quiz et gagnez de l'argent.</div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="paths"><span class="icon">🎯</span>Parcours</button>
    <button class="tab" data-tab="certificates"><span class="icon">📜</span>Certificats</button>
  </div>

  <div class="tab-content active" id="tab-paths">
    <div class="paths-list" id="pathsList">
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div><div class="skel-line"></div></div>
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div><div class="skel-line"></div></div>
    </div>
  </div>

  <div class="tab-content" id="tab-certificates">
    <div class="certs-list" id="certsList">
      <div class="empty-state">
        <div class="icon">📜</div>
        <h3>Aucun certificat</h3>
        <p>Terminez vos premiers parcours pour les débloquer.</p>
      </div>
    </div>
  </div>

  <div style="height: 32px;"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  let allPaths = [];

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }

  async function loadPaths() {
    const list = document.getElementById('pathsList');
    try {
      const res = await fetch('/api/courses/paths?t=' + Date.now(), { headers: headers() });
      const data = await res.json();
      allPaths = data.paths || [];

      if (allPaths.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">🎯</div><h3>Aucun parcours</h3><p>Revenez plus tard.</p></div>';
        return;
      }

      list.innerHTML = allPaths.map(function(p, idx) { return renderPath(p, idx); }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur de chargement</h3></div>';
    }
  }

  function renderPath(p, idx) {
    const totalLessons = p.lessons_count || 0;
    const completed = p.completed_lessons || 0;
    const pct = totalLessons > 0 ? Math.round((completed / totalLessons) * 100) : 0;
    const isUnlocked = p.is_unlocked || false;

    let badgeHTML = '';
    if (isUnlocked) {
      badgeHTML = '<div class="badge-unlocked">✓ DÉBLOQUÉ</div>';
    }

    let progressHTML = '';
    if (isUnlocked) {
      progressHTML = '<div class="path-progress">' +
        '<div class="progress-bar"><div class="progress-fill" style="width:' + pct + '%"></div></div>' +
        '<div class="path-stats"><span>' + completed + ' / ' + totalLessons + ' leçons</span><span>' + pct + '%</span></div>' +
        '</div>';
    }

    let footerHTML = '';
    if (isUnlocked) {
      footerHTML = '<div class="path-footer">' +
        '<div><div style="font-size:10px;color:#757575;font-weight:700;">PROGRESSION</div>' +
        '<div style="font-size:14px;font-weight:900;color:#2e7d32;">' + completed + '/' + totalLessons + '</div></div>' +
        '<a href="/parcours/' + p.id + '" class="action-btn continue">Continuer →</a>' +
        '</div>';
    } else {
      footerHTML = '<div class="path-footer">' +
        '<div class="price-tag">' + fmt(p.unlock_price || 5000) + ' F</div>' +
        '<a href="/parcours/' + p.id + '" class="action-btn">Voir →</a>' +
        '</div>';
    }

    const color = p.color || 'green';

    return '<a href="/parcours/' + p.id + '" class="path-card ' + color + '">' +
      badgeHTML +
      '<div class="path-header">' +
      '<div class="path-icon">' + (p.icon || '📚') + '</div>' +
      '<div class="path-info">' +
      '<div class="path-title">' + escapeHtml(p.title || '') + '</div>' +
      '<div class="path-desc">' + escapeHtml(p.description || '') + '</div>' +
      '</div>' +
      '</div>' +
      '<div class="path-meta">' +
      '<span class="meta-chip">📖 ' + (p.chapters_count || 0) + ' chapitres</span>' +
      '<span class="meta-chip">📝 ' + totalLessons + ' leçons</span>' +
      '<span class="meta-chip">🏆 +' + fmt(p.final_bonus || 500) + ' F</span>' +
      '</div>' +
      progressHTML +
      footerHTML +
      '</a>';
  }

  async function loadCertificates() {
    const list = document.getElementById('certsList');
    try {
      const res = await fetch('/api/formations/certificates?t=' + Date.now(), { headers: headers() });
      const data = await res.json();
      const certs = data.certificates || [];

      if (certs.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">📜</div><h3>Aucun certificat</h3><p>Terminez vos premiers parcours pour les débloquer.</p></div>';
        return;
      }

      list.innerHTML = certs.map(function(c) {
        return '<div class="cert-card">' +
          '<div class="cert-type">' + (c.type === 'parcours' ? '🏆 Parcours complet' : '🎓 Certificat') + '</div>' +
          '<div class="cert-title">' + escapeHtml(c.title || '') + '</div>' +
          '<div class="cert-name">' + escapeHtml(c.full_name || '') + '</div>' +
          '<div class="cert-code">' + escapeHtml(c.code || '') + '</div>' +
          '<div class="cert-share">' +
          '<button onclick="copyCert(\\'' + c.code + '\\', \\'' + (c.title || '').replace(/'/g, '') + '\\')">📋 Copier</button>' +
          '<button class="wa" onclick="shareWhatsapp(\\'' + c.code + '\\', \\'' + (c.title || '').replace(/'/g, '') + '\\')">💬 WhatsApp</button>' +
          '</div></div>';
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  function copyCert(code, title) {
    const text = '🏆 Certificat TriBoost\\n\\n' + title + '\\nCode : ' + code;
    navigator.clipboard.writeText(text).then(function() {
      alert('✅ Certificat copié !');
    });
  }

  function shareWhatsapp(code, title) {
    const text = encodeURIComponent('🏆 J\\'ai obtenu un certificat TriBoost !\\n\\n' + title + '\\nCode : ' + code);
    window.open('https://wa.me/?text=' + text, '_blank');
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

  loadPaths();
</script>
</body>
</html>
"""
)