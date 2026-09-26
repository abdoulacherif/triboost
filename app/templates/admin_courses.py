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

  .path-select { margin: 16px; background: #fff; border-radius: 14px; padding: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .path-select label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px; display: block; }
  .path-select select { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 15px; font-family: inherit; outline: none; background: #fff; }

  .section-title { margin: 16px 16px 10px; font-size: 14px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; }
  .btn-add { background: var(--green); color: #fff; border: none; padding: 8px 14px; border-radius: 10px; font-size: 12px; font-weight: 800; font-family: inherit; cursor: pointer; }

  .chapter-item { margin: 0 16px 12px; background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .chapter-head { padding: 14px; display: flex; align-items: center; gap: 12px; cursor: pointer; }
  .chapter-num { width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; flex-shrink: 0; }
  .chapter-info { flex: 1; }
  .chapter-title { font-size: 14px; font-weight: 800; }
  .chapter-sub { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
  .btn-del { background: #ffebee; color: #d32f2f; border: none; padding: 6px 10px; border-radius: 8px; font-size: 11px; font-weight: 800; cursor: pointer; font-family: inherit; }

  .lessons-list { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
  .chapter-item.open .lessons-list { max-height: 3000px; }

  .lesson-item { padding: 12px 14px; border-top: 1px solid #f5f5f5; display: flex; align-items: center; gap: 10px; }
  .lesson-num { width: 28px; height: 28px; border-radius: 8px; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 12px; flex-shrink: 0; }
  .lesson-info { flex: 1; min-width: 0; }
  .lesson-title { font-size: 13px; font-weight: 700; }
  .lesson-sub { font-size: 10px; color: var(--text-muted); margin-top: 2px; }

  .questions-list { padding: 8px 14px 14px; background: #fafafa; }
  .q-item { padding: 10px 12px; background: #fff; border-radius: 10px; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; font-size: 12px; }
  .q-text { flex: 1; }

  .empty { text-align: center; padding: 40px 20px; color: var(--text-muted); font-size: 13px; }

  /* MODAL */
  #modalOverlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 99999; align-items: flex-end; justify-content: center; }
  #modalOverlay.open { display: flex; }
  #modalOverlay .content { background: #fff; border-radius: 24px 24px 0 0; padding: 20px 20px 40px; width: 100%; max-width: 480px; max-height: 92vh; overflow-y: auto; box-sizing: border-box; animation: slideUp 0.3s ease; }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .modal-handle { width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; margin: 0 auto 16px; }
  .modal-title { font-size: 18px; font-weight: 800; margin-bottom: 16px; }
  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; }
  .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; outline: none; box-sizing: border-box; }
  .form-group textarea { min-height: 70px; resize: vertical; }
  .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .modal-actions { display: flex; gap: 8px; margin-top: 16px; }
  .modal-btn { flex: 1; padding: 14px; border-radius: 12px; border: none; font-weight: 800; font-size: 14px; font-family: inherit; cursor: pointer; }
  .modal-btn.cancel { background: #f5f5f5; color: var(--text-dark); }
  .modal-btn.confirm { background: var(--green); color: #fff; }

  .toast-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; display: flex; flex-direction: column; gap: 10px; width: 340px; max-width: 90vw; }
  .toast { padding: 16px 20px; border-radius: 16px; color: #fff; font-size: 14px; font-weight: 700; box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: toastIn 0.3s ease; }
  .toast.success { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .toast.error { background: linear-gradient(135deg, #d32f2f, #b71c1c); }
  @keyframes toastIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

  @media (min-width: 768px) {
    .app { max-width: 900px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); overflow: hidden; background: #f5f5f5; }
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

  <div class="path-select">
    <label>Parcours à modifier</label>
    <select id="pathSelect" onchange="loadChapters()">
      <option value="">-- Choisir un parcours --</option>
    </select>
  </div>

  <div class="section-title">
    <span>📚 Chapitres</span>
    <button class="btn-add" onclick="openChapterModal()">+ Chapitre</button>
  </div>

  <div id="chaptersContainer"><div class="empty">Sélectionne un parcours</div></div>

  <div style="height: 40px;"></div>
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

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }

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
  }

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

  async function loadPaths() {
    const sel = document.getElementById('pathSelect');
    const r = await apiCall('/api/courses/paths');
    allPaths = (r.data.paths || []);

    sel.innerHTML = '<option value="">-- Choisir un parcours --</option>' +
      allPaths.map(p => '<option value="' + p.id + '">' + (p.icon || '📚') + ' ' + escapeHtml(p.title) + '</option>').join('');
  }

  async function loadChapters() {
    currentPathId = document.getElementById('pathSelect').value;
    const container = document.getElementById('chaptersContainer');

    if (!currentPathId) {
      container.innerHTML = '<div class="empty">Sélectionne un parcours</div>';
      return;
    }

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
      '<div class="chapter-sub">' + lessons.length + ' leçon(s)</div>' +
      '</div>' +
      '<button class="btn-del" onclick="event.stopPropagation(); deleteChapter(\\'' + ch.id + '\\')">🗑</button>' +
      '</div>' +
      '<div class="lessons-list">' +
      '<div style="padding: 8px 14px;">' +
      '<button class="btn-add" style="width:100%;" onclick="openLessonModal(\\'' + ch.id + '\\')">+ Ajouter une leçon</button>' +
      '</div>' +
      lessons.map((l, i) => renderLesson(l, i, ch.id)).join('') +
      '</div></div>';
  }

  function renderLesson(l, idx, chapterId) {
    const questions = l.questions || [];
    return '<div class="lesson-item">' +
      '<div class="lesson-num">' + l.day_number + '</div>' +
      '<div class="lesson-info">' +
      '<div class="lesson-title">' + escapeHtml(l.title) + '</div>' +
      '<div class="lesson-sub">+' + l.gain_amount + ' F / -' + l.loss_amount + ' F · ' + questions.length + ' question(s)</div>' +
      '</div>' +
      '<button class="btn-del" onclick="openQuestionModal(\\'' + l.id + '\\')" style="background:#e3f2fd;color:#1976d2;">+ Q</button>' +
      '<button class="btn-del" onclick="deleteLesson(\\'' + l.id + '\\')">🗑</button>' +
      '</div>' +
      (questions.length > 0 ?
        '<div class="questions-list">' +
        questions.map((q, i) =>
          '<div class="q-item">' +
          '<div class="q-text">' + (i + 1) + '. ' + escapeHtml(q.question) + '</div>' +
          '<button class="btn-del" onclick="deleteQuestion(\\'' + q.id + '\\')" style="padding: 4px 8px;">✕</button>' +
          '</div>'
        ).join('') +
        '</div>' : '');
  }

  function toggleChapter(id) {
    const el = document.getElementById('ch-' + id);
    if (el) el.classList.toggle('open');
  }

  function openChapterModal() {
    if (!currentPathId) { showToast('Choisis d\\'abord un parcours', 'error'); return; }

    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Nouveau chapitre</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="chTitle" placeholder="Ex: Chapitre 1 - Les bases">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="chDesc" placeholder="Description du chapitre..."></textarea>
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
    document.body.style.overflow = 'hidden';
  }

  async function saveChapter() {
    const title = document.getElementById('chTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }

    const payload = {
      path_id: currentPathId,
      title: title,
      description: document.getElementById('chDesc').value.trim(),
      sort_order: parseInt(document.getElementById('chOrder').value) || 1,
    };

    const r = await apiCall('/api/admin/courses/chapters/create', {
      method: 'POST', body: JSON.stringify(payload)
    });
    if (r.ok) { closeModal(); showToast('Chapitre créé', 'success'); loadChapters(); }
    else { showToast(r.data.detail || 'Erreur', 'error'); }
  }

  async function deleteChapter(id) {
    if (!confirm('Supprimer ce chapitre et toutes ses leçons ?')) return;
    await apiCall('/api/admin/courses/chapters/' + id, { method: 'DELETE' });
    showToast('Chapitre supprimé', 'info');
    loadChapters();
  }

  function openLessonModal(chapterId) {
    const ch = currentChapters.find(c => c.id === chapterId);
    const nextDay = (ch && ch.lessons) ? ch.lessons.length + 1 : 1;

    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Nouvelle leçon</div>
      <div class="form-group">
        <label>Titre *</label>
        <input type="text" id="lTitle" placeholder="Ex: Leçon 1 - Introduction">
      </div>
      <div class="form-group">
        <label>Contenu (texte)</label>
        <textarea id="lContent" placeholder="Contenu de la leçon..."></textarea>
      </div>
      <div class="form-group">
        <label>Lien contenu (vidéo/PDF)</label>
        <input type="url" id="lUrl" placeholder="https://...">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Numéro du jour *</label>
          <input type="number" id="lDay" value="${nextDay}" min="1">
        </div>
        <div class="form-group">
          <label>Ordre</label>
          <input type="number" id="lOrder" value="${nextDay}" min="1">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Gain bonne réponse (F)</label>
          <input type="number" id="lGain" value="50" min="0" step="10">
        </div>
        <div class="form-group">
          <label>Perte mauvaise (F)</label>
          <input type="number" id="lLoss" value="20" min="0" step="10">
        </div>
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveLesson('${chapterId}')">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  async function saveLesson(chapterId) {
    const title = document.getElementById('lTitle').value.trim();
    if (!title) { showToast('Titre obligatoire', 'error'); return; }

    const payload = {
      chapter_id: chapterId,
      title: title,
      content: document.getElementById('lContent').value.trim(),
      content_url: document.getElementById('lUrl').value.trim(),
      day_number: parseInt(document.getElementById('lDay').value) || 1,
      sort_order: parseInt(document.getElementById('lOrder').value) || 1,
      gain_amount: parseFloat(document.getElementById('lGain').value) || 50,
      loss_amount: parseFloat(document.getElementById('lLoss').value) || 20,
    };

    const r = await apiCall('/api/admin/courses/lessons/create', {
      method: 'POST', body: JSON.stringify(payload)
    });
    if (r.ok) { closeModal(); showToast('Leçon créée', 'success'); loadChapters(); }
    else { showToast(r.data.detail || 'Erreur', 'error'); }
  }

  async function deleteLesson(id) {
    if (!confirm('Supprimer cette leçon ?')) return;
    await apiCall('/api/admin/courses/lessons/' + id, { method: 'DELETE' });
    showToast('Leçon supprimée', 'info');
    loadChapters();
  }

  function openQuestionModal(lessonId) {
    document.getElementById('modalContent').innerHTML = `
      <div class="modal-handle"></div>
      <div class="modal-title">➕ Nouvelle question</div>
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
        <label>Option C (optionnel)</label>
        <input type="text" id="qOptC">
      </div>
      <div class="form-group">
        <label>Option D (optionnel)</label>
        <input type="text" id="qOptD">
      </div>
      <div class="form-group">
        <label>Bonne réponse *</label>
        <select id="qCorrect">
          <option value="0">Option A</option>
          <option value="1">Option B</option>
          <option value="2">Option C</option>
          <option value="3">Option D</option>
        </select>
      </div>
      <div class="modal-actions">
        <button class="modal-btn cancel" onclick="closeModal()">Annuler</button>
        <button class="modal-btn confirm" onclick="saveQuestion('${lessonId}')">Enregistrer</button>
      </div>
    `;
    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  async function saveQuestion(lessonId) {
    const question = document.getElementById('qText').value.trim();
    if (!question) { showToast('Question obligatoire', 'error'); return; }

    const options = [
      document.getElementById('qOptA').value.trim(),
      document.getElementById('qOptB').value.trim(),
      document.getElementById('qOptC').value.trim(),
      document.getElementById('qOptD').value.trim(),
    ].filter(o => o);

    if (options.length < 2) { showToast('Au moins 2 options', 'error'); return; }

    const payload = {
      lesson_id: lessonId,
      question: question,
      options: options,
      correct_index: parseInt(document.getElementById('qCorrect').value) || 0,
      sort_order: 1,
    };

    const r = await apiCall('/api/admin/courses/questions/create', {
      method: 'POST', body: JSON.stringify(payload)
    });
    if (r.ok) { closeModal(); showToast('Question créée', 'success'); loadChapters(); }
    else { showToast(r.data.detail || 'Erreur', 'error'); }
  }

  async function deleteQuestion(id) {
    if (!confirm('Supprimer cette question ?')) return;
    await apiCall('/api/admin/courses/questions/' + id, { method: 'DELETE' });
    showToast('Question supprimée', 'info');
    loadChapters();
  }

  loadPaths();
</script>
</body>
</html>
"""
)