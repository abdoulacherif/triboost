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
    transition: transform 0.15s;
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
  }
  .add-btn:active { transform: scale(0.92); }

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

  .banner-section { padding: 0 16px 16px; }
  .banner-card {
    background: linear-gradient(135deg, #fbc02d, #f57c00);
    border-radius: 18px; padding: 16px;
    display: flex; gap: 12px; align-items: center;
    box-shadow: 0 6px 16px rgba(245,124,0,0.3);
    margin-bottom: 10px; text-decoration: none; color: #212121;
    position: relative; overflow: hidden;
  }
  .banner-card::before {
    content: '★'; position: absolute; top: -10px; right: 10px;
    font-size: 60px; opacity: 0.15; color: #fff;
  }
  .banner-img {
    width: 60px; height: 60px; border-radius: 12px;
    background: rgba(255,255,255,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; overflow: hidden; flex-shrink: 0;
  }
  .banner-img img { width: 100%; height: 100%; object-fit: cover; }
  .banner-info { flex: 1; min-width: 0; position: relative; z-index: 2; }
  .banner-label {
    font-size: 10px; font-weight: 900; text-transform: uppercase;
    letter-spacing: 0.5px; color: #212121; opacity: 0.7; margin-bottom: 4px;
  }
  .banner-title {
    font-size: 14px; font-weight: 800; margin-bottom: 4px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .banner-price { font-size: 15px; font-weight: 900; }

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
  .boosted-badge {
    position: absolute; top: 8px; right: 8px;
    background: linear-gradient(135deg, #fbc02d, #f57c00);
    color: #212121; font-size: 9px; font-weight: 900;
    padding: 3px 8px; border-radius: 6px;
    letter-spacing: 0.5px; text-transform: uppercase;
    z-index: 2; box-shadow: 0 2px 6px rgba(0,0,0,0.2);
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

  .boost-btn {
    display: flex; align-items: center; justify-content: center; gap: 4px;
    background: linear-gradient(135deg, #fbc02d, #f57c00);
    color: #212121; border: none; padding: 6px 10px;
    border-radius: 8px; font-size: 10px; font-weight: 800;
    font-family: inherit; cursor: pointer; margin-top: 4px;
  }
  .boost-btn:active { transform: scale(0.95); }

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

  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(3px);
    z-index: 999;
    display: none;
    align-items: flex-end;
    justify-content: center;
  }
  .modal-overlay.open { display: flex; }
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
    font-family: inherit;
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

  .boost-options { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
  .boost-option {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px; border: 2px solid var(--border); border-radius: 14px;
    cursor: pointer; transition: all 0.2s; background: #fff;
  }
  .boost-option.selected { border-color: var(--green); background: var(--green-light); }
  .boost-option-title { font-size: 14px; font-weight: 800; color: var(--text-dark); }
  .boost-option-desc { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
  .boost-option-price { font-size: 16px; font-weight: 900; color: var(--green); }

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

  <div class="search-wrap">
    <div class="search-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input type="text" id="searchInput" placeholder="Rechercher un produit, une ville...">
    </div>
  </div>

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

  <div id="bannerContainer"></div>

  <div class="items-list" id="itemsList">
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
    <div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>
  </div>

  <button class="fab" onclick="openPublishModal()" aria-label="Publier">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="12" y1="5" x2="12" y2="19"></line>
      <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
  </button>

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

<div class="modal-overlay" id="boostModal" onclick="if(event.target===this) closeBoostModal()">
  <div class="modal-content">
    <div class="modal-handle"></div>
    <div class="modal-title">
      <span>🚀 Booster mon annonce</span>
      <button class="modal-close" onclick="closeBoostModal()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    <div class="boost-options" id="boostOptions">
      <div class="boost-option" onclick="selectBoost(this, '24h', 200)">
        <div>
          <div class="boost-option-title">⭐ Boost 24h</div>
          <div class="boost-option-desc">Annonce mise en avant 24h</div>
        </div>
        <div class="boost-option-price">200 F</div>
      </div>
      <div class="boost-option" onclick="selectBoost(this, '7d', 500)">
        <div>
          <div class="boost-option-title">🔥 Boost 7 jours</div>
          <div class="boost-option-desc">Annonce en tête pendant 7 jours</div>
        </div>
        <div class="boost-option-price">500 F</div>
      </div>
      <div class="boost-option" onclick="selectBoost(this, 'banner', 1500)">
        <div>
          <div class="boost-option-title">📢 Bannière</div>
          <div class="boost-option-desc">Bannière en haut du marché 7 jours</div>
        </div>
        <div class="boost-option-price">1 500 F</div>
      </div>
      <div class="boost-option" onclick="selectBoost(this, 'notify', 2000)">
        <div>
          <div class="boost-option-title">🔔 Notification à tous</div>
          <div class="boost-option-desc">Notification push à tous les utilisateurs</div>
        </div>
        <div class="boost-option-price">2 000 F</div>
      </div>
    </div>
    <div class="modal-actions">
      <button type="button" class="btn-cancel" onclick="closeBoostModal()">Annuler</button>
      <button type="button" class="btn-submit" id="boostConfirmBtn" onclick="confirmBoost()">
        <span>Booster</span>
      </button>
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
  let currentCategory = 'tous';
  let imageBase64 = null;
  let currentBoostItem = null;
  let currentBoostType = null;

  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (res.status === 401) { localStorage.clear(); window.location.href = '/login'; return; }
      if (!res.ok) return;
      const data = await res.json();
      isActivated = data.profile?.is_activated || false;
      if (!isActivated) document.getElementById('inactiveBanner').classList.add('show');
    } catch (e) {}
  }

  async function loadItems(category, search) {
    category = category || 'tous';
    search = search || '';
    const list = document.getElementById('itemsList');
    const bannerContainer = document.getElementById('bannerContainer');

    list.innerHTML = Array(4).fill('<div class="skel-card"><div class="skel-img"></div><div class="skel-line"></div><div class="skel-line short"></div></div>').join('');
    bannerContainer.innerHTML = '';

    try {
      let url = '/api/marketplace/items?limit=100&t=' + Date.now();
      if (category && category !== 'tous') url += '&category=' + category;
      if (search) url += '&search=' + encodeURIComponent(search);

      const res = await fetch(url);
      const data = await res.json();

      if (!data.success || !data.items || data.items.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg></div><h3>Aucune annonce</h3><p>Soyez le premier à publier !</p></div>';
        return;
      }

      const now = new Date();
      const sorted = (data.items || []).sort((a, b) => {
        const aBanner = a.is_banner && a.banner_until && new Date(a.banner_until) > now;
        const bBanner = b.is_banner && b.banner_until && new Date(b.banner_until) > now;
        if (aBanner && !bBanner) return -1;
        if (!aBanner && bBanner) return 1;

        const aBoost = a.boosted_until && new Date(a.boosted_until) > now;
        const bBoost = b.boosted_until && new Date(b.boosted_until) > now;
        if (aBoost && !bBoost) return -1;
        if (!aBoost && bBoost) return 1;

        return 0;
      });

      const banners = sorted.filter(i => i.is_banner && i.banner_until && new Date(i.banner_until) > now);
      if (banners.length > 0) {
        bannerContainer.innerHTML = '<div class="banner-section">' + banners.map(b => {
          const img = b.image_url ? '<img src="' + b.image_url + '">' : '⭐';
          const waNum = (b.whatsapp || '').replace(/[^0-9]/g, '');
          const price = b.price > 0 ? Number(b.price).toLocaleString('fr-FR') + ' F' : 'Gratuit';
          return '<a href="https://wa.me/' + waNum + '" target="_blank" class="banner-card">' +
            '<div class="banner-img">' + img + '</div>' +
            '<div class="banner-info">' +
            '<div class="banner-label">⭐ Sponsorisé</div>' +
            '<div class="banner-title">' + escapeHtml(b.title) + '</div>' +
            '<div class="banner-price">' + price + '</div>' +
            '</div></a>';
        }).join('') + '</div>';
      }

      const nonBanners = sorted.filter(i => !(i.is_banner && i.banner_until && new Date(i.banner_until) > now));
      list.innerHTML = nonBanners.map(item => renderItem(item)).join('') || '<div class="empty-state"><h3>Aucune annonce</h3></div>';

    } catch (err) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur de chargement</h3><p>' + err.message + '</p></div>';
    }
  }

  function renderItem(item) {
    const price = Number(item.price || 0).toLocaleString('fr-FR');
    const priceDisplay = item.price > 0 ? price + ' F' : 'Gratuit';
    const waNumber = (item.whatsapp || '').replace(/[^0-9]/g, '');
    const waMsg = encodeURIComponent('Bonjour, je suis intéressé par votre annonce "' + item.title + '" sur TriBoost.');
    const waLink = 'https://wa.me/' + waNumber + '?text=' + waMsg;

    const imageHtml = item.image_url
      ? '<img src="' + item.image_url + '" alt="" loading="lazy">'
      : '<div class="placeholder"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg></div>';

    const catLabels = { electronique: '📱', mode: '👕', maison: '🏠', vehicule: '🚗', service: '🛠️', immobilier: '🏢', autre: '📦' };
    const catBadge = catLabels[item.category] || '📦';

    const now = new Date();
    const isBoosted = item.boosted_until && new Date(item.boosted_until) > now;
    const isMine = item.user_id === userId;

    const boostBadge = isBoosted ? '<div class="boosted-badge">⭐ Boosté</div>' : '';
    const boostBtn = isMine ? '<button class="boost-btn" onclick="openBoostModal(\\'' + item.id + '\\')">🚀 Booster</button>' : '';

    return '<div class="item-card">' +
      '<div class="item-image">' +
      imageHtml +
      boostBadge +
      '<div class="item-badge">' + catBadge + ' ' + (item.category || 'autre') + '</div>' +
      '</div>' +
      '<div class="item-content">' +
      '<div class="item-title">' + escapeHtml(item.title) + '</div>' +
      '<div class="item-price">' + priceDisplay + '</div>' +
      (item.city ? '<div class="item-city"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>' + escapeHtml(item.city) + '</div>' : '') +
      '<a href="' + waLink + '" target="_blank" rel="noopener" class="wa-btn" onclick="vibrate(10)">' +
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>' +
      'Contacter</a>' +
      boostBtn +
      '</div></div>';
  }

  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, function(c) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c];
    });
  }

  document.querySelectorAll('.cat-chip').forEach(function(chip) {
    chip.addEventListener('click', function() {
      document.querySelectorAll('.cat-chip').forEach(function(c) { c.classList.remove('active'); });
      this.classList.add('active');
      currentCategory = this.dataset.cat;
      vibrate(5);
      loadItems(currentCategory, document.getElementById('searchInput').value);
    });
  });

  let searchTimer = null;
  document.getElementById('searchInput').addEventListener('input', function(e) {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function() {
      loadItems(currentCategory, e.target.value.trim());
    }, 400);
  });

  function openPublishModal() {
    vibrate(8);
    if (!isActivated) { showInactiveToast(); return; }
    document.getElementById('publishModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closePublishModal() {
    document.getElementById('publishModal').classList.remove('open');
    document.body.style.overflow = '';
    document.getElementById('publishForm').reset();
    imageBase64 = null;
    document.querySelectorAll('.image-upload img, .image-upload .remove-img').forEach(function(el) { el.remove(); });
    document.getElementById('uploadIcon').style.display = '';
    document.getElementById('uploadLabel').style.display = '';
  }

  function handleImage(e) {
    const file = e.target.files[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) { alert('Image trop lourde (max 5 MB)'); return; }
    const reader = new FileReader();
    reader.onload = function(ev) {
      imageBase64 = ev.target.result;
      const upload = document.getElementById('imageUpload');
      upload.querySelectorAll('img, .remove-img').forEach(function(el) { el.remove(); });
      const img = document.createElement('img');
      img.src = imageBase64;
      upload.appendChild(img);
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'remove-img';
      btn.innerHTML = '✕';
      btn.onclick = function(evt) {
        evt.preventDefault(); evt.stopPropagation();
        imageBase64 = null; img.remove(); btn.remove();
        document.getElementById('uploadIcon').style.display = '';
        document.getElementById('uploadLabel').style.display = '';
      };
      upload.appendChild(btn);
      document.getElementById('uploadIcon').style.display = 'none';
      document.getElementById('uploadLabel').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

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
      errEl.textContent = '⚠ Titre et WhatsApp obligatoires';
      errEl.style.display = 'block';
      return;
    }

    setButtonLoading(btn, true);

    try {
      const res = await fetch('/api/marketplace/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ title, description, price, category, city, whatsapp, image_base64: imageBase64 })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      vibrate(20);
      closePublishModal();
      showToast('✅ Annonce publiée !');
      loadItems(currentCategory, document.getElementById('searchInput').value);
    } catch (err) {
      vibrate([30, 50, 30]);
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
    } finally {
      setButtonLoading(btn, false, 'Publier');
    }
  }

  function openBoostModal(itemId) {
    if (!isActivated) { showInactiveToast(); return; }
    currentBoostItem = itemId;
    currentBoostType = null;
    document.querySelectorAll('.boost-option').forEach(function(o) { o.classList.remove('selected'); });
    document.getElementById('boostModal').classList.add('open');
    document.body.style.overflow = 'hidden';
    vibrate(8);
  }

  function closeBoostModal() {
    document.getElementById('boostModal').classList.remove('open');
    document.body.style.overflow = '';
    currentBoostItem = null;
    currentBoostType = null;
  }

  function selectBoost(el, type, price) {
    document.querySelectorAll('.boost-option').forEach(function(o) { o.classList.remove('selected'); });
    el.classList.add('selected');
    currentBoostType = type;
    vibrate(5);
  }

  async function confirmBoost() {
    if (!currentBoostType) { alert('⚠ Choisissez un type de boost'); return; }

    const btn = document.getElementById('boostConfirmBtn');
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/ads/boost/' + currentBoostItem, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ boost_type: currentBoostType })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      vibrate(20);
      closeBoostModal();
      showToast('✅ ' + data.result.message);
      loadItems(currentCategory, document.getElementById('searchInput').value);
    } catch (e) {
      alert('⚠ ' + e.message);
    }
    btn.disabled = false;
    btn.innerHTML = '<span>Booster</span>';
  }

  function showToast(msg) {
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#2e7d32;color:#fff;padding:14px 20px;border-radius:14px;font-size:13px;font-weight:700;z-index:10001;box-shadow:0 8px 24px rgba(0,0,0,0.3);max-width:340px;text-align:center;';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function() { t.remove(); }, 3000);
  }

  function showInactiveToast() {
    vibrate([20, 40, 20]);
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#e65100,#bf360c);color:#fff;padding:16px 20px;border-radius:16px;font-size:13px;font-weight:600;z-index:10000;box-shadow:0 10px 30px rgba(230,81,0,0.5);max-width:340px;text-align:center;line-height:1.5;';
    t.innerHTML = '<div style="font-size:24px;margin-bottom:6px;">🔒</div><div><strong>Compte non activé</strong></div><div style="font-size:12px;opacity:0.9;margin-top:4px;">Activez pour 3 600 FCFA</div><button onclick="location.href=\\'/activation\\'" style="margin-top:12px;background:#fff;color:#e65100;border:none;padding:10px 20px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;font-family:inherit;width:100%;">Activer maintenant</button>';
    document.body.appendChild(t);
    setTimeout(function() { t.remove(); }, 6000);
  }

  (async function() {
    await loadProfile();
    loadItems();
  })();
</script>
</body>
</html>
"""
)