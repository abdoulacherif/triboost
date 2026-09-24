from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_TACHES = (
    HTML_HEAD.format(title="Tâches — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
    --blue: #1976d2;
    --blue-light: #e3f2fd;
  }
  body { background: #f5f5f5; }
  .app {
    width: 100%; max-width: 480px;
    background: #f5f5f5; min-height: 100vh;
    padding-bottom: calc(40px + var(--safe-bottom));
    padding-top: var(--safe-top);
    margin: 0 auto;
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
    text-decoration: none;
  }
  .page-title {
    font-size: 18px; font-weight: 800; color: var(--text-dark);
    flex: 1; text-align: center;
  }
  .spacer { width: 40px; }

  /* ===== HERO ===== */
  .hero {
    margin: 16px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 20px;
    padding: 20px;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3);
  }
  .hero::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .hero::after {
    content: ''; position: absolute; bottom: -40px; left: -40px;
    width: 120px; height: 120px;
    background: rgba(251, 192, 45, 0.2); border-radius: 50%;
  }
  .hero-content { position: relative; z-index: 2; }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 6px; }
  .hero-sub { font-size: 13px; opacity: 0.9; line-height: 1.5; margin-bottom: 16px; }
  .hero-stats {
    display: flex; gap: 20px;
    position: relative; z-index: 2;
  }
  .hero-stat { display: flex; flex-direction: column; }
  .hero-stat .value { font-size: 20px; font-weight: 900; line-height: 1; }
  .hero-stat .label { font-size: 10px; opacity: 0.85; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

  /* ===== SECTION TITLE ===== */
  .section-title {
    font-size: 15px; font-weight: 800;
    margin: 20px 16px 12px;
    color: var(--text-dark);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .section-title .right { font-size: 12px; color: var(--text-muted); font-weight: 600; }

  /* ===== LISTE TÂCHES ===== */
  .tasks-list {
    padding: 0 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .task-card {
    background: #fff;
    border-radius: 18px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    animation: fadeIn 0.3s ease-out;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s;
  }
  .task-card:active { transform: scale(0.98); }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .task-card.done { opacity: 0.6; }
  .task-card.pending { opacity: 0.85; }

  .tc-header {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
  }
  .tc-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    background: var(--green-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
  }
  .tc-header-info { flex: 1; min-width: 0; }
  .tc-title {
    font-size: 14px;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 4px;
    line-height: 1.3;
  }
  .tc-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .tc-badge.available { background: var(--green-light); color: var(--green); }
  .tc-badge.pending { background: #fff3e0; color: #e65100; }
  .tc-badge.approved { background: var(--green-light); color: var(--green); }
  .tc-badge.rejected { background: var(--red-light); color: var(--red); }

  .tc-reward {
    font-size: 20px;
    font-weight: 900;
    color: var(--green);
    white-space: nowrap;
    flex-shrink: 0;
  }

  .tc-desc {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 12px;
  }

  .tc-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .tc-network {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .tc-btn {
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 12px;
    font-weight: 800;
    font-size: 13px;
    font-family: inherit;
    cursor: pointer;
    transition: transform 0.15s;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
  }
  .tc-btn:active { transform: scale(0.95); }
  .tc-btn:disabled { opacity: 0.5; cursor: not-allowed; box-shadow: none; }
  .tc-btn.pending-btn { background: #fff3e0; color: #e65100; box-shadow: none; }
  .tc-btn.done-btn { background: #f5f5f5; color: #9e9e9e; box-shadow: none; }
  .tc-btn.rejected-btn { background: var(--red-light); color: var(--red); box-shadow: none; }

  /* ===== MODAL ===== */
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(3px);
    z-index: 999;
    display: none;
    align-items: flex-end;
    justify-content: center;
  }
  .modal-overlay.open { display: flex; }
  .modal-content {
    width: 100%;
    max-width: 480px;
    background: #fff;
    border-radius: 24px 24px 0 0;
    max-height: 92vh;
    overflow-y: auto;
    padding: 20px 20px calc(20px + var(--safe-bottom));
    animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }
  .modal-handle {
    width: 40px; height: 4px;
    background: #e0e0e0;
    border-radius: 2px;
    margin: 0 auto 16px;
  }
  .modal-title {
    font-size: 18px; font-weight: 800;
    margin-bottom: 16px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .modal-close {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #f5f5f5;
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-muted);
  }

  .task-preview {
    background: var(--green-light);
    border-radius: 14px;
    padding: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
  }
  .task-preview .icon { font-size: 24px; }
  .task-preview .info { flex: 1; }
  .task-preview .name { font-size: 13px; font-weight: 800; color: var(--text-dark); }
  .task-preview .reward { font-size: 11px; color: var(--green); font-weight: 700; }

  .form-group { margin-bottom: 14px; }
  .form-group label {
    display: block; font-size: 12px;
    font-weight: 700; margin-bottom: 6px;
    color: var(--text-dark);
  }
  .form-group input,
  .form-group select,
  .form-group textarea {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    font-size: 15px;
    font-family: inherit;
    color: var(--text-dark);
    outline: none;
    transition: border-color 0.2s;
    background: #fff;
    -webkit-appearance: none;
  }
  .form-group textarea { min-height: 70px; resize: vertical; }
  .form-group input:focus,
  .form-group select:focus,
  .form-group textarea:focus { border-color: var(--green); }

  .instructions {
    background: #fff8e1;
    border-left: 3px solid var(--gold);
    border-radius: 10px;
    padding: 12px;
    font-size: 12px;
    color: #6d4c00;
    line-height: 1.6;
    margin-bottom: 16px;
    white-space: pre-line;
  }

  .modal-actions {
    display: flex; gap: 10px;
    margin-top: 20px;
  }
  .btn-cancel {
    flex: 1; background: #f5f5f5;
    color: var(--text-dark); border: none;
    padding: 14px; border-radius: 12px;
    font-weight: 700; font-size: 14px;
    font-family: inherit; cursor: pointer;
  }
  .btn-submit {
    flex: 2; background: var(--green);
    color: #fff; border: none;
    padding: 14px; border-radius: 12px;
    font-weight: 800; font-size: 14px;
    font-family: inherit; cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 8px;
  }
  .btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

  .spinner {
    width: 18px; height: 18px;
    border: 2.5px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ===== EMPTY ===== */
  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
  }
  .empty-state .icon {
    width: 80px; height: 80px;
    margin: 0 auto 16px;
    border-radius: 50%;
    background: var(--green-light);
    color: var(--green);
    display: flex; align-items: center; justify-content: center;
  }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  /* ===== SKELETON ===== */
  .skel-card {
    background: #fff;
    border-radius: 18px;
    padding: 16px;
    animation: pulse 1.4s infinite;
  }
  .skel-line { height: 12px; background: #f0f0f0; border-radius: 6px; margin-bottom: 10px; }
  .skel-line.short { width: 60%; }
  .skel-line.tiny { width: 40%; }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
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
    <div class="page-title">Tâches</div>
    <div class="spacer"></div>
  </header>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-content">
      <div class="hero-title">💼 Gagne de l'argent facilement</div>
      <div class="hero-sub">Accomplis des tâches simples et reçois ton argent directement dans ton wallet.</div>
      <div class="hero-stats">
        <div class="hero-stat">
          <span class="value" id="heroTotal">-</span>
          <span class="label">Tâches</span>
        </div>
        <div class="hero-stat">
          <span class="value" id="heroAvailable">-</span>
          <span class="label">Disponibles</span>
        </div>
        <div class="hero-stat">
          <span class="value" id="heroPotential">- F</span>
          <span class="label">À gagner</span>
        </div>
      </div>
    </div>
  </div>

  <!-- SECTION TITRE -->
  <div class="section-title">
    <span>🎯 Tâches disponibles</span>
    <span class="right" id="taskCount">Chargement...</span>
  </div>

  <!-- LISTE -->
  <div class="tasks-list" id="tasksList">
    <div class="skel-card">
      <div class="skel-line short"></div>
      <div class="skel-line"></div>
      <div class="skel-line tiny"></div>
    </div>
    <div class="skel-card">
      <div class="skel-line short"></div>
      <div class="skel-line"></div>
      <div class="skel-line tiny"></div>
    </div>
  </div>

  <div style="height: 32px;"></div>
</div>

<!-- MODAL SOUMISSION -->
<div class="modal-overlay" id="submitModal" onclick="if(event.target===this) closeModal()">
  <div class="modal-content">
    <div class="modal-handle"></div>
    <div class="modal-title">
      <span>Soumettre la preuve</span>
      <button class="modal-close" onclick="closeModal()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <div class="task-preview">
      <div class="icon" id="modalIcon">🎯</div>
      <div class="info">
        <div class="name" id="modalTitle">-</div>
        <div class="reward" id="modalReward">+0 F</div>
      </div>
    </div>

    <div class="instructions" id="modalInstructions"></div>

    <div id="modalError" class="alert error" style="display:none;"></div>

    <form id="submitForm" onsubmit="submitProof(event)">

      <div class="form-group">
        <label>Réseau utilisé *</label>
        <input type="text" id="networkInput" required maxlength="50"
               placeholder="Ex : TikTok, Facebook, Instagram...">
      </div>

      <div class="form-group">
        <label>Lien de la publication *</label>
        <input type="url" id="proofUrlInput" required
               placeholder="https://tiktok.com/@ton_compte/video/...">
      </div>

      <div class="form-group">
        <label>Commentaire (optionnel)</label>
        <textarea id="commentInput" maxlength="200"
                  placeholder="Ajoute une précision pour l'admin..."></textarea>
      </div>

      <div class="modal-actions">
        <button type="button" class="btn-cancel" onclick="closeModal()">Annuler</button>
        <button type="submit" class="btn-submit" id="submitBtn">
          <span>Envoyer la preuve</span>
        </button>
      </div>
    </form>
  </div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) {
    window.location.href = '/login';
  }

  let allTasks = [];
  let currentTask = null;

  // ===== CHARGER LES TÂCHES =====
  async function loadTasks() {
    const list = document.getElementById('tasksList');

    try {
      const res = await fetch('/api/tasks/?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });

      if (res.status === 401) {
        localStorage.clear();
        window.location.href = '/login';
        return;
      }

      if (!res.ok) throw new Error('Erreur');

      const data = await res.json();
      allTasks = data.tasks || [];

      updateHero();
      renderTasks();

    } catch (err) {
      list.innerHTML = `
        <div class="empty-state">
          <h3>Erreur de chargement</h3>
          <p>${err.message}</p>
        </div>
      `;
    }
  }

  // ===== HERO =====
  function updateHero() {
    const total = allTasks.length;
    const available = allTasks.filter(t => !t.user_status || t.user_status === 'rejected').length;
    const potential = allTasks
      .filter(t => !t.user_status || t.user_status === 'rejected')
      .reduce((sum, t) => sum + Number(t.reward || 0), 0);

    document.getElementById('heroTotal').textContent = total;
    document.getElementById('heroAvailable').textContent = available;
    document.getElementById('heroPotential').textContent =
      potential >= 1000 ? (potential / 1000).toFixed(1) + 'k F' : potential + ' F';

    document.getElementById('taskCount').textContent = total + ' au total';
  }

  // ===== RENDER =====
  function renderTasks() {
    const list = document.getElementById('tasksList');

    if (allTasks.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 11l3 3L22 4"></path>
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
            </svg>
          </div>
          <h3>Aucune tâche disponible</h3>
          <p>Reviens plus tard, de nouvelles tâches arrivent régulièrement.</p>
        </div>
      `;
      return;
    }

    list.innerHTML = allTasks.map(t => renderTask(t)).join('');
  }

  function renderTask(t) {
    const reward = Number(t.reward || 0);
    const status = t.user_status;

    let badge = '<span class="tc-badge available">Disponible</span>';
    let btnHTML = `<button class="tc-btn" onclick="openModal('${t.id}')">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
      Valider
    </button>`;
    let cardClass = '';

    if (status === 'pending') {
      badge = '<span class="tc-badge pending">⏳ En attente</span>';
      btnHTML = `<button class="tc-btn pending-btn" disabled>Vérification...</button>`;
      cardClass = 'pending';
    } else if (status === 'approved') {
      badge = '<span class="tc-badge approved">✓ Validé</span>';
      btnHTML = `<button class="tc-btn done-btn" disabled>Terminé</button>`;
      cardClass = 'done';
    } else if (status === 'rejected') {
      badge = '<span class="tc-badge rejected">✗ Rejeté</span>';
      btnHTML = `<button class="tc-btn rejected-btn" onclick="openModal('${t.id}')">Ressoumettre</button>`;
    }

    return `
      <div class="task-card ${cardClass}">
        <div class="tc-header">
          <div class="tc-icon">${t.icon || '🎯'}</div>
          <div class="tc-header-info">
            <div class="tc-title">${escapeHtml(t.title)}</div>
            ${badge}
          </div>
          <div class="tc-reward">+${reward.toLocaleString('fr-FR')} F</div>
        </div>
        <div class="tc-desc">${escapeHtml(t.description)}</div>
        <div class="tc-footer">
          <div class="tc-network">
            ${t.network_hint ? '📱 ' + escapeHtml(t.network_hint) : ''}
          </div>
          ${btnHTML}
        </div>
      </div>
    `;
  }

  // ===== MODAL =====
  function openModal(taskId) {
    currentTask = allTasks.find(t => t.id === taskId);
    if (!currentTask) return;

    vibrate(8);

    document.getElementById('modalIcon').textContent = currentTask.icon || '🎯';
    document.getElementById('modalTitle').textContent = currentTask.title;
    document.getElementById('modalReward').textContent = '+' + Number(currentTask.reward).toLocaleString('fr-FR') + ' F';
    document.getElementById('modalInstructions').textContent = currentTask.instructions || currentTask.description || '';

    // Pré-remplir le réseau si hint
    if (currentTask.network_hint) {
      document.getElementById('networkInput').value = currentTask.network_hint;
    }

    document.getElementById('modalError').style.display = 'none';
    document.getElementById('submitForm').reset();
    if (currentTask.network_hint) {
      document.getElementById('networkInput').value = currentTask.network_hint;
    }

    document.getElementById('submitModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    document.getElementById('submitModal').classList.remove('open');
    document.body.style.overflow = '';
    currentTask = null;
  }

  // ===== SOUMETTRE =====
  async function submitProof(e) {
    e.preventDefault();
    if (!currentTask) return;

    vibrate(8);

    const btn = document.getElementById('submitBtn');
    const errEl = document.getElementById('modalError');
    errEl.style.display = 'none';

    const network = document.getElementById('networkInput').value.trim();
    const proofUrl = document.getElementById('proofUrlInput').value.trim();
    const comment = document.getElementById('commentInput').value.trim();

    if (!network || !proofUrl) {
      errEl.textContent = '⚠ Remplis tous les champs obligatoires';
      errEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/tasks/' + currentTask.id + '/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify({ network, proof_url: proofUrl, comment }),
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Erreur');

      vibrate(20);
      closeModal();
      showToast('✅ Preuve envoyée ! Vérification sous 24-48h.');
      loadTasks();

    } catch (err) {
      vibrate([30, 50, 30]);
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.innerHTML = '<span>Envoyer la preuve</span>';
    }
  }

  // ===== HELPERS =====
  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function showToast(msg) {
    const t = document.createElement('div');
    t.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: linear-gradient(135deg, #2e7d32, #1b5e20);
      color: #fff; padding: 14px 20px; border-radius: 14px;
      font-size: 13px; font-weight: 700; z-index: 10001;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      max-width: 340px; text-align: center;
    `;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 4000);
  }

  // ===== INIT =====
  loadTasks();
</script>
</body>
</html>
"""
)