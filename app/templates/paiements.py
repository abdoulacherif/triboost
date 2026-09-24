from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_PAIEMENTS = (
    HTML_HEAD.format(title="Paiements — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: #e8f5e9; color: #2e7d32; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: #212121; flex: 1; text-align: center; }
  .spacer { width: 40px; }
  .balance-card { margin: 16px; background: linear-gradient(135deg, #2e7d32, #1b5e20); border-radius: 20px; padding: 20px; color: #fff; box-shadow: 0 8px 20px rgba(46,125,50,0.3); }
  .balance-label { font-size: 11px; font-weight: 700; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px; }
  .balance-value { font-size: 32px; font-weight: 900; margin: 8px 0 4px; line-height: 1; }
  .balance-value span { font-size: 16px; font-weight: 600; }
  .balance-sub { font-size: 12px; opacity: 0.85; }
  .tabs { display: flex; gap: 8px; padding: 0 16px; margin-bottom: 16px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid #e0e0e0; color: #757575; padding: 12px 8px; border-radius: 14px; font-size: 13px; font-weight: 700; font-family: inherit; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: #2e7d32; color: #fff; border-color: #2e7d32; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
  .form-card { margin: 0 16px 16px; background: #fff; border-radius: 20px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .form-card h3 { font-size: 15px; font-weight: 800; margin-bottom: 16px; color: #212121; }
  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: #212121; }
  .form-group input, .form-group select { width: 100%; padding: 12px 14px; border: 1.5px solid #e0e0e0; border-radius: 12px; font-size: 15px; font-family: inherit; color: #212121; outline: none; background: #fff; -webkit-appearance: none; }
  .form-group select { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23757575' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>"); background-repeat: no-repeat; background-position: right 14px center; padding-right: 38px; }
  .info-min { background: #fff8e1; border-left: 3px solid #fbc02d; border-radius: 10px; padding: 10px 12px; font-size: 11px; color: #6d4c00; margin-bottom: 14px; line-height: 1.5; }
  .btn-primary { width: 100%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; padding: 16px; border-radius: 14px; font-weight: 800; font-size: 15px; font-family: inherit; cursor: pointer; box-shadow: 0 4px 14px rgba(46,125,50,0.3); }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-primary.gold { background: linear-gradient(135deg, #fbc02d, #f57c00); color: #212121; }
  .spinner { width: 18px; height: 18px; border: 2.5px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .history-list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .history-item { background: #fff; border-radius: 14px; padding: 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .hi-icon { width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; background: #e8f5e9; color: #2e7d32; }
  .hi-info { flex: 1; min-width: 0; }
  .hi-title { font-size: 13px; font-weight: 700; color: #212121; }
  .hi-meta { font-size: 11px; color: #757575; display: flex; gap: 8px; margin-top: 2px; }
  .hi-amount { font-size: 15px; font-weight: 900; }
  .hi-amount.negative { color: #f57c00; }
  .hi-amount.positive { color: #2e7d32; }
  .empty-state { text-align: center; padding: 40px 20px; color: #757575; }
  .empty-state h3 { font-size: 14px; font-weight: 700; color: #212121; margin-bottom: 4px; }
</style>
</head>
<body>
<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Paiements</div>
    <div class="spacer"></div>
  </header>

  <div class="balance-card">
    <div class="balance-label">Solde disponible</div>
    <div class="balance-value" id="walletBalance">- <span>FCFA</span></div>
    <div class="balance-sub">Frais 2% · Minimum 2 000 F</div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="withdraw"><span class="icon">💸</span>Retrait</button>
    <button class="tab" data-tab="recharge"><span class="icon">💰</span>Recharge</button>
    <button class="tab" data-tab="history"><span class="icon">📜</span>Historique</button>
  </div>

  <div class="tab-content active" id="tab-withdraw">
    <div class="form-card">
      <h3>💸 Demander un retrait</h3>
      <div class="info-min">⚠️ Minimum 2 000 F · Frais 2% · Traitement 24-72h</div>
      <div id="withdrawError" style="display:none;background:#ffebee;color:#d32f2f;padding:12px;border-radius:10px;font-size:13px;margin-bottom:14px;"></div>
      <form id="withdrawForm" onsubmit="submitWithdraw(event)">
        <div class="form-group">
          <label>Pays *</label>
          <select id="wCountry" required>
            <option value="">-- Choisir un pays --</option>
            <option value="CM">🇨🇲 Cameroun</option>
            <option value="CI">🇨🇮 Côte d'Ivoire</option>
            <option value="SN">🇸🇳 Sénégal</option>
            <option value="BJ">🇧🇯 Bénin</option>
            <option value="TG">🇹🇬 Togo</option>
            <option value="BF">🇧🇫 Burkina Faso</option>
            <option value="ML">🇲🇱 Mali</option>
            <option value="NE">🇳🇪 Niger</option>
            <option value="GN">🇬🇳 Guinée</option>
            <option value="CD">🇨🇩 RD Congo</option>
            <option value="CG">🇨🇬 Congo</option>
            <option value="GA">🇬🇦 Gabon</option>
            <option value="TD">🇹🇩 Tchad</option>
            <option value="CF">🇨🇫 Centrafrique</option>
            <option value="GQ">🇬🇶 Guinée Équatoriale</option>
          </select>
        </div>
        <div class="form-group">
          <label>Opérateur *</label>
          <select id="wOperator" required disabled><option value="">-- Choisir un pays d'abord --</option></select>
        </div>
        <div class="form-group">
          <label>Numéro de téléphone *</label>
          <input type="tel" id="wPhone" required placeholder="+237 6XX XXX XXX" inputmode="tel">
        </div>
        <div class="form-group">
          <label>Nom complet *</label>
          <input type="text" id="wName" required maxlength="80" placeholder="Ex : Abdoula Diallo">
        </div>
        <div class="form-group">
          <label>Montant (FCFA) *</label>
          <input type="number" id="wAmount" required min="2000" step="500" placeholder="Minimum 2 000">
        </div>
        <button type="submit" class="btn-primary" id="withdrawBtn">💸 Demander le retrait</button>
      </form>
    </div>
  </div>

  <div class="tab-content" id="tab-recharge">
    <div class="form-card">
      <h3>💰 Recharger mon wallet</h3>
      <div class="info-min">💡 Minimum 1 000 F · Paiement sécurisé via LeekPay</div>
      <div id="rechargeError" style="display:none;background:#ffebee;color:#d32f2f;padding:12px;border-radius:10px;font-size:13px;margin-bottom:14px;"></div>
      <form id="rechargeForm" onsubmit="submitRecharge(event)">
        <div class="form-group">
          <label>Pays *</label>
          <select id="rCountry" required>
            <option value="">-- Choisir un pays --</option>
            <option value="CM">🇨🇲 Cameroun</option>
            <option value="CI">🇨🇮 Côte d'Ivoire</option>
            <option value="SN">🇸🇳 Sénégal</option>
            <option value="BJ">🇧🇯 Bénin</option>
            <option value="TG">🇹🇬 Togo</option>
            <option value="BF">🇧🇫 Burkina Faso</option>
            <option value="ML">🇲🇱 Mali</option>
            <option value="NE">🇳🇪 Niger</option>
            <option value="GN">🇬🇳 Guinée</option>
            <option value="CD">🇨🇩 RD Congo</option>
            <option value="CG">🇨🇬 Congo</option>
            <option value="GA">🇬🇦 Gabon</option>
            <option value="TD">🇹🇩 Tchad</option>
            <option value="CF">🇨🇫 Centrafrique</option>
            <option value="GQ">🇬🇶 Guinée Équatoriale</option>
          </select>
        </div>
        <div class="form-group">
          <label>Opérateur *</label>
          <select id="rOperator" required disabled><option value="">-- Choisir un pays d'abord --</option></select>
        </div>
        <div class="form-group">
          <label>Numéro *</label>
          <input type="tel" id="rPhone" required placeholder="+237 6XX XXX XXX" inputmode="tel">
        </div>
        <div class="form-group">
          <label>Nom complet *</label>
          <input type="text" id="rName" required maxlength="80" placeholder="Ex : Abdoula Diallo">
        </div>
        <div class="form-group">
          <label>Montant (FCFA) *</label>
          <input type="number" id="rAmount" required min="1000" step="500" placeholder="Minimum 1 000">
        </div>
        <button type="submit" class="btn-primary gold" id="rechargeBtn">💰 Recharger maintenant</button>
      </form>
    </div>
  </div>

  <div class="tab-content" id="tab-history">
    <h3 style="margin: 16px; font-size: 14px; font-weight: 800;">💸 Retraits</h3>
    <div class="history-list" id="withdrawalsList"></div>
    <h3 style="margin: 16px; font-size: 14px; font-weight: 800;">💰 Recharges</h3>
    <div class="history-list" id="rechargesList"></div>
  </div>

  <div style="height: 32px;"></div>
</div>
"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  const OPERATORS = {
    CM: [['mtn','📱 MTN'],['orange','🟠 Orange']],
    CI: [['mtn','📱 MTN'],['orange','🟠 Orange'],['moov','🔵 Moov'],['wave','🌊 Wave']],
    SN: [['orange','🟠 Orange'],['free','🔵 Free'],['wave','🌊 Wave']],
    BJ: [['mtn','📱 MTN'],['moov','🔵 Moov']],
    TG: [['togocom','🔵 Togocom'],['moov','🟣 Moov']],
    BF: [['orange','🟠 Orange'],['moov','🔵 Moov']],
    ML: [['orange','🟠 Orange'],['moov','🔵 Moov']],
    NE: [['airtel','🔴 Airtel'],['orange','🟠 Orange']],
    GN: [['orange','🟠 Orange'],['mtn','📱 MTN']],
    CD: [['vodacom','🔴 Vodacom'],['airtel','🔴 Airtel'],['orange','🟠 Orange']],
    CG: [['mtn','📱 MTN'],['airtel','🔴 Airtel']],
    GA: [['airtel','🔴 Airtel'],['moov','🔵 Moov']],
    TD: [['airtel','🔴 Airtel'],['tigo','🔵 Tigo']],
    CF: [['orange','🟠 Orange'],['telecel','🔵 Telecel']],
    GQ: [['orange','🟠 Orange'],['muni','🔵 Muni']]
  };

  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), { headers: { 'Authorization': 'Bearer ' + token } });
      if (!res.ok) return;
      const data = await res.json();
      const balance = Number(data.profile?.wallet_balance || 0);
      document.getElementById('walletBalance').innerHTML = balance.toLocaleString('fr-FR') + ' <span>FCFA</span>';
    } catch (e) {}
  }

  function setupCountry(countryId, opId) {
    const c = document.getElementById(countryId);
    const o = document.getElementById(opId);
    c.addEventListener('change', function() {
      const code = this.value;
      o.innerHTML = '<option value="">-- Choisir un opérateur --</option>';
      if (OPERATORS[code]) {
        o.disabled = false;
        OPERATORS[code].forEach(([v, l]) => {
          const opt = document.createElement('option');
          opt.value = v;
          opt.textContent = l;
          o.appendChild(opt);
        });
      } else { o.disabled = true; }
    });
  }
  setupCountry('wCountry', 'wOperator');
  setupCountry('rCountry', 'rOperator');

  async function submitWithdraw(e) {
    e.preventDefault();
    const btn = document.getElementById('withdrawBtn');
    const errEl = document.getElementById('withdrawError');
    errEl.style.display = 'none';
    const payload = {
      country: document.getElementById('wCountry').value,
      operator: document.getElementById('wOperator').value,
      phone: document.getElementById('wPhone').value.trim(),
      full_name: document.getElementById('wName').value.trim(),
      amount: parseFloat(document.getElementById('wAmount').value) || 0
    };
    if (!payload.country || !payload.operator || !payload.phone || !payload.full_name) {
      errEl.textContent = '⚠ Tous les champs sont obligatoires'; errEl.style.display = 'block'; return;
    }
    if (payload.amount < 2000) {
      errEl.textContent = '⚠ Minimum 2 000 F'; errEl.style.display = 'block'; return;
    }
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';
    try {
      const res = await fetch('/api/payments/withdraw', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token }, body: JSON.stringify(payload) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (navigator.vibrate) navigator.vibrate(20);
      alert('✅ Demande envoyée ! Traitement 24-72h');
      document.getElementById('withdrawForm').reset();
      document.getElementById('wOperator').disabled = true;
      loadProfile();
    } catch (err) {
      errEl.textContent = '⚠ ' + err.message; errEl.style.display = 'block';
    }
    btn.disabled = false;
    btn.textContent = '💸 Demander le retrait';
  }

  async function submitRecharge(e) {
    e.preventDefault();
    const btn = document.getElementById('rechargeBtn');
    const errEl = document.getElementById('rechargeError');
    errEl.style.display = 'none';
    const payload = {
      country: document.getElementById('rCountry').value,
      operator: document.getElementById('rOperator').value,
      phone: document.getElementById('rPhone').value.trim(),
      full_name: document.getElementById('rName').value.trim(),
      amount: parseFloat(document.getElementById('rAmount').value) || 0
    };
    if (!payload.country || !payload.operator || !payload.phone || !payload.full_name) {
      errEl.textContent = '⚠ Tous les champs sont obligatoires'; errEl.style.display = 'block'; return;
    }
    if (payload.amount < 1000) {
      errEl.textContent = '⚠ Minimum 1 000 F'; errEl.style.display = 'block'; return;
    }
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';
    try {
      const res = await fetch('/api/payments/recharge', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token }, body: JSON.stringify(payload) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (data.payment_url) {
        window.location.href = data.payment_url;
      } else { throw new Error('URL manquante'); }
    } catch (err) {
      errEl.textContent = '⚠ ' + err.message; errEl.style.display = 'block';
      btn.disabled = false;
      btn.textContent = '💰 Recharger maintenant';
    }
  }

  async function loadWithdrawals() {
    const list = document.getElementById('withdrawalsList');
    try {
      const res = await fetch('/api/payments/withdrawals?t=' + Date.now(), { headers: { 'Authorization': 'Bearer ' + token } });
      const data = await res.json();
      const items = data.withdrawals || [];
      if (items.length === 0) { list.innerHTML = '<div class="empty-state"><h3>Aucun retrait</h3></div>'; return; }
      list.innerHTML = items.map(w => '<div class="history-item"><div class="hi-icon">💸</div><div class="hi-info"><div class="hi-title">' + (w.operator || '') + ' · ' + (w.phone || '') + '</div><div class="hi-meta">' + (w.status || '') + '</div></div><div class="hi-amount negative">-' + Number(w.amount).toLocaleString('fr-FR') + ' F</div></div>').join('');
    } catch (e) { list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>'; }
  }

  async function loadRecharges() {
    const list = document.getElementById('rechargesList');
    try {
      const res = await fetch('/api/payments/recharges?t=' + Date.now(), { headers: { 'Authorization': 'Bearer ' + token } });
      const data = await res.json();
      const items = data.recharges || [];
      if (items.length === 0) { list.innerHTML = '<div class="empty-state"><h3>Aucune recharge</h3></div>'; return; }
      list.innerHTML = items.map(r => '<div class="history-item"><div class="hi-icon">💰</div><div class="hi-info"><div class="hi-title">' + (r.operator || '') + ' · ' + (r.phone || '') + '</div><div class="hi-meta">' + (r.status || '') + '</div></div><div class="hi-amount positive">+' + Number(r.amount).toLocaleString('fr-FR') + ' F</div></div>').join('');
    } catch (e) { list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>'; }
  }

  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      if (this.dataset.tab === 'history') { loadWithdrawals(); loadRecharges(); }
    });
  });

  (async () => { await loadProfile(); })();
</script>
</body>
</html>
"""
)