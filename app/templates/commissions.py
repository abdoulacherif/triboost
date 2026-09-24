from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_COMMISSIONS = (
    HTML_HEAD.format(title="Commissions — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
  }
  body { background: #f5f5f5; }
  .app {
    width: 100%; max-width: 480px;
    background: #f5f5f5; min-height: 100vh;
    padding-bottom: calc(40px + var(--safe-bottom));
    padding-top: var(--safe-top);
    margin: 0 auto;
  }

  /* ===== TOPBAR ===== */
  .topbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 20px;
    background: #fff;
    position: sticky; top: 0; z-index: 50;
  }
  .back-btn {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--green-light); color: var(--green);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    text-decoration: none;
  }
  .page-title {
    font-size: 18px; font-weight: 800; color: var(--text-dark);
    flex: 1; text-align: center;
  }
  .spacer { width: 40px; }

  /* ===== TOTAL CARD ===== */
  .total-card {
    margin: 16px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 20px;
    padding: 20px;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3);
  }
  .total-card::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .total-label {
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    opacity: 0.9;
    margin-bottom: 8px;
    position: relative; z-index: 2;
  }
  .total-value {
    font-size: 34px; font-weight: 900; line-height: 1;
    position: relative; z-index: 2;
    margin-bottom: 4px;
  }
  .total-value span { font-size: 16px; font-weight: 600; }
  .total-sub {
    font-size: 12px; opacity: 0.85;
    position: relative; z-index: 2;
  }

  /* ===== COMMENT GAGNER ===== */
  .info-box {
    margin: 16px;
    background: linear-gradient(135deg, #fff8e1, #fffde7);
    border: 1.5px solid var(--gold);
    border-radius: 16px;
    padding: 14px 16px;
  }
  .info-box h4 {
    font-size: 13px;
    font-weight: 800;
    color: #6d4c00;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .info-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #6d4c00;
    font-weight: 600;
  }
  .info-row .badge-level {
    background: rgba(255,255,255,0.7);
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 10px;
  }
  .info-row .amount {
    background: #2e7d32;
    color: #fff;
    padding: 2px 10px;
    border-radius: 8px;
    font-weight: 800;
  }

  /* ===== LEVEL TABS ===== */
  .level-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    padding: 0 16px;
    margin-bottom: 16px;
  }
  .level-tab {
    background: #fff;
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 14px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
    font-family: inherit;
  }
  .level-tab::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    transition: height 0.2s;
  }
  .level-tab.n1::before { background: var(--green); }
  .level-tab.n2::before { background: var(--gold); }
  .level-tab.n3::before { background: var(--orange); }
  .level-tab.active.n1 { background: var(--green-light); border-color: var(--green); }
  .level-tab.active.n2 { background: var(--gold-light); border-color: var(--gold); }
  .level-tab.active.n3 { background: var(--orange-light); border-color: var(--orange); }
  .level-tab .label {
    font-size: 11px;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 6px;
    display: block;
  }
  .level-tab .value {
    font-size: 14px;
    font-weight: 900;
    color: var(--text-dark);
    display: block;
    margin-bottom: 2px;
  }
  .level-tab .count {
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 600;
    display: block;
  }
  .level-tab.n1 .value { color: var(--green); }
  .level-tab.n2 .value { color: #f9a825; }
  .level-tab.n3 .value { color: var(--orange); }

  /* ===== SECTION TITLE ===== */
  .section-title {
    font-size: 14px;
    font-weight: 800;
    color: var(--text-dark);
    margin: 0 16px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .section-title .count {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 600;
  }

  /* ===== LISTE COMMISSIONS ===== */
  .commissions-list {
    padding: 0 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .commission-item {
    background: #fff;
    border-radius: 14px;
    padding: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    animation: fadeIn 0.3s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .ci-avatar {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800;
    font-size: 12px;
    flex-shrink: 0;
    color: #fff;
  }
  .ci-avatar.n1 { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .ci-avatar.n2 { background: linear-gradient(135deg, #fbc02d, #f9a825); }
  .ci-avatar.n3 { background: linear-gradient(135deg, #f57c00, #e65100); }
  .ci-info {
    flex: 1; min-width: 0;
  }
  .ci-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .ci-meta {
    font-size: 11px;
    color: var(--text-muted);
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .ci-level-badge {
    display: inline-block;
    font-size: 9px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 5px;
    letter-spacing: 0.5px;
  }
  .ci-level-badge.n1 { background: var(--green-light); color: var(--green); }
  .ci-level-badge.n2 { background: var(--gold-light); color: #f9a825; }
  .ci-level-badge.n3 { background: var(--orange-light); color: var(--orange); }
  .ci-amount {
    font-size: 15px;
    font-weight: 900;
    color: var(--green);
    white-space: nowrap;
    flex-shrink: 0;
  }

  /* ===== EMPTY ===== */
  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
  }
  .empty-state .icon {
    width: 80px; height: 80px;
    margin: 0 auto 16px;
    border-radius: 50%;
    background: var(--green-light);
    color: var(--green);
    display: flex; align-items: center; justify-content: center;
  }
  .empty-state h3 {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 6px;
  }
  .empty-state p {
    font-size: 12px;
    line-height: 1.5;
  }

  /* ===== SKELETON ===== */
  .skel {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.4s infinite;
    border-radius: 12px;
  }
  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
</style>
</head>
<body>

<div class="app">

  <header class="topbar">
    <a href="/dashboard" class="back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </a>
    <div class="page-title">Mes Commissions</div>
    <div class="spacer"></div>
  </header>

  <!-- TOTAL -->
  <div class="total-card">
    <div class="total-label">Total des commissions</div>
    <div class="total-value" id="totalValue">0 <span>FCFA</span></div>
    <div class="total-sub" id="totalSub">0 commission reçue</div>
  </div>

  <!-- COMMENT GAGNER -->
  <div class="info-box">
    <h4>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
      Barème des commissions
    </h4>
    <div class="info-list">
      <div class="info-row">
        <span class="badge-level">NIVEAU 1</span>
        <span class="amount">1 500 F</span>
      </div>
      <div class="info-row">
        <span class="badge-level">NIVEAU 2</span>
        <span class="amount">750 F</span>
      </div>
      <div class="info-row">
        <span class="badge-level">NIVEAU 3</span>
        <span class="amount">325 F</span>
      </div>
    </div>
  </div>

  <!-- LEVEL TABS -->
  <div class="level-tabs">
    <button class="level-tab n1 active" data-level="all">
      <span class="label">TOUT</span>
      <span class="value" id="allValue">- F</span>
      <span class="count" id="allCount">0</span>
    </button>
    <button class="level-tab n1" data-level="1">
      <span class="label">N1</span>
      <span class="value" id="n1Value">- F</span>
      <span class="count" id="n1Count">0</span>
    </button>
    <button class="level-tab n2" data-level="2">
      <span class="label">N2</span>
      <span class="value" id="n2Value">- F</span>
      <span class="count" id="n2Count">0</span>
    </button>
  </div>

  <!-- Bouton N3 séparé -->
  <div style="padding: 0 16px 16px;">
    <button class="level-tab n3" data-level="3" style="width: 100%;">
      <span class="label">NIVEAU 3</span>
      <span class="value" id="n3Value">- F</span>
      <span class="count" id="n3Count">0 commission</span>
    </button>
  </div>

  <!-- LISTE -->
  <div class="section-title">
    <span>Détail des commissions</span>
    <span class="count" id="listCount">0</span>
  </div>

  <div class="commissions-list" id="commissionsList">
    <div class="skel" style="height:70px;"></div>
    <div class="skel" style="height:70px;"></div>
    <div class="skel" style="height:70px;"></div>
  </div>

  <div style="height: 32px;"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) {
    window.location.href = '/login';
  }

  let allCommissions = [];
  let currentLevel = 'all';

  // ===== CHARGER LES COMMISSIONS =====
  async function loadCommissions() {
    try {
      const res = await fetch('/api/history/?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });

      if (res.status === 401) {
        localStorage.clear();
        window.location.href = '/login';
        return;
      }

      if (!res.ok) throw new Error('Erreur de chargement');

      const data = await res.json();
      allCommissions = data.commissions || [];
      const stats = data.stats || {};

      renderStats(stats);
      renderList();

    } catch (err) {
      console.error(err);
      document.getElementById('commissionsList').innerHTML = `
        <div class="empty-state">
          <h3>Erreur de chargement</h3>
          <p>${err.message}</p>
        </div>
      `;
    }
  }

  // ===== AFFICHER LES STATS =====
  function renderStats(stats) {
    const total = Number(stats.total_gains || 0);
    const totalCount = Number(stats.total_commissions || 0);

    document.getElementById('totalValue').innerHTML =
      total.toLocaleString('fr-FR') + ' <span>FCFA</span>';
    document.getElementById('totalSub').textContent =
      totalCount + ' commission' + (totalCount > 1 ? 's' : '') + ' reçue' + (totalCount > 1 ? 's' : '');

    const ls = stats.level_stats || { n1: 0, n2: 0, n3: 0 };
    const lc = stats.level_counts || { n1: 0, n2: 0, n3: 0 };

    // Tab "Tout"
    document.getElementById('allValue').textContent = formatF(total);
    document.getElementById('allCount').textContent = totalCount + ' gain' + (totalCount > 1 ? 's' : '');

    // Tab N1
    document.getElementById('n1Value').textContent = formatF(ls.n1);
    document.getElementById('n1Count').textContent = lc.n1 + ' gain' + (lc.n1 > 1 ? 's' : '');

    // Tab N2
    document.getElementById('n2Value').textContent = formatF(ls.n2);
    document.getElementById('n2Count').textContent = lc.n2 + ' gain' + (lc.n2 > 1 ? 's' : '');

    // Tab N3
    document.getElementById('n3Value').textContent = formatF(ls.n3);
    document.getElementById('n3Count').textContent = lc.n3 + ' commission' + (lc.n3 > 1 ? 's' : '');
  }

  // ===== AFFICHER LA LISTE FILTRÉE =====
  function renderList() {
    const list = document.getElementById('commissionsList');

    let filtered = allCommissions;
    if (currentLevel !== 'all') {
      filtered = allCommissions.filter(c => c.level === parseInt(currentLevel));
    }

    document.getElementById('listCount').textContent = filtered.length;

    if (filtered.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </div>
          <h3>Aucune commission</h3>
          <p>Invitez des personnes pour commencer à gagner.</p>
        </div>
      `;
      return;
    }

    list.innerHTML = filtered.map(c => {
      const level = c.level || 1;
      const amount = Number(c.amount || 0);
      const date = formatDate(c.created_at);
      const desc = c.description || 'Commission N' + level;

      return `
        <div class="commission-item">
          <div class="ci-avatar n${level}">N${level}</div>
          <div class="ci-info">
            <div class="ci-title">${escapeHtml(desc)}</div>
            <div class="ci-meta">
              <span class="ci-level-badge n${level}">NIVEAU ${level}</span>
              <span>${date}</span>
            </div>
          </div>
          <div class="ci-amount">+${amount.toLocaleString('fr-FR')} F</div>
        </div>
      `;
    }).join('');
  }

  // ===== FILTRES NIVEAU =====
  document.querySelectorAll('.level-tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.level-tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      currentLevel = this.dataset.level;
      vibrate(5);
      renderList();
    });
  });

  // ===== HELPERS =====
  function formatF(n) {
    const v = Number(n) || 0;
    if (v >= 1000000) return (v / 1000000).toFixed(1) + 'M';
    if (v >= 1000) return (v / 1000).toFixed(1) + 'k';
    return v.toString();
  }

  function formatDate(isoStr) {
    if (!isoStr) return '';
    try {
      const dt = new Date(isoStr);
      const now = new Date();
      const diff = (now - dt) / 1000;

      if (diff < 60) return 'À l\\'instant';
      if (diff < 3600) return Math.floor(diff / 60) + ' min';
      if (diff < 86400) return Math.floor(diff / 3600) + 'h';
      if (diff < 604800) return Math.floor(diff / 86400) + 'j';

      return dt.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    } catch {
      return '';
    }
  }

  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  // ===== INIT =====
  loadCommissions();
</script>
</body>
</html>
"""
)