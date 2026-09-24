from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN


HTML_AFFILIE = (
    HTML_HEAD.format(title="Mon Réseau — TriBoost")
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
    padding-bottom: calc(40px + var(--safe-bottom));
    padding-top: var(--safe-top);
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
    transition: transform 0.15s;
    text-decoration: none;
  }
  .back-btn:active { transform: scale(0.92); }
  .page-title {
    font-size: 18px; font-weight: 800; color: var(--text-dark);
    flex: 1; text-align: center;
  }
  .spacer { width: 40px; }

  /* ===== BANNIÈRE INACTIF ===== */
  .inactive-banner {
    display: none;
    margin: 12px 16px;
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border: 1.5px solid #ffb74d;
    border-radius: 16px;
    padding: 14px 16px;
    align-items: center;
    gap: 12px;
  }
  .inactive-banner.show { display: flex; }
  .inactive-banner .icon {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: #ffe0b2;
    color: #e65100;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .inactive-banner .text { flex: 1; min-width: 0; }
  .inactive-banner .title {
    font-size: 13px; font-weight: 800; color: #e65100;
    margin-bottom: 2px;
  }
  .inactive-banner .desc {
    font-size: 11px; color: #bf360c;
  }
  .inactive-banner .action {
    background: #e65100; color: #fff;
    border: none; padding: 8px 12px;
    border-radius: 10px; font-size: 11px; font-weight: 700;
    cursor: pointer; flex-shrink: 0;
  }

  /* ===== CARD RÉFÉRENCE ===== */
  .ref-card {
    margin: 0 16px 16px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 20px;
    padding: 20px;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3);
  }
  .ref-card::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .ref-card::after {
    content: ''; position: absolute; bottom: -40px; left: -40px;
    width: 120px; height: 120px;
    background: rgba(251, 192, 45, 0.2); border-radius: 50%;
  }
  .ref-label {
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    opacity: 0.9;
    margin-bottom: 8px;
    position: relative; z-index: 2;
    display: flex; align-items: center; gap: 6px;
  }
  .ref-code {
    font-size: 26px;
    font-weight: 900;
    font-family: 'Courier New', monospace;
    letter-spacing: 2px;
    margin-bottom: 14px;
    position: relative; z-index: 2;
    color: var(--gold);
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
  .ref-link-box {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 4px 4px 4px 14px;
    position: relative; z-index: 2;
    backdrop-filter: blur(4px);
  }
  .ref-link-box input {
    flex: 1;
    background: transparent;
    border: none;
    color: #fff;
    font-size: 12px;
    font-family: inherit;
    outline: none;
    padding: 10px 0;
    min-width: 0;
  }
  .ref-link-box input::placeholder { color: rgba(255,255,255,0.6); }
  .copy-btn {
    background: #fff;
    color: var(--green);
    border: none;
    padding: 10px 14px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 12px;
    cursor: pointer;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: transform 0.15s;
    white-space: nowrap;
  }
  .copy-btn:active { transform: scale(0.95); }
  .copy-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .copy-btn.copied {
    background: var(--gold);
    color: #212121;
  }

  /* Boutons partage */
  .share-row {
    display: flex; gap: 8px;
    margin-top: 12px;
    position: relative; z-index: 2;
  }
  .share-btn {
    flex: 1;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(4px);
    border: none;
    color: #fff;
    padding: 10px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 11px;
    font-family: inherit;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 5px;
    transition: transform 0.15s, background 0.2s;
    text-decoration: none;
  }
  .share-btn:active { transform: scale(0.95); background: rgba(255,255,255,0.25); }

  /* ===== STATS GRID ===== */
  .section-title {
    font-size: 15px; font-weight: 800;
    margin: 20px 16px 12px;
    display: flex; align-items: center; gap: 8px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    padding: 0 16px;
  }
  .stat-card {
    background: #fff;
    border-radius: 16px;
    padding: 14px 10px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
  }
  .stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .stat-card.n1::before { background: var(--green); }
  .stat-card.n2::before { background: var(--gold); }
  .stat-card.n3::before { background: var(--orange); }
  .stat-card .level-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }
  .stat-card.n1 .level-badge { background: var(--green-light); color: var(--green); }
  .stat-card.n2 .level-badge { background: var(--gold-light); color: #f9a825; }
  .stat-card.n3 .level-badge { background: var(--orange-light); color: var(--orange); }

  .stat-count {
    font-size: 22px;
    font-weight: 900;
    color: var(--text-dark);
    line-height: 1;
    margin-bottom: 4px;
  }
  .stat-count-label {
    font-size: 10px;
    color: var(--text-muted);
    margin-bottom: 10px;
  }
  .stat-gain {
    font-size: 12px;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 8px;
    display: inline-block;
  }
  .stat-card.n1 .stat-gain { background: var(--green-light); color: var(--green); }
  .stat-card.n2 .stat-gain { background: var(--gold-light); color: #f9a825; }
  .stat-card.n3 .stat-gain { background: var(--orange-light); color: var(--orange); }

  /* ===== TOTAL CARD ===== */
  .total-card {
    margin: 12px 16px;
    background: linear-gradient(135deg, #1b5e20, var(--green));
    border-radius: 18px;
    padding: 18px 20px;
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 6px 16px rgba(46, 125, 50, 0.25);
    position: relative;
    overflow: hidden;
  }
  .total-card::before {
    content: ''; position: absolute; top: -30px; right: -30px;
    width: 100px; height: 100px;
    background: rgba(255,255,255,0.08); border-radius: 50%;
  }
  .total-card .left {
    position: relative; z-index: 2;
  }
  .total-card .label {
    font-size: 11px; font-weight: 700;
    opacity: 0.85;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  .total-card .value {
    font-size: 24px;
    font-weight: 900;
    line-height: 1;
  }
  .total-card .value span { font-size: 14px; font-weight: 600; }
  .total-card .right {
    position: relative; z-index: 2;
    text-align: right;
  }
  .total-card .count {
    font-size: 22px;
    font-weight: 900;
    line-height: 1;
  }
  .total-card .count-label {
    font-size: 10px;
    opacity: 0.85;
    margin-top: 2px;
  }

  /* ===== TABS ===== */
  .tabs {
    display: flex;
    gap: 6px;
    padding: 0 16px;
    margin-bottom: 12px;
  }
  .tab {
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
    position: relative;
  }
  .tab.active {
    background: var(--green);
    color: #fff;
    border-color: var(--green);
    box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25);
  }
  .tab .tab-count {
    display: block;
    font-size: 16px;
    font-weight: 900;
    margin-top: 2px;
  }

  /* ===== LISTE FILLEULS ===== */
  .members-list {
    padding: 0 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .member-item {
    background: #fff;
    border-radius: 14px;
    padding: 12px 14px;
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
  .member-avatar {
    width: 42px; height: 42px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800;
    font-size: 16px;
    color: #fff;
    flex-shrink: 0;
    position: relative;
  }
  .member-avatar.n1 { background: linear-gradient(135deg, var(--green), var(--green-dark)); }
  .member-avatar.n2 { background: linear-gradient(135deg, #fbc02d, #f9a825); }
  .member-avatar.n3 { background: linear-gradient(135deg, #f57c00, #e65100); }
  .member-avatar .status-dot {
    position: absolute;
    bottom: -2px; right: -2px;
    width: 14px; height: 14px;
    border-radius: 50%;
    border: 2px solid #fff;
  }
  .member-avatar .status-dot.active { background: #4caf50; }
  .member-avatar .status-dot.inactive { background: #bdbdbd; }
  .member-info {
    flex: 1; min-width: 0;
  }
  .member-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .member-meta {
    font-size: 10px;
    color: var(--text-muted);
    display: flex; gap: 8px; flex-wrap: wrap;
  }
  .member-meta .badge {
    padding: 2px 6px;
    border-radius: 5px;
    font-weight: 700;
  }
  .member-meta .badge.active {
    background: var(--green-light);
    color: var(--green);
  }
  .member-meta .badge.inactive {
    background: #f5f5f5;
    color: #9e9e9e;
  }

  /* ===== EMPTY ===== */
  .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-muted);
  }
  .empty-state .icon {
    width: 64px; height: 64px;
    margin: 0 auto 12px;
    border-radius: 50%;
    background: var(--green-light);
    color: var(--green);
    display: flex; align-items: center; justify-content: center;
  }
  .empty-state h3 {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 4px;
  }
  .empty-state p {
    font-size: 12px;
    line-height: 1.5;
  }

  /* ===== INFO BOX ===== */
  .info-box {
    margin: 16px;
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border-radius: 16px;
    padding: 16px;
    border-left: 4px solid var(--green);
  }
  .info-box h4 {
    font-size: 13px;
    font-weight: 800;
    color: var(--green);
    margin-bottom: 10px;
    display: flex; align-items: center; gap: 6px;
  }
  .info-box ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .info-box li {
    font-size: 12px;
    color: #2e7d32;
    padding: 4px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }
  .info-box li span {
    background: rgba(255,255,255,0.7);
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 800;
  }

  /* ===== SKELETON ===== */
  .skel {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.4s infinite;
    border-radius: 8px;
    color: transparent !important;
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
    <div class="page-title">Mon Réseau</div>
    <div class="spacer"></div>
  </header>

  <!-- BANNIÈRE INACTIF -->
  <div class="inactive-banner" id="inactiveBanner">
    <div class="icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
      </svg>
    </div>
    <div class="text">
      <div class="title">Compte non activé</div>
      <div class="desc">Activez pour copier votre lien</div>
    </div>
    <button class="action" onclick="location.href='/activation'">Activer</button>
  </div>

  <!-- CARTE RÉFÉRENCE -->
  <div class="ref-card">
    <div class="ref-label">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
      </svg>
      Votre code d'invitation
    </div>
    <div class="ref-code" id="refCode">TB------</div>

    <div class="ref-link-box">
      <input type="text" id="refLink" readonly value="Chargement...">
      <button class="copy-btn" id="copyBtn" onclick="copyLink()" disabled>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span>Copier</span>
      </button>
    </div>

    <div class="share-row">
      <a class="share-btn" id="shareWa" href="#" target="_blank" rel="noopener">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
        </svg>
        WhatsApp
      </a>
      <button class="share-btn" onclick="shareNative()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="18" cy="5" r="3"></circle>
          <circle cx="6" cy="12" r="3"></circle>
          <circle cx="18" cy="19" r="3"></circle>
          <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
          <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
        </svg>
        Partager
      </button>
    </div>
  </div>

  <!-- SECTION STATS -->
  <div class="section-title">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="18" y1="20" x2="18" y2="10"></line>
      <line x1="12" y1="20" x2="12" y2="4"></line>
      <line x1="6" y1="20" x2="6" y2="14"></line>
    </svg>
    Statistiques du réseau
  </div>

  <div class="stats-grid">
    <div class="stat-card n1">
      <div class="level-badge">NIVEAU 1</div>
      <div class="stat-count" id="n1Count">-</div>
      <div class="stat-count-label">filleuls</div>
      <div class="stat-gain" id="n1Gain">- F</div>
    </div>
    <div class="stat-card n2">
      <div class="level-badge">NIVEAU 2</div>
      <div class="stat-count" id="n2Count">-</div>
      <div class="stat-count-label">filleuls</div>
      <div class="stat-gain" id="n2Gain">- F</div>
    </div>
    <div class="stat-card n3">
      <div class="level-badge">NIVEAU 3</div>
      <div class="stat-count" id="n3Count">-</div>
      <div class="stat-count-label">filleuls</div>
      <div class="stat-gain" id="n3Gain">- F</div>
    </div>
  </div>

  <!-- TOTAL -->
  <div class="total-card">
    <div class="left">
      <div class="label">Gains totaux du réseau</div>
      <div class="value" id="totalGain">0 <span>FCFA</span></div>
    </div>
    <div class="right">
      <div class="count" id="totalCount">0</div>
      <div class="count-label">filleuls total</div>
    </div>
  </div>

  <!-- COMMENT ÇA MARCHE -->
  <div class="info-box">
    <h4>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
      Comment gagner ?
    </h4>
    <ul>
      <li>Filleul direct (N1) <span>1 500 F</span></li>
      <li>Filleul indirect (N2) <span>750 F</span></li>
      <li>Filleul indirect (N3) <span>325 F</span></li>
    </ul>
  </div>

  <!-- TABS FILLEULS -->
  <div class="section-title">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
      <circle cx="9" cy="7" r="4"></circle>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </svg>
    Mes filleuls
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="n1">
      Niveau 1
      <span class="tab-count" id="tabN1">0</span>
    </button>
    <button class="tab" data-tab="n2">
      Niveau 2
      <span class="tab-count" id="tabN2">0</span>
    </button>
    <button class="tab" data-tab="n3">
      Niveau 3
      <span class="tab-count" id="tabN3">0</span>
    </button>
  </div>

  <div class="members-list" id="membersList">
    <div style="height:60px;background:#fff;border-radius:14px;" class="skel"></div>
    <div style="height:60px;background:#fff;border-radius:14px;" class="skel"></div>
    <div style="height:60px;background:#fff;border-radius:14px;" class="skel"></div>
  </div>

  <div style="height: 32px;"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  const referralCode = localStorage.getItem('user_referral_code') || 'TB------';

  if (!token || !userId) {
    window.location.href = '/login';
  }

  let isActivated = false;
  let downline = { n1: [], n2: [], n3: [] };
  let activeTab = 'n1';

  // ===== CHARGER LE PROFIL =====
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
      const p = data.profile;
      isActivated = p.is_activated || false;

      // Code + lien
      const code = p.referral_code || referralCode;
      document.getElementById('refCode').textContent = code;

      const link = window.location.origin + '/register?ref=' + code;
      document.getElementById('refLink').value = link;

      // WhatsApp share
      const waMsg = encodeURIComponent(
        `Rejoins TriBoost avec moi ! Utilise mon code ${code} pour t'inscrire et gagne des commissions.\\n\\n${link}`
      );
      document.getElementById('shareWa').href = 'https://wa.me/?text=' + waMsg;

      // Activer/désactiver le bouton copier
      const copyBtn = document.getElementById('copyBtn');
      if (isActivated) {
        copyBtn.disabled = false;
        copyBtn.style.opacity = '1';
      } else {
        copyBtn.disabled = true;
        copyBtn.style.opacity = '0.5';
        document.getElementById('inactiveBanner').classList.add('show');
      }

    } catch (e) {
      console.error(e);
    }
  }

  // ===== CHARGER LES STATS =====
  async function loadStats() {
    try {
      const res = await fetch('/api/network/stats', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      const s = data.stats;

      document.getElementById('n1Count').textContent = s.n1_count || 0;
      document.getElementById('n2Count').textContent = s.n2_count || 0;
      document.getElementById('n3Count').textContent = s.n3_count || 0;

      document.getElementById('n1Gain').textContent = formatF(s.n1_gain || 0);
      document.getElementById('n2Gain').textContent = formatF(s.n2_gain || 0);
      document.getElementById('n3Gain').textContent = formatF(s.n3_gain || 0);

      document.getElementById('totalGain').innerHTML = Number(s.total_gain || 0).toLocaleString('fr-FR') + ' <span>FCFA</span>';
      document.getElementById('totalCount').textContent = s.total_count || 0;

      document.getElementById('tabN1').textContent = s.n1_count || 0;
      document.getElementById('tabN2').textContent = s.n2_count || 0;
      document.getElementById('tabN3').textContent = s.n3_count || 0;

    } catch (e) {
      console.error(e);
    }
  }

  function formatF(n) {
    return Number(n).toLocaleString('fr-FR') + ' F';
  }

  // ===== CHARGER LES FILLEULS =====
  async function loadDownline() {
    try {
      const res = await fetch('/api/network/downline', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      downline = data.downline || { n1: [], n2: [], n3: [] };
      renderMembers();
    } catch (e) {
      console.error(e);
    }
  }

  function renderMembers() {
    const list = document.getElementById('membersList');
    const items = downline[activeTab] || [];

    if (items.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <h3>Aucun filleul niveau ${activeTab.toUpperCase()}</h3>
          <p>Partagez votre lien pour commencer à gagner des commissions.</p>
        </div>
      `;
      return;
    }

    list.innerHTML = items.map(m => {
      const initial = (m.full_name || 'U').charAt(0).toUpperCase();
      const statusClass = m.is_activated ? 'active' : 'inactive';
      const statusLabel = m.is_activated ? 'Actif' : 'Inactif';
      const date = m.created_at ? new Date(m.created_at).toLocaleDateString('fr-FR') : '';

      return `
        <div class="member-item">
          <div class="member-avatar ${activeTab}">
            ${initial}
            <span class="status-dot ${statusClass}"></span>
          </div>
          <div class="member-info">
            <div class="member-name">${escapeHtml(m.full_name || 'Utilisateur')}</div>
            <div class="member-meta">
              <span class="badge ${statusClass}">${statusLabel}</span>
              ${m.country ? `<span>${escapeHtml(m.country)}</span>` : ''}
              ${date ? `<span>${date}</span>` : ''}
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      activeTab = this.dataset.tab;
      if (navigator.vibrate) navigator.vibrate(5);
      renderMembers();
    });
  });

  // ===== COPIER LE LIEN =====
  function copyLink() {
    if (!isActivated) {
      showInactiveToast();
      return;
    }
    const input = document.getElementById('refLink');
    const btn = document.getElementById('copyBtn');

    navigator.clipboard.writeText(input.value).then(() => {
      if (navigator.vibrate) navigator.vibrate(15);
      btn.classList.add('copied');
      btn.querySelector('span').textContent = 'Copié !';
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.querySelector('span').textContent = 'Copier';
      }, 1800);
    }).catch(() => {
      input.select();
      document.execCommand('copy');
    });
  }

  // ===== PARTAGE NATIF =====
  function shareNative() {
    if (!isActivated) {
      showInactiveToast();
      return;
    }
    const link = document.getElementById('refLink').value;
    const code = document.getElementById('refCode').textContent;
    const text = `Rejoins TriBoost avec mon code ${code} !\\n\\n${link}`;
    if (navigator.share) {
      navigator.share({ title: 'TriBoost', text: text }).catch(() => {});
    } else {
      navigator.clipboard.writeText(text);
      alert('Lien copié !');
    }
  }

  // ===== TOAST INACTIF =====
  function showInactiveToast() {
    if (navigator.vibrate) navigator.vibrate([20, 40, 20]);
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
      <div style="font-size:24px; margin-bottom:6px;">🔒</div>
      <div><strong>Compte non activé</strong></div>
      <div style="font-size:12px; opacity:0.9; margin-top:4px;">
        Activez pour 3 600 FCFA pour partager votre lien
      </div>
      <button onclick="location.href='/activation'" style="
        margin-top:12px; background:#fff; color:#e65100;
        border:none; padding:10px 20px; border-radius:10px;
        font-weight:800; font-size:13px; cursor:pointer;
        font-family:inherit; width:100%;
      ">Activer maintenant</button>
      <button onclick="this.parentElement.remove()" style="
        margin-top:6px; background:transparent; color:#fff;
        border:1px solid rgba(255,255,255,0.4);
        padding:8px 20px; border-radius:10px;
        font-weight:600; font-size:12px; cursor:pointer;
        font-family:inherit; width:100%;
      ">Plus tard</button>
    `;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 6000);
  }

  // ===== INIT =====
  loadProfile();
  loadStats();
  loadDownline();
</script>
</body>
</html>
"""
)