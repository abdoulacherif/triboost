from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_TOURNER = (
    HTML_HEAD.format(title="Tourner — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .hero { margin: 16px; background: linear-gradient(135deg, #fbc02d, #f57c00); border-radius: 20px; padding: 20px; color: #212121; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(245, 124, 0, 0.3); text-align: center; }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 4px; }
  .hero-sub { font-size: 13px; font-weight: 600; }

  /* Roue */
  .wheel-container { position: relative; width: 320px; height: 320px; margin: 24px auto; }
  .wheel-pointer { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 16px solid transparent; border-right: 16px solid transparent; border-top: 28px solid #d32f2f; z-index: 10; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); }
  .wheel { width: 100%; height: 100%; border-radius: 50%; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.2), inset 0 0 0 8px #fff, inset 0 0 0 12px #fbc02d; transition: transform 4.5s cubic-bezier(0.16, 1, 0.3, 1); }
  .wheel-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 900; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 5; }
  .wheel-segment { position: absolute; width: 50%; height: 50%; top: 0; left: 50%; transform-origin: 0 100%; display: flex; align-items: center; justify-content: center; padding-left: 40%; color: #fff; font-weight: 900; font-size: 12px; text-shadow: 0 1px 2px rgba(0,0,0,0.4); }

  /* Boutons */
  .action-card { margin: 16px; background: #fff; border-radius: 20px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); text-align: center; }
  .status-info { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
  .status-badge { display: inline-block; background: var(--green-light); color: var(--green); padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 12px; margin-bottom: 16px; }
  .status-badge.wait { background: #fff3e0; color: #e65100; }
  .btn-spin { width: 100%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; padding: 18px; border-radius: 16px; font-weight: 900; font-size: 16px; font-family: inherit; cursor: pointer; box-shadow: 0 6px 20px rgba(46,125,50,0.3); transition: transform 0.15s; margin-bottom: 10px; }
  .btn-spin:active { transform: scale(0.98); }
  .btn-spin:disabled { opacity: 0.5; cursor: not-allowed; box-shadow: none; }
  .btn-spin.gold { background: linear-gradient(135deg, #fbc02d, #f57c00); color: #212121; }
  .btn-spin.gold:disabled { opacity: 0.5; }
  .spinner { width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Historique */
  .section-title { font-size: 15px; font-weight: 800; margin: 24px 16px 12px; color: var(--text-dark); }
  .history-list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .history-item { background: #fff; border-radius: 14px; padding: 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .hi-icon { width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
  .hi-icon.win { background: #fff8e1; color: #f57c00; }
  .hi-icon.lose { background: #f5f5f5; color: #9e9e9e; }
  .hi-info { flex: 1; min-width: 0; }
  .hi-title { font-size: 13px; font-weight: 700; color: var(--text-dark); }
  .hi-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
  .hi-amount { font-size: 15px; font-weight: 900; color: var(--green); }
  .hi-amount.lose { color: #9e9e9e; }
  .empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }

  /* Modal */
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); z-index: 999; display: none; align-items: center; justify-content: center; padding: 20px; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 24px; padding: 30px 24px; max-width: 340px; width: 100%; text-align: center; animation: scaleIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
  @keyframes scaleIn { from { transform: scale(0.7); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  .modal-icon { font-size: 80px; margin-bottom: 12px; animation: bounce 0.6s ease; }
  @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
  .modal-title { font-size: 22px; font-weight: 900; color: #f57c00; margin-bottom: 8px; }
  .modal-text { font-size: 15px; color: var(--text-dark); font-weight: 700; margin-bottom: 20px; }
  .modal-prize { font-size: 32px; font-weight: 900; color: var(--green); margin: 16px 0; }
  .modal-btn { background: var(--green); color: #fff; border: none; padding: 14px; border-radius: 12px; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; width: 100%; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Tourner</div>
    <div class="spacer"></div>
  </header>

  <div class="hero">
    <div class="hero-title">🎡 Roue de la chance</div>
    <div class="hero-sub">Un tour gratuit toutes les semaines !</div>
  </div>

  <div class="wheel-container">
    <div class="wheel-pointer"></div>
    <div class="wheel" id="wheel">
      <div class="wheel-center">🎁</div>
    </div>
  </div>

  <div class="action-card">
    <div id="statusBadge" class="status-badge">Chargement...</div>
    <div id="statusInfo" class="status-info"></div>
    <button class="btn-spin" id="spinFreeBtn" onclick="spinWheel('free')" disabled>
      🎁 Tour gratuit
    </button>
    <button class="btn-spin gold" id="spinPaidBtn" onclick="spinWheel('paid')" disabled>
      💰 Tour payant · 200 F
    </button>
  </div>

  <div class="section-title">📜 Mes derniers tours</div>
  <div class="history-list" id="historyList">
    <div class="empty-state">Chargement...</div>
  </div>

  <div style="height: 32px;"></div>
</div>

<div class="modal-overlay" id="resultModal">
  <div class="modal-content">
    <div class="modal-icon" id="modalIcon">🎉</div>
    <div class="modal-title" id="modalTitle">Félicitations !</div>
    <div class="modal-text" id="modalText"></div>
    <div class="modal-prize" id="modalPrize"></div>
    <button class="modal-btn" onclick="closeModal()">Super !</button>
  </div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  let wheelConfig = [];
  let currentRotation = 0;
  let canSpinFree = false;

  // ===== CHARGER LA CONFIG DE LA ROUE =====
  async function loadConfig() {
    try {
      const res = await fetch('/api/wheel/config');
      const data = await res.json();
      wheelConfig = data.config || [];
      buildWheel();
    } catch (e) { console.error(e); }
  }

  function buildWheel() {
    const wheel = document.getElementById('wheel');
    const total = wheelConfig.length;
    if (total === 0) return;

    // Nettoyer sauf le centre
    wheel.querySelectorAll('.wheel-segment').forEach(function(s) { s.remove(); });

    const anglePerSegment = 360 / total;

    wheelConfig.forEach(function(seg, i) {
      const segDiv = document.createElement('div');
      segDiv.className = 'wheel-segment';
      segDiv.style.background = seg.color;
      segDiv.style.transform = 'rotate(' + (i * anglePerSegment) + 'deg) skewY(-' + (90 - anglePerSegment) + 'deg)';
      segDiv.style.transformOrigin = '0 100%';
      segDiv.textContent = seg.label;
      wheel.insertBefore(segDiv, wheel.querySelector('.wheel-center'));
    });
  }

  // ===== CHARGER LE STATUT =====
  async function loadStatus() {
    try {
      const res = await fetch('/api/wheel/status?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      canSpinFree = data.can_spin_free;

      const badge = document.getElementById('statusBadge');
      const info = document.getElementById('statusInfo');
      const freeBtn = document.getElementById('spinFreeBtn');
      const paidBtn = document.getElementById('spinPaidBtn');

      if (canSpinFree) {
        badge.textContent = '🎁 Tour gratuit disponible !';
        badge.className = 'status-badge';
        info.textContent = 'Vous pouvez tourner gratuitement maintenant.';
        freeBtn.disabled = false;
      } else {
        const nextDate = data.next_free_at ? new Date(data.next_free_at).toLocaleDateString('fr-FR') : '';
        badge.textContent = '⏳ Prochain tour dans 7 jours';
        badge.className = 'status-badge wait';
        info.textContent = nextDate ? 'Disponible le ' + nextDate : '';
        freeBtn.disabled = true;
      }

      paidBtn.disabled = false;
      renderHistory(data.history || []);
    } catch (e) { console.error(e); }
  }

  function renderHistory(items) {
    const list = document.getElementById('historyList');
    if (items.length === 0) {
      list.innerHTML = '<div class="empty-state"><h3>Aucun tour</h3><p>Tournez la roue pour commencer !</p></div>';
      return;
    }
    list.innerHTML = items.map(function(s) {
      const win = Number(s.prize_amount) > 0;
      const icon = win ? '🎉' : '😢';
      const iconClass = win ? 'win' : 'lose';
      const date = new Date(s.created_at).toLocaleDateString('fr-FR');
      return '<div class="history-item">' +
        '<div class="hi-icon ' + iconClass + '">' + icon + '</div>' +
        '<div class="hi-info">' +
        '<div class="hi-title">' + s.prize_label + '</div>' +
        '<div class="hi-meta">' + (s.spin_type === 'paid' ? 'Payant' : 'Gratuit') + ' · ' + date + '</div>' +
        '</div>' +
        '<div class="hi-amount ' + (win ? '' : 'lose') + '">' + (win ? '+' + Number(s.prize_amount).toLocaleString('fr-FR') + ' F' : 'Perdu') + '</div>' +
        '</div>';
    }).join('');
  }

  // ===== TOURNER =====
  async function spinWheel(type) {
    if (navigator.vibrate) navigator.vibrate(15);

    if (type === 'paid' && !confirm('Tour payant : 200 F seront débités de votre wallet. Continuer ?')) return;
    if (type === 'free' && !canSpinFree) return;

    const freeBtn = document.getElementById('spinFreeBtn');
    const paidBtn = document.getElementById('spinPaidBtn');
    freeBtn.disabled = true;
    paidBtn.disabled = true;

    if (type === 'free') freeBtn.innerHTML = '<div class="spinner"></div>';
    else paidBtn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/wheel/spin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ spin_type: type })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result || !data.result.success) throw new Error(data.result?.message || 'Erreur');

      // Animer la roue pour tomber sur le bon segment
      const prizeIndex = wheelConfig.findIndex(function(c) { return c.label === data.result.prize_label; });
      const total = wheelConfig.length;
      const anglePerSegment = 360 / total;
      const targetAngle = 360 - (prizeIndex * anglePerSegment) - (anglePerSegment / 2);
      const fullRotations = 360 * 5;
      currentRotation += fullRotations + targetAngle;

      const wheel = document.getElementById('wheel');
      wheel.style.transform = 'rotate(' + currentRotation + 'deg)';

      setTimeout(function() {
        showResult(data.result);
        loadStatus();
        if (navigator.vibrate) navigator.vibrate([30, 50, 30]);
      }, 4600);

    } catch (err) {
      alert('⚠ ' + err.message);
      freeBtn.disabled = false;
      paidBtn.disabled = false;
      freeBtn.innerHTML = '🎁 Tour gratuit';
      paidBtn.innerHTML = '💰 Tour payant · 200 F';
    }
  }

  function showResult(result) {
    const modal = document.getElementById('resultModal');
    const icon = document.getElementById('modalIcon');
    const title = document.getElementById('modalTitle');
    const text = document.getElementById('modalText');
    const prize = document.getElementById('modalPrize');

    if (result.prize_amount > 0) {
      icon.textContent = result.prize_amount >= 500 ? '🏆' : '🎉';
      title.textContent = 'Félicitations !';
      text.textContent = 'Vous avez gagné :';
      prize.textContent = '+' + Number(result.prize_amount).toLocaleString('fr-FR') + ' FCFA';
    } else {
      icon.textContent = '😢';
      title.textContent = 'Dommage...';
      text.textContent = 'Vous n\\'avez rien gagné cette fois.';
      prize.textContent = '';
    }

    modal.classList.add('open');

    // Reset boutons
    setTimeout(function() {
      document.getElementById('spinFreeBtn').innerHTML = '🎁 Tour gratuit';
      document.getElementById('spinPaidBtn').innerHTML = '💰 Tour payant · 200 F';
    }, 500);
  }

  function closeModal() {
    document.getElementById('resultModal').classList.remove('open');
  }

  (async function() {
    await loadConfig();
    await loadStatus();
  })();
</script>
</body>
</html>
"""
)