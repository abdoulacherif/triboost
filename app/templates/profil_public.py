from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_PROFIL_PUBLIC = (
    HTML_HEAD.format(title="Profil — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 16px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .profile-hero { background: linear-gradient(135deg, var(--green), var(--green-dark)); padding: 30px 20px; text-align: center; color: #fff; position: relative; overflow: hidden; }
  .profile-hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .profile-avatar { width: 90px; height: 90px; border-radius: 50%; background: rgba(255,255,255,0.2); color: #fff; font-weight: 900; font-size: 36px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; border: 3px solid rgba(255,255,255,0.3); position: relative; z-index: 2; }
  .profile-name { font-size: 22px; font-weight: 900; margin-bottom: 4px; position: relative; z-index: 2; }
  .profile-country { font-size: 13px; opacity: 0.9; position: relative; z-index: 2; }
  .profile-badges { display: flex; gap: 6px; justify-content: center; margin-top: 12px; position: relative; z-index: 2; }
  .profile-badge { background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; }

  .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 16px; }
  .stat-card { background: #fff; border-radius: 16px; padding: 14px 10px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
  .stat-card .val { font-size: 20px; font-weight: 900; color: var(--text-dark); }
  .stat-card .lbl { font-size: 10px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; margin-top: 4px; }

  .action-card { margin: 0 16px 16px; background: #fff; border-radius: 20px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .action-card h3 { font-size: 15px; font-weight: 800; margin-bottom: 14px; display: flex; align-items: center; gap: 6px; color: var(--text-dark); }

  .tip-amounts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; }
  .tip-btn { background: #f5f5f5; border: 1.5px solid transparent; padding: 12px 6px; border-radius: 12px; font-size: 13px; font-weight: 800; font-family: inherit; cursor: pointer; color: var(--text-dark); }
  .tip-btn.active { background: var(--green-light); border-color: var(--green); color: var(--green); }

  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; }
  .form-group input, .form-group textarea { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; background: #fff; }
  .form-group textarea { min-height: 60px; resize: vertical; }

  .btn-tip { width: 100%; background: linear-gradient(135deg, #fbc02d, #f57c00); color: #212121; border: none; padding: 16px; border-radius: 14px; font-weight: 900; font-size: 15px; font-family: inherit; cursor: pointer; box-shadow: 0 4px 14px rgba(245,124,0,0.3); display: flex; align-items: center; justify-content: center; gap: 8px; }
  .btn-tip:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-tip:active { transform: scale(0.98); }

  .info-tip { background: #fff8e1; border-left: 3px solid #fbc02d; border-radius: 10px; padding: 10px 12px; font-size: 11px; color: #6d4c00; line-height: 1.5; margin-bottom: 12px; }

  .spinner { width: 18px; height: 18px; border: 2.5px solid rgba(0,0,0,0.2); border-top-color: #212121; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 60px; margin-bottom: 12px; }
  .empty-state h3 { font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <div class="back-btn" onclick="history.back()">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </div>
    <div class="page-title">Profil</div>
    <div class="spacer"></div>
  </header>

  <div id="loading" style="text-align:center;padding:60px 20px;color:#757575;">Chargement...</div>

  <div id="content" style="display:none;">
    <div class="profile-hero">
      <div class="profile-avatar" id="avatar">U</div>
      <div class="profile-name" id="profileName">-</div>
      <div class="profile-country" id="profileCountry">-</div>
      <div class="profile-badges" id="profileBadges"></div>
    </div>

    <div class="stats-grid">
      <div class="stat-card"><div class="val" id="statProducts">-</div><div class="lbl">Produits</div></div>
      <div class="stat-card"><div class="val" id="statServices">-</div><div class="lbl">Services</div></div>
      <div class="stat-card"><div class="val" id="statTips">-</div><div class="lbl">Tips reçus</div></div>
    </div>

    <div class="action-card">
      <h3>🎁 Offrir un pourboire</h3>
      <div class="info-tip">
        💡 Vous payez le montant, la personne reçoit <strong>90%</strong> (TriBoost prélève 10%).
      </div>

      <div class="tip-amounts">
        <button class="tip-btn" onclick="setTip(100, this)">100</button>
        <button class="tip-btn" onclick="setTip(200, this)">200</button>
        <button class="tip-btn active" onclick="setTip(500, this)">500</button>
        <button class="tip-btn" onclick="setTip(1000, this)">1 000</button>
      </div>

      <div class="form-group">
        <label>Montant (FCFA)</label>
        <input type="number" id="tipAmount" value="500" min="100" step="100">
      </div>

      <div class="form-group">
        <label>Message (optionnel)</label>
        <textarea id="tipMessage" maxlength="200" placeholder="Ex: Merci pour ton aide !"></textarea>
      </div>

      <button class="btn-tip" id="tipBtn" onclick="sendTip()">
        🎁 Envoyer le pourboire
      </button>
    </div>

    <div style="height: 32px;"></div>
  </div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const myId = localStorage.getItem('user_id');
  if (!token || !myId) window.location.href = '/login';

  const pathParts = window.location.pathname.split('/');
  const targetUserId = pathParts[pathParts.length - 1];

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }

  function setTip(amount, btn) {
    document.getElementById('tipAmount').value = amount;
    document.querySelectorAll('.tip-btn').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
  }

  async function loadProfile() {
    try {
      const res = await fetch('/api/ads/profile/' + targetUserId, { headers: headers() });
      if (!res.ok) throw new Error('Profil introuvable');
      const data = await res.json();

      const p = data.profile;
      const s = data.stats;

      document.getElementById('loading').style.display = 'none';
      document.getElementById('content').style.display = 'block';

      const initial = (p.full_name || 'U').charAt(0).toUpperCase();
      document.getElementById('avatar').textContent = initial;
      document.getElementById('profileName').textContent = p.full_name || 'Utilisateur';
      document.getElementById('profileCountry').textContent = '📍 ' + (p.country || 'Inconnu');

      let badges = '';
      if (p.is_activated) badges += '<div class="profile-badge">✓ Vérifié</div>';
      if (myId === targetUserId) badges += '<div class="profile-badge">👤 Vous</div>';
      document.getElementById('profileBadges').innerHTML = badges;

      document.getElementById('statProducts').textContent = s.products || 0;
      document.getElementById('statServices').textContent = s.services || 0;
      document.getElementById('statTips').textContent = fmt(s.tips_total) + ' F';

      // Bloquer si c'est moi-même
      if (myId === targetUserId) {
        document.getElementById('tipBtn').disabled = true;
        document.getElementById('tipBtn').innerHTML = '👤 C\\'est votre profil';
      }

    } catch (e) {
      document.getElementById('loading').innerHTML = '<div class="empty-state"><div class="icon">❌</div><h3>Profil introuvable</h3></div>';
    }
  }

  async function sendTip() {
    const amount = parseFloat(document.getElementById('tipAmount').value) || 0;
    const message = document.getElementById('tipMessage').value.trim();

    if (amount < 100) {
      alert('⚠ Minimum 100 F');
      return;
    }

    if (!confirm('Envoyer ' + fmt(amount) + ' F de pourboire ?')) return;

    const btn = document.getElementById('tipBtn');
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/ads/tip', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({
          receiver_id: targetUserId,
          amount: amount,
          message: message,
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      if (navigator.vibrate) navigator.vibrate([30, 50, 30]);
      alert('🎁 Pourboire envoyé ! La personne reçoit ' + fmt(data.result.receiver_gets) + ' F');
      document.getElementById('tipMessage').value = '';
      loadProfile();
    } catch (e) {
      alert('⚠ ' + e.message);
    }
    btn.disabled = false;
    btn.innerHTML = '🎁 Envoyer le pourboire';
  }

  loadProfile();
</script>
</body>
</html>
"""
)