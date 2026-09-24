from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_MARCHE = (
    HTML_HEAD.format(title="Marché — TriBoost")
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
    padding-bottom: calc(100px + var(--safe-bottom));
    padding-top: var(--safe-top);
    position: relative;
  }

  /* ===== TOPBAR ===== */
  .topbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 20px 8px;
    background: #fff;
    position: sticky; top: 0; z-index: 50;
  }
  .back-btn {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--green-light); color: var(--green);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.15s;
    text-decoration: none;
  }
  .back-btn:active { transform: scale(0.92); }
  .page-title {
    font-size: 20px; font-weight: 800; color: var(--text-dark);
    flex: 1; text-align: center;
  }
  .add-btn {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--green); color: #fff;
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.15s, background 0.2s;
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
  }
  .add-btn:active { transform: scale(0.92); }

  /* ===== BANNIÈRE INACTIF ===== */
  .inactive-banner {
    display: none;
    margin: 12px 16px;
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border: 1.5px solid #ffb74d;
    border-radius: 16px;
    padding: 12px 14px;
    align-items: center;
    gap: 10px;
  }
  .inactive-banner.show { display: flex; }
  .inactive-banner .icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: #ffe0b2;
    color: #e65100;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .inactive-banner .text { flex: 1; min-width: 0; }
  .inactive-banner .title {
    font-size: 12px; font-weight: 800; color: #e65100;
  }
  .inactive-banner .desc {
    font-size: 10px; color: #bf360c;
  }
  .inactive-banner .action {
    background: #e65100; color: #fff;
    border: none; padding: 6px 10px;
    border-radius: 8px; font-size: 10px; font-weight: 700;
    cursor: pointer; flex-shrink: 0;
  }

  /* ===== RECHERCHE ===== */
  .search-wrap {
    padding: 8px 16px 12px;
    background: #fff;
    position: sticky; top: 64px; z-index: 49;
  }
  .search-box {
    display: flex; align-items: center; gap: 10px;
    background: #f5f5f5;
    border-radius: 14px;
    padding: 0 14px;
    height: 48px;
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
    background: #fff;
    scrollbar-width: none;
    position: sticky; top: 128px; z-index: 48;
  }
  .categories::-webkit-scrollbar { display: none; }
  .cat-chip {
    flex-shrink: 0;
    background: #f5f5f5;
    color: var(--text-muted);
    border: none;
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
    box-shadow: 0 4px 10px rgba(46, 125, 50, 0.3);
  }

  /* ===== LISTE ANNONCES ===== */
  .items-list {
    padding: 16px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .item-card {
    background: #fff;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    display: flex;
    flex-direction: column;
    animation: fadeIn 0.3s ease-out;
    cursor: pointer;
    transition: transform 0.15s;
  }
  .item-card:active { transform: scale(0.98); }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .item-image {
    width: 100%;
    aspect-ratio: 1 / 1;
    background: #f5f5f5;
    position: relative;
    overflow: hidden;
  }
  .item-image img {
    width: 100%; height: 100%;
    object-fit: cover;
    display: block;
  }
  .item-image .placeholder {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    color: #bdbdbd;
  }
  .item-badge {
    position: absolute;
    top: 8px; left: 8px;
    background: rgba(0,0,0,0.7);
    color: #fff;
    font-size: 9px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .item-content {
    padding: 10px 12px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex: 1;
  }
  .item-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-dark);
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 34px;
  }
  .item-price {
    font-size: 15px;
    font-weight: 800;
    color: var(--green);
  }
  .item-city {
    font-size: 10px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 3px;
  }
  .wa-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: #25D366;
    color: #fff;
    border: none;
    padding: 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.15s, background 0.2s;
    margin-top: 4px;
  }
  .wa-btn:active { transform: scale(0.96); background: #128C7E; }

  /* ===== EMPTY ===== */
  .empty-state {
    grid-column: 1 / -1;
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
    font-size: 16px; font-weight: 700;
    color: var(--text-dark); margin-bottom: 6px;
  }
  .empty-state p {
    font-size: 13px; line-height: 1.5;
  }

  /* ===== SKELETON ===== */
  .skel-card {
    background: #fff;
    border-radius: 18px;
    overflow: hidden;
    animation: pulse 1.4s infinite;
  }
  .skel-img {
    width: 100%;
    aspect-ratio: 1 / 1;
    background: #f0f0f0;
  }
  .skel-line {
    height: 12px;
    background: #f0f0f0;
    border-radius: 6px;
    margin: 10px 12px 0;
  }
  .skel-line.short { width: 50%; }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
  }

  /* ===== MODAL PUBLIER ===== */
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(3px);
    z-index: 999;
    display: none;
    align-items: flex-end;
    justify-content: center;
    animation: fadeInOverlay 0.2s ease-out;
  }
  .modal-overlay.open { display: flex; }
  @keyframes fadeInOverlay {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  .modal-content {
    width: 100%;
    max-width: 480px;
    background: #fff;
    border-radius: 24px 24px 0 0;
    max-height: 92vh;
    overflow-y: auto;
    padding: 20px 20px calc(20px + var(--safe-bottom));
    animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
  }
  @keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }
  .modal-handle {
    width: 40px; height: 4px;
    background: #e0e0e0;
    border-radius: 2px;
    margin: 0 auto 16px;
  }
  .modal-title {
    font-size: 18px; font-weight: 800;
    margin-bottom: 20px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .modal-close {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #f5f5f5;
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-muted);
  }

  .form-group { margin-bottom: 14px; }
  .form-group label {
    display: block; font-size: 12px;
    font-weight: 700; margin-bottom: 6px;
    color: var(--text-dark);
  }
  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    font-size: 15px;
    font-family: inherit;
    color: var(--text-dark);
    outline: none;
    transition: border-color 0.2s;
    background: #fff;
    -webkit-appearance: none;
    appearance: none;
  }
  .form-group textarea {
    min-height: 80px;
    resize: vertical;
  }
  .form-group input:focus,
  .form-group textarea:focus,
  .form-group select:focus {
    border-color: var(--green);
  }
  .form-group select {
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23757575' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>");
    background-repeat: no-repeat;
    background-position: right 14px center;
    padding-right: 38px;
  }

  .image-upload {
    width: 100%;
    height: 140px;
    border: 2px dashed var(--border);
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    cursor: pointer;
    background: #fafafa;
    transition: border-color 0.2s, background 0.2s;
    overflow: hidden;
    position: relative;
  }
  .image-upload:active { background: #f0f0f0; }
  .image-upload input { display: none; }
  .image-upload .label {
    font-size: 12px; color: var(--text-muted);
    font-weight: 600;
  }
  .image-upload img {
    position: absolute;
    inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
  }
  .image-upload .remove-img {
    position: absolute;
    top: 8px; right: 8px;
    width: 28px; height: 28px;
    background: rgba(0,0,0,0.7);
    color: #fff;
    border: none; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    z-index: 2;
  }

  .modal-actions {
    display: flex; gap: 10px;
    margin-top: 20px;
  }
  .btn-cancel {
    flex: 1; background: #f5f5f5;
    color: var(--text-dark); border: none;
    padding: 14px; border-radius: 12px;
    font-weight: 700; font-size: 14px;
    font-family: inherit; cursor: pointer;
  }
  .btn-submit {
    flex: 2; background: var(--green);
    color: #fff; border: none;
    padding: 14px; border-radius: 12px;
    font-weight: 700; font-size: 14px;
    font-family: inherit; cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 8px;
  }
  .btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

  /* ===== BOTTOM NAV ===== */
  .bottom-nav {
    position: fixed; bottom: 0;
    left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 480px;
    background: #fff; border-top: 1px solid var(--border);
    display: flex; justify-content: space-around; align-items: center;
    padding: 12px 10px calc(20px + var(--safe-bottom));
    border-radius: 24px 24px 0 0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    z-index: 100;
  }
  .nav-item {
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    font-size: 11px; color: #757575; text-decoration: none;
    font-weight: 500; padding: 4px;
  }
  .nav-item.active { color: var(--green); font-weight: 700; }
  .nav-item.active .nav-icon { background: var(--green-light); color: var(--green); }
  .nav-icon {
    width: 40px; height: 30px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
  }

  /* ===== FAB ===== */
  .fab {
    position: fixed;
    bottom: calc(90px + var(--safe-bottom));
    right: 20px;
    width: 56px; height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    color: #fff;
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 8px 24px rgba(46, 125, 50, 0.4);
    z-index: 90;
    transition: transform 0.15s;
  }
  .fab:active { transform: scale(0.9); }
</style>
</head>
<body>

<div class="app">

  <!-- TOPBAR -->
  <header class="topbar">
    <a href="/dashboard" class="back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </a>
    <div class="page-title">Marché</div>
    <button class="add-btn" onclick="openPublishModal()" aria-label="Publier">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
    </button>
  </header>

  <!-- BANNIÈRE INACTIF -->
  <div class="inactive-banner" id="inactiveBanner">
    <div class="icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
      </svg>
    </div>
    <div class="text">
      <div class="title">Lecture seule</div>
      <div class="desc">Activez pour publier vos annonces</div>
    </div>
    <button class="action" onclick="location.href='/activation'">Activer</button>
  </div>

  <!-- RECHERCHE -->
  <div class="search-wrap">
    <div class="search-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input type="text" id="searchInput" placeholder="Rechercher un produit, une ville...">
    </div>
  </div>

  <!-- CATÉGORIES -->
  <div class="categories" id="categories">
    <button class="cat-chip active" data-cat="tous">Tous</button>
    <button class="cat-chip" data-cat="electronique">📱 Électronique</button>
    <button class="cat-chip" data-cat="mode">👕 Mode</button>
    <button class="cat-chip" data-cat="maison">🏠 Maison</button>
    <button class="cat-chip" data-cat="vehicule">🚗 Véhicule</button>
    <button class="cat-chip" data-cat="service">🛠️ Service</button>
    <button class="cat-chip" data-cat="immobilier">🏢 Immobilier</button>
    <button class="cat-chip" data-cat="autre">📦 Autre</button>
  </div>

  <!-- LISTE -->
  <div class="items-list" id="itemsList">
    <!-- Skeletons -->
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
  </div>

  <!-- FAB -->
  <button class="fab" onclick="openPublishModal()" aria-label="Publier">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="12" y1="5" x2="12" y2="19"></line>
      <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
  </button>

  <!-- BOTTOM NAV -->
  <nav class="bottom-nav">
    <a href="/dashboard" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </div>
      Accueil
    </a>
    <a href="/marche" class="nav-item active">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
      </div>
      Marché
    </a>
    <a href="/affilie" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      </div>
      Réseau
    </a>
    <a href="/paiements" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
      </div>
      Paiements
    </a>
    <a href="/dashboard" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="1"></circle>
          <circle cx="12" cy="5" r="1"></circle>
          <circle cx="12" cy="19" r="1"></circle>
        </svg>
      </div>
      Plus
    </a>
  </nav>
</div>

<!-- MODAL PUBLIER -->
<div class="modal-overlay" id="publishModal" onclick="if(event.target===this) closePublishModal()">
  <div class="modal-content">
    <div class="modal-handle"></div>
    <div class="modal-title">
      <span>Publier une annonce</span>
      <button class="modal-close" onclick="closePublishModal()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <div id="modalError" class="alert error"></div>

    <form id="publishForm" onsubmit="submitItem(event)">

      <div class="form-group">
        <label>Photo du produit</label>
        <label class="image-upload" id="imageUpload">
          <input type="file" id="imageInput" accept="image/*" onchange="handleImage(event)">
          <svg id="uploadIcon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#bdbdbd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span class="label" id="uploadLabel">Ajouter une photo</span>
        </label>
      </div>

      <div class="form-group">
        <label>Titre de l'annonce *</label>
        <input type="text" id="itemTitle" required maxlength="100" placeholder="Ex : iPhone 13 Pro">
      </div>

      <div class="form-group">
        <label>Description</label>
        <textarea id="itemDesc" maxlength="500" placeholder="Décrivez votre produit..."></textarea>
      </div>

      <div class="form-group">
        <label>Prix (FCFA)</label>
        <input type="number" id="itemPrice" min="0" step="100" placeholder="Ex : 150000">
      </div>

      <div class="form-group">
        <label>Catégorie</label>
        <select id="itemCategory">
          <option value="electronique">📱 Électronique</option>
          <option value="mode">👕 Mode</option>
          <option value="maison">🏠 Maison</option>
          <option value="vehicule">🚗 Véhicule</option>
          <option value="service">🛠️ Service</option>
          <option value="immobilier">🏢 Immobilier</option>
          <option value="autre" selected>📦 Autre</option>
        </select>
      </div>

      <div class="form-group">
        <label>Ville</label>
        <input type="text" id="itemCity" maxlength="50" placeholder="Ex : Douala">
      </div>

      <div class="form-group">
        <label>Numéro WhatsApp *</label>
        <input type="tel" id="itemWhatsapp" required placeholder="+237 6XX XXX XXX">
      </div>

      <div class="modal-actions">
        <button type="button" class="btn-cancel" onclick="closePublishModal()">Annuler</button>
        <button type="submit" class="btn-submit" id="publishBtn">
          <span>Publier</span>
        </button>
      </div>
    </form>
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

  let isActivated = false;
  let currentCategory = 'tous';
  let imageBase64 = null;

  // ===== CHARGER PROFIL =====
  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId, {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (res.status === 401) {
        localStorage.clear();
        window.location.href = '/login';
        return;
      }
      if (!res.ok) return;
      const data = await res.json();
      isActivated = data.profile?.is_activated || false;
      if (!isActivated) {
        document.getElementById('inactiveBanner').classList.add('show');
      }
    } catch (e) {}
  }

  // ===== CHARGER ANNONCES =====
  async function loadItems(category = 'tous', search = '') {
    const list = document.getElementById('itemsList');

    // Skeletons
    list.innerHTML = Array(4).fill(`
      <div class="skel-card">
        <div class="skel-img"></div>
        <div class="skel-line"></div>
        <div class="skel-line short"></div>
      </div>
    `).join('');

    try {
      let url = '/api/marketplace/items?limit=100';
      if (category && category !== 'tous') url += '&category=' + category;
      if (search) url += '&search=' + encodeURIComponent(search);

      const res = await fetch(url);
      const data = await res.json();

      if (!data.success || !data.items || data.items.length === 0) {
        list.innerHTML = `
          <div class="empty-state">
            <div class="icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <h3>Aucune annonce</h3>
            <p>Soyez le premier à publier quelque chose !</p>
          </div>
        `;
        return;
      }

      list.innerHTML = data.items.map(item => renderItem(item)).join('');

    } catch (err) {
      list.innerHTML = `
        <div class="empty-state">
          <h3>Erreur de chargement</h3>
          <p>${err.message}</p>
        </div>
      `;
    }
  }

  // ===== RENDER UNE CARTE =====
  function renderItem(item) {
    const price = Number(item.price || 0).toLocaleString('fr-FR');
    const priceDisplay = item.price > 0 ? price + ' F' : 'Gratuit';
    const waNumber = (item.whatsapp || '').replace(/[^0-9]/g, '');
    const waMsg = encodeURIComponent(`Bonjour, je suis intéressé par votre annonce "${item.title}" sur TriBoost.`);
    const waLink = `https://wa.me/${waNumber}?text=${waMsg}`;
    const imageHtml = item.image_url
      ? `<img src="${item.image_url}" alt="${item.title}" loading="lazy">`
      : `<div class="placeholder">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>`;

    const catLabels = {
      electronique: '📱', mode: '👕', maison: '🏠',
      vehicule: '🚗', service: '🛠️', immobilier: '🏢', autre: '📦'
    };
    const badge = catLabels[item.category] || '📦';

    return `
      <div class="item-card">
        <div class="item-image">
          ${imageHtml}
          <div class="item-badge">${badge} ${item.category || 'autre'}</div>
        </div>
        <div class="item-content">
          <div class="item-title">${escapeHtml(item.title)}</div>
          <div class="item-price">${priceDisplay}</div>
          ${item.city ? `<div class="item-city">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            ${escapeHtml(item.city)}
          </div>` : ''}
          <a href="${waLink}" target="_blank" rel="noopener" class="wa-btn" onclick="vibrate(10)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
            </svg>
            Contacter
          </a>
        </div>
      </div>
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
      loadItems(currentCategory, document.getElementById('searchInput').value);
    });
  });

  // ===== RECHERCHE =====
  let searchTimer = null;
  document.getElementById('searchInput').addEventListener('input', function(e) {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      loadItems(currentCategory, e.target.value.trim());
    }, 400);
  });

  // ===== MODAL PUBLIER =====
  function openPublishModal() {
    vibrate(8);
    if (!isActivated) {
      showInactiveToast();
      return;
    }
    document.getElementById('publishModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closePublishModal() {
    document.getElementById('publishModal').classList.remove('open');
    document.body.style.overflow = '';
    document.getElementById('publishForm').reset();
    imageBase64 = null;
    document.querySelectorAll('.image-upload img, .image-upload .remove-img').forEach(el => el.remove());
    document.getElementById('uploadIcon').style.display = '';
    document.getElementById('uploadLabel').style.display = '';
  }

  // ===== UPLOAD IMAGE =====
  function handleImage(e) {
    const file = e.target.files[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert('Image trop lourde (max 5 MB)');
      return;
    }
    const reader = new FileReader();
    reader.onload = function(ev) {
      imageBase64 = ev.target.result;
      const upload = document.getElementById('imageUpload');
      // Supprimer ancien contenu
      upload.querySelectorAll('img, .remove-img').forEach(el => el.remove());
      // Ajouter nouvelle image
      const img = document.createElement('img');
      img.src = imageBase64;
      upload.appendChild(img);
      // Ajouter bouton supprimer
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'remove-img';
      btn.innerHTML = '✕';
      btn.onclick = function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        imageBase64 = null;
        img.remove();
        btn.remove();
        document.getElementById('uploadIcon').style.display = '';
        document.getElementById('uploadLabel').style.display = '';
      };
      upload.appendChild(btn);
      document.getElementById('uploadIcon').style.display = 'none';
      document.getElementById('uploadLabel').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

  // ===== SOUMETTRE =====
  async function submitItem(e) {
    e.preventDefault();
    vibrate(8);

    const btn = document.getElementById('publishBtn');
    const errEl = document.getElementById('modalError');
    errEl.style.display = 'none';

    const title = document.getElementById('itemTitle').value.trim();
    const description = document.getElementById('itemDesc').value.trim();
    const price = parseFloat(document.getElementById('itemPrice').value) || 0;
    const category = document.getElementById('itemCategory').value;
    const city = document.getElementById('itemCity').value.trim();
    const whatsapp = document.getElementById('itemWhatsapp').value.trim();

    if (!title || !whatsapp) {
      errEl.textContent = '⚠ Titre et WhatsApp sont obligatoires';
      errEl.style.display = 'block';
      return;
    }

    setButtonLoading(btn, true);

    try {
      const res = await fetch('/api/marketplace/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify({
          title, description, price,
          category, city, whatsapp,
          image_base64: imageBase64,
        }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Erreur de publication');

      vibrate(20);
      closePublishModal();
      showToast('✅ Annonce publiée avec succès !');
      loadItems(currentCategory, document.getElementById('searchInput').value);

    } catch (err) {
      vibrate([30, 50, 30]);
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
    } finally {
      setButtonLoading(btn, false, 'Publier');
    }
  }

  // ===== TOAST =====
  function showToast(msg, isError) {
    const old = document.getElementById('toast');
    if (old) old.remove();
    const t = document.createElement('div');
    t.id = 'toast';
    t.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: ${isError ? '#d32f2f' : '#2e7d32'};
      color: #fff; padding: 14px 20px; border-radius: 14px;
      font-size: 13px; font-weight: 600; z-index: 10001;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3); max-width: 340px;
      text-align: center; animation: slideDown 0.3s ease-out;
    `;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  // ===== TOAST INACTIF =====
  function showInactiveToast() {
    vibrate([20, 40, 20]);
    const old = document.getElementById('inactiveToast');
    if (old) old.remove();
    const t = document.createElement('div');
    t.id = 'inactiveToast';
    t.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: linear-gradient(135deg, #e65100, #bf360c);
      color: #fff; padding: 16px 20px; border-radius: 16px;
      font-size: 13px; font-weight: 600; z-index: 10000;
      box-shadow: 0 10px 30px rgba(230, 81, 0, 0.5);
      max-width: 340px; text-align: center; line-height: 1.5;
    `;
    t.innerHTML = `
      <div style="font-size:22px;">🔒</div>
      <div><strong>Compte non activé</strong></div>
      <div style="font-size:12px; opacity:0.9; margin-top:4px;">
        Activez pour 3 600 FCFA pour publier
      </div>
      <button onclick="location.href='/activation'" style="
        margin-top:10px; background:#fff; color:#e65100;
        border:none; padding:10px 20px; border-radius:10px;
        font-weight:800; font-size:12px; cursor:pointer;
        font-family:inherit; width:100%;
      ">Activer maintenant</button>
      <button onclick="this.parentElement.remove()" style="
        margin-top:6px; background:transparent; color:#fff;
        border:1px solid rgba(255,255,255,0.4);
        padding:8px 20px; border-radius:10px;
        font-weight:600; font-size:11px;
        cursor:pointer; font-family:inherit; width:100%;
      ">Plus tard</button>
    `;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 6000);
  }

  // ===== INIT =====
  loadProfile();
  loadItems();
</script>
</body>
</html>
"""
)