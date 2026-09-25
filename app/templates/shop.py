from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_SHOP = (
    HTML_HEAD.format(title="Shop — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .hero { margin: 16px; background: linear-gradient(135deg, #2e7d32, #1b5e20); border-radius: 20px; padding: 20px; color: #fff; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(46,125,50,0.3); }
  .hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .hero-title { font-size: 20px; font-weight: 900; margin-bottom: 4px; position: relative; z-index: 2; }
  .hero-sub { font-size: 13px; opacity: 0.9; position: relative; z-index: 2; }

  .tabs { display: flex; gap: 8px; padding: 0 16px 12px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 13px; font-weight: 700; font-family: inherit; cursor: pointer; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .products-grid { padding: 0 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .product-card { background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; }
  .product-img { width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); display: flex; align-items: center; justify-content: center; color: #2e7d32; font-size: 40px; overflow: hidden; }
  .product-img img { width: 100%; height: 100%; object-fit: cover; }
  .product-body { padding: 10px; display: flex; flex-direction: column; gap: 6px; flex: 1; }
  .product-title { font-size: 13px; font-weight: 700; color: var(--text-dark); line-height: 1.3; min-height: 34px; }
  .product-price { font-size: 14px; font-weight: 900; color: var(--green); }
  .product-commission { font-size: 10px; color: #f57c00; font-weight: 700; background: #fff3e0; padding: 2px 6px; border-radius: 6px; display: inline-block; align-self: flex-start; }
  .product-btn { background: var(--green); color: #fff; border: none; padding: 8px; border-radius: 10px; font-weight: 700; font-size: 11px; font-family: inherit; cursor: pointer; margin-top: auto; }
  .product-btn.affiliated { background: #fff3e0; color: #e65100; }

  .aff-card { margin: 0 16px 10px; background: #fff; border-radius: 14px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .aff-header { display: flex; gap: 12px; margin-bottom: 10px; }
  .aff-img { width: 60px; height: 60px; border-radius: 10px; background: #e8f5e9; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; overflow: hidden; }
  .aff-img img { width: 100%; height: 100%; object-fit: cover; }
  .aff-info { flex: 1; min-width: 0; }
  .aff-title { font-size: 14px; font-weight: 800; color: var(--text-dark); }
  .aff-prices { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
  .aff-prices strong { color: var(--green); }
  .aff-stats { display: flex; gap: 8px; margin-top: 8px; }
  .aff-stat { flex: 1; background: #f9f9f9; border-radius: 8px; padding: 6px; text-align: center; }
  .aff-stat .val { font-size: 13px; font-weight: 800; color: var(--text-dark); }
  .aff-stat .lbl { font-size: 9px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }
  .aff-link-box { display: flex; gap: 6px; margin-top: 10px; }
  .aff-link-box input { flex: 1; padding: 8px 10px; border: 1px solid var(--border); border-radius: 8px; font-size: 11px; outline: none; background: #f9f9f9; min-width: 0; }
  .aff-link-box button { background: var(--green); color: #fff; border: none; padding: 8px 12px; border-radius: 8px; font-weight: 700; font-size: 11px; cursor: pointer; font-family: inherit; white-space: nowrap; }
  .aff-link-box button.wa { background: #25D366; }
  .aff-delete { background: transparent; color: #d32f2f; border: none; font-size: 11px; font-weight: 700; margin-top: 6px; cursor: pointer; font-family: inherit; }

  .empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 50px; margin-bottom: 12px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; }

  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: flex-end; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 20px 20px 0 0; padding: 20px 20px calc(20px + var(--safe-bottom)); max-width: 480px; width: 100%; max-height: 90vh; overflow-y: auto; }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; }
  .form-group input { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 15px; font-family: inherit; outline: none; }
  .form-group input:focus { border-color: var(--green); }
  .info-min { background: #fff8e1; border-left: 3px solid #fbc02d; border-radius: 10px; padding: 10px 12px; font-size: 11px; color: #6d4c00; margin-bottom: 14px; line-height: 1.6; }
  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: var(--text-dark); }
  .modal-btn.confirm { background: var(--green); color: #fff; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Shop</div>
    <div class="spacer"></div>
  </header>

  <div class="hero">
    <div class="hero-title">🛍️ Boutique TriBoost</div>
    <div class="hero-sub">Affiliez un produit, fixez votre prix et vendez à votre réseau.</div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="products">🛍️ Produits</button>
    <button class="tab" data-tab="myaff">🔗 Mes liens</button>
    <button class="tab" data-tab="sales">💰 Mes ventes</button>
  </div>

  <div class="tab-content active" id="tab-products">
    <div class="products-grid" id="productsList"></div>
  </div>

  <div class="tab-content" id="tab-myaff">
    <div id="myAffList"></div>
  </div>

  <div class="tab-content" id="tab-sales">
    <div id="salesList"></div>
  </div>

  <div style="height: 40px;"></div>
</div>

<div class="modal-overlay" id="affModal">
  <div class="modal-content">
    <div class="modal-title" id="affModalTitle">Affilier ce produit</div>
    <div class="info-min" id="affInfo"></div>
    <div class="form-group">
      <label>Votre prix de vente (FCFA) *</label>
      <input type="number" id="affPrice" step="100" min="0">
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('affModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="confirmAffiliate()">Affilier</button>
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

  let allProducts = [];
  let myAffiliations = [];
  let currentProduct = null;

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }
  function openModal(id) { document.getElementById(id).classList.add('open'); }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }

  // ===== PRODUITS =====
  async function loadProducts() {
    const list = document.getElementById('productsList');
    list.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:#757575;">Chargement...</div>';
    try {
      const res = await fetch('/api/shop/products', { headers: headers() });
      const data = await res.json();
      allProducts = data.products || [];
      if (allProducts.length === 0) {
        list.innerHTML = '<div class="empty-state" style="grid-column:1/-1;"><div class="icon">🛍️</div><h3>Aucun produit</h3><p>Revenez plus tard.</p></div>';
        return;
      }
      renderProducts();
    } catch (e) {
      list.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:#d32f2f;">Erreur</div>';
    }
  }

  function renderProducts() {
    const list = document.getElementById('productsList');
    list.innerHTML = allProducts.map(p => {
      const img = p.image_url ? '<img src="' + p.image_url + '" alt="">' : '📦';
      const aff = myAffiliations.find(a => a.product_id === p.id);
      const btn = aff
        ? '<button class="product-btn affiliated" onclick="openAffModal(\\'' + p.id + '\\')">✓ Modifier</button>'
        : '<button class="product-btn" onclick="openAffModal(\\'' + p.id + '\\')">+ Affilier</button>';
      return '<div class="product-card">' +
        '<div class="product-img">' + img + '</div>' +
        '<div class="product-body">' +
        '<div class="product-title">' + escapeHtml(p.title) + '</div>' +
        '<div class="product-price">' + fmt(p.price) + ' F</div>' +
        '<div class="product-commission">💰 +' + fmt(p.commission) + ' F</div>' +
        btn +
        '</div></div>';
    }).join('');
  }

  // ===== MES AFFILIATIONS =====
  async function loadMyAff() {
    const list = document.getElementById('myAffList');
    list.innerHTML = '<div style="text-align:center;padding:30px;color:#757575;">Chargement...</div>';
    try {
      const res = await fetch('/api/shop/my-affiliations', { headers: headers() });
      const data = await res.json();
      myAffiliations = data.affiliations || [];

      if (myAffiliations.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">🔗</div><h3>Aucun lien</h3><p>Affiliez un produit pour obtenir votre lien de vente.</p></div>';
        return;
      }

      const baseUrl = window.location.origin;
      list.innerHTML = myAffiliations.map(a => {
        const p = a.shop_products || {};
        const link = baseUrl + '/shop/p/' + a.affiliate_code;
        const img = p.image_url ? '<img src="' + p.image_url + '" alt="">' : '📦';
        const waText = encodeURIComponent('Découvre ce produit : ' + (p.title || '') + '\\n\\n' + link);
        return '<div class="aff-card">' +
          '<div class="aff-header">' +
          '<div class="aff-img">' + img + '</div>' +
          '<div class="aff-info">' +
          '<div class="aff-title">' + escapeHtml(p.title || '') + '</div>' +
          '<div class="aff-prices">Mon prix : <strong>' + fmt(a.custom_price) + ' F</strong></div>' +
          '<div class="aff-prices">Commission : +' + fmt(p.commission) + ' F</div>' +
          '</div>' +
          '</div>' +
          '<div class="aff-stats">' +
          '<div class="aff-stat"><div class="val">' + (a.total_sales || 0) + '</div><div class="lbl">Ventes</div></div>' +
          '<div class="aff-stat"><div class="val">' + fmt(a.total_earned) + ' F</div><div class="lbl">Gains</div></div>' +
          '</div>' +
          '<div class="aff-link-box">' +
          '<input type="text" value="' + link + '" readonly onclick="this.select()">' +
          '<button onclick="copyLink(\\'' + link + '\\', this)">Copier</button>' +
          '<button class="wa" onclick="window.open(\\'https://wa.me/?text=' + waText + '\\')">💬</button>' +
          '</div>' +
          '<button class="aff-delete" onclick="deleteAff(\\'' + a.id + '\\')">🗑 Supprimer ce lien</button>' +
          '</div>';
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  function copyLink(link, btn) {
    navigator.clipboard.writeText(link).then(function() {
      const orig = btn.textContent;
      btn.textContent = '✓';
      setTimeout(function() { btn.textContent = orig; }, 1500);
    });
  }

  async function deleteAff(id) {
    if (!confirm('Supprimer ce lien d\\'affiliation ?')) return;
    try {
      await fetch('/api/shop/affiliate/' + id, { method: 'DELETE', headers: headers() });
      loadMyAff();
      loadProducts();
    } catch (e) { alert('Erreur'); }
  }

  // ===== MODAL AFFILIER =====
  function openAffModal(productId) {
    currentProduct = allProducts.find(p => p.id === productId);
    if (!currentProduct) return;
    const aff = myAffiliations.find(a => a.product_id === productId);
    const currentPrice = aff ? aff.custom_price : currentProduct.price;

    document.getElementById('affModalTitle').textContent = aff ? 'Modifier mon prix' : 'Affilier ce produit';
    document.getElementById('affPrice').value = currentPrice;
    document.getElementById('affPrice').min = currentProduct.price;

    document.getElementById('affInfo').innerHTML =
      'Prix minimum : <strong>' + fmt(currentProduct.price) + ' F</strong><br>' +
      'Votre commission de base : <strong>+' + fmt(currentProduct.commission) + ' F</strong><br>' +
      'Tout montant au-dessus du prix minimum vous revient à 100%.';

    openModal('affModal');
  }

  async function confirmAffiliate() {
    const price = parseFloat(document.getElementById('affPrice').value);
    if (!price || price < currentProduct.price) {
      alert('⚠ Prix minimum : ' + fmt(currentProduct.price) + ' F');
      return;
    }

    try {
      const res = await fetch('/api/shop/affiliate/' + currentProduct.id, {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ custom_price: price })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      closeModal('affModal');
      await loadMyAff();
      renderProducts();
      alert('✅ ' + (data.result?.message || 'Produit affilié !'));
    } catch (e) {
      alert('⚠ ' + e.message);
    }
  }

  // ===== MES VENTES =====
  async function loadSales() {
    const list = document.getElementById('salesList');
    list.innerHTML = '<div style="text-align:center;padding:30px;color:#757575;">Chargement...</div>';
    try {
      const res = await fetch('/api/shop/my-sales', { headers: headers() });
      const data = await res.json();
      const sales = data.sales || [];

      if (sales.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">💰</div><h3>Aucune vente</h3><p>Partagez vos liens pour commencer à vendre.</p></div>';
        return;
      }

      list.innerHTML = sales.map(s => {
        const p = s.shop_products || {};
        const statusLabel = { pending: '⏳ En attente', paid: '✓ Livré', cancelled: '✗ Annulé' }[s.status] || s.status;
        const statusColor = { pending: '#e65100', paid: '#2e7d32', cancelled: '#d32f2f' }[s.status];

        return '<div class="aff-card">' +
          '<div class="aff-title">' + escapeHtml(p.title || '') + ' × ' + s.quantity + '</div>' +
          '<div class="aff-prices">👤 ' + escapeHtml(s.buyer_name || 'Client') + ' · 📞 ' + escapeHtml(s.buyer_phone || '') + '</div>' +
          '<div class="aff-prices">Total : ' + fmt(s.total_paid) + ' F</div>' +
          '<div class="aff-prices" style="color:' + statusColor + '; font-weight: 800;">' + statusLabel + '</div>' +
          '<div class="aff-stats">' +
          '<div class="aff-stat"><div class="val" style="color:#2e7d32;">+' + fmt(s.user_share) + ' F</div><div class="lbl">Ma part</div></div>' +
          '<div class="aff-stat"><div class="val">' + fmt(s.total_paid) + ' F</div><div class="lbl">Total</div></div>' +
          '</div>' +
          '</div>';
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      if (this.dataset.tab === 'myaff') loadMyAff();
      if (this.dataset.tab === 'sales') loadSales();
    });
  });

  // ===== INIT =====
  (async function() {
    await loadMyAff();
    loadProducts();
  })();
</script>
</body>
</html>
"""
)