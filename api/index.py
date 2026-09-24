from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="TriBoost")


# ============================================================
# HTML EN DUR (pas de fichiers templates → pas de 404)
# ============================================================

CSS_COMMUN = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', Roboto, sans-serif;
    background: #fcfcfc; color: #212121;
    display: flex; justify-content: center; min-height: 100vh;
  }
  .wrap {
    width: 100%; max-width: 420px;
    padding: 40px 24px;
    display: flex; flex-direction: column; justify-content: center;
    min-height: 100vh;
  }
  .logo {
    text-align: center; font-size: 32px;
    font-weight: 800; color: #2e7d32; margin-bottom: 8px;
  }
  .logo span { color: #fbc02d; }
  .subtitle {
    text-align: center; color: #757575;
    font-size: 14px; margin-bottom: 32px;
  }
  .form-group { margin-bottom: 16px; }
  .form-group label {
    display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px;
  }
  .form-group input {
    width: 100%; padding: 14px;
    border: 1px solid #eeeeee; border-radius: 12px;
    font-size: 14px; outline: none;
  }
  .form-group input:focus { border-color: #2e7d32; }
  .btn-primary {
    width: 100%; padding: 14px; background: #2e7d32;
    color: #fff; border: none; border-radius: 12px;
    font-weight: 700; font-size: 15px; cursor: pointer;
    margin-top: 8px;
  }
  .footer {
    text-align: center; margin-top: 24px;
    font-size: 14px; color: #757575;
  }
  .footer a { color: #2e7d32; font-weight: 600; text-decoration: none; }
</style>
"""


HTML_LOGIN = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Connexion — TriBoost</title>
""" + CSS_COMMUN + """
</head>
<body>
<div class="wrap">
  <div class="logo">Tri<span>Boost</span></div>
  <div class="subtitle">Connectez-vous à votre compte</div>
  <form onsubmit="event.preventDefault(); window.location.href='/dashboard';">
    <div class="form-group">
      <label>Email</label>
      <input type="email" required placeholder="vous@exemple.com">
    </div>
    <div class="form-group">
      <label>Mot de passe</label>
      <input type="password" required placeholder="••••••••">
    </div>
    <button type="submit" class="btn-primary">Se connecter</button>
  </form>
  <div class="footer">
    Pas de compte ? <a href="/register">Inscrivez-vous</a>
  </div>
</div>
</body>
</html>
"""


HTML_REGISTER = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Inscription — TriBoost</title>
""" + CSS_COMMUN + """
<style>
  .referral-info {
    background: #e8f5e9; color: #2e7d32;
    padding: 10px 14px; border-radius: 10px;
    font-size: 13px; margin-bottom: 16px; text-align: center;
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="logo">Tri<span>Boost</span></div>
  <div class="subtitle">Créez votre compte gratuit</div>
  <div class="referral-info">🎁 Inscription via un lien de parrainage</div>
  <form onsubmit="event.preventDefault(); alert('Compte créé (démo)'); window.location.href='/login';">
    <div class="form-group">
      <label>Nom complet</label>
      <input type="text" required placeholder="Ex : Abdoula Diallo">
    </div>
    <div class="form-group">
      <label>Email</label>
      <input type="email" required placeholder="vous@exemple.com">
    </div>
    <div class="form-group">
      <label>Numéro Mobile Money</label>
      <input type="tel" required placeholder="+237 6XX XXX XXX">
    </div>
    <div class="form-group">
      <label>Mot de passe (min. 10 caractères)</label>
      <input type="password" minlength="10" required>
    </div>
    <button type="submit" class="btn-primary">Créer mon compte</button>
  </form>
  <div class="footer">
    Déjà inscrit ? <a href="/login">Se connecter</a>
  </div>
</div>
</body>
</html>
"""


HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Accueil — TriBoost</title>
<style>
  :root {
    --green: #2e7d32;
    --green-dark: #1b5e20;
    --green-light: #e8f5e9;
    --gold: #fbc02d;
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
    --red: #d32f2f;
    --red-light: #ffebee;
    --border: #eeeeee;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', Roboto, sans-serif;
    background: #fcfcfc; color: #212121;
    display: flex; justify-content: center; min-height: 100vh;
  }
  .app {
    width: 100%; max-width: 420px;
    background: #fff; min-height: 100vh;
    padding-bottom: 100px; position: relative;
    box-shadow: 0 0 20px rgba(0,0,0,0.05);
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
  .menu-icon {
    width: 36px; height: 36px; border-radius: 50%;
    background: var(--green-light); color: var(--green);
    display: flex; align-items: center; justify-content: center;
    border: none; cursor: pointer;
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
  .profile-info { flex: 1; }
  .profile-info h3 { font-size: 15px; font-weight: 700; }
  .profile-info h3 span { color: var(--gold); }
  .badge-abonne {
    display: inline-block; background: var(--green-light);
    color: var(--green); font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 10px; margin-top: 4px;
  }
  .profile-info p { font-size: 12px; color: #757575; margin-top: 4px; }
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
    width: 100%; max-width: 420px;
    background: #fff; border-top: 1px solid var(--border);
    display: flex; justify-content: space-around; align-items: center;
    padding: 12px 10px 20px;
    border-radius: 24px 24px 0 0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    z-index: 100;
  }
  .nav-item {
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    font-size: 11px; color: #757575; text-decoration: none;
    font-weight: 500;
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
    <div class="avatar-top">A</div>
    <div class="logo">Tri<span>Boost</span></div>
    <button class="menu-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
  </header>

  <div class="profile-card">
    <div class="profile-avatar">
      A
      <div class="online-dot"></div>
    </div>
    <div class="profile-info">
      <h3>Bon après-midi, <span>abdo...</span></h3>
      <div class="badge-abonne">Abonné</div>
      <p>abdoula · 147 filleuls</p>
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
        <div class="service-desc">Boutiques & produits</div>
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
</body>
</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_LOGIN


@app.get("/login", response_class=HTMLResponse)
async def login():
    return HTML_LOGIN


@app.get("/register", response_class=HTMLResponse)
async def register():
    return HTML_REGISTER


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return HTML_DASHBOARD


@app.get("/health")
async def health():
    return {"status": "ok", "app": "TriBoost"}


@app.get("/api/test")
async def test_api():
    return {"message": "API TriBoost fonctionne", "routes": ["/", "/login", "/register", "/dashboard", "/health"]}


# Handler pour Vercel
handler = app