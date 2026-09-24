from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_BOOST = (
    HTML_HEAD.format(title="Boost — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
    --purple: #7b1fa2;
    --purple-light: #f3e5f5;
  }
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }

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

  .hero { margin: 16px; background: linear-gradient(135deg, var(--gold), #f57c00); border-radius: 20px; padding: 24px 20px; color: #212121; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(245, 124, 0, 0.3); }
  .hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.2); border-radius: 50%; }
  .hero-content { position: relative; z-index: 2; }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 6px; }
  .hero-sub { font-size: 13px; line-height: 1.5; font-weight: 600; }

  .tabs { display: flex; gap: 8px; padding: 0 16px; margin-bottom: 16px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; transition: all 0.2s; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .info-card { margin: 0 16px 16px; background: #fff; border-radius: 18px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .info-card h3 { font-size: 15px; font-weight: 800; color: var(--text-dark); margin-bottom: 14px; display: flex; align-items: center; gap: 6px; }
  .info-row { display: flex; gap: 12px; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
  .info-row:last-child { border-bottom: none; }
  .info-num { width: 28px; height: 28px; border-radius: 50%; background: var(--gold-light); color: #f9a825; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; flex-shrink: 0; }
  .info-text { flex: 1; font-size: 13px; line-height: 1.5; color: var(--text-dark); }

  .buy-card { margin: 0 16px 16px; background: linear-gradient(135deg, #1a1a1a, #333); border-radius: 20px; padding: 24px 20px; color: #fff; position: relative; overflow: hidden; }
  .buy-card::before { content: ''; position: absolute; top: -60px; right: -60px; width: 180px; height: 180px; background: rgba(251, 192, 45, 0.15); border-radius: 50%; }
  .buy-card .label { font-size: 11px; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; position: relative; z-index: 2; }
  .buy-card .price { font-size: 36px; font-weight: 900; color: var(--gold); line-height: 1; margin-bottom: 4px; position: relative; z-index: 2; }
  .buy-card .price span { font-size: 18px; }
  .buy-card .desc { font-size: 12px; opacity: 0.8; margin-bottom: 18px; position: relative; z-index: 2; line-height: 1.5; }
  .buy-card .btn { background: var(--gold); color: #212121; border: none; padding: 16px; border-radius: 14px; font-weight: 900; font-size: 15px; font-family: inherit; cursor: pointer; width: 100%; position: relative; z-index: 2; display: flex; align-items: center; justify-content: center; gap: 8px; }
  .buy-card .btn:active { transform: scale(0.98); }
  .buy-card .btn:disabled { opacity: 0.6; cursor: not-allowed; }

  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: #fff; }
  .form-group input, .form-group select { width: 100%; padding: 12px 14px; border: 1.5px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; font-family: inherit; color: #fff; outline: none; background: rgba(255,255,255,0.1); }
  .form-group input::placeholder { color: rgba(255,255,255,0.5); }
  .form-group select { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>"); background-repeat: no-repeat; background-position: right 14px center; padding-right: 38px; }
  .form-group select option { background: #212121; color: #fff; }

  .franchise-item { margin: 0 16px 12px; background: #fff; border-radius: 18px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); position: relative; overflow: hidden; }
  .franchise-item::before { content: ''; position: absolute; top: 0; left: 0; bottom: 0; width: 4px; background: linear-gradient(180deg, var(--gold), #f57c00); }
  .fi-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
  .fi-city { font-size: 16px; font-weight: 900; color: var(--text-dark); display: flex; align-items: center; gap: 6px; }
  .fi-quartier { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
  .fi-badge { font-size: 10px; font-weight: 800; padding: 4px 10px; border-radius: 8px; background: var(--green-light); color: var(--green); text-transform: uppercase; letter-spacing: 0.5px; }
  .fi-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
  .fi-stat { background: #f9f9f9; border-radius: 12px; padding: 10px; text-align: center; }
  .fi-stat .value { font-size: 18px; font-weight: 900; color: var(--gold); }
  .fi-stat .label { font-size: 10px; color: var(--text-muted); font-weight: 600; margin-top: 2px; text-transform: uppercase; }

  .stats-grid { margin: 0 16px 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .stat-card { background: #fff; border-radius: 16px; padding: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .stat-card .value { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 4px; }
  .stat-card .label { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }

  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
  .empty-state .icon { width: 80px; height: 80px; margin: 0 auto 16px; border-radius: 50%; background: var(--gold-light); color: #f9a825; display: flex; align-items: center; justify-content: center; font-size: 36px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  .skel-card { background: #fff; border-radius: 18px; padding: 16px; animation: pulse 1.4s infinite; margin: 0 16px 12px; }
  .skel-line { height: 12px; background: #f0f0f0; border-radius: 6px; margin-bottom: 10px; }
  .skel-line.short { width: 60%; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </a>
    <div class="page-title">Boost</div>
    <div class="spacer"></div>
  </header>

  <div class="inactive-banner" id="inactiveBanner">
    <div class="icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
    </div>
    <div class="text">
      <div class="title">Lecture seule</div>
      <div class="desc">Activez pour accéder</div>
    </div>
    <button class="action" onclick="location.href='/activation'">Activer</button>
  </div>

  <div class="hero">
    <div class="hero-content">
      <div class="hero-title">🚀 Boostez vos revenus</div>
      <div class="hero-sub">Achetez une micro-franchise et touchez 15% sur tout ce qui se passe dans votre zone.</div>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="franchise">
      <span class="icon">🏪</span>
      Franchise
    </button>
    <button class="tab" data-tab="mine">
      <span class="icon">📊</span>
      Mes zones
    </button>
  </div>

  <!-- TAB FRANCHISE (achat) -->
  <div class="tab-content active" id="tab-franchise">
    <div class="info-card">
      <h3>💡 Comment ça marche ?</h3>
      <div class="info-row"><div class="info-num">1</div><div class="info-text">Achetez une zone exclusive (ville + quartier) pour <strong>50 000 F</strong></div></div>
      <div class="info-row"><div class="info-num">2</div><div class="info-text">Vous devenez représentant officiel TriBoost dans cette zone</div></div>
      <div class="info-row"><div class="info-num">3</div><div class="info-text">Vous touchez <strong>15%</strong> sur toutes les activations de votre zone</div></div>
      <div class="info-row"><div class="info-num">4</div><div class="info-text">Vous touchez aussi 10% sur les ventes de formations et services</div></div>
    </div>

    <div class="buy-card">
      <div class="label">Investissement unique</div>
      <div class="price">50 000 <span>FCFA</span></div>
      <div class="desc">Zone exclusive · Revenus à vie · Activation immédiate</div>

      <div id="buyError" class="alert error" style="display:none;background:rgba(211,47,47,0.3);color:#fff;border-left:3px solid #fff;"></div>

      <form id="buyForm" onsubmit="buyFranchise(event)">
        <div class="form-group">
          <label>Ville *</label>
          <input type="text" id="cityInput" required maxlength="50" placeholder="Ex : Douala, Yaoundé...">
        </div>
        <div class="form-group">
          <label>Quartier *</label>
          <input type="text" id="quartierInput" required maxlength="50" placeholder="Ex : Bonapriso, Akwa...">
        </div>
        <button type="submit" class="btn" id="buyBtn">
          <span>🏪 Acheter ma franchise</span>
        </button>
      </form>
    </div>
  </div>

  <!-- TAB MES ZONES -->
  <div class="tab-content" id="tab-mine">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="value" id="statFranchises">-</div>
        <div class="label">Zones</div>
      </div>
      <div class="stat-card">
        <div class="value" id="statEarned">- F</div>
        <div class="label">Gains totaux</div>
      </div>
    </div>
    <div id="myFranchises">
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div></div>
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

  let isActivated = false;

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

  async function loadMyFranchises() {
    const container = document.getElementById('myFranchises');
    try {
      const res = await fetch('/api/boost/franchises/me?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();
      const franchises = data.franchises || [];

      document.getElementById('statFranchises').textContent = franchises.length;

      const total = franchises.reduce((s, f) => s + Number(f.total_earned || 0), 0);
      document.getElementById('statEarned').textContent =
        total >= 1000 ? (total / 1000).toFixed(1) + 'k F' : total + ' F';

      if (franchises.length === 0) {
        container.innerHTML = `
          <div class="empty-state">
            <div class="icon">🏪</div>
            <h3>Aucune franchise</h3>
            <p>Achetez votre première zone et commencez à gagner 15% sur chaque activation.</p>
          </div>
        `;
        return;
      }

      container.innerHTML = franchises.map(f => `
        <div class="franchise-item">
          <div class="fi-header">
            <div>
              <div class="fi-city">📍 ${escapeHtml(f.city)}</div>
              <div class="fi-quartier">${escapeHtml(f.quartier || 'Toute la ville')}</div>
            </div>
            <span class="fi-badge">Active</span>
          </div>
          <div class="fi-stats">
            <div class="fi-stat">
              <div class="value">${Number(f.total_earned || 0).toLocaleString('fr-FR')} F</div>
              <div class="label">Gains</div>
            </div>
            <div class="fi-stat">
              <div class="value">15%</div>
              <div class="label">Commission</div>
            </div>
          </div>
        </div>
      `).join('');
    } catch (err) {
      container.innerHTML = '<div class="empty-state"><h3>Erreur</h3><p>' + err.message + '</p></div>';
    }
  }

  async function buyFranchise(e) {
    e.preventDefault();
    if (!isActivated) { showInactiveToast(); return; }

    const city = document.getElementById('cityInput').value.trim();
    const quartier = document.getElementById('quartierInput').value.trim();
    const btn = document.getElementById('buyBtn');
    const errEl = document.getElementById('buyError');
    errEl.style.display = 'none';

    if (!city || !quartier) {
      errEl.textContent = '⚠ Ville et quartier obligatoires';
      errEl.style.display = 'block';
      return;
    }

    if (!confirm(`Acheter la franchise de ${city} - ${quartier} pour 50 000 F ?\\n\\nLe montant sera débité de votre wallet.`)) return;

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/boost/franchises/buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ city, quartier })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (data.result && !data.result.success) throw new Error(data.result.message || 'Erreur');

      vibrate(30);
      showToast('🎉 Franchise activée !');
      document.getElementById('buyForm').reset();
      setTimeout(() => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.querySelector('[data-tab="mine"]').classList.add('active');
        document.getElementById('tab-mine').classList.add('active');
        loadMyFranchises();
      }, 800);
    } catch (err) {
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.innerHTML = '<span>🏪 Acheter ma franchise</span>';
    }
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      vibrate(5);
      if (this.dataset.tab === 'mine') loadMyFranchises();
    });
  });

  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  }

  function showInactiveToast() {
    vibrate([20, 40, 20]);
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#e65100,#bf360c);color:#fff;padding:16px 20px;border-radius:16px;font-size:13px;font-weight:600;z-index:10000;box-shadow:0 10px 30px rgba(230,81,0,0.5);max-width:340px;text-align:center;line-height:1.5;';
    t.innerHTML = '<div><strong>Compte non activé</strong></div><button onclick="location.href=\\'/activation\\'" style="margin-top:12px;background:#fff;color:#e65100;border:none;padding:10px 20px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;font-family:inherit;width:100%;">Activer</button>';
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

  (async () => {
    await loadProfile();
    loadMyFranchises();
  })();
</script>
</body>
</html>
"""
)