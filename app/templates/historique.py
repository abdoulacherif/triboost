from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_HISTORIQUE = (
    HTML_HEAD.format(title="Historique — TriBoost")
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
  .app {
    width: 100%; max-width: 480px;
    background: #f5f5f5; min-height: 100vh;
    padding-bottom: calc(40px + var(--safe-bottom));
    padding-top: var(--safe-top);
    margin: 0 auto;
    position: relative;
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
  .total-card::after {
    content: ''; position: absolute; bottom: -40px; left: -40px;
    width: 120px; height: 120px;
    background: rgba(251, 192, 45, 0.2); border-radius: 50%;
  }
  .total-label {
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    opacity: 0.9;
    margin-bottom: 8px;
    position: relative; z-index: 2;
  }
  .total-value {
    font-size: 32px; font-weight: 900; line-height: 1;
    position: relative; z-index: 2;
    margin-bottom: 4px;
  }
  .total-value span { font-size: 16px; font-weight: 600; }
  .total-sub {
    font-size: 12px; opacity: 0.85;
    position: relative; z-index: 2;
  }

  /* ===== CHART SECTION ===== */
  .chart-section {
    margin: 16px;
    background: #fff;
    border-radius: 20px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .chart-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 16px;
  }
  .chart-title {
    font-size: 14px; font-weight: 800;
    color: var(--text-dark);
  }
  .period-tabs {
    display: flex; gap: 4px;
    background: #f5f5f5;
    padding: 3px;
    border-radius: 10px;
  }
  .period-tab {
    background: transparent;
    border: none;
    padding: 5px 10px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }
  .period-tab.active {
    background: #fff;
    color: var(--green);
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  }

  /* Chart SVG */
  .chart-container {
    position: relative;
    width: 100%;
    height: 160px;
  }
  .chart-container svg {
    width: 100%;
    height: 100%;
    overflow: visible;
  }
  .chart-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 600;
  }

  /* ===== LEVEL STATS ===== */
  .level-stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin: 16px;
  }
  .level-card {
    background: #fff;
    border-radius: 16px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
  }
  .level-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .level-card.n1::before { background: var(--green); }
  .level-card.n2::before { background: var(--gold); }
  .level-card.n3::before { background: var(--orange); }
  .level-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 6px;
    margin-bottom: 6px;
  }
  .level-card.n1 .level-badge { background: var(--green-light); color: var(--green); }
  .level-card.n2 .level-badge { background: var(--gold-light); color: #f9a825; }
  .level-card.n3 .level-badge { background: var(--orange-light); color: var(--orange); }
  .level-value {
    font-size: 15px;
    font-weight: 900;
    color: var(--text-dark);
    margin-bottom: 2px;
  }
  .level-count {
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 600;
  }

  /* ===== FILTER TABS ===== */
  .filter-tabs {
    display: flex;
    gap: 8px;
    padding: 0 16px;
    margin-bottom: 12px;
  }
  .filter-tab {
    flex: 1;
    background: #fff;
    border: 1.5px solid var(--border);
    color: var(--text-muted);
    padding: 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s;
  }
  .filter-tab.active {
    background: var(--green);
    color: #fff;
    border-color: var(--green);
    box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25);
  }

  /* ===== LISTE HISTORIQUE ===== */
  .history-list {
    padding: 0 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .history-item {
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
  .hi-icon {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-weight: 800;
    font-size: 12px;
  }
  .hi-icon.n1 { background: var(--green-light); color: var(--green); }
  .hi-icon.n2 { background: var(--gold-light); color: #f9a825; }
  .hi-icon.n3 { background: var(--orange-light); color: var(--orange); }
  .hi-icon.activation { background: var(--blue-light); color: var(--blue); }
  .hi-info { flex: 1; min-width: 0; }
  .hi-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .hi-desc {
    font-size: 11px;
    color: var(--text-muted);
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .hi-amount {
    font-size: 15px;
    font-weight: 900;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .hi-amount.positive { color: var(--green); }
  .hi-amount.negative { color: var(--red); }
  .hi-amount.pending { color: #f9a825; font-size: 12px; }

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
    <div class="page-title">Historique</div>
    <div class="spacer"></div>
  </header>

  <!-- TOTAL -->
  <div class="total-card">
    <div class="total-label">Gains totaux</div>
    <div class="total-value" id="totalGains">0 <span>FCFA</span></div>
    <div class="total-sub" id="totalCount">0 commissions</div>
  </div>

  <!-- CHART -->
  <div class="chart-section">
    <div class="chart-header">
      <div class="chart-title">Évolution des gains</div>
      <div class="period-tabs">
        <button class="period-tab active" data-period="daily">7j</button>
        <button class="period-tab" data-period="weekly">4sem</button>
        <button class="period-tab" data-period="monthly">6m</button>
      </div>
    </div>
    <div class="chart-container" id="chartContainer">
      <div class="skel" style="width:100%; height:100%;"></div>
    </div>
    <div class="chart-labels" id="chartLabels"></div>
  </div>

  <!-- LEVEL STATS -->
  <div class="level-stats">
    <div class="level-card n1">
      <div class="level-badge">N1</div>
      <div class="level-value" id="n1Value">- F</div>
      <div class="level-count" id="n1Count">0 gains</div>
    </div>
    <div class="level-card n2">
      <div class="level-badge">N2</div>
      <div class="level-value" id="n2Value">- F</div>
      <div class="level-count" id="n2Count">0 gains</div>
    </div>
    <div class="level-card n3">
      <div class="level-badge">N3</div>
      <div class="level-value" id="n3Value">- F</div>
      <div class="level-count" id="n3Count">0 gains</div>
    </div>
  </div>

  <!-- TABS -->
  <div class="filter-tabs">
    <button class="filter-tab active" data-type="all">Tout</button>
    <button class="filter-tab" data-type="commissions">Commissions</button>
    <button class="filter-tab" data-type="activations">Paiements</button>
  </div>

  <!-- LISTE -->
  <div class="history-list" id="historyList">
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

  let historyData = { commissions: [], activations: [] };
  let currentPeriod = 'daily';
  let currentType = 'all';

  // ===== CHARGER L'HISTORIQUE =====
  async function loadHistory() {
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
      historyData.commissions = data.commissions || [];
      historyData.activations = data.activations || [];

      renderStats(data.stats);
      renderChart(data.stats);
      renderList();

    } catch (err) {
      console.error(err);
      document.getElementById('historyList').innerHTML = `
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
    document.getElementById('totalGains').innerHTML =
      total.toLocaleString('fr-FR') + ' <span>FCFA</span>';
    document.getElementById('totalCount').textContent =
      stats.total_commissions + ' commission' + (stats.total_commissions > 1 ? 's' : '');

    const ls = stats.level_stats || { n1: 0, n2: 0, n3: 0 };
    const lc = stats.level_counts || { n1: 0, n2: 0, n3: 0 };

    document.getElementById('n1Value').textContent = formatF(ls.n1);
    document.getElementById('n2Value').textContent = formatF(ls.n2);
    document.getElementById('n3Value').textContent = formatF(ls.n3);

    document.getElementById('n1Count').textContent = lc.n1 + ' gain' + (lc.n1 > 1 ? 's' : '');
    document.getElementById('n2Count').textContent = lc.n2 + ' gain' + (lc.n2 > 1 ? 's' : '');
    document.getElementById('n3Count').textContent = lc.n3 + ' gain' + (lc.n3 > 1 ? 's' : '');
  }

  // ===== DESSINER LE GRAPHIQUE =====
  function renderChart(stats) {
    const data = stats[currentPeriod] || {};
    const keys = Object.keys(data);
    const values = keys.map(k => data[k]);

    const container = document.getElementById('chartContainer');
    const labelsEl = document.getElementById('chartLabels');

    // Si pas de données
    if (values.length === 0 || values.every(v => v === 0)) {
      container.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:center;height:100%;color:#bdbdbd;font-size:13px;">
          Aucune donnée pour cette période
        </div>
      `;
      labelsEl.innerHTML = '';
      return;
    }

    const W = 320;
    const H = 150;
    const PAD = 10;
    const innerW = W - PAD * 2;
    const innerH = H - PAD * 2;
    const maxVal = Math.max(...values, 1);

    // Points du graphique
    const points = values.map((v, i) => {
      const x = PAD + (i / Math.max(values.length - 1, 1)) * innerW;
      const y = PAD + innerH - (v / maxVal) * innerH;
      return { x, y, v };
    });

    // Ligne de courbe
    let pathD = '';
    if (points.length > 0) {
      pathD = `M ${points[0].x} ${points[0].y}`;
      for (let i = 1; i < points.length; i++) {
        // Courbe lissée (Catmull-Rom simplifié → Bézier)
        const p0 = points[i - 1];
        const p1 = points[i];
        const cpX = (p0.x + p1.x) / 2;
        pathD += ` C ${cpX} ${p0.y}, ${cpX} ${p1.y}, ${p1.x} ${p1.y}`;
      }
    }

    // Zone remplie
    const areaD = pathD + ` L ${points[points.length - 1].x} ${H - PAD} L ${points[0].x} ${H - PAD} Z`;

    // Points (cercles)
    const circles = points.map((p, i) => `
      <circle cx="${p.x}" cy="${p.y}" r="3" fill="#fff" stroke="#2e7d32" stroke-width="2">
        <title>${p.v.toLocaleString('fr-FR')} F</title>
      </circle>
    `).join('');

    container.innerHTML = `
      <svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
        <defs>
          <linearGradient id="gradArea" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#2e7d32" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#2e7d32" stop-opacity="0"/>
          </linearGradient>
          <linearGradient id="gradLine" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#2e7d32"/>
            <stop offset="100%" stop-color="#fbc02d"/>
          </linearGradient>
        </defs>
        <path d="${areaD}" fill="url(#gradArea)"/>
        <path d="${pathD}" fill="none" stroke="url(#gradLine)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        ${circles}
      </svg>
    `;

    // Labels
    const labels = keys.map(k => {
      if (currentPeriod === 'daily') {
        // "2026-09-24" → "24/09"
        const parts = k.split('-');
        return parts[2] + '/' + parts[1];
      } else if (currentPeriod === 'weekly') {
        // "2026-W39" → "S39"
        const w = k.split('-W');
        return 'S' + w[1];
      } else {
        // "2026-09" → "Sep"
        const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];
        const parts = k.split('-');
        return months[parseInt(parts[1]) - 1] || k;
      }
    });

    labelsEl.innerHTML = labels.map(l => `<span>${l}</span>`).join('');
  }

  // ===== AFFICHER LA LISTE =====
  function renderList() {
    const list = document.getElementById('historyList');
    let items = [];

    // Ajouter les commissions
    if (currentType === 'all' || currentType === 'commissions') {
      items = items.concat(historyData.commissions.map(c => ({
        type: 'commission',
        data: c,
        date: c.created_at,
      })));
    }

    // Ajouter les activations
    if (currentType === 'all' || currentType === 'activations') {
      items = items.concat(historyData.activations.map(a => ({
        type: 'activation',
        data: a,
        date: a.created_at,
      })));
    }

    // Trier par date décroissante
    items.sort((a, b) => new Date(b.date) - new Date(a.date));

    if (items.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
              <polyline points="17 6 23 6 23 12"></polyline>
            </svg>
          </div>
          <h3>Aucun historique</h3>
          <p>Vos gains et paiements apparaîtront ici.</p>
        </div>
      `;
      return;
    }

    list.innerHTML = items.map(item => renderItem(item)).join('');
  }

  function renderItem(item) {
    if (item.type === 'commission') {
      const c = item.data;
      const level = c.level || 1;
      const amount = Number(c.amount || 0);
      const date = formatDate(c.created_at);
      const levelLabel = 'N' + level;

      return `
        <div class="history-item">
          <div class="hi-icon n${level}">${levelLabel}</div>
          <div class="hi-info">
            <div class="hi-title">Commission ${levelLabel}</div>
            <div class="hi-desc">
              <span>${date}</span>
            </div>
          </div>
          <div class="hi-amount positive">+${amount.toLocaleString('fr-FR')} F</div>
        </div>
      `;
    } else {
      const a = item.data;
      const amount = Number(a.amount || 0);
      const date = formatDate(a.created_at);
      const status = a.status || 'pending';
      let statusLabel = '';
      let statusClass = '';

      if (status === 'completed') { statusLabel = 'Activation'; statusClass = 'positive'; }
      else if (status === 'pending') { statusLabel = 'En attente'; statusClass = 'pending'; }
      else { statusLabel = 'Échoué'; statusClass = 'negative'; }

      const displayAmount = status === 'completed'
        ? '-' + amount.toLocaleString('fr-FR') + ' F'
        : status === 'pending'
          ? 'En attente'
          : 'Échoué';

      return `
        <div class="history-item">
          <div class="hi-icon activation">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
          </div>
          <div class="hi-info">
            <div class="hi-title">${statusLabel}</div>
            <div class="hi-desc">
              <span>${date}</span>
            </div>
          </div>
          <div class="hi-amount ${statusClass}">${displayAmount}</div>
        </div>
      `;
    }
  }

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

  // ===== TABS PÉRIODE =====
  document.querySelectorAll('.period-tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.period-tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      currentPeriod = this.dataset.period;
      vibrate(5);
      // Recharger avec les mêmes stats
      fetch('/api/history/?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      }).then(r => r.json()).then(d => renderChart(d.stats));
    });
  });

  // ===== TABS TYPE =====
  document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      currentType = this.dataset.type;
      vibrate(5);
      renderList();
    });
  });

  // ===== INIT =====
  loadHistory();
</script>
</body>
</html>
"""
)