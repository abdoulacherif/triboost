from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ACTIVATION_SUCCESS = (
    HTML_HEAD.format(title="Activation réussie — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app {
    width: 100%; max-width: 480px;
    background: #fff; min-height: 100vh;
    padding: 40px 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding-top: var(--safe-top);
    padding-bottom: var(--safe-bottom);
  }
  .success-icon {
    width: 100px; height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    color: #fff;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(46, 125, 50, 0.4);
    animation: popIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes popIn {
    from { transform: scale(0); }
    to { transform: scale(1); }
  }
  h1 {
    font-size: 24px; font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 12px;
  }
  p {
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 32px;
    max-width: 300px;
  }
  .btn-primary {
    background: var(--green);
    color: #fff;
    border: none;
    padding: 16px 32px;
    border-radius: 14px;
    font-weight: 700;
    font-size: 15px;
    font-family: inherit;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: transform 0.15s;
  }
  .btn-primary:active { transform: scale(0.96); }
</style>
</head>
<body>
<div class="app">
  <div class="success-icon">
    <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
  </div>

  <h1>Activation réussie !</h1>
  <p>Votre compte est maintenant actif. Vous pouvez profiter de toutes les fonctionnalités TriBoost.</p>

  <a href="/dashboard" class="btn-primary">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
      <polyline points="9 22 9 12 15 12 15 22"></polyline>
    </svg>
    Aller au tableau de bord
  </a>
</div>

"""
    + JS_COMMUN
    + """
<script>
  if (navigator.vibrate) navigator.vibrate([30, 50, 30]);
</script>
</body>
</html>
"""
)