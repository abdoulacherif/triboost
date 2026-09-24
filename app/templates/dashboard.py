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
  }
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
  .logout-btn {
    background: var(--red-light); color: var(--red);
    border: none; padding: 8px 14px; border-radius: 10px;
    font-size: 12px; font-weight: 700; cursor: pointer;
  }
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
  }
  .service-icon {
    width: 100%; height: 80px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
  }
  .icon-green { background: var(--green-light); color: var(--green); }
  .icon-orange { background: var(--orange-light); color: var(--orange); }
  .icon-gold { background: var(--gold-light); color: var(--gold); }
  .icon-red { background: var(--red-light); color: var(--red); }
  .service-title { font-size: 14px; font-weight: 700; }
  .service-desc { font-size: 12px; color: #757575; }
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
<div class="app">
  <header class="topbar">
    <div class="avatar-top" id="userInitial">A</div>
    <div class="logo">Tri<span>Boost</span></div>
    <button class="logout-btn" onclick="logout()">Déconnexion</button>
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
    <a href="#" class="service-card">
      <div class="service-icon icon-green">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
        </svg>
      </div>
      <div>
        <div class="service-title">Formations</div>
        <div class="service-desc">9 formations</div>
      </div>
    </a>
    <a href="#" class="service-card">
      <div class="service-icon icon-orange">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
      </div>
      <div>
        <div class="service-title">TriBoost Shop</div>
        <div class="service-desc">Boutiques</div>
      </div>
    </a>
    <a href="#" class="service-card">
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
    <a href="#" class="service-card">
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
    <a href="#" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
      </div>
      Shop
    </a>
    <a href="#" class="nav-item">
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
    <a href="#" class="nav-item">
      <div class="nav-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
      </div>
      Paiements
    </a>
    <a href="#" class="nav-item">
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
  if (!token) window.location.href = '/login';

  const displayName = name || (email ? email.split('@')[0] : 'utilisateur');
  if (email) {
    document.getElementById('userName').textContent = displayName;
    const initial = displayName.charAt(0).toUpperCase();
    document.getElementById('userInitial').textContent = initial;
    document.getElementById('userInitial2').textContent = initial;
    document.getElementById('userInfo').textContent = email;
  }
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