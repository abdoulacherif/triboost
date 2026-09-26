from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ADMIN_COURSES = (
    HTML_HEAD.format(title="Admin Cours — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; margin: 0 auto; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: rgba(255,255,255,0.1); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 16px; font-weight: 800; flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding: 16px; }
  .stat-card { background: #fff; border-radius: 14px; padding: 12px 8px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
  .stat-card .v { font-size: 18px; font-weight: 900; color: var(--text-dark); line-height: 1; }
  .stat-card .l { font-size: 9px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; font-weight: 700; }

  .tabs { display: flex; gap: 6px; padding: 0 16px 12px; overflow-x: auto; scrollbar-width: none; }
  .tabs::-webkit-scrollbar { display: none; }
  .tab { flex-shrink: 0; background: #fff; border: 1.5px solid #e0e0e0; color: #757575; padding: 10px 14px; border-radius: 12px; font-size: 12px; font-weight: 700; font-family: inherit; cursor: pointer; white-space: nowrap; }
  .tab.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
  .tab-content { display: none; padding-top: 12px; }
  .tab-content.active { display: block; }

  .path-select { margin: 0 16px 12px; background: #fff; border-radius: 14px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
  .path-select label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px; display: block; }
  .path-select select { width: 100%; padding: 10px 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; background: #fff; }

  .section-title { margin: 0 16px 10px; font-size: 13px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; color: var(--text-dark); }
  .btn-add { background: var(--green); color: #fff; border: none; padding: 8px 14px; border-radius: 10px; font-size: 11px; font-weight: 800; font-family: inherit; cursor: pointer; }
  .btn-add.small { padding: 6px 10px; font-size: 10px; }

  .list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }

  .chapter-item { background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .chapter-head { padding: 14px; display: flex; align-items: center; gap: 10px; cursor: pointer; }
  .chapter-num { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 14px; flex-shrink: 0; }
  .chapter-info { flex: 1; min-width: 0; }
  .chapter-title { font-size: 13px; font-weight: 800; color: var(--text-dark); }
  .chapter-sub { font-size: 10px; color: var(--text-muted); margin-top: 2px; }
  .icon-btn { background: #f5f5f5; color: #757575; border: none; width: 30px; height: 30px; border-radius: 8px; font-size: 13px; cursor: pointer; font-family: inherit; display: flex; align-items: center; justify-content: center; }
  .icon-btn.danger { background: #ffebee; color: #d32f2f; }
  .icon-btn.info { background: #e3f2fd; color: #1976d2; }
  .icon-btn.warn { background: #fff3e0; color: #f57c00; }

  .lessons-list { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
  .chapter-item.open .lessons-list { max-height: 5000px; }

  .lesson-item { padding: 12px 14px; border-top: 1px solid #f5f5f5; }
  .lesson-head { display: flex; align-items: center; gap: 8px; }
  .lesson-num { width: 26px; height: 26px; border-radius: 8px; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; flex-shrink: 0; }
  .lesson-info { flex: 1; min-width: 0; }
  .lesson-title { font-size: 12px; font-weight: 700; color: var(--text-dark); }
  .lesson-sub { font-size: 10px; color: var(--text-muted); margin-top: 2px; }
  .lesson-actions { display: flex; gap: 4px; }
  .lesson-actions .icon-btn { width: 26px; height: 26px; font-size: 12px; }

  .sub-section { background: #fafafa; border-radius: 10px; padding: 10px; margin: 8px 0; }
  .sub-title { font-size: 10px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
  .sub-item { padding: 6px 8px; background: #fff; border-radius: 8px; margin-bottom: 4px; font-size: 11px; display: flex; align-items: center; gap: 6px; }
  .sub-item .txt { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .sub-item .del { background: #ffebee; color: #d32f2f; border: none; width: 22px; height: 22px; border-radius: 6px; font-size: 11px; cursor: pointer; font-family: inherit; }
  .type-badge { font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 5px; text-transform: uppercase; }
  .type-text { background: #e3f2fd; color: #1976d2; }
  .type-heading { background: #f3e5f5; color: #7b1fa2; }
  .type-video { background: #ffebee; color: #d32f2f; }
  .type-image { background: #e0f2f1; color: #00796b; }
  .type-code { background: #1a1a1a; color: #00ff88; }
  .type-quote { background: #fff8e1; color: #f9a825; }
  .type-tip { background: #fff3e0; color: #f57c00; }

  .progress-card { background: #fff; border-radius: 14px; padding: 14px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .progress-user { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
  .progress-avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 16px; flex-shrink: 0; }
  .progress-name { font-size: 13px; font-weight: 800; }
  .progress-meta { font-size: 10px; color: var(--text-muted); margin-top: 2px; }
  .progress-stats { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; }
  .progress-stat { background: #f9f9f9; border-radius: 8px; padding: 8px; text-align: center; }
  .progress-stat .v { font-size: 14px; font-weight: 900; }
  .progress-stat .l { font-size: 9px; color: var(--text-muted); text-transform: uppercase; margin-top: 2px; }
  .progress-stat.up .v { color: #2e7d32; }
  .progress-stat.down .v { color: #d32f2f; }

  .api-key-item { background: #fff; border-radius: 14px; padding: 14px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .api-key-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 8px; }
  .api-key-name { font-size: 13px; font-weight: 800; }
  .api-key-value { font-family: 'Courier New', monospace; font-size: 10px; color: #757575; background: #f5f5f5; padding: 6px 8px; border-radius: 6px; word-break: break-all; margin: 8px 0; }
  .api-key-meta { font-size: 10px; color: var(--text-muted); }

  /* MODAL */
  #modalOverlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 99999; align-items: flex-end; justify-content: center; }
  #modalOverlay.open { display: flex; }
  #modalOverlay .content { background: #fff; border-radius: 24px 24px 0 0; padding: 20px 20px 40px; width: 100%; max-width: 480px; max-height: 92vh; overflow-y: auto; box-sizing: border-box; animation: slideUp 0.3s ease; }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-handle { width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; margin: 0 auto 16px; }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 11px; font-weight: 700; margin-bottom: 6px; color: var(--text-dark); }
  .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; box-sizing: border-box; }
  .form-group textarea { min-height: 80px; resize: vertical; }
  .form-group input:focus, .form-group textarea:focus, .form-group select:focus { border-color: var(--green); }
  .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: var(--text-dark); }
  .modal-btn.confirm { background: var(--green); color: #fff; }
  .modal-btn.danger { background: #d32f2f; color: #fff; }

  .image-upload { width: 100%; height: 140px; border: 2px dashed #e0e0e0; border-radius: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; cursor: pointer; background: #fafafa; overflow: hidden; position: relative; }
  .image-upload input { display: none; }
  .image-upload .label { font-size: 11px; color: #757575; font-weight: 600; }
  .image-upload img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .image-upload .remove-img { position: absolute; top: 6px; right: 6px; width: 28px; height: 28px; background: rgba(0,0,0,0.7); color: #fff; border: none; border-radius: 50%; cursor: pointer; font-family: inherit; font-size: 12px; z-index: 2; }

  .empty { text-align: center; padding: 40px 20px; color: var(--text-muted); font-size: 12px; }

  .fab { position: fixed; bottom: calc(30px + var(--safe-bottom)); right: 20px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 26px; box-shadow: 0 8px 24px rgba(46,125,50,0.4); z-index: 90; font-family: inherit; }

  .toast-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; display: flex; flex-direction: column; gap: 10px; width: 340px; max-width: 90vw; }
  .toast { padding: 14px 18px; border-radius: 14px; color: #fff; font-size: 13px; font-weight: 700; box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: toastIn 0.3s ease; }
  .toast.success { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .toast.error { background: linear-gradient(135deg, #d32f2f, #b71c1c); }
  .toast.warning { background: linear-gradient(135deg, #f57c00, #e65100); }
  .toast.info { background: linear-gradient(135deg, #1976d2, #0d47a1); }
  @keyframes toastIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

  @media (min-width: 768px) {
    .app { max-width: 1000px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); overflow: hidden; }
    .stats-grid { grid-template-columns: repeat(7, 1fr); }
    .list { display: grid; grid-template-columns: 1fr 1fr; }
  }
</style>
</head>
<body>

<div class="toast-container" id="toastContainer"></div>

<div class="app">
  <header class="topbar">
    <a href="/admin" class="back-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg></a>
    <div class="page-title">Gestion Cours</div>
    <div class="spacer"></div>
  </header>

  <div class="stats-grid" id="statsGrid"></div>

  <div class="tabs">
    <button class="tab active" data-tab="content">📚 Contenu</button>
    <button class="tab" data-tab="progress">👥 Progression</button>
    <button class="tab" data-tab="api-keys">🔑 API</button>
  </div>

  <!-- CONTENU -->
  <div class="tab-content active" id="tab-content">
    <div class="path-select">
      <label>📖 Parcours</label>
      <select id="pathSelect" onchange="loadChapters()">
        <option value="">-- Choisir un parcours --</option>
      </select>
    </div>

    <div class="section-title" id="chaptersTitle" style="display:none;">
      <span>📑 Chapitres</span>
      <button class="btn-add" onclick="openChapterModal()">+ Chapitre</button>
    </div>

    <div class="list" id="chaptersList"><div class="empty">Sélectionne un parcours</div></div>
    <div style="height: 40px;"></div>
  </div>

  <!-- PROGRESSION -->
  <div class="tab-content" id="tab-progress">
    <div class="path-select">
      <label>🔍 Filtrer par parcours</label>
      <select id="progressPathSelect" onchange="loadProgress()">
        <option value="">-- Tous les parcours --</option>
      </select>
    </div>
    <div class="list" id="progressList" style="grid-template-columns: 1fr;"><div class="empty">Chargement...</div></div>
    <div style="height: 40px;"></div>
  </div>

  <!-- API KEYS -->
  <div class="tab-content" id="tab-api-keys">
    <div class="section-title">
      <span>🔑 Clés API externes</span>
      <button class="btn-add" onclick="openApiKeyModal()">+ Nouvelle clé</button>
    </div>
    <div class="list" id="apiKeysList" style="grid-template-columns: 1fr;"><div class="empty">Chargement...</div></div>
    <div style="height: 40px;"></div>
  </div>

</div>

<div id="modalOverlay" onclick="if(event.target===this) closeModal()">
  <div class="content" id="modalContent"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  let allPaths = [];
  let currentPathId = null;
  let currentChapters = [];
  let currentEditingLesson = null;
  let imageBase64 = null;

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }

  function showToast(msg, type) {
    type = type || 'success';
    const container = document.getElementById('toastContainer');
    const t = document.createElement('div');
    t.className = 'toast ' + type;
    t.textContent = msg;
    container.appendChild(t);
    setTimeout(function() { t.remove(); }, 3000);
  }

  function closeModal() {
    document.getElementById('modalOverlay').classList.remove('open');
    document.body.style.overflow = '';
    imageBase64 = null;
  }

  async function apiCall(url, options) {
    options = options || {};
    try {
      const res = await fetch(url, Object.assign({ headers: headers() }, options));
      const text = await res.text();
      let data;
      try { data = JSON.parse(text); } catch (e) { data = { error: 'Non-JSON', raw: text }; }
      return { ok: res.ok, status: res.status, data: data };
    } catch (e) {
      return { ok: false, status: 0, data: { error: e.message } };
    }
  }

  // ===== STATS =====
  async function loadStats() {
    const r = await apiCall('/api/admin/courses/stats');
    if (!r.ok) return;
    const s = r.data.stats || {};
    document.getElementById('statsGrid').innerHTML =
      '<div class="stat-card"><div class="v">' + (s.paths || 0) + '</div><div class="l">Parcours</div></div>' +
      '<div class="stat-card"><div class="v">' + (s.chapters || 0) + '</div><div class="l">Chapitres</div></div>' +
      '<div class="stat-card"><div class="v">' + (s.lessons || 0) + '</div><div class="l">Leçons</div></div>' +
      '<div class="stat-card"><div class="v">' + (s.blocks || 0) + '</div><div class="l">Blocs</div></div>' +
      '<div class="stat-card"><div class="v">' + (s.exercises || 0) + '</div><div class="l">Exercices</div></div>' +
      '<div class="stat-card"><div class="v">' + (s.unlocks || 0) + '</div><div class="l">Inscrits</div></div>' +
      '<div class="stat-card"><div class="v">' + (s.completed_lessons || 0) + '</div><div class="l">Leçons finies</div></div>';
  }

  // ===== PATHS =====
  async function loadPaths() {
    const r = await apiCall('/api/admin/courses/paths');
    if (!r.ok) return;
    allPaths = r.data.paths || [];

    const sel = document.getElementById('pathSelect');
    const selProg = document.getElementById('progressPathSelect');

    const optionsHTML = '<option value="">-- Choisir un parcours --</option>' +
      allPaths.map(p => '<option value="' + p.id + '">' + (p.icon || '📚') + ' ' + escapeHtml(p.title) + '</option>').join('');

    sel.innerHTML = optionsHTML;
    if (selProg) selProg.innerHTML = '<option value="">-- Tous --</option>' + allPaths.map(p => '<option value="' + p.id + '">' + (p.icon || '📚') + ' ' + escapeHtml(p.title) + '</option>').join('');
  }

  // ===== CHAPITRES =====
  async function loadChapters() {
    currentPathId = document.getElementById('pathSelect').value;
    const container = document.getElementById('chaptersList');
    const title = document.getElementById('chaptersTitle');

    if (!currentPathId) {
      container.innerHTML = '<div class="empty">Sélectionne un parcours</div>';
      title.style.display = 'none';
      return;
    }

    title.style.display = 'flex';
    container.innerHTML = '<div class="empty">Chargement...</div>';

    const r = await apiCall('/api/admin/courses/paths/' + currentPathId + '/chapters');
    if (!r.ok) { container.innerHTML = '<div class="empty">Erreur</div>'; return; }

    currentChapters = r.data.chapters || [];

    if (currentChapters.length === 0) {
      container.innerHTML = '<div class="empty">Aucun chapitre. Ajoute-en un !</div>';
      return;
    }

    container.innerHTML = currentChapters.map((ch, idx) => renderChapter(ch, idx)).join('');
  }

  function renderChapter(ch, idx) {
    const lessons = ch.lessons || [];

    return '<div class="chapter-item" id="ch-' + ch.id + '">' +
      '<div class="chapter-head" onclick="toggleChapter(\\'' + ch.id + '\\')">' +
      '<div class="chapter-num">' + (idx + 1) + '</div>' +
      '<div class="chapter-info">' +
      '<div class="chapter-title">' + escapeHtml(ch.title) + '</div>' +
      '<div class="chapter-sub">' + lessons.length + ' leçon(s) · Ordre ' + (ch.sort_order || 0) + '</div>' +
      '</div>' +
      '<button class="icon-btn info" onclick="event.stopPropagation(); editChapter(\\'' + ch.id + '\\')" title="Modifier">✏️</button>' +
      '<button class="icon-btn danger" onclick="event.stopPropagation(); deleteChapter(\\'' + ch.id + '\\')" title="Supprimer">🗑</button>' +
      '</div>' +
      '<div class="lessons-list">' +
      '<div style="padding: 8px 14px;">' +
      '<button class="btn-add small" style="width:100%;" onclick="openLessonModal(\\'' + ch.id + '\\')">+ Ajouter une leçon</button>' +
      '</div>' +
      lessons.map(l => renderLesson(l, ch.id)).join('') +
      '</div></div>';
  }

  function renderLesson(l, chapterId) {
    const questions = l.questions || [];
    const blocks = l.blocks || [];
    const exercises = l.exercises || [];

    const blocksHTML = blocks.length > 0 ?
      '<div class="sub-section">' +
      '<div class="sub-title"><span>📄 Blocs de contenu (' + blocks.length + ')</span>' +
      '<button class="icon-btn info" style="width:22px;height:22px;font-size:11px;" onclick="openBlockModal(\\'' + l.id + '\\')">+</button>' +
      '</div>' +
      blocks.map(b => '<div class="sub-item">' +
        '<span class="type-badge type-' + (b.block_type || 'text') + '">' + (b.block_type || 'text') + '</span>' +
        '<span class="txt">' + escapeHtml((b.content || '').substring(0, 50)) + '</span>' +
        '<button class="del" onclick="deleteBlock(\\'' + b.id + '\\')">✕</button>' +
        '</div>').join('') +
      '</div>' : '';

    const exercisesHTML = exercises.length > 0 ?
      '<div class="sub-section">' +
      '<div class="sub-title"><span>🎯 Exercices (' + exercises.length + ')</span>' +
      '<button class="icon-btn info" style="width:22px;height:22px;font-size:11px;" onclick="openExerciseModal(\\'' + l.id + '\\')">+</button>' +
      '</div>' +
      exercises.map(e => '<div class="sub-item">' +
        '<span class="type-badge type-text">' + (e.exercise_type || 'text') + '</span>' +
        '<span class="txt">' + escapeHtml(e.title) + '</span>' +
        '<button class="del" onclick="deleteExercise(\\'' + e.id + '\\')">✕</button>' +
        '</div>').join('') +
      '</div>' : '';

    const questionsHTML = questions.length > 0 ?
      '<div class="sub-section">' +
      '<div class="sub-title"><span>❓ QCM (' + questions.length + ')</span>' +
      '<button class="icon-btn info" style="width:22px;height:22px;font-size:11px;" onclick="openQuestionModal(\\'' + l.id + '\\')">+</button>' +
      '</div>' +
      questions.map((q, i) => '<div class="sub-item">' +
        '<span class="type-badge type-heading">Q' + (i + 1) + '</span>' +
        '<span class="txt">' + escapeHtml(q.question) + '</span>' +
        '<button class="del" onclick="deleteQuestion(\\'' + q.id + '\\')">✕</button>' +
        '</div>').join('') +
      '</div>' : '';

    const noContent = (blocks.length === 0 && exercises.length === 0 && questions.length === 0) ?
      '<div class="sub-section" style="text-align:center;padding:12px;">' +
      '<div style="font-size:11px;color:#757575;margin-bottom:8px;">Aucun contenu</div>' +
      '<div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap;">' +
      '<button class="btn-add small" onclick="openBlockModal(\\'' + l.id + '\\')">+ Bloc</button>' +
      '<button class="btn-add small" style="background:#f57c00;" onclick="openExerciseModal(\\'' + l.id + '\\')">+ Exo</button>' +
      '<button class="btn-add small" style="background:#1976d2;" onclick="openQuestionModal(\\'' + l.id + '\\')">+ QCM</button>' +
      '</div></div>' : '';

    return '<div class="lesson-item">' +
      '<div class="lesson-head">' +
      '<div class="lesson-num">' + l.day_number + '</div>' +
      '<div class="lesson-info">' +
      '<div class="lesson-title">' + escapeHtml(l.title) + '</div>' +
      '<div class="lesson-sub">' + (l.duration_minutes || 30) + 'min · +' + l.gain_amount + ' / -' + l.loss_amount + ' · ' + blocks.length + 'B/' + exercises.length + 'E/' + questions.length + 'Q</div>' +
      '</div>' +
      '<div class="lesson-actions">' +
      '<button class="icon-btn info" onclick="editLesson(\\'' + l.id + '\\')" title="Modifier">✏️</button>' +
      '<button class="icon-btn warn" onclick="openLessonContent(\\'' + l.id + '\\')" title="Contenu">📄</button>' +
      '<button class="icon-btn danger" onclick="deleteLesson(\\'' + l.id + '\\')" title="Supprimer">🗑</button>' +
      '</div>' +
      '</div>' +
      '<div id="lesson-content-' + l.id + '" style="display:none;">' +
      blocksHTML + exercisesHTML + questionsHTML + noContent +
      '</div>' +
      '</div>';
  }

  function toggleChapter(id) {
    const el = document.getElementById('ch-' + id);
    if (el) el.classList.toggle('open');
  }

  function openLessonContent(id) {
    const el = document.getElementById('lesson-content-' + id);
    if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
  }

  // ===== MODALES CHAPITRE =====
  function openChapterModal() {
    if (!currentPathId) { showToast('Choisis un parcours', 'error'); return; }
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Nouveau chapitre</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="chTitle" placeholder="Ex: Chapitre 1">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="chDesc"></textarea>
      </div>
      <div class="form-group">
        <label>Ordre</label>
        <input type="number" id="chOrder" value="${currentChapters.length + 1}" min="1">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveChapter()">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  function editChapter(id) {
    const ch = currentChapters.find(c => c.id === id);
    if (!ch) return;
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">✏️ Modifier le chapitre</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="chTitle" value="${escapeHtml(ch.title)}">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="chDesc">${escapeHtml(ch.description || '')}</textarea>
      </div>
      <div class="form-group">
        <label>Ordre</label>
        <input type="number" id="chOrder" value="${ch.sort_order || 0}" min="0">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="updateChapter('${id}')">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function saveChapter() {
    const title = document.getElementById('chTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }
    const r = await apiCall('/api/admin/courses/chapters/create', {
      method: 'POST',
      body: JSON.stringify({
        path_id: currentPathId,
        title: title,
        description: document.getElementById('chDesc').value.trim(),
        sort_order: parseInt(document.getElementById('chOrder').value) || 1,
      })
    });
    if (r.ok) { closeModal(); showToast('Chapitre créé', 'success'); loadChapters(); loadStats(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function updateChapter(id) {
    const title = document.getElementById('chTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }
    const r = await apiCall('/api/admin/courses/chapters/' + id + '/update', {
      method: 'POST',
      body: JSON.stringify({
        title: title,
        description: document.getElementById('chDesc').value.trim(),
        sort_order: parseInt(document.getElementById('chOrder').value) || 0,
      })
    });
    if (r.ok) { closeModal(); showToast('Chapitre mis à jour', 'success'); loadChapters(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function deleteChapter(id) {
    if (!confirm('Supprimer ce chapitre et tout son contenu ?')) return;
    await apiCall('/api/admin/courses/chapters/' + id, { method: 'DELETE' });
    showToast('Chapitre supprimé', 'info');
    loadChapters();
    loadStats();
  }

  // ===== MODALES LEÇON =====
  function openLessonModal(chapterId) {
    const ch = currentChapters.find(c => c.id === chapterId);
    const nextDay = (ch && ch.lessons) ? ch.lessons.length + 1 : 1;

    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Nouvelle leçon</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="lTitle" placeholder="Ex: Introduction">
      </div>
      <div class="form-group">
        <label>Objectifs</label>
        <textarea id="lObjectives" placeholder="Ce que l'apprenant va maîtriser..."></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Jour n° *</label>
          <input type="number" id="lDay" value="${nextDay}" min="1">
        </div>
        <div class="form-group">
          <label>Durée (min)</label>
          <input type="number" id="lDuration" value="30" min="1">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Gain bonne (F)</label>
          <input type="number" id="lGain" value="50" min="0">
        </div>
        <div class="form-group">
          <label>Perte mauvaise (F)</label>
          <input type="number" id="lLoss" value="20" min="0">
        </div>
      </div>
      <div class="form-group">
        <label>Vidéo URL (YouTube/Vimeo)</label>
        <input type="url" id="lVideo" placeholder="https://...">
      </div>
      <div class="form-group">
        <label>PDF URL</label>
        <input type="url" id="lPdf" placeholder="https://...">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveLesson('${chapterId}')">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  function editLesson(lessonId) {
    let lesson = null;
    for (const ch of currentChapters) {
      const l = (ch.lessons || []).find(x => x.id === lessonId);
      if (l) { lesson = l; break; }
    }
    if (!lesson) return;

    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">✏️ Modifier la leçon</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="lTitle" value="${escapeHtml(lesson.title)}">
      </div>
      <div class="form-group">
        <label>Objectifs</label>
        <textarea id="lObjectives">${escapeHtml(lesson.objectives || '')}</textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Jour n°</label>
          <input type="number" id="lDay" value="${lesson.day_number}" min="1">
        </div>
        <div class="form-group">
          <label>Durée (min)</label>
          <input type="number" id="lDuration" value="${lesson.duration_minutes || 30}" min="1">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Gain bonne (F)</label>
          <input type="number" id="lGain" value="${lesson.gain_amount}" min="0">
        </div>
        <div class="form-group">
          <label>Perte mauvaise (F)</label>
          <input type="number" id="lLoss" value="${lesson.loss_amount}" min="0">
        </div>
      </div>
      <div class="form-group">
        <label>Vidéo URL</label>
        <input type="url" id="lVideo" value="${escapeHtml(lesson.video_url || '')}">
      </div>
      <div class="form-group">
        <label>PDF URL</label>
        <input type="url" id="lPdf" value="${escapeHtml(lesson.pdf_url || '')}">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="updateLesson('${lessonId}')">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function saveLesson(chapterId) {
    const title = document.getElementById('lTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }
    const r = await apiCall('/api/admin/courses/lessons/create', {
      method: 'POST',
      body: JSON.stringify({
        chapter_id: chapterId,
        title: title,
        objectives: document.getElementById('lObjectives').value.trim(),
        day_number: parseInt(document.getElementById('lDay').value) || 1,
        duration_minutes: parseInt(document.getElementById('lDuration').value) || 30,
        gain_amount: parseFloat(document.getElementById('lGain').value) || 50,
        loss_amount: parseFloat(document.getElementById('lLoss').value) || 20,
        video_url: document.getElementById('lVideo').value.trim(),
        pdf_url: document.getElementById('lPdf').value.trim(),
      })
    });
    if (r.ok) { closeModal(); showToast('Leçon créée', 'success'); loadChapters(); loadStats(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function updateLesson(lessonId) {
    const title = document.getElementById('lTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }
    const r = await apiCall('/api/admin/courses/lessons/' + lessonId + '/update', {
      method: 'POST',
      body: JSON.stringify({
        title: title,
        objectives: document.getElementById('lObjectives').value.trim(),
        day_number: parseInt(document.getElementById('lDay').value) || 1,
        duration_minutes: parseInt(document.getElementById('lDuration').value) || 30,
        gain_amount: parseFloat(document.getElementById('lGain').value) || 50,
        loss_amount: parseFloat(document.getElementById('lLoss').value) || 20,
        video_url: document.getElementById('lVideo').value.trim(),
        pdf_url: document.getElementById('lPdf').value.trim(),
      })
    });
    if (r.ok) { closeModal(); showToast('Leçon mise à jour', 'success'); loadChapters(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function deleteLesson(id) {
    if (!confirm('Supprimer cette leçon et tout son contenu ?')) return;
    await apiCall('/api/admin/courses/lessons/' + id, { method: 'DELETE' });
    showToast('Leçon supprimée', 'info');
    loadChapters();
    loadStats();
  }

  // ===== BLOCS =====
  function openBlockModal(lessonId) {
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Bloc de contenu</div>
      <div class="form-group">
        <label>Type de bloc</label>
        <select id="bType">
          <option value="text">📝 Texte / Paragraphe</option>
          <option value="heading">📰 Titre / Sous-titre</option>
          <option value="video">🎬 Vidéo</option>
          <option value="image">🖼️ Image</option>
          <option value="code">💻 Code</option>
          <option value="quote">❝ Citation</option>
          <option value="tip">💡 Astuce</option>
        </select>
      </div>
      <div class="form-group">
        <label>Contenu (texte / URL)</label>
        <textarea id="bContent" placeholder="Écris ici..." style="min-height:120px;"></textarea>
      </div>
      <div class="form-group">
        <label>URL média (si vidéo/image)</label>
        <input type="url" id="bMedia" placeholder="https://...">
      </div>
      <div class="form-group">
        <label>Ordre</label>
        <input type="number" id="bOrder" value="0" min="0">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveBlock('${lessonId}')">Ajouter</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function saveBlock(lessonId) {
    const content = document.getElementById('bContent').value.trim();
    if (!content && !document.getElementById('bMedia').value.trim()) {
      showToast('Contenu obligatoire', 'error'); return;
    }
    const r = await apiCall('/api/admin/courses/lessons/' + lessonId + '/blocks/create', {
      method: 'POST',
      body: JSON.stringify({
        block_type: document.getElementById('bType').value,
        content: content,
        media_url: document.getElementById('bMedia').value.trim(),
        sort_order: parseInt(document.getElementById('bOrder').value) || 0,
      })
    });
    if (r.ok) { closeModal(); showToast('Bloc ajouté', 'success'); loadChapters(); loadStats(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function deleteBlock(id) {
    if (!confirm('Supprimer ce bloc ?')) return;
    await apiCall('/api/admin/courses/blocks/' + id, { method: 'DELETE' });
    showToast('Bloc supprimé', 'info');
    loadChapters();
  }

  // ===== EXERCICES =====
  function openExerciseModal(lessonId) {
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Exercice final</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="exTitle" placeholder="Ex: Exercice pratique">
      </div>
      <div class="form-group">
        <label>Instructions</label>
        <textarea id="exInstructions" placeholder="Ce que l'apprenant doit faire..."></textarea>
      </div>
      <div class="form-group">
        <label>Type</label>
        <select id="exType">
          <option value="text">Réponse courte</option>
          <option value="code">Code</option>
          <option value="choice">Choix multiple</option>
        </select>
      </div>
      <div class="form-group">
        <label>Réponse attendue *</label>
        <textarea id="exAnswer" placeholder="Réponse correcte" style="min-height:60px;"></textarea>
      </div>
      <div class="form-group">
        <label>Points</label>
        <input type="number" id="exPoints" value="100" min="10">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveExercise('${lessonId}')">Ajouter</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function saveExercise(lessonId) {
    const title = document.getElementById('exTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }
    const r = await apiCall('/api/admin/courses/lessons/' + lessonId + '/exercises/create', {
      method: 'POST',
      body: JSON.stringify({
        title: title,
        instructions: document.getElementById('exInstructions').value.trim(),
        exercise_type: document.getElementById('exType').value,
        correct_answer: document.getElementById('exAnswer').value.trim(),
        points: parseInt(document.getElementById('exPoints').value) || 100,
      })
    });
    if (r.ok) { closeModal(); showToast('Exercice ajouté', 'success'); loadChapters(); loadStats(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function deleteExercise(id) {
    if (!confirm('Supprimer cet exercice ?')) return;
    await apiCall('/api/admin/courses/exercises/' + id, { method: 'DELETE' });
    showToast('Exercice supprimé', 'info');
    loadChapters();
  }

  // ===== QCM =====
  function openQuestionModal(lessonId) {
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Question QCM</div>
      <div class="form-group">
        <label>Question *</label>
        <textarea id="qText" placeholder="Pose ta question..."></textarea>
      </div>
      <div class="form-group">
        <label>Option A *</label>
        <input type="text" id="qOptA">
      </div>
      <div class="form-group">
        <label>Option B *</label>
        <input type="text" id="qOptB">
      </div>
      <div class="form-group">
        <label>Option C</label>
        <input type="text" id="qOptC">
      </div>
      <div class="form-group">
        <label>Option D</label>
        <input type="text" id="qOptD">
      </div>
      <div class="form-group">
        <label>Réponse correcte *</label>
        <select id="qCorrect">
          <option value="0">Option A</option>
          <option value="1">Option B</option>
          <option value="2">Option C</option>
          <option value="3">Option D</option>
        </select>
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveQuestion('${lessonId}')">Ajouter</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function saveQuestion(lessonId) {
    const q = document.getElementById('qText').value.trim();
    if (!q) { showToast('Question obligatoire', 'error'); return; }
    const options = [
      document.getElementById('qOptA').value.trim(),
      document.getElementById('qOptB').value.trim(),
      document.getElementById('qOptC').value.trim(),
      document.getElementById('qOptD').value.trim(),
    ].filter(o => o);
    if (options.length < 2) { showToast('Au moins 2 options', 'error'); return; }

    const r = await apiCall('/api/admin/courses/lessons/' + lessonId + '/questions/create', {
      method: 'POST',
      body: JSON.stringify({
        question: q,
        options: options,
        correct_index: parseInt(document.getElementById('qCorrect').value) || 0,
      })
    });
    if (r.ok) { closeModal(); showToast('Question ajoutée', 'success'); loadChapters(); loadStats(); }
    else showToast(r.data.detail || 'Erreur', 'error');
  }

  async function deleteQuestion(id) {
    if (!confirm('Supprimer cette question ?')) return;
    await apiCall('/api/admin/courses/questions/' + id, { method: 'DELETE' });
    showToast('Question supprimée', 'info');
    loadChapters();
  }

  // ===== PROGRESSION =====
  async function loadProgress() {
    const list = document.getElementById('progressList');
    list.innerHTML = '<div class="empty">Chargement...</div>';

    const pathId = document.getElementById('progressPathSelect').value;
    let url = '/api/admin/courses/progress';
    if (pathId) url += '?path_id=' + pathId;

    const r = await apiCall(url);
    if (!r.ok) { list.innerHTML = '<div class="empty">Erreur</div>'; return; }
    const data = r.data.data || [];

    if (data.length === 0) {
      list.innerHTML = '<div class="empty">Aucun utilisateur inscrit à un parcours</div>';
      return;
    }

    list.innerHTML = data.map(item => {
      const user = item.user || {};
      const path = item.path || {};
      const initial = (user.full_name || 'U').charAt(0).toUpperCase();
      const unlock = item.unlock || {};

      return '<div class="progress-card">' +
        '<div class="progress-user">' +
        '<div class="progress-avatar">' + initial + '</div>' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="progress-name">' + escapeHtml(user.full_name || 'Anonyme') + '</div>' +
        '<div class="progress-meta">' + escapeHtml(path.icon || '📚') + ' ' + escapeHtml(path.title || '') + ' · ' + escapeHtml(user.phone || '') + '</div>' +
        '<div class="progress-meta">💸 Payé : ' + fmt(unlock.amount_paid) + ' F · Inscrit le ' + formatDate(unlock.started_at) + '</div>' +
        '</div>' +
        '</div>' +
        '<div class="progress-stats">' +
        '<div class="progress-stat"><div class="v">' + (item.lessons_completed || 0) + '</div><div class="l">Leçons</div></div>' +
        '<div class="progress-stat up"><div class="v">+' + fmt(unlock.total_gained) + ' F</div><div class="l">Gagné</div></div>' +
        '<div class="progress-stat down"><div class="v">-' + fmt(unlock.total_lost) + ' F</div><div class="l">Perdu</div></div>' +
        '</div>' +
        (unlock.is_completed ? '<div style="margin-top:8px;background:#e8f5e9;color:#2e7d32;padding:6px 10px;border-radius:8px;font-size:11px;font-weight:800;text-align:center;">✓ Parcours terminé</div>' : '') +
        '</div>';
    }).join('');
  }

  function formatDate(iso) {
    if (!iso) return '';
    try {
      const d = new Date(iso);
      return d.toLocaleDateString('fr-FR') + ' ' + d.toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'});
    } catch (e) { return ''; }
  }

  // ===== API KEYS =====
  async function loadApiKeys() {
    const list = document.getElementById('apiKeysList');
    list.innerHTML = '<div class="empty">Chargement...</div>';

    const r = await apiCall('/api/admin/courses/api-keys');
    if (!r.ok) { list.innerHTML = '<div class="empty">Erreur</div>'; return; }
    const keys = r.data.keys || [];

    if (keys.length === 0) {
      list.innerHTML = '<div class="empty">Aucune clé API</div>';
      return;
    }

    list.innerHTML = keys.map(k => {
      return '<div class="api-key-item">' +
        '<div class="api-key-head">' +
        '<div style="flex:1;min-width:0;">' +
        '<div class="api-key-name">' + escapeHtml(k.name) + '</div>' +
        '<div class="api-key-meta">' + escapeHtml(k.owner_email || 'Aucun email') + '</div>' +
        '</div>' +
        '<span class="type-badge ' + (k.is_active ? 'type-tip' : 'type-video') + '">' + (k.is_active ? 'ACTIF' : 'INACTIF') + '</span>' +
        '</div>' +
        '<div class="api-key-value">' + escapeHtml(k.api_key) + '</div>' +
        '<div class="api-key-meta">📊 ' + (k.calls_today || 0) + ' / ' + (k.rate_limit_per_day || 1000) + ' appels aujourd\\'hui</div>' +
        '<div style="display:flex;gap:6px;margin-top:10px;">' +
        '<button class="btn-add small" style="background:#1976d2;" onclick="copyApiKey(\\'' + k.api_key + '\\')">📋 Copier</button>' +
        '<button class="btn-add small" style="background:' + (k.is_active ? '#f57c00' : '#2e7d32') + ';" onclick="toggleApiKey(\\'' + k.id + '\\')">' + (k.is_active ? '⏸ Désactiver' : '▶ Activer') + '</button>' +
        '<button class="btn-add small" style="background:#d32f2f;" onclick="deleteApiKey(\\'' + k.id + '\\')">🗑</button>' +
        '</div>' +
        '</div>';
    }).join('');
  }

  function openApiKeyModal() {
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">🔑 Nouvelle clé API</div>
      <div class="form-group">
        <label>Nom de la plateforme *</label>
        <input type="text" id="keyName" placeholder="Ex: MaSuperPlateforme">
      </div>
      <div class="form-group">
        <label>Email du propriétaire</label>
        <input type="email" id="keyEmail" placeholder="contact@exemple.com">
      </div>
      <div class="form-group">
        <label>Limite d'appels/jour</label>
        <input type="number" id="keyLimit" value="1000" min="100">
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveApiKey()">Créer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
  }

  async function saveApiKey() {
    const name = document.getElementById('keyName').value.trim();
    if (!name) { showToast('Nom obligatoire', 'error'); return; }
    const r = await apiCall('/api/admin/courses/api-keys/create', {
      method: 'POST',
      body: JSON.stringify({
        name: name,
        owner_email: document.getElementById('keyEmail').value.trim(),
        rate_limit_per_day: parseInt(document.getElementById('keyLimit').value) || 1000,
      })
    });
    if (r.ok) {
      closeModal();
      showToast('Clé API créée !', 'success');
      setTimeout(function() {
        alert('🔑 Ta clé API :\\n\\n' + r.data.api_key + '\\n\\n⚠️ Copie-la maintenant, elle ne sera plus affichée !');
      }, 500);
      loadApiKeys();
    } else showToast(r.data.detail || 'Erreur', 'error');
  }

  function copyApiKey(key) {
    navigator.clipboard.writeText(key).then(function() { showToast('Clé copiée !', 'success'); });
  }

  async function toggleApiKey(id) {
    await apiCall('/api/admin/courses/api-keys/' + id + '/toggle', { method: 'POST' });
    loadApiKeys();
  }

  async function deleteApiKey(id) {
    if (!confirm('Supprimer cette clé API ?')) return;
    await apiCall('/api/admin/courses/api-keys/' + id, { method: 'DELETE' });
    showToast('Clé supprimée', 'info');
    loadApiKeys();
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

      if (tabName === 'progress') loadProgress();
      else if (tabName === 'api-keys') loadApiKeys();
    });
  });

  // ===== INIT =====
  (async function() {
    await loadStats();
    await loadPaths();
  })();
</script>
</body>
</html>
"""
)