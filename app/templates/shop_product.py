from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_SHOP_PRODUCT = (
    HTML_HEAD.format(title="Produit — TriBoost")
    + CSS_COMMUN
    + """
<style>
  /* FIX : force le body en block pour éviter le conflit avec shared.py */
  body { display: block !important; background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #fff; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 16px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .product-img { width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); display: flex; align-items: center; justify-content: center; color: #2e7d32; font-size: 80px; overflow: hidden; }
  .product-img img { width: 100%; height: 100%; object-fit: cover; }

  .product-body { padding: 20px; }
  .product-title { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 8px; line-height: 1.2; }
  .product-price { font-size: 28px; font-weight: 900; color: var(--green); margin: 12px 0; }
  .product-desc { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px; }
  .seller-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--green-light); color: var(--green); padding: 6px 12px; border-radius: 10px; font-size: 12px; font-weight: 700; margin-bottom: 16px; }

  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 13px; font-weight: 700; margin-bottom: 6px; color: var(--text-dark); }
  .form-group input { width: 100%; padding: 14px; border: 1.5px solid #e0e0e0; border-radius: 12px; font-size: 15px; font-family: inherit; outline: none; background: #fff; box-sizing: border-box; }
  .form-group input:focus { border-color: var(--green); }

  .qty-row { display: flex; align-items: center; gap: 10px; }
  .qty-btn { width: 40px; height: 40px; border-radius: 10px; background: var(--green-light); color: var(--green); border: none; font-size: 20px; font-weight: 900; cursor: pointer; font-family: inherit; }
  .qty-input { flex: 1; text-align: center; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 10px; font-size: 16px; font-weight: 700; outline: none; min-width: 0; }

  .btn-order { width: 100%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; padding: 18px; border-radius: 14px; font-weight: 900; font-size: 16px; font-family: inherit; cursor: pointer; box-shadow: 0 6px 20px rgba(46,125,50,0.3); margin-top: 10px; display: flex; align-items: center; justify-content: center; gap: 8px; }
  .btn-order:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-order.gold { background: linear-gradient(135deg, #fbc02d, #f57c00); color: #212121; }

  .total-line { display: flex; justify-content: space-between; padding: 10px 0; font-size: 14px; border-bottom: 1px solid #f5f5f5; }
  .total-line.final { border-bottom: none; font-size: 18px; font-weight: 900; color: var(--green); margin-top: 6px; }

  .lk-spinner { width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: lkspin 0.8s linear infinite; display: inline-block; }
  @keyframes lkspin { to { transform: rotate(360deg); } }

  .empty-state { text-align: center; padding: 80px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 60px; margin-bottom: 16px; }
  .empty-state h3 { font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 8px; }

  .success-screen { display: none; padding: 30px 20px; text-align: center; }
  .success-screen.show { display: block; }
  .success-icon { width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 50px; margin: 0 auto 20px; animation: lkpop 0.5s ease; }
  @keyframes lkpop { from { transform: scale(0); } to { transform: scale(1); } }
  .success-screen h2 { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 12px; }
  .success-screen p { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px; }

  .delivery-box { background: linear-gradient(135deg, #e8f5e9, #f1f8e9); border: 2px solid var(--green); border-radius: 16px; padding: 20px; margin: 20px 0; text-align: left; }
  .delivery-box h3 { font-size: 15px; font-weight: 800; color: var(--green); margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }
  .delivery-link { display: flex; align-items: center; gap: 8px; background: #fff; padding: 14px; border-radius: 12px; text-decoration: none; color: var(--text-dark); font-weight: 700; font-size: 13px; margin-bottom: 10px; }
  .delivery-link:active { transform: scale(0.98); }
  .delivery-link .icon { width: 40px; height: 40px; border-radius: 10px; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
  .delivery-text { background: #fff; padding: 14px; border-radius: 12px; font-size: 13px; line-height: 1.6; font-family: monospace; white-space: pre-wrap; word-break: break-word; }
</style>
</head>
<body>

<div class="app" id="app">
  <header class="topbar">
    <div class="back-btn" onclick="history.back()">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </div>
    <div class="page-title">Produit</div>
    <div class="spacer"></div>
  </header>

  <div id="loading" style="text-align:center;padding:60px 20px;color:#757575;">Chargement...</div>

  <div id="productContent" style="display:none;">
    <div class="product-img" id="productImg"></div>
    <div class="product-body">
      <div class="seller-badge">👤 Vendu par <span id="sellerName"></span></div>
      <div class="product-title" id="productTitle"></div>
      <div class="product-price" id="productPrice"></div>
      <div class="product-desc" id="productDesc"></div>

      <div style="background: #f9f9f9; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
        <div style="font-size: 13px; font-weight: 800; margin-bottom: 10px;">🛒 Quantité</div>
        <div class="qty-row">
          <button class="qty-btn" onclick="changeQty(-1)">−</button>
          <input type="number" class="qty-input" id="qty" value="1" min="1" onchange="updateTotal()">
          <button class="qty-btn" onclick="changeQty(1)">+</button>
        </div>
      </div>

      <div style="background: #f9f9f9; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
        <div class="total-line"><span>Prix unitaire</span><span id="unitPrice">-</span></div>
        <div class="total-line"><span>Quantité</span><span id="qtyDisplay">1</span></div>
        <div class="total-line final"><span>Total</span><span id="totalPrice">-</span></div>
      </div>

      <button class="btn-order" id="payWalletBtn" onclick="payWithWallet()">
        💰 Payer avec mon solde
      </button>

      <button class="btn-order gold" onclick="openLeekpayModal()" style="margin-top: 10px;">
        📱 Payer par Mobile Money
      </button>

      <p style="text-align: center; font-size: 11px; color: #9e9e9e; margin-top: 16px;">
        Livraison instantanée après paiement
      </p>
    </div>
  </div>

  <div class="success-screen" id="successScreen">
    <div class="success-icon">✓</div>
    <h2>Paiement réussi !</h2>
    <p>Voici votre produit :</p>
    <div class="delivery-box" id="deliveryBox"></div>
    <button class="btn-order" onclick="location.href='/shop'">Retour au shop</button>
  </div>
</div>

<!-- MODAL LEEKPAY - TOUT EN INLINE POUR ÉVITER LES CONFLITS -->
<div id="lkModalOverlay" onclick="if(event.target===this) closeLeekpayModal()" style="display:none; position:fixed !important; inset:0 !important; width:100vw !important; height:100vh !important; background:rgba(0,0,0,0.6); z-index:2147483647 !important; align-items:flex-end; justify-content:center; box-sizing:border-box; margin:0 !important; padding:0 !important;">
  <div style="background:#fff; border-radius:24px 24px 0 0; width:100%; max-width:480px; max-height:92vh; overflow-y:auto; padding:20px 20px 40px; box-sizing:border-box; position:relative;">
    <div style="width:40px; height:4px; background:#e0e0e0; border-radius:2px; margin:0 auto 16px;"></div>

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <span style="font-size:18px; font-weight:800; color:#212121;">📱 Payer par Mobile Money</span>
      <button onclick="closeLeekpayModal()" style="width:32px; height:32px; border-radius:50%; background:#f5f5f5; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; color:#757575; font-size:18px; font-family:inherit;">✕</button>
    </div>

    <div style="background:#fff8e1; border-left:3px solid #fbc02d; border-radius:10px; padding:10px 12px; font-size:11px; color:#6d4c00; margin-bottom:14px; line-height:1.5;">
      💡 Vous serez redirigé vers LeekPay pour finaliser le paiement.
    </div>

    <div class="form-group">
      <label>Numéro Mobile Money *</label>
      <input type="tel" id="payPhone" placeholder="+237 6XX XXX XXX" inputmode="tel">
    </div>

    <div style="display:flex; gap:10px; margin-top:20px;">
      <button type="button" onclick="closeLeekpayModal()" style="flex:1; background:#f5f5f5; color:#212121; border:none; padding:14px; border-radius:12px; font-weight:700; font-size:14px; font-family:inherit; cursor:pointer;">Annuler</button>
      <button type="button" id="leekpayBtn" onclick="payWithLeekpay()" style="flex:2; background:var(--green); color:#fff; border:none; padding:14px; border-radius:12px; font-weight:700; font-size:14px; font-family:inherit; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;">
        <span>Payer <span id="modalTotal">-</span></span>
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

  const pathParts = window.location.pathname.split('/');
  const affiliateCode = pathParts[pathParts.length - 1];

  let product = null;
  let affiliate = null;

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }

  function closeLeekpayModal() {
    document.getElementById('lkModalOverlay').style.display = 'none';
    document.body.style.overflow = '';
  }

  async function loadProduct() {
    try {
      const res = await fetch('/api/shop/p/' + affiliateCode);
      if (!res.ok) throw new Error('Lien introuvable');
      const data = await res.json();

      product = data.product;
      affiliate = data.affiliate;

      document.getElementById('loading').style.display = 'none';
      document.getElementById('productContent').style.display = 'block';

      const img = product.image_url ? '<img src="' + product.image_url + '" alt="">' : '📦';
      document.getElementById('productImg').innerHTML = img;
      document.getElementById('productTitle').textContent = product.title;
      document.getElementById('productDesc').textContent = product.description || 'Aucune description.';
      document.getElementById('productPrice').textContent = fmt(affiliate.custom_price) + ' F';
      document.getElementById('sellerName').textContent = data.seller.full_name || 'Vendeur';

      updateTotal();
    } catch (e) {
      document.getElementById('loading').innerHTML = '<div class="empty-state"><div class="icon">❌</div><h3>Lien invalide</h3><p>Ce produit n\\'est plus disponible.</p></div>';
    }
  }

  function changeQty(delta) {
    const input = document.getElementById('qty');
    const v = Math.max(1, (parseInt(input.value) || 1) + delta);
    input.value = v;
    updateTotal();
  }

  function updateTotal() {
    if (!affiliate) return;
    const qty = parseInt(document.getElementById('qty').value) || 1;
    const unit = parseFloat(affiliate.custom_price);
    const total = unit * qty;
    document.getElementById('unitPrice').textContent = fmt(unit) + ' F';
    document.getElementById('qtyDisplay').textContent = qty;
    document.getElementById('totalPrice').textContent = fmt(total) + ' F';
    document.getElementById('modalTotal').textContent = fmt(total) + ' F';
  }

  // ===== PAIEMENT VIA WALLET =====
  async function payWithWallet() {
    const qty = parseInt(document.getElementById('qty').value) || 1;
    if (!confirm('Payer ' + fmt(affiliate.custom_price * qty) + ' F avec votre solde ?')) return;

    const btn = document.getElementById('payWalletBtn');
    btn.disabled = true;
    btn.innerHTML = '<div class="lk-spinner"></div>';

    try {
      const res = await fetch('/api/shop/order-with-wallet', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ affiliate_code: affiliateCode, quantity: qty })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      showDelivery(data.result.content_url, data.result.content_text, data.result.delivery_type);
    } catch (e) {
      alert('⚠ ' + e.message);
      btn.disabled = false;
      btn.innerHTML = '💰 Payer avec mon solde';
    }
  }

  // ===== PAIEMENT VIA LEEKPAY =====
  function openLeekpayModal() {
    document.getElementById('payPhone').value = '';
    updateTotal();
    document.getElementById('lkModalOverlay').style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  async function payWithLeekpay() {
    const qty = parseInt(document.getElementById('qty').value) || 1;
    const phone = document.getElementById('payPhone').value.trim();

    if (!phone) { alert('⚠ Numéro obligatoire'); return; }

    const btn = document.getElementById('leekpayBtn');
    btn.disabled = true;
    btn.innerHTML = '<div class="lk-spinner"></div>';

    try {
      const res = await fetch('/api/shop/order-with-leekpay', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ affiliate_code: affiliateCode, quantity: qty, phone: phone })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');

      if (data.payment_url) {
        localStorage.setItem('pending_shop_order', data.order_id);
        window.location.href = data.payment_url;
      } else {
        throw new Error('URL de paiement manquante');
      }
    } catch (e) {
      alert('⚠ ' + e.message);
      btn.disabled = false;
      btn.innerHTML = '<span>Payer</span>';
    }
  }

  // ===== AFFICHER LE PRODUIT APRÈS PAIEMENT =====
  function showDelivery(contentUrl, contentText, deliveryType) {
    document.getElementById('productContent').style.display = 'none';
    const box = document.getElementById('deliveryBox');
    let html = '';

    if (contentUrl) {
      html += '<a href="' + contentUrl + '" target="_blank" class="delivery-link">' +
        '<div class="icon">📥</div>' +
        '<div>Télécharger / Accéder au produit</div>' +
        '</a>';
    }
    if (contentText) {
      html += '<div style="font-size: 12px; font-weight: 700; margin-bottom: 6px; color: var(--green);">📋 Contenu / Instructions :</div>';
      html += '<div class="delivery-text">' + escapeHtml(contentText) + '</div>';
    }
    if (!html) {
      html = '<p style="text-align:center; font-size: 13px; color: #757575;">Le vendeur va vous contacter bientôt.</p>';
    }
    box.innerHTML = html;

    document.getElementById('successScreen').classList.add('show');
    if (navigator.vibrate) navigator.vibrate([30, 50, 30]);
  }

  // ===== AU CHARGEMENT =====
  loadProduct();
</script>
</body>
</html>
"""
)