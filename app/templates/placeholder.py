from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN


def make_placeholder(title: str, icon_svg: str, description: str, color: str = "green") -> str:
    """
    Génère une page placeholder avec bouton retour.
    color: green, orange, gold, red, blue, purple, teal
    """
    return (
        HTML_HEAD.format(title=f"{title} — TriBoost")
        + CSS_COMMUN
        + """
<style>
  body { background: #f5f5f5; }
  .app {
    width: 100%; max-width: 480px;
    background: #fff; min-height: 100vh;
    padding-bottom: calc(40px + var(--safe-bottom));
    padding-top: var(--safe-top);
    display: flex;
    flex-direction: column;
  }
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
    transition: transform 0.15s;
    text-decoration: none;
  }
  .back-btn:active { transform: scale(0.92); }
  .page-title {
    font-size: 18px; font-weight: 800; color: var(--text-dark);
    flex: 1; text-align: center;
  }
  .spacer { width: 40px; }

  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 24px;
    text-align: center;
  }
  .icon-big {
    width: 120px; height: 120px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  .icon-green  { background: var(--green-light);  color: var(--green);  }
  .icon-orange { background: #fff3e0;             color: #f57c00;        }
  .icon-gold   { background: #fff8e1;             color: #f9a825;        }
  .icon-red    { background: var(--red-light);    color: var(--red);     }
  .icon-blue   { background: #e3f2fd;             color: #1976d2;        }
  .icon-purple { background: #f3e5f5;             color: #7b1fa2;        }
  .icon-teal   { background: #e0f2f1;             color: #00796b;        }

  h1 {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 12px;
  }
  p {
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 300px;
    margin-bottom: 24px;
  }
  .badge-soon {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #fff3e0;
    color: #e65100;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .btn-back {
    margin-top: 24px;
    background: var(--green);
    color: #fff;
    border: none;
    padding: 14px 32px;
    border-radius: 14px;
    font-weight: 700;
    font-size: 14px;
    font-family: inherit;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3);
    transition: transform 0.15s;
  }
  .btn-back:active { transform: scale(0.96); }
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
    <div class="page-title">""" + title + """</div>
    <div class="spacer"></div>
  </header>

  <div class="content">
    <div class="icon-big icon-""" + color + """">
      """ + icon_svg + """
    </div>

    <h1>""" + title + """</h1>
    <p>""" + description + """</p>

    <div class="badge-soon">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
      Bientôt disponible
    </div>

    <a href="/dashboard" class="btn-back">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
      Retour au dashboard
    </a>
  </div>
</div>

"""
        + JS_COMMUN
        + """
<script>
  const token = localStorage.getItem('access_token');
  if (!token) window.location.href = '/login';
</script>
</body>
</html>
"""
    )


# ============================================================
# ICÔNES SVG RÉUTILISABLES
# ============================================================
ICON_AFFAIRE = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
</svg>"""

ICON_TACHE = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 11l3 3L22 4"></path>
  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
</svg>"""

ICON_TOURNER = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="23 4 23 10 17 10"></polyline>
  <polyline points="1 20 1 14 7 14"></polyline>
  <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
</svg>"""

ICON_FORMATION = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
</svg>"""

ICON_SHOP = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="9" cy="21" r="1"></circle>
  <circle cx="20" cy="21" r="1"></circle>
  <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
</svg>"""

ICON_BOOST = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
</svg>"""

ICON_AFFILIE = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
  <circle cx="9" cy="7" r="4"></circle>
  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
</svg>"""

ICON_BOUTIQUE = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
  <polyline points="9 22 9 12 15 12 15 22"></polyline>
</svg>"""

ICON_COMMISSIONS = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
  <polyline points="17 6 23 6 23 12"></polyline>
</svg>"""

ICON_PAIEMENTS = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
  <line x1="1" y1="10" x2="23" y2="10"></line>
</svg>"""

ICON_CHAT = """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
</svg>"""