from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ADMIN_SHOP = (
    HTML_HEAD.format(title="Admin Shop — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: rgba(255,255,255,0.1); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 16px; font-weight: 800; flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .tabs { display: flex; gap: 6px; padding: 12px 16px 0; overflow-x: auto; scrollbar-width: none; }
  .tabs::-webkit-scrollbar { display: none; }
  .tab { flex-shrink: 0; background: #fff; border: 1.5px solid #e0e0e0; color: #757575; padding: 10px 14px; border-radius: 12px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; white-space: nowrap; }
  .tab.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
  .tab-content { display: none; padding-top: 12px; }
  .tab-content.active { display: block; }

  .list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .item { background: #fff; border-radius: 14px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .item-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 8px; }
  .item-title { font-size: 14px; font-weight: 800; color: #212121; flex: 1; min-width: 0; }
  .item-sub { font-size: 11px; color: #757575; margin-top: 2px; }
  .item-badge { font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px; white-space: nowrap; }
  .badge-active { background: #e8f5e9; color: #2e7d32; }
  .badge-inactive { background: #f5f5f5; color: #9e9e9e; }
  .badge-pending { background: #fff3e0; color: #e65100; }
  .badge-paid { background: #e8f5e9; color: #2e7d32; }
  .badge-cancelled { background: #ffebee; color: #d32f2f; }

  .item-img { width: 60px; height: 60px; border-radius: 10px; background: #e8f5e9; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; overflow: hidden; }
  .item-img img { width: 100%; height: 100%; object-fit: cover; }

  .item-actions { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
  .btn-sm { border: none; padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 800; cursor: pointer; font-family: inherit; }
  .btn-approve { background: #2e7d32; color: #fff; }
  .btn-edit { background: #e3f2fd; color: #1976d2; }
  .btn-warn { background: #fff3e0; color: #f57c00; }
  .btn-danger { background: #d32f2f; color: #fff; }
  .btn-sm:active { transform: scale(0.95); }

  .empty { text-align: center; padding: 40px 20px; color: #757575; font-size: 13px; }

  .fab { position: fixed; bottom: calc(30px + var(--safe-bottom)); right: 20px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 8px 24px rgba(46,125,50,0.4); z-index: 90; }
  .fab:active { transform: scale(0.9); }

  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(3px); z-index: 999; display: none; align-items: flex-end; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal-content { background: #fff; border-radius: 20px 20px 0 0; padding: 20px 20px calc(20px + var(--safe-bottom)); max-width: 480px; width: 100%; max-height: 90vh; overflow-y: auto; animation: slideUp 0.3s ease; }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; }
  .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; background: #fff; }
  .form-group textarea { min-height: 70px; resize: vertical; }
  .info-box { background: #fff8e1; border-left: 3px solid #fbc02d; border-radius: 10px; padding: 10px 12px; font-size: 11px; color: #6d4c00; margin-bottom: 12px; line-height: 1.5; }
  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: #212121; }
  .modal-btn.confirm { background: #2e7d32; color: #fff; }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/admin" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Admin Shop</div>
    <div class="spacer"></div>
  </header>

  <div class="tabs">
    <button class="tab active" data-tab="products">📦 Produits</button>
    <button class="tab" data-tab="orders">🛒 Commandes</button>
    <button class="tab" data-tab="affiliations">🔗 Affiliations</button>
  </div>

  <div class="tab-content active" id="tab-products">
    <div class="list" id="productsList"><div class="empty">Chargement...</div></div>
    <button class="fab" onclick="openProductModal()">+</button>
  </div>

  <div class="tab-content" id="tab-orders">
    <div class="filter-row" style="display:flex;gap:6px;padding:0 16px 12px;overflow-x:auto;">
      <button class="tab" style="flex:0;padding:6px 12px;font-size:11px;" onclick="setOrderFilter(this, 'all')">Tout</button>
      <button class="tab" style="flex:0;padding:6px 12px;font-size:11px;" onclick="setOrderFilter(this, 'pending')">En attente</button>
      <button class="tab" style="flex:0;padding:6px 12px;font-size:11px;" onclick="setOrderFilter(this, 'paid')">Payées</button>
    </div>
    <div class="list" id="ordersList"><div class="empty">Chargement...</div></div>
  </div>

  <div class="tab-content" id="tab-affiliations">
    <div class="list" id="affiliationsList"><div class="empty">Chargement...</div></div>
  </div>

  <div style="height: 40px;"></div>
</div>

<div class="modal-overlay" id="productModal">
  <div class="modal-content">
    <div class="modal-title" id="productModalTitle">Nouveau produit</div>
    <div class="info-box" id="commissionInfo">La commission est le montant que l'affilié gagne sur chaque vente. Elle ne peut pas dépasser le prix.</div>
    <div class="form-group">
      <label>Image URL</label>
      <input type="url" id="pImage" placeholder="https://...">
    </div>
    <div class="form-group">
      <label>Titre *</label>
      <input type="text" id="pTitle">
    </div>
    <div class="form-group">
      <label>Description</label>
      <textarea id="pDesc"></textarea>
    </div>
    <div class="form-group">
      <label>Catégorie</label>
      <select id="pCategory">
        <option value="electronique">📱 Électronique</option>
        <option value="mode">👕 Mode</option>
        <option value="maison">🏠 Maison</option>
        <option value="beauté">💄 Beauté</option>
        <option value="sport">⚽ Sport</option>
        <option value="autre" selected>📦 Autre</option>
      </select>
    </div>
    <div class="form-group">
      <label>Prix plateforme (FCFA) *</label>
      <input type="number" id="pPrice" min="0" step="100" oninput="updateCommissionHint()">
    </div>
    <div class="form-group">
      <label>Commission affilié (FCFA) *</label>
      <input type="number" id="pCommission" min="0" step="100" oninput="updateCommissionHint()">
    </div>
    <div class="modal-actions">
      <button class="modal-btn cancel" onclick="closeModal('productModal')">Annuler</button>
      <button class="modal-btn confirm" onclick="saveProduct()">Enregistrer</button>
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

  let editingProductId = null;
  let productsCache = [];
  let orderFilter = 'all';

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }
  function openModal(id) { document.getElementById(id).classList.add('open'); }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }

  async function apiCall(url, options) {
    options = options || {};
    try {
      const res = await fetch(url, Object.assign({ headers: headers() }, options));
      const text = await res.text();
      let data;
      try { data = JSON.parse(text); } catch (e) { data = { error: 'Non-JSON' }; }
      return { ok: res.ok, status: res.status, data: data };
    } catch (e) {
      return { ok: false, status: 0, data: { error: e.message } };
    }
  }

  // ===== PRODUITS =====
  async function loadProducts() {
    const list = document.getElementById('productsList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/shop/products');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    productsCache = r.data.products || [];
    if (productsCache.length === 0) { list.innerHTML = '<div class="empty">Aucun produit. Clique sur + pour en créer.</div>'; return; }

    list.innerHTML = productsCache.map(p => {
      const img = p.image_url ? '<img src="' + p.image_url + '" alt="">' : '📦';
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div class="item-img">' + img + '</div>' +
        '<div style="flex:1;min-width:0;margin-left:10px;">' +
        '<div class="item-title">' + escapeHtml(p.title) + '</div>' +
        '<div class="item-sub">💰 ' + fmt(p.price) + ' F · Commission : ' + fmt(p.commission) + ' F</div>' +
        '<div class="item-sub">📊 ' + (p.sales || 0) + ' ventes · ' + escapeHtml(p.category || 'autre') + '</div>' +
        '</div>' +
        '<span class="item-badge ' + (p.is_active ? 'badge-active' : 'badge-inactive') + '">' + (p.is_active ? 'Actif' : 'Inactif') + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-edit" onclick="editProduct(\\'' + p.id + '\\')">✏️ Modifier</button>' +
        '<button class="btn-sm ' + (p.is_active ? 'btn-warn' : 'btn-approve') + '" onclick="toggleProduct(\\'' + p.id + '\\', ' + (p.is_active ? 'true' : 'false') + ')">' + (p.is_active ? '⏸' : '▶') + '</button>' +
        '<button class="btn-sm btn-danger" onclick="deleteProduct(\\'' + p.id + '\\')">🗑</button>' +
        '</div></div>';
    }).join('');
  }

  function updateCommissionHint() {
    const price = parseFloat(document.getElementById('pPrice').value) || 0;
    const commission = parseFloat(document.getElementById('pCommission').value) || 0;
    const triboost = price - commission;
    if (price > 0) {
      document.getElementById('commissionInfo').innerHTML =
        'Prix : <strong>' + fmt(price) + ' F</strong><br>' +
        'Commission affilié : <strong>' + fmt(commission) + ' F</strong><br>' +
        'Part TriBoost : <strong>' + fmt(triboost) + ' F</strong>';
    } else {
      document.getElementById('commissionInfo').textContent = 'La commission est le montant que l\\'affilié gagne sur chaque vente.';
    }
  }

  function openProductModal() {
    editingProductId = null;
    document.getElementById('productModalTitle').textContent = 'Nouveau produit';
    document.getElementById('pImage').value = '';
    document.getElementById('pTitle').value = '';
    document.getElementById('pDesc').value = '';
    document.getElementById('pCategory').value = 'autre';
    document.getElementById('pPrice').value = '';
    document.getElementById('pCommission').value = '';
    updateCommissionHint();
    openModal('productModal');
  }

  function editProduct(id) {
    const p = productsCache.find(x => x.id === id);
    if (!p) return;
    editingProductId = id;
    document.getElementById('productModalTitle').textContent = 'Modifier le produit';
    document.getElementById('pImage').value = p.image_url || '';
    document.getElementById('pTitle').value = p.title || '';
    document.getElementById('pDesc').value = p.description || '';
    document.getElementById('pCategory').value = p.category || 'autre';
    document.getElementById('pPrice').value = p.price || '';
    document.getElementById('pCommission').value = p.commission || '';
    updateCommissionHint();
    openModal('productModal');
  }

  async function saveProduct() {
    const price = parseFloat(document.getElementById('pPrice').value) || 0;
    const commission = parseFloat(document.getElementById('pCommission').value) || 0;

    if (commission >= price) {
      alert('⚠ La commission doit être inférieure au prix');
      return;
    }

    const payload = {
      title: document.getElementById('pTitle').value.trim(),
      description: document.getElementById('pDesc').value.trim(),
      image_url: document.getElementById('pImage').value.trim(),
      category: document.getElementById('pCategory').value,
      price: price,
      commission: commission,
    };

    if (!payload.title || price <= 0) { alert('⚠ Titre et prix obligatoires'); return; }

    const url = editingProductId
      ? '/api/admin/shop/products/' + editingProductId + '/update'
      : '/api/admin/shop/products/create';

    const r = await apiCall(url, { method: 'POST', body: JSON.stringify(payload) });
    if (r.ok) {
      closeModal('productModal');
      loadProducts();
      alert('✅ Produit enregistré');
    } else {
      alert('⚠ ' + (r.data.detail || 'Erreur'));
    }
  }

  async function toggleProduct(id, isActive) {
    await apiCall('/api/admin/shop/products/' + id + '/update', {
      method: 'POST', body: JSON.stringify({ is_active: !isActive })
    });
    loadProducts();
  }

  async function deleteProduct(id) {
    if (!confirm('Supprimer ce produit ? Les affiliations seront aussi supprimées.')) return;
    await apiCall('/api/admin/shop/products/' + id, { method: 'DELETE' });
    loadProducts();
  }

  // ===== COMMANDES =====
  function setOrderFilter(el, filter) {
    orderFilter = filter;
    document.querySelectorAll('#tab-orders .tab').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    loadOrders();
  }

  async function loadOrders() {
    const list = document.getElementById('ordersList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/shop/orders?status=' + orderFilter);
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const orders = r.data.orders || [];
    if (orders.length === 0) { list.innerHTML = '<div class="empty">Aucune commande</div>'; return; }

    list.innerHTML = orders.map(o => {
      const p = o.shop_products || {};
      const badge = o.status === 'pending' ? 'badge-pending' : (o.status === 'paid' ? 'badge-paid' : 'badge-cancelled');
      const statusLabel = { pending: '⏳ En attente', paid: '✓ Payée', delivered: '✓ Livrée', cancelled: '✗ Annulée' }[o.status] || o.status;

      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(p.title || 'Produit') + ' × ' + o.quantity + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(o.buyer_name) + ' · 📞 ' + escapeHtml(o.buyer_phone) + '</div>' +
        (o.buyer_address ? '<div class="item-sub">📍 ' + escapeHtml(o.buyer_address) + '</div>' : '') +
        '<div class="item-sub">🏪 Vendeur : ' + escapeHtml(o.seller_name || 'Inconnu') + '</div>' +
        '<div class="item-sub">💰 Total : ' + fmt(o.total_paid) + ' F</div>' +
        '<div class="item-sub">🟢 TriBoost : ' + fmt(o.platform_share) + ' F · 👤 Vendeur : ' + fmt(o.user_share) + ' F</div>' +
        '</div>' +
        '<span class="item-badge ' + badge + '">' + statusLabel + '</span>' +
        '</div>' +
        '<div class="item-actions">' +
        (o.status === 'pending' ? '<button class="btn-sm btn-approve" onclick="completeOrder(\\'' + o.id + '\\')">✓ Valider (crédite le vendeur)</button>' : '') +
        '<button class="btn-sm btn-danger" onclick="deleteOrder(\\'' + o.id + '\\')">🗑</button>' +
        '</div></div>';
    }).join('');
  }

  async function completeOrder(id) {
    if (!confirm('Valider cette commande ? Le vendeur sera crédité automatiquement.')) return;
    const r = await apiCall('/api/admin/shop/orders/' + id + '/complete', { method: 'POST' });
    if (r.ok) {
      alert('✅ Commande validée, vendeur crédité !');
      loadOrders();
    } else {
      alert('⚠ ' + (r.data.detail || 'Erreur'));
    }
  }

  async function deleteOrder(id) {
    if (!confirm('Supprimer cette commande ?')) return;
    await apiCall('/api/admin/shop/orders/' + id, { method: 'DELETE' });
    loadOrders();
  }

  // ===== AFFILIATIONS =====
  async function loadAffiliations() {
    const list = document.getElementById('affiliationsList');
    list.innerHTML = '<div class="empty">Chargement...</div>';
    const r = await apiCall('/api/admin/shop/affiliations');
    if (!r.ok) { list.innerHTML = '<div class="empty" style="color:#d32f2f;">Erreur ' + r.status + '</div>'; return; }
    const items = r.data.affiliations || [];
    if (items.length === 0) { list.innerHTML = '<div class="empty">Aucune affiliation</div>'; return; }

    list.innerHTML = items.map(a => {
      const p = a.shop_products || {};
      return '<div class="item">' +
        '<div class="item-header">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="item-title">' + escapeHtml(p.title || 'Produit') + '</div>' +
        '<div class="item-sub">👤 ' + escapeHtml(a.user_name || '') + '</div>' +
        '<div class="item-sub">💰 Prix vendeur : ' + fmt(a.custom_price) + ' F · Prix plateforme : ' + fmt(p.price) + ' F</div>' +
        '<div class="item-sub">📊 ' + (a.total_sales || 0) + ' ventes · Gains : ' + fmt(a.total_earned) + ' F</div>' +
        '<div class="item-sub">🔗 ' + escapeHtml(a.affiliate_code || '') + '</div>' +
        '</div>' +
        '</div>' +
        '<div class="item-actions">' +
        '<button class="btn-sm btn-danger" onclick="deleteAffiliation(\\'' + a.id + '\\')">🗑 Supprimer</button>' +
        '</div></div>';
    }).join('');
  }

  async function deleteAffiliation(id) {
    if (!confirm('Supprimer cette affiliation ? Le lien du vendeur ne marchera plus.')) return;
    await apiCall('/api/admin/shop/affiliations/' + id, { method: 'DELETE' });
    loadAffiliations();
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      const tabName = this.dataset.tab;
      if (!tabName) return;
      document.querySelectorAll('.tabs .tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + tabName).classList.add('active');

      if (tabName === 'products') loadProducts();
      else if (tabName === 'orders') loadOrders();
      else if (tabName === 'affiliations') loadAffiliations();
    });
  });

  // ===== INIT =====
  loadProducts();
</script>
</body>
</html>
"""
)