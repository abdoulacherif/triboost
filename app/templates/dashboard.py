from app.templates.shared import CSS_COMMUN, HTML_HEAD

HTML_DASHBOARD = (
    HTML_HEAD.format(title="Accueil — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
  }
  .app {
    width: 100%; max-width: 480px;
    background: #fff; min-height: 100vh;
    padding-bottom: calc(100px + var(--safe-bottom));
    padding-top: var(--safe-top);
    position: relative;
  }

  /* ===== TOPBAR ===== */
  .topbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 20px;
  }
  .avatar-top {
    width: 36px; height: 36px; border-radius: 50%;
    background: var(--green); color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 14px;
  }
  .logo { font-size: 22px; font-weight: 800; color: var(--green); }
  .logo span { color: var(--gold); }
  .menu-burger {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: var(--green-light);
    color: var(--green);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.15s, background 0.2s;
  }
  .menu-burger:active {
    transform: scale(0.92);
    background: #c8e6c9;
  }

  /* ===== OVERLAY ===== */
  .menu-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
    z-index: 998;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }
  .menu-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }

  /* ===== DRAWER LATÉRAL ===== */
  .side-drawer {
    position: fixed;
    top: 0; right: 0;
    height: 100vh;
    height: 100dvh;
    width: 82%;
    max-width: 340px;
    background: #fff;
    z-index: 999;
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    flex-direction: column;
    box-shadow: -8px 0 30px rgba(0,0,0,0.15);
    padding-top: var(--safe-top);
    padding-bottom: var(--safe-bottom);
    overflow-y: auto;
  }
  .side-drawer.open {
    transform: translateX(0);
  }

  /* En-tête du drawer */
  .drawer-header {
    padding: 24px 20px 20px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    color: #fff;
    position: relative;
    overflow: hidden;
  }
  .drawer-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
  }
  .drawer-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 120px; height: 120px;
    background: rgba(251, 192, 45, 0.2);
    border-radius: 50%;
  }
  .drawer-close {
    position: absolute;
    top: 16px; right: 16px;
    width: 36px; height: 36px;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    color: #fff;
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    z-index: 2;
    transition: transform 0.15s, background 0.2s;
  }
  .drawer-close:active {
    transform: scale(0.9);
    background: rgba(255,255,255,0.3);
  }
  .drawer-user {
    display: flex; align-items: center; gap: 14px;
    position: relative; z-index: 2;
    margin-top: 8px;
  }
  .drawer-avatar {
    width: 56px; height: 56px; border-radius: 50%;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(4px);
    color: #fff; font-weight: 800; font-size: 22px;
    display: flex; align-items: center; justify-content: center;
    border: 2px solid rgba(255,255,255,0.3);
  }
  .drawer-user-info h4 {
    font-size: 15px; font-weight: 700;
    margin-bottom: 2px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 180px;
  }
  .drawer-user-info p {
    font-size: 12px; opacity: 0.85;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 180px;
  }
  .drawer-user-info .drawer-code {
    display: inline-block;
    background: rgba(251, 192, 45, 0.25);
    color: #fff;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    margin-top: 6px;
    font-family: 'Courier New', monospace;
    letter-spacing: 0.5px;
  }

  /* Liste des items */
  .drawer-nav {
    padding: 12px 12px 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .drawer-section-label {
    font-size: 10px;
    font-weight: 800;
    color: #bdbdbd;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 14px 14px 6px;
  }
  .drawer-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px;
    border-radius: 14px;
    text-decoration: none;
    color: var(--text-dark);
    font-size: 15px;
    font-weight: 600;
    transition: background 0.2s, transform 0.15s;
    position: relative;
    overflow: hidden;
  }
  .drawer-item:active {
    background: #f5f5f5;
    transform: scale(0.98);
  }
  .drawer-item:hover {
    background: var(--green-light);
  }
  .drawer-item-icon {
    width: 40px; height: 40px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .drawer-item-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .drawer-item-text .title {
    font-size: 15px;
    font-weight: 700;
  }
  .drawer-item-text .desc {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
  }
  .drawer-item-arrow {
    color: #bdbdbd;
    flex-shrink: 0;
  }

  /* Icônes couleurs */
  .di-green  { background: var(--green-light);  color: var(--green);  }
  .di-orange { background: var(--orange-light); color: var(--orange); }
  .di-gold   { background: var(--gold-light);   color: #f9a825;        }
  .di-red    { background: var(--red-light);    color: var(--red);    }
  .di-blue   { background: #e3f2fd;             color: #1976d2;        }
  .di-purple { background: #f3e5f5;             color: #7b1fa2;        }
  .di-teal   { background: #e0f2f1;             color: #00796b;        }

  /* Déconnexion */
  .drawer-footer {
    padding: 12px 12px 20px;
    border-top: 1px solid var(--border);
  }
  .drawer-logout {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px;
    border-radius: 14px;
    background: var(--red-light);
    color: var(--red);
    font-size: 15px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    width: 100%;
    transition: transform 0.15s, background 0.2s;
    font-family: inherit;
  }
  .drawer-logout:active {
    transform: scale(0.98);
    background: #ffcdd2;
  }
  .drawer-logout-icon {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: rgba(211, 47, 47, 0.15);
    display: flex; align-items: center; justify-content: center;
  }

  /* ===== PROFIL CARD ===== */
  .profile-card {
    margin: 0 20px 20px; padding: 16px;
    border-radius: 20px; border: 1px solid var(--border);
    display: flex; align-items: center; gap: 12px;
    background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }
  .profile-avatar {
    width: 50px; height: 50px; border-radius: 50%;
    background: var(--green); color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 20px; position: relative;
  }
  .online-dot {
    width: 12px; height: 12px; background: var(--gold);
    border: 2px solid #fff; border-radius: 50%;
    position: absolute; bottom: 0; right: 0;
  }
  .profile-info { flex: 1; min-width: 0; }
  .profile-info h3 { font-size: 15px; font-weight: 700; }
  .profile-info h3 span { color: var(--gold); }
  .badge-abonne {
    display: inline-block; background: var(--green-light);
    color: var(--green); font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 10px; margin-top: 4px;
  }
  .profile-info p {
    font-size: 12px; color: #757575; margin-top: 4px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }

  /* ===== BALANCE ===== */
  .balance-card {
    margin: 0 20px 24px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 20px; padding: 20px; color: #fff;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3);
  }
  .balance-card::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .balance-label {
    font-size: 12px; font-weight: 600; opacity: 0.9;
    text-transform: uppercase; letter-spacing: 0.5px;
    display: flex; justify-content: space-between; align-items: center;
    position: relative; z-index: 2;
  }
  .arrow-circle {
    width: 28px; height: 28px; border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
  }
  .balance-amount { font-size: 32px; font-weight: 800; margin: 8px 0; position: relative; z-index: 2; }
  .balance-amount span { font-size: 16px; font-weight: 600; }
  .balance-sub { font-size: 13px; opacity: 0.8; margin-bottom: 16px; position: relative; z-index: 2; }
  .balance-buttons { display: flex; gap: 10px; position: relative; z-index: 2; }
  .btn-white {
    flex: 1; background: #fff; color: var(--green);
    border: none; padding: 12px; border-radius: 12px;
    font-weight: 700; font-size: 14px; cursor: pointer;
  }
  .btn-gold {
    flex: 1; background: var(--gold); color: #212121;
    border: none; padding: 12px; border-radius: 12px;
    font-weight: 700; font-size: 14px; cursor: pointer;
  }

  /* ===== SERVICES ===== */
  .section-title { margin: 0 20px 14px; font-size: 18px; font-weight: 800; }
  .services-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 14px; padding: 0 20px;
  }
  .service-card {
    background: #fff; border: 1px solid var(--border);
    border-radius: 20px; padding: 16px;
    display: flex; flex-direction: column; gap: 12px;
    text-decoration: none; color: inherit;
    transition: transform 0.15s;
  }
  .service-card:active { transform: scale(0.97); }
  .service-icon {
    width: 100%; height: 80px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
  }
  .icon-green { background: var(--green-light); color: var(--green); }
  .icon-orange { background: var(--orange-light); color: var(--orange); }
  .icon-gold { background: var(--gold-light); color: #f9a825; }
  .icon-red { background: var(--red-light); color: var(--red); }
  .service-title { font-size: 14px; font-weight: 700; }
  .service-desc { font-size: 12px; color: #757575; }

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
</style>
</head>
<body>

<!-- OVERLAY -->
<div class="menu-overlay" id="menuOverlay" onclick="closeMenu()"></div>

<!-- DRAWER LATÉRAL -->
<aside class="side-drawer" id="sideDrawer">
  <div class="drawer-header">
    <button class="drawer-close" onclick="closeMenu()" aria-label="Fermer">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
    <div class="drawer-user">
      <div class="drawer-avatar" id="drawerInitial">A</div>
      <div class="drawer-user-info">
        <h4 id="drawerName">Utilisateur</h4>
        <p id="drawerEmail">email@exemple.com</p>
        <span class="drawer-code" id="drawerCode">TB------</span>
      </div>
    </div>
  </div>

  <nav class="drawer-nav">
    <div class="drawer-section-label">Navigation</div>

    <a href="/affaire" class="drawer-item">
      <div class="drawer-item-icon di-green">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Affaire</span>
        <span class="desc">Opportunités business</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>

    <a href="/tache" class="drawer-item">
      <div class="drawer-item-icon di-blue">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 11l3 3L22 4"></path>
          <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Tâche</span>
        <span class="desc">Missions à accomplir</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>

    <a href="/tourner" class="drawer-item">
      <div class="drawer-item-icon di-purple">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Tourner</span>
        <span class="desc">Faire tourner la roue</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>

    <a href="/formation" class="drawer-item">
      <div class="drawer-item-icon di-orange">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Formation</span>
        <span class="desc">Apprendre & progresser</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>

    <a href="/shop" class="drawer-item">
      <div class="drawer-item-icon di-teal">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Shop</span>
        <span class="desc">Produits & services</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>

    <a href="/boost" class="drawer-item">
      <div class="drawer-item-icon di-gold">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Boost</span>
        <span class="desc">Accélérer vos gains</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>

    <a href="/affilie" class="drawer-item">
      <div class="drawer-item-icon di-red">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      </div>
      <div class="drawer-item-text">
        <span class="title">Affilié</span>
        <span class="desc">Votre réseau à 3 niveaux</span>
      </div>
      <div class="drawer-item-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </a>
  </nav>

  <div class="drawer-footer">
    <button class="drawer-logout" onclick="logout()">
      <div class="drawer-logout-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </div>
      <span>Déconnexion</span>
    </button>
  </div>
</aside>

<!-- APP -->
<div class="app">
  <header class="topbar">
    <div class="avatar-top" id="userInitial">A</div>
    <div class="logo">Tri<span>Boost</span></div>
    <button class="menu-burger" onclick="openMenu()" aria-label="Menu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
  </header>

  <div class="profile-card">
    <div class="profile-avatar">
      <span id="userInitial2">A</span>
      <div class="online-dot"></div>
    </div>
    <div class="profile-info">
      <h3>Bonjour, <span id="userName">...</span></h3>
      <div class="badge-abonne">Compte actif</div>
      <p id="userInfo">TriBoost</p>
    </div>
  </div>

  <div class="balance-card">
    <div class="balance-label">
      VOS SOLDES DISPONIBLES
      <div class="arrow-circle">›</div>
    </div>
    <div class="balance-amount">1 048 <span>FCFA</span></div>
    <div class="balance-sub">Principal 1 048 F · Crypto 0.00 $</div>
    <div class="balance-buttons">
      <button class="btn-white">Retirer</button>
      <button class="btn-gold">Historique</button>
    </div>
  </div>

  <div class="section-title">Nos services</div>
  <div class="services-grid">

    <a href="/marche" class="service-card">
      <div class="service-icon icon-green">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </div>
      <div>
        <div class="service-title">Marché</div>
        <div class="service-desc">Acheter & vendre</div>
      </div>
    </a>

    <a href="/boutique" class="service-card">
      <div class="service-icon icon-orange">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
      </div>
      <div>
        <div class="service-title">Boutique</div>
        <div class="service-desc">Nos produits</div>
      </div>
    </a>

    <a href="/affilie" class="service-card">
      <div class="service-icon icon-gold">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      </div>
      <div>
        <div class="service-title">Mon Réseau</div>
        <div class="service-desc">3 niveaux</div>
      </div>
    </a>

    <a href="/commissions" class="service-card">
      <div class="service-icon icon-red">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
          <polyline points="17 6 23 6 23 12"></polyline>
        </svg>
      </div>
      <div>
        <div class="service-title">Commissions</div>
        <div class="service-desc">Vos gains</div>
      </div>
    </a>
  </div>

  <nav class="bottom-nav">
    <a href="/dashboard" class="nav-item active">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </div>
      Accueil
    </a>
    <a href="/shop" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
      </div>
      Shop
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
    <a href="/chat" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </div>
      Chat
    </a>
  </nav>
</div>

<script>
  const token = localStorage.getItem('access_token');
  const email = localStorage.getItem('user_email');
  const name = localStorage.getItem('user_name');
  const referralCode = localStorage.getItem('user_referral_code') || 'TB------';

  if (!token) window.location.href = '/login';

  const displayName = name || (email ? email.split('@')[0] : 'utilisateur');
  if (email) {
    document.getElementById('userName').textContent = displayName;
    const initial = displayName.charAt(0).toUpperCase();
    document.getElementById('userInitial').textContent = initial;
    document.getElementById('userInitial2').textContent = initial;
    document.getElementById('userInfo').textContent = email;

    // Drawer
    document.getElementById('drawerInitial').textContent = initial;
    document.getElementById('drawerName').textContent = displayName;
    document.getElementById('drawerEmail').textContent = email;
    document.getElementById('drawerCode').textContent = referralCode;
  }

  // ===== MENU =====
  function openMenu() {
    document.getElementById('sideDrawer').classList.add('open');
    document.getElementById('menuOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
    if (navigator.vibrate) navigator.vibrate(8);
  }

  function closeMenu() {
    document.getElementById('sideDrawer').classList.remove('open');
    document.getElementById('menuOverlay').classList.remove('open');
    document.body.style.overflow = '';
  }

  // ===== FERMER AVEC BOUTON RETOUR ANDROID =====
  window.addEventListener('popstate', () => {
    if (document.getElementById('sideDrawer').classList.contains('open')) {
      closeMenu();
    }
  });

  // ===== FERMER AVEC ESC =====
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });

  // ===== DÉCONNEXION =====
  function logout() {
    if (navigator.vibrate) navigator.vibrate(15);
    localStorage.clear();
    window.location.href = '/login';
  }
</script>
</body>
</html>
"""
)