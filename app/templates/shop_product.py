from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_SHOP_PRODUCT = (
    HTML_HEAD.format(title="Produit — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
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
  .form-group input, .form-group textarea { width: 100%; padding: 14px; border: 1.5px solid var(--border); border-radius: 12px; font-size: 15px; font-family: inherit; outline: none; background: #fff; }
  .form-group input:focus, .form-group textarea:focus { border-color: var(--green); }
  .form-group textarea { min-height: 70px; resize: vertical; }

  .qty-row { display: flex; align-items: center; gap: 10px; }
  .qty-btn { width: 40px; height: 40px; border-radius: 10px; background: var(--green-light); color: var(--green); border: none; font-size: 20px; font-weight: 900; cursor: pointer; font-family: inherit; }
  .qty-input { flex: 1; text-align: center; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 16px; font-weight: 700; outline: none; }

  .btn-order { width: 100%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; padding: 18px; border-radius: 14px; font-weight: 900; font-size: 16px; font-family: inherit; cursor: pointer; box-shadow: 0 6px 20px rgba(46,125,50,0.3); margin-top: 10px; }
  .btn-order:disabled { opacity: 0.6; cursor: not-allowed; }

  .total-line { display: flex; justify-content: space-between; padding: 10px 0; font-size: 14px; border-bottom: 1px solid #f5f5f5; }
  .total-line.final { border-bottom: none; font-size: 18px; font-weight: 900; color: var(--green); margin-top: 6px; }

  .spinner { width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .empty-state { text-align: center; padding: 80px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 60px; margin-bottom: 16px; }
  .empty-state h3 { font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 8px; }

  .success-screen { display: none; padding: 40px 20px; text-align: center; }
  .success-screen.show { display: block; }
  .success-icon { width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 50px; margin: 0 auto 20px; animation: pop 0.5s ease; }
  @keyframes pop { from { transform: scale(0); } to { transform: scale(1); } }
  .success-screen h2 { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 12px; }
  .success-screen p { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px; }
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
        <div style="font-size: 13px; font-weight: 800; margin-bottom: 10px;">📋 Vos informations</div>
        <div class="form-group">
          <label>Nom complet *</label>
          <input type="text" id="buyerName" placeholder="Ex : Jean Dupont" required>
        </div>
        <div class="form-group">
          <label>Téléphone *</label>
          <input type="tel" id="buyerPhone" placeholder="+237 6XX XXX XXX" inputmode="tel" required>
        </div>
        <div class="form-group">
          <label>Adresse de livraison</label>
          <textarea id="buyerAddress" placeholder="Quartier, ville..."></textarea>
        </div>
        <div class="form-group">
          <label>Quantité</label>
          <div class="qty-row">
            <button class="qty-btn" onclick="changeQty(-1)">−</button>
            <input type="number" class="qty-input" id="qty" value="1" min="1" onchange="updateTotal()">
            <button class="qty-btn" onclick="changeQty(1)">+</button>
          </div>
        </div>
      </div>

      <div style="background: #f9f9f9; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
        <div class="total-line"><span>Prix unitaire</span><span id="unitPrice">-</span></div>
        <div class="total-line"><span>Quantité</span><span id="qtyDisplay">1</span></div>
        <div class="total-line final"><span>Total</span><span id="totalPrice">-</span></div>
      </div>

      <button class="btn-order" id="orderBtn" onclick="submitOrder()">🛒 Commander</button>

      <p style="text-align: center; font-size: 11px; color: #9e9e9e; margin-top: 16px;">
        Le vendeur vous contactera pour finaliser la transaction.
      </p>
    </div>
  </div>

  <div class="success-screen" id="successScreen">
    <div class="success-icon">✓</div>
    <h2>Commande envoyée !</h2>
    <p>Le vendeur vous contactera bientôt pour finaliser la transaction.</p>
    <button class="btn-order" onclick="location.href='/'">Fermer</button>
  </div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const pathParts = window.location.pathname.split('/');
  const affiliateCode = pathParts[pathParts.length - 1];

  let product = null;
  let affiliate = null;

  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }

  async function loadProduct() {
    try {
      const res = await fetch('/api/shop/p/' + affiliateCode);
      if (!res.ok) throw new Error('Lien introuvable');
      const data = await res.json();

      product = data.product;
      affiliate = data.affiliate;

      document.getElementById('loading').style.display = 'none';
      document.getElementById('productContent').style.display = 'block';

      const img = product.image_url
        ? '<img src="' + product.image_url + '" alt="">'
        : '📦';

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
    const newVal = Math.max(1, (parseInt(input.value) || 1) + delta);
    input.value = newVal;
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
  }

  async function submitOrder() {
    const name = document.getElementById('buyerName').value.trim();
    const phone = document.getElementById('buyerPhone').value.trim();
    const address = document.getElementById('buyerAddress').value.trim();
    const qty = parseInt(document.getElementById('qty').value) || 1;

    if (!name || !phone) {
      alert('⚠ Nom et téléphone obligatoires');
      return;
    }

    const btn = document.getElementById('orderBtn');
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/shop/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          affiliate_code: affiliateCode,
          buyer_name: name,
          buyer_phone: phone,
          buyer_address: address,
          quantity: qty,
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');

      document.getElementById('productContent').style.display = 'none';
      document.getElementById('successScreen').classList.add('show');

      if (navigator.vibrate) navigator.vibrate([30, 50, 30]);
    } catch (e) {
      alert('⚠ ' + e.message);
      btn.disabled = false;
      btn.textContent = '🛒 Commander';
    }
  }

  loadProduct();
</script>
</body>
</html>
"""
)