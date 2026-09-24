from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_BOUTIQUE = (
    HTML_HEAD.format(title="Boutique — TriBoost")
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
    --teal: #00796b;
    --teal-light: #e0f2f1;
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

  /* ===== HERO ===== */
  .hero {
    margin: 16px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 20px;
    padding: 20px;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3);
  }
  .hero::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .hero::after {
    content: ''; position: absolute; bottom: -40px; left: -40px;
    width: 120px; height: 120px;
    background: rgba(251, 192, 45, 0.2); border-radius: 50%;
  }
  .hero-content {
    position: relative; z-index: 2;
  }
  .hero-title {
    font-size: 22px; font-weight: 900; margin-bottom: 6px;
  }
  .hero-sub {
    font-size: 13px; opacity: 0.9; line-height: 1.5;
  }
  .hero-stats {
    display: flex; gap: 20px; margin-top: 16px;
    position: relative; z-index: 2;
  }
  .hero-stat {
    display: flex; flex-direction: column;
  }
  .hero-stat .value {
    font-size: 20px; font-weight: 900; line-height: 1;
  }
  .hero-stat .label {
    font-size: 10px; opacity: 0.85; margin-top: 4px;
    text-transform: uppercase; letter-spacing: 0.5px;
  }

  /* ===== RECHERCHE ===== */
  .search-wrap {
    padding: 0 16px 12px;
  }
  .search-box {
    display: flex; align-items: center; gap: 10px;
    background: #fff;
    border-radius: 14px;
    padding: 0 14px;
    height: 48px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .search-box svg { color: #9e9e9e; flex-shrink: 0; }
  .search-box input {
    flex: 1; border: none; background: transparent;
    font-size: 15px; font-family: inherit;
    outline: none; color: var(--text-dark);
  }
  .search-box input::placeholder { color: #bdbdbd; }

  /* ===== CATÉGORIES ===== */
  .categories {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 0 16px 14px;
    scrollbar-width: none;
  }
  .categories::-webkit-scrollbar { display: none; }
  .cat-chip {
    flex-shrink: 0;
    background: #fff;
    color: var(--text-muted);
    border: 1.5px solid var(--border);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .cat-chip.active {
    background: var(--green);
    color: #fff;
    border-color: var(--green);
    box-shadow: 0 4px 10px rgba(46, 125, 50, 0.3);
  }

  /* ===== SECTION TITLE ===== */
  .section-title {
    font-size: 15px; font-weight: 800;
    margin: 0 16px 12px;
    color: var(--text-dark);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ===== LISTE FORMATIONS ===== */
  .formations-list {
    padding: 0 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .formation-card {
    background: #fff;
    border-radius: 18px;
    overflow: hidden;
    display: flex;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    animation: fadeIn 0.3s ease-out;
    text-decoration: none;
    color: inherit;
    transition: transform 0.15s;
  }
  .formation-card:active { transform: scale(0.98); }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .fc-cover {
    width: 100px;
    min-height: 110px;
    flex-shrink: 0;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 900;
    font-size: 22px;
    position: relative;
    overflow: hidden;
  }
  .fc-cover img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .fc-cover .badge-free {
    position: absolute;
    top: 6px; left: 6px;
    background: #4caf50;
    color: #fff;
    font-size: 9px;
    font-weight: 800;
    padding: 3px 6px;
    border-radius: 5px;
    letter-spacing: 0.5px;
    z-index: 2;
  }

  .fc-body {
    flex: 1;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-width: 0;
  }
  .fc-cat {
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--green);
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .fc-title {
    font-size: 14px;
    font-weight: 800;
    color: var(--text-dark);
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .fc-desc {
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .fc-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
  }
  .fc-meta {
    display: flex;
    gap: 10px;
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 600;
  }
  .fc-meta span {
    display: flex;
    align-items: center;
    gap: 3px;
  }
  .fc-price {
    font-size: 14px;
    font-weight: 900;
    color: var(--green);
  }
  .fc-price.free {
    background: var(--green-light);
    color: var(--green);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 11px;
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
  .skel-card {
    background: #fff;
    border-radius: 18px;
    overflow: hidden;
    display: flex;
    animation: pulse 1.4s infinite;
  }
  .skel-cover {
    width: 100px;
    background: #f0f0f0;
  }
  .skel-body {
    flex: 1;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .skel-line {
    height: 12px;
    background: #f0f0f0;
    border-radius: 6px;
  }
  .skel-line.short { width: 60%; }
  .skel-line.tiny { width: 40%; }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
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
    <div class="page-title">Boutique</div>
    <div class="spacer"></div>
  </header>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-content">
      <div class="hero-title">📚 Formations TriBoost</div>
      <div class="hero-sub">Apprenez de nouvelles compétences et développez votre business.</div>
      <div class="hero-stats">
        <div class="hero-stat">
          <span class="value" id="heroTotal">-</span>
          <span class="label">Formations</span>
        </div>
        <div class="hero-stat">
          <span class="value" id="heroFree">-</span>
          <span class="label">Gratuites</span>
        </div>
        <div class="hero-stat">
          <span class="value" id="heroPaid">-</span>
          <span class="label">Payantes</span>
        </div>
      </div>
    </div>
  </div>

  <!-- RECHERCHE -->
  <div class="search-wrap">
    <div class="search-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input type="text" id="searchInput" placeholder="Rechercher une formation...">
    </div>
  </div>

  <!-- CATÉGORIES -->
  <div class="categories" id="categories">
    <button class="cat-chip active" data-cat="tous">Tous</button>
    <button class="cat-chip" data-cat="marketing">📣 Marketing</button>
    <button class="cat-chip" data-cat="business">💼 Business</button>
    <button class="cat-chip" data-cat="tech">💻 Tech</button>
    <button class="cat-chip" data-cat="finance">💰 Finance</button>
    <button class="cat-chip" data-cat="créatif">🎨 Créatif</button>
    <button class="cat-chip" data-cat="développement">🚀 Développement</button>
    <button class="cat-chip" data-cat="autre">📦 Autre</button>
  </div>

  <!-- SECTION TITRE -->
  <div class="section-title" id="sectionTitle">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
    </svg>
    Toutes les formations
  </div>

  <!-- LISTE -->
  <div class="formations-list" id="formationsList">
    <div class="skel-card">
      <div class="skel-cover"></div>
      <div class="skel-body">
        <div class="skel-line short"></div>
        <div class="skel-line"></div>
        <div class="skel-line tiny"></div>
      </div>
    </div>
    <div class="skel-card">
      <div class="skel-cover"></div>
      <div class="skel-body">
        <div class="skel-line short"></div>
        <div class="skel-line"></div>
        <div class="skel-line tiny"></div>
      </div>
    </div>
    <div class="skel-card">
      <div class="skel-cover"></div>
      <div class="skel-body">
        <div class="skel-line short"></div>
        <div class="skel-line"></div>
        <div class="skel-line tiny"></div>
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

  if (!token || !userId) {
    window.location.href = '/login';
  }

  let currentCategory = 'tous';
  let allFormations = [];

  // ===== CHARGER LES FORMATIONS =====
  async function loadFormations(category = 'tous', search = '') {
    const list = document.getElementById('formationsList');

    // Skeleton
    list.innerHTML = `
      <div class="skel-card">
        <div class="skel-cover"></div>
        <div class="skel-body">
          <div class="skel-line short"></div>
          <div class="skel-line"></div>
          <div class="skel-line tiny"></div>
        </div>
      </div>
    `;

    try {
      let url = '/api/formations/?t=' + Date.now();
      if (category && category !== 'tous') url += '&category=' + encodeURIComponent(category);
      if (search) url += '&search=' + encodeURIComponent(search);

      const res = await fetch(url);
      const data = await res.json();

      if (!data.success || !data.formations || data.formations.length === 0) {
        list.innerHTML = `
          <div class="empty-state">
            <div class="icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
            </div>
            <h3>Aucune formation</h3>
            <p>Aucune formation dans cette catégorie pour le moment.</p>
          </div>
        `;
        return;
      }

      allFormations = data.formations;
      updateHeroStats(data.formations);
      list.innerHTML = data.formations.map(f => renderFormation(f)).join('');

    } catch (err) {
      list.innerHTML = `
        <div class="empty-state">
          <h3>Erreur de chargement</h3>
          <p>${err.message}</p>
        </div>
      `;
    }
  }

  // ===== HERO STATS =====
  function updateHeroStats(formations) {
    const total = formations.length;
    const free = formations.filter(f => f.is_free).length;
    const paid = total - free;

    document.getElementById('heroTotal').textContent = total;
    document.getElementById('heroFree').textContent = free;
    document.getElementById('heroPaid').textContent = paid;
  }

  // ===== RENDER UNE CARTE =====
  function renderFormation(f) {
    const initials = (f.title || 'F').substring(0, 2).toUpperCase();
    const cover = f.cover_url
      ? `<img src="${f.cover_url}" alt="${escapeHtml(f.title)}" loading="lazy">`
      : `<span>${initials}</span>`;

    const priceDisplay = f.is_free
      ? `<div class="fc-price free">GRATUIT</div>`
      : `<div class="fc-price">${Number(f.price).toLocaleString('fr-FR')} F</div>`;

    const catIcons = {
      marketing: '📣',
      business: '💼',
      tech: '💻',
      finance: '💰',
      créatif: '🎨',
      développement: '🚀',
      autre: '📦'
    };
    const catIcon = catIcons[f.category] || '📚';

    return `
      <a href="/boutique/${f.id}" class="formation-card">
        <div class="fc-cover">
          ${f.is_free ? '<div class="badge-free">GRATUIT</div>' : ''}
          ${cover}
        </div>
        <div class="fc-body">
          <div class="fc-cat">${catIcon} ${f.category || 'autre'}</div>
          <div class="fc-title">${escapeHtml(f.title)}</div>
          <div class="fc-desc">${escapeHtml(f.description)}</div>
          <div class="fc-footer">
            <div class="fc-meta">
              ${f.duration ? `<span>⏱ ${f.duration}</span>` : ''}
              ${f.level ? `<span>🎯 ${f.level}</span>` : ''}
            </div>
            ${priceDisplay}
          </div>
        </div>
      </a>
    `;
  }

  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  // ===== CATÉGORIES =====
  document.querySelectorAll('.cat-chip').forEach(chip => {
    chip.addEventListener('click', function() {
      document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      currentCategory = this.dataset.cat;
      vibrate(5);

      const titles = {
        tous: 'Toutes les formations',
        marketing: '📣 Marketing',
        business: '💼 Business',
        tech: '💻 Tech',
        finance: '💰 Finance',
        'créatif': '🎨 Créatif',
        'développement': '🚀 Développement',
        autre: '📦 Autre'
      };
      document.getElementById('sectionTitle').innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
        </svg>
        ${titles[currentCategory] || 'Formations'}
      `;

      loadFormations(currentCategory, document.getElementById('searchInput').value);
    });
  });

  // ===== RECHERCHE =====
  let searchTimer = null;
  document.getElementById('searchInput').addEventListener('input', function(e) {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      loadFormations(currentCategory, e.target.value.trim());
    }, 400);
  });

  // ===== INIT =====
  loadFormations();
</script>
</body>
</html>
"""
)