from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_FORMATION_DETAIL = (
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
  .app {
    width: 100%; max-width: 480px;
    background: #f5f5f5; min-height: 100vh;
    padding-bottom: calc(120px + var(--safe-bottom));
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
  .spacer { width: 40px; }

  /* ===== COVER ===== */
  .cover {
    width: 100%;
    height: 220px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 900;
    font-size: 60px;
    position: relative;
    overflow: hidden;
  }
  .cover img {
    width: 100%; height: 100%;
    object-fit: cover;
  }
  .cover::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.4) 100%);
  }
  .cover-badge {
    position: absolute;
    top: 16px; left: 16px;
    background: rgba(255,255,255,0.95);
    color: var(--green);
    font-size: 11px;
    font-weight: 800;
    padding: 6px 12px;
    border-radius: 8px;
    z-index: 2;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .cover-badge.free {
    background: #4caf50;
    color: #fff;
  }

  /* ===== BODY ===== */
  .body {
    padding: 20px;
    margin-top: -30px;
    position: relative;
    z-index: 3;
  }
  .main-card {
    background: #fff;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  }
  .cat {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--green);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .title {
    font-size: 22px;
    font-weight: 900;
    color: var(--text-dark);
    line-height: 1.2;
    margin-bottom: 12px;
  }
  .meta {
    display: flex;
    gap: 14px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .meta span {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  /* ===== DESCRIPTION ===== */
  .desc-section {
    margin: 20px 0;
  }
  .desc-section h3 {
    font-size: 14px;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 8px;
  }
  .desc-section p {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.6;
  }

  /* ===== CONTENU (si accès) ===== */
  .content-section {
    background: linear-gradient(135deg, var(--green-light), #f1f8e9);
    border-radius: 16px;
    padding: 16px;
    margin: 20px 0;
    border-left: 4px solid var(--green);
  }
  .content-section h3 {
    font-size: 14px;
    font-weight: 800;
    color: var(--green);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .content-url {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #fff;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    text-decoration: none;
    color: var(--text-dark);
    font-weight: 700;
    font-size: 13px;
    transition: transform 0.15s;
  }
  .content-url:active { transform: scale(0.98); }
  .content-url .icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: var(--green-light);
    color: var(--green);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .content-text {
    background: #fff;
    padding: 14px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.7;
    color: var(--text-dark);
  }

  /* ===== LOCKED ===== */
  .locked {
    text-align: center;
    padding: 24px 16px;
    background: #fff;
    border-radius: 16px;
    margin: 20px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .locked .lock-icon {
    width: 60px; height: 60px;
    margin: 0 auto 12px;
    border-radius: 50%;
    background: #fff3e0;
    color: #e65100;
    display: flex; align-items: center; justify-content: center;
  }
  .locked h3 {
    font-size: 15px;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 6px;
  }
  .locked p {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.5;
  }

  /* ===== BOTTOM BAR ===== */
  .bottom-bar {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 480px;
    background: #fff;
    border-top: 1px solid var(--border);
    padding: 16px 20px calc(20px + var(--safe-bottom));
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 100;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.06);
  }
  .price-display {
    flex: 1;
  }
  .price-display .label {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 2px;
  }
  .price-display .value {
    font-size: 22px;
    font-weight: 900;
    color: var(--green);
    line-height: 1;
  }
  .price-display .value.free {
    color: var(--green);
  }
  .btn-action {
    flex: 1.5;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    color: #fff;
    border: none;
    padding: 16px;
    border-radius: 14px;
    font-weight: 800;
    font-size: 15px;
    font-family: inherit;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 6px;
    box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3);
    transition: transform 0.15s;
  }
  .btn-action:active { transform: scale(0.97); }
  .btn-action:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-action.unlocked {
    background: #f5f5f5;
    color: var(--text-muted);
    box-shadow: none;
  }

  /* ===== SPINNER ===== */
  .spinner {
    width: 18px; height: 18px;
    border: 2.5px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

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

<div class="app" id="app">
  <!-- Skeleton initial -->
  <div class="skel" style="height: 220px; border-radius: 0;"></div>
  <div style="padding: 20px;">
    <div class="skel" style="height: 300px;"></div>
  </div>
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

  // Récupérer l'ID depuis l'URL
  const pathParts = window.location.pathname.split('/');
  const formationId = pathParts[pathParts.length - 1];

  let currentFormation = null;
  let hasAccess = false;

  // ===== CHARGER LA FORMATION =====
  async function loadFormation() {
    try {
      const res = await fetch('/api/formations/' + formationId + '?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });

      if (!res.ok) {
        if (res.status === 404) {
          document.getElementById('app').innerHTML = `
            <div style="padding: 60px 20px; text-align: center;">
              <h2>Formation introuvable</h2>
              <p style="color: #757575; margin-top: 12px;">Cette formation n'existe pas ou a été retirée.</p>
              <a href="/boutique" style="display: inline-block; margin-top: 20px; background: #2e7d32; color: #fff; padding: 12px 24px; border-radius: 12px; text-decoration: none; font-weight: 700;">Retour à la boutique</a>
            </div>
          `;
          return;
        }
        throw new Error('Erreur');
      }

      const data = await res.json();
      currentFormation = data.formation;
      hasAccess = data.has_access;
      render();

    } catch (err) {
      console.error(err);
      document.getElementById('app').innerHTML = `
        <div style="padding: 60px 20px; text-align: center;">
          <h2>Erreur de chargement</h2>
          <p style="color: #757575; margin-top: 12px;">${err.message}</p>
        </div>
      `;
    }
  }

  // ===== AFFICHER =====
  function render() {
    const f = currentFormation;
    const app = document.getElementById('app');

    const initials = (f.title || 'F').substring(0, 2).toUpperCase();
    const cover = f.cover_url
      ? `<img src="${f.cover_url}" alt="${escapeHtml(f.title)}">`
      : `<span>${initials}</span>`;

    const catIcons = {
      marketing: '📣', business: '💼', tech: '💻',
      finance: '💰', 'créatif': '🎨', 'développement': '🚀',
      autre: '📦'
    };
    const catIcon = catIcons[f.category] || '📚';

    // Contenu (si accès)
    let contentHTML = '';
    if (hasAccess) {
      if (f.content_url || f.content_text) {
        contentHTML = `
          <div class="content-section">
            <h3>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              Contenu de la formation
            </h3>
            ${f.content_url ? `
              <a href="${f.content_url}" target="_blank" rel="noopener" class="content-url">
                <div class="icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                </div>
                <span>Accéder au contenu</span>
              </a>
            ` : ''}
            ${f.content_text ? `
              <div class="content-text">${f.content_text}</div>
            ` : ''}
          </div>
        `;
      } else {
        contentHTML = `
          <div class="content-section" style="text-align: center;">
            <p style="color: #2e7d32; font-weight: 700;">✓ Vous avez accès à cette formation</p>
            <p style="color: #2e7d32; font-size: 12px; margin-top: 6px;">Le contenu sera ajouté prochainement.</p>
          </div>
        `;
      }
    } else {
      contentHTML = `
        <div class="locked">
          <div class="lock-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <h3>Contenu verrouillé</h3>
          <p>Achetez cette formation pour accéder au contenu complet.</p>
        </div>
      `;
    }

    // Bouton action
    let buttonHTML = '';
    if (hasAccess) {
      buttonHTML = `
        <button class="btn-action unlocked" disabled>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          Déjà accessible
        </button>
      `;
    } else if (f.is_free) {
      buttonHTML = `
        <button class="btn-action" id="actionBtn" onclick="activateFree()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
          </svg>
          Accéder gratuitement
        </button>
      `;
    } else {
      buttonHTML = `
        <button class="btn-action" id="actionBtn" onclick="buyFormation()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          Acheter cette formation
        </button>
      `;
    }

    app.innerHTML = `
      <header class="topbar">
        <a href="/boutique" class="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </a>
        <div style="flex: 1; text-align: center; font-size: 15px; font-weight: 800;">Formation</div>
        <div class="spacer"></div>
      </header>

      <div class="cover">
        <div class="cover-badge ${f.is_free ? 'free' : ''}">
          ${f.is_free ? '🎁 Gratuit' : '💎 Premium'}
        </div>
        ${cover}
      </div>

      <div class="body">
        <div class="main-card">
          <div class="cat">${catIcon} ${f.category || 'autre'}</div>
          <div class="title">${escapeHtml(f.title)}</div>
          <div class="meta">
            ${f.duration ? `<span>⏱ ${f.duration}</span>` : ''}
            ${f.level ? `<span>🎯 ${f.level}</span>` : ''}
            ${f.author ? `<span>👤 ${escapeHtml(f.author)}</span>` : ''}
            <span>👁 ${f.views || 0} vues</span>
          </div>

          <div class="desc-section">
            <h3>Description</h3>
            <p>${escapeHtml(f.description) || 'Aucune description.'}</p>
          </div>
        </div>

        ${contentHTML}
      </div>

      <div class="bottom-bar">
        <div class="price-display">
          <div class="label">Prix</div>
          <div class="value ${f.is_free ? 'free' : ''}">
            ${f.is_free ? 'Gratuit' : Number(f.price).toLocaleString('fr-FR') + ' F'}
          </div>
        </div>
        ${buttonHTML}
      </div>
    `;
  }

  // ===== ACTIONS =====
  async function activateFree() {
    if (navigator.vibrate) navigator.vibrate(10);
    await purchase();
  }

  async function buyFormation() {
    const f = currentFormation;
    const price = Number(f.price);
    if (!confirm(`Acheter "${f.title}" pour ${price.toLocaleString('fr-FR')} FCFA ?\\n\\nLe montant sera déduit de votre solde.`)) {
      return;
    }
    await purchase();
  }

  async function purchase() {
    const btn = document.getElementById('actionBtn');
    if (!btn) return;

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/formations/' + formationId + '/purchase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Erreur');

      if (!data.result || !data.result.success) {
        throw new Error(data.result?.message || 'Échec de l\\'achat');
      }

      if (navigator.vibrate) navigator.vibrate([20, 40, 20]);
      showToast('✅ Achat réussi !');
      setTimeout(() => window.location.reload(), 1200);

    } catch (err) {
      alert('⚠ ' + err.message);
      btn.disabled = false;
      btn.innerHTML = 'Réessayer';
    }
  }

  // ===== HELPERS =====
  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function showToast(msg) {
    const t = document.createElement('div');
    t.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: linear-gradient(135deg, #2e7d32, #1b5e20);
      color: #fff; padding: 14px 20px; border-radius: 14px;
      font-size: 13px; font-weight: 700; z-index: 10001;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      max-width: 340px; text-align: center;
    `;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  // ===== INIT =====
  loadFormation();
</script>
</body>
</html>
"""
)