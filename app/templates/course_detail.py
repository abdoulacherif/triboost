from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_COURSE_DETAIL = (
    HTML_HEAD.format(title="Parcours — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { display: block !important; background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; margin: 0 auto; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 16px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .hero { margin: 16px; background: linear-gradient(135deg, var(--green), var(--green-dark)); border-radius: 20px; padding: 24px 20px; color: #fff; position: relative; overflow: hidden; box-shadow: 0 8px 24px rgba(46,125,50,0.3); }
  .hero::before { content: ''; position: absolute; top: -50px; right: -50px; width: 180px; height: 180px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .hero::after { content: ''; position: absolute; bottom: -40px; left: -40px; width: 120px; height: 120px; background: rgba(251,192,45,0.2); border-radius: 50%; }
  .hero-icon { font-size: 48px; margin-bottom: 8px; position: relative; z-index: 2; animation: float 3s ease-in-out infinite; }
  @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
  .hero-title { font-size: 22px; font-weight: 900; margin-bottom: 6px; position: relative; z-index: 2; }
  .hero-desc { font-size: 13px; opacity: 0.9; line-height: 1.5; position: relative; z-index: 2; }

  .stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 0 16px 16px; }
  .stat-box { background: #fff; border-radius: 14px; padding: 12px 8px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
  .stat-box .v { font-size: 18px; font-weight: 900; color: var(--text-dark); line-height: 1; }
  .stat-box .l { font-size: 10px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; font-weight: 600; }

  .progress-card { margin: 0 16px 16px; background: #fff; border-radius: 16px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .progress-label { display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; color: var(--text-dark); margin-bottom: 10px; }
  .progress-bar-bg { background: #f0f0f0; height: 10px; border-radius: 5px; overflow: hidden; }
  .progress-fill { height: 100%; background: linear-gradient(90deg, var(--green), var(--gold)); border-radius: 5px; transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
  .rewards-row { display: flex; gap: 8px; margin-top: 12px; }
  .reward-chip { flex: 1; background: #e8f5e9; border-radius: 10px; padding: 8px; text-align: center; }
  .reward-chip.red { background: #ffebee; }
  .reward-chip .v { font-size: 14px; font-weight: 900; color: var(--green); }
  .reward-chip.red .v { color: #d32f2f; }
  .reward-chip .l { font-size: 9px; color: var(--text-muted); margin-top: 2px; text-transform: uppercase; }

  .unlock-card { margin: 0 16px 16px; background: linear-gradient(135deg, #fff8e1, #fffde7); border: 2px solid var(--gold); border-radius: 20px; padding: 24px 20px; text-align: center; box-shadow: 0 8px 20px rgba(251,192,45,0.25); }
  .unlock-price { font-size: 36px; font-weight: 900; color: #e65100; line-height: 1; margin: 12px 0 4px; }
  .unlock-price span { font-size: 16px; }
  .unlock-sub { font-size: 12px; color: #6d4c00; margin-bottom: 20px; }
  .btn-unlock { width: 100%; background: linear-gradient(135deg, var(--gold), #f57c00); color: #212121; border: none; padding: 16px; border-radius: 14px; font-weight: 900; font-size: 15px; font-family: inherit; cursor: pointer; box-shadow: 0 6px 20px rgba(245,124,0,0.3); transition: transform 0.15s; }
  .btn-unlock:active { transform: scale(0.97); }
  .btn-unlock:disabled { opacity: 0.6; cursor: not-allowed; }

  .chapter { margin: 0 16px 12px; background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); animation: slideIn 0.3s ease-out backwards; }
  @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  .chapter-header { padding: 16px; display: flex; align-items: center; gap: 12px; cursor: pointer; user-select: none; }
  .chapter-num { width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; flex-shrink: 0; }
  .chapter-info { flex: 1; min-width: 0; }
  .chapter-title { font-size: 15px; font-weight: 800; color: var(--text-dark); }
  .chapter-meta { font-size: 11px; color: var(--text-muted); margin-top: 3px; }
  .chapter-arrow { color: var(--text-muted); transition: transform 0.3s; font-size: 20px; }
  .chapter.open .chapter-arrow { transform: rotate(180deg); }
  .chapter-lessons { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
  .chapter.open .chapter-lessons { max-height: 2000px; }

  .lesson-item { padding: 14px 16px; border-top: 1px solid #f5f5f5; display: flex; align-items: center; gap: 12px; transition: background 0.2s; }
  .lesson-item:active { background: #f9f9f9; }
  .lesson-status { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 16px; font-weight: 900; }
  .lesson-status.done { background: var(--green); color: #fff; }
  .lesson-status.today { background: var(--gold); color: #212121; animation: pulse-gold 1.5s infinite; }
  .lesson-status.locked { background: #f5f5f5; color: #9e9e9e; }
  @keyframes pulse-gold { 0%,100% { box-shadow: 0 0 0 0 rgba(251,192,45,0.5); } 50% { box-shadow: 0 0 0 8px rgba(251,192,45,0); } }
  .lesson-info { flex: 1; min-width: 0; }
  .lesson-title { font-size: 13px; font-weight: 700; color: var(--text-dark); }
  .lesson-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
  .lesson-btn { background: var(--green); color: #fff; border: none; padding: 8px 12px; border-radius: 10px; font-size: 11px; font-weight: 800; font-family: inherit; cursor: pointer; white-space: nowrap; }
  .lesson-btn:disabled { background: #f5f5f5; color: #9e9e9e; cursor: not-allowed; }

  #quizOverlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); z-index: 99999; align-items: center; justify-content: center; padding: 16px; }
  #quizOverlay.open { display: flex; }
  .quiz-box { background: #fff; border-radius: 24px; width: 100%; max-width: 480px; max-height: 92vh; overflow-y: auto; padding: 24px; box-sizing: border-box; animation: popIn 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
  @keyframes popIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  .quiz-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
  .quiz-title { font-size: 16px; font-weight: 900; color: var(--text-dark); }
  .quiz-close { width: 32px; height: 32px; border-radius: 50%; background: #f5f5f5; border: none; cursor: pointer; font-size: 16px; color: #757575; font-family: inherit; }
  .quiz-content { background: #f9f9f9; border-radius: 12px; padding: 14px; font-size: 13px; line-height: 1.6; color: var(--text-dark); margin-bottom: 16px; }
  .q-item { background: #fff; border: 1.5px solid #e0e0e0; border-radius: 14px; padding: 16px; margin-bottom: 12px; }
  .q-text { font-size: 14px; font-weight: 700; color: var(--text-dark); margin-bottom: 12px; line-height: 1.5; }
  .q-opt { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border: 1.5px solid #e0e0e0; border-radius: 10px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; font-size: 13px; color: var(--text-dark); }
  .q-opt.selected { border-color: var(--green); background: var(--green-light); font-weight: 700; }
  .q-opt .circle { width: 22px; height: 22px; border-radius: 50%; border: 2px solid #e0e0e0; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
  .q-opt.selected .circle { border-color: var(--green); background: var(--green); }
  .q-opt.selected .circle::after { content: '✓'; color: #fff; font-size: 12px; font-weight: 900; }
  .quiz-submit { width: 100%; background: var(--green); color: #fff; border: none; padding: 16px; border-radius: 14px; font-weight: 900; font-size: 15px; font-family: inherit; cursor: pointer; margin-top: 8px; }
  .quiz-submit:disabled { opacity: 0.6; cursor: not-allowed; }
  .result-box { text-align: center; padding: 20px 0; }
  .result-icon { font-size: 64px; margin-bottom: 12px; }
  .result-title { font-size: 22px; font-weight: 900; margin-bottom: 8px; }
  .result-title.win { color: var(--green); }
  .result-title.lose { color: #d32f2f; }
  .result-stats { display: flex; gap: 8px; margin: 16px 0; }
  .result-stat { flex: 1; background: #f9f9f9; border-radius: 12px; padding: 12px; text-align: center; }
  .result-stat .v { font-size: 20px; font-weight: 900; }
  .result-stat .l { font-size: 10px; color: var(--text-muted); margin-top: 2px; text-transform: uppercase; }
  .result-net { font-size: 28px; font-weight: 900; margin: 16px 0; }
  .result-net.up { color: var(--green); }
  .result-net.down { color: #d32f2f; }
  .result-bonus { background: linear-gradient(135deg, #fff8e1, #fffde7); border: 2px solid var(--gold); border-radius: 14px; padding: 14px; margin: 16px 0; font-size: 13px; color: #6d4c00; font-weight: 700; }

  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 60px; margin-bottom: 12px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }

  .toast-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; display: flex; flex-direction: column; gap: 10px; width: 340px; max-width: 90vw; }
  .toast { padding: 16px 20px; border-radius: 16px; color: #fff; font-size: 14px; font-weight: 700; box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: toastIn 0.3s ease; }
  .toast.success { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .toast.error { background: linear-gradient(135deg, #d32f2f, #b71c1c); }
  .toast.warning { background: linear-gradient(135deg, #f57c00, #e65100); }
  @keyframes toastIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

  /* BLOQUÉ */
  .locked-screen { padding: 60px 24px; text-align: center; min-height: 70vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
  .locked-icon { width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #fff3e0, #ffe0b2); color: #e65100; display: flex; align-items: center; justify-content: center; font-size: 60px; margin-bottom: 24px; animation: pulse-lock 2s infinite; }
  @keyframes pulse-lock { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
  .locked-title { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 12px; }
  .locked-text { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin-bottom: 32px; max-width: 320px; }
  .locked-btn { background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; padding: 16px 32px; border-radius: 14px; text-decoration: none; font-weight: 900; font-size: 15px; box-shadow: 0 6px 20px rgba(46,125,50,0.3); display: inline-flex; align-items: center; gap: 8px; }

  @media (min-width: 768px) {
    body { background: linear-gradient(135deg, #f0f4f0, #e8f5e9); padding: 20px 0; }
    .app { max-width: 900px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); overflow: hidden; }
    .hero { padding: 40px 32px; }
    .hero-title { font-size: 32px; }
  }
</style>
</head>
<body>

<div class="toast-container" id="toastContainer"></div>

<div class="app" id="app">
  <header class="topbar">
    <div class="back-btn" onclick="history.back()">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </div>
    <div class="page-title">Parcours</div>
    <div class="spacer"></div>
  </header>

  <div id="loading" style="text-align:center;padding:80px 20px;color:#757575;">Chargement...</div>

  <div id="content" style="display:none;"></div>
</div>

<div id="quizOverlay">
  <div class="quiz-box" id="quizBox"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  const pathParts = window.location.pathname.split('/');
  const pathId = pathParts[pathParts.length - 1];

  let currentPath = null;
  let currentLesson = null;
  let currentAnswers = {};
  let isActivated = false;

  function headers() { return { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }; }
  function fmt(n) { return Number(n || 0).toLocaleString('fr-FR'); }
  function escapeHtml(s) { return s ? String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : ''; }

  function showToast(msg, type) {
    type = type || 'success';
    const container = document.getElementById('toastContainer');
    const t = document.createElement('div');
    t.className = 'toast ' + type;
    t.textContent = msg;
    container.appendChild(t);
    if (navigator.vibrate) navigator.vibrate(type === 'error' ? [30, 50, 30] : 20);
    setTimeout(function() { t.remove(); }, 3000);
  }

  // ===== PROFIL =====
  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), {
        headers: headers()
      });
      if (!res.ok) return;
      const data = await res.json();
      const raw = data.profile?.is_activated;
      isActivated = (raw === true || raw === "true" || raw === 1 || raw === "1");
    } catch (e) {}
  }

  // ===== BLOCAGE SI NON ACTIVÉ =====
  function renderLocked() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = `
      <div class="locked-screen">
        <div class="locked-icon">🔒</div>
        <div class="locked-title">Compte non activé</div>
        <div class="locked-text">
          Pour accéder aux parcours et gagner de l'argent, vous devez d'abord activer votre compte pour <strong>3 600 FCFA</strong>.
        </div>
        <a href="/activation" class="locked-btn">
          🔓 Activer mon compte
        </a>
      </div>
    `;
  }

  // ===== CHARGER LE PARCOURS =====
  async function loadPath() {
    try {
      const res = await fetch('/api/courses/paths/' + pathId, { headers: headers() });
      if (!res.ok) throw new Error('Parcours introuvable');
      const data = await res.json();
      currentPath = data.path;
      render();
    } catch (e) {
      document.getElementById('loading').innerHTML = '<div class="empty-state"><div class="icon">❌</div><h3>Parcours introuvable</h3></div>';
    }
  }

  // ===== RENDER =====
  function render() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('content').style.display = 'block';

    const p = currentPath;

    const totalLessons = (p.chapters || []).reduce((sum, c) => sum + (c.lessons || []).length, 0);

    let progressHTML = '';
    if (p.is_unlocked) {
      const completed = (p.completed_lesson_ids || []).length;
      const pct = totalLessons > 0 ? Math.round((completed / totalLessons) * 100) : 0;
      progressHTML = `
        <div class="progress-card">
          <div class="progress-label">
            <span>Progression</span>
            <span>${completed} / ${totalLessons}</span>
          </div>
          <div class="progress-bar-bg"><div class="progress-fill" style="width: ${pct}%"></div></div>
          <div class="rewards-row">
            <div class="reward-chip">
              <div class="v">+${fmt(p.total_gained)} F</div>
              <div class="l">Gagné</div>
            </div>
            <div class="reward-chip red">
              <div class="v">-${fmt(p.total_lost)} F</div>
              <div class="l">Perdu</div>
            </div>
          </div>
        </div>
      `;
    }

    let unlockHTML = '';
    if (!p.is_unlocked) {
      unlockHTML = `
        <div class="unlock-card">
          <div style="font-size: 40px;">🔒</div>
          <div style="font-size: 13px; color: #6d4c00; font-weight: 700; margin-top: 8px;">Débloquez ce parcours pour</div>
          <div class="unlock-price">${fmt(p.unlock_price || 5000)} <span>FCFA</span></div>
          <div class="unlock-sub">${totalLessons} leçons · ${fmt(p.final_bonus || 500)} F de bonus final</div>
          <button class="btn-unlock" id="unlockBtn" onclick="unlockPath()">Débloquer maintenant</button>
        </div>
      `;
    }

    let chaptersHTML = '';
    if (p.chapters && p.chapters.length > 0) {
      chaptersHTML = p.chapters.map((ch, idx) => {
        const lessons = ch.lessons || [];
        const completed = lessons.filter(l => (p.completed_lesson_ids || []).indexOf(l.id) !== -1).length;

        const lessonsHTML = lessons.map(l => renderLesson(l, p)).join('');

        return `
          <div class="chapter" id="chapter-${ch.id}">
            <div class="chapter-header" onclick="toggleChapter('${ch.id}')">
              <div class="chapter-num">${idx + 1}</div>
              <div class="chapter-info">
                <div class="chapter-title">${escapeHtml(ch.title)}</div>
                <div class="chapter-meta">${completed} / ${lessons.length} leçons</div>
              </div>
              <div class="chapter-arrow">▾</div>
            </div>
            <div class="chapter-lessons">${lessonsHTML}</div>
          </div>
        `;
      }).join('');
    } else {
      chaptersHTML = '<div class="empty-state"><div class="icon">📚</div><h3>Aucune leçon</h3><p>Le parcours sera bientôt disponible.</p></div>';
    }

    document.getElementById('content').innerHTML = `
      <div class="hero">
        <div class="hero-icon">${p.icon || '📚'}</div>
        <div class="hero-title">${escapeHtml(p.title || '')}</div>
        <div class="hero-desc">${escapeHtml(p.description || '')}</div>
      </div>

      <div class="stats-row">
        <div class="stat-box"><div class="v">${(p.chapters || []).length}</div><div class="l">Chapitres</div></div>
        <div class="stat-box"><div class="v">${totalLessons}</div><div class="l">Leçons</div></div>
        <div class="stat-box"><div class="v">${fmt(p.final_bonus || 500)} F</div><div class="l">Bonus</div></div>
      </div>

      ${progressHTML}
      ${unlockHTML}
      ${chaptersHTML}

      <div style="height: 40px;"></div>
    `;
  }

  function renderLesson(l, p) {
    const isDone = (p.completed_lesson_ids || []).indexOf(l.id) !== -1;
    const lastDay = p.last_day || 0;
    const isToday = p.is_unlocked && !isDone && l.day_number === lastDay + 1;

    let statusClass = 'locked';
    let statusIcon = '🔒';
    let btnHTML = '<button class="lesson-btn" disabled>Bloqué</button>';

    if (isDone) {
      statusClass = 'done';
      statusIcon = '✓';
      btnHTML = '<button class="lesson-btn" disabled>Terminé</button>';
    } else if (isToday) {
      statusClass = 'today';
      statusIcon = '▶';
      btnHTML = `<button class="lesson-btn" onclick="startLesson('${l.id}')">Commencer</button>`;
    } else if (!p.is_unlocked) {
      btnHTML = '<button class="lesson-btn" disabled>Débloquer</button>';
    }

    return `
      <div class="lesson-item">
        <div class="lesson-status ${statusClass}">${statusIcon}</div>
        <div class="lesson-info">
          <div class="lesson-title">${escapeHtml(l.title)}</div>
          <div class="lesson-meta">Jour ${l.day_number} · +${fmt(l.gain_amount)} F / -${fmt(l.loss_amount)} F</div>
        </div>
        ${btnHTML}
      </div>
    `;
  }

  function toggleChapter(id) {
    const el = document.getElementById('chapter-' + id);
    if (el) el.classList.toggle('open');
    if (navigator.vibrate) navigator.vibrate(5);
  }

  // ===== DÉBLOQUER =====
  async function unlockPath() {
    if (!isActivated) {
      showToast('Compte non activé', 'error');
      setTimeout(() => location.href = '/activation', 1000);
      return;
    }

    if (!confirm('Débloquer ce parcours pour ' + fmt(currentPath.unlock_price) + ' F ?')) return;

    const btn = document.getElementById('unlockBtn');
    btn.disabled = true;
    btn.textContent = 'Déblocage...';

    try {
      const res = await fetch('/api/courses/paths/' + pathId + '/unlock', {
        method: 'POST', headers: headers()
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      if (navigator.vibrate) navigator.vibrate([30, 50, 30]);
      showToast('Parcours débloqué ! 🎉', 'success');
      setTimeout(loadPath, 800);
    } catch (e) {
      showToast(e.message, 'error');
      btn.disabled = false;
      btn.textContent = 'Débloquer maintenant';
    }
  }

  // ===== DÉMARRER LEÇON =====
  async function startLesson(lessonId) {
    if (!isActivated) {
      showToast('Compte non activé', 'error');
      return;
    }

    try {
      const res = await fetch('/api/courses/lessons/' + lessonId + '/questions', { headers: headers() });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      currentLesson = data.lesson;
      currentAnswers = {};
      renderQuiz(data.questions || []);
    } catch (e) {
      showToast(e.message, 'error');
    }
  }

  function renderQuiz(questions) {
    const box = document.getElementById('quizBox');
    box.innerHTML = `
      <div class="quiz-head">
        <div class="quiz-title">${escapeHtml(currentLesson.title)}</div>
        <button class="quiz-close" onclick="closeQuiz()">✕</button>
      </div>
      ${currentLesson.content ? '<div class="quiz-content">' + escapeHtml(currentLesson.content) + '</div>' : ''}
      ${currentLesson.content_url ? '<a href="' + currentLesson.content_url + '" target="_blank" style="display:block;padding:14px;background:#e8f5e9;border-radius:12px;text-decoration:none;color:#2e7d32;font-weight:700;font-size:13px;margin-bottom:16px;">📥 Voir le contenu complet</a>' : ''}
      <div style="font-size:12px;color:#757575;margin-bottom:12px;">
        📅 Jour ${currentLesson.day_number} · ✅ Bonne = +${fmt(currentLesson.gain_amount)} F · ❌ Mauvaise = -${fmt(currentLesson.loss_amount)} F
      </div>
      <div id="questionsList">
        ${questions.map((q, i) => renderQuestion(q, i)).join('')}
      </div>
      <button class="quiz-submit" id="quizSubmitBtn" onclick="submitQuiz()">Valider mes réponses</button>
    `;

    document.getElementById('quizOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function renderQuestion(q, index) {
    const opts = q.options || [];
    return `
      <div class="q-item">
        <div class="q-text">${index + 1}. ${escapeHtml(q.question)}</div>
        ${opts.map((opt, i) =>
          `<div class="q-opt" onclick="selectAnswer('${q.id}', ${i}, this)">
            <div class="circle"></div>
            <div>${escapeHtml(opt)}</div>
          </div>`
        ).join('')}
      </div>
    `;
  }

  function selectAnswer(questionId, optionIndex, el) {
    currentAnswers[questionId] = optionIndex;
    el.closest('.q-item').querySelectorAll('.q-opt').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    if (navigator.vibrate) navigator.vibrate(5);
  }

  function closeQuiz() {
    document.getElementById('quizOverlay').classList.remove('open');
    document.body.style.overflow = '';
    currentLesson = null;
    currentAnswers = {};
  }

  async function submitQuiz() {
    const answered = Object.keys(currentAnswers).length;
    const totalQ = document.querySelectorAll('.q-item').length;

    if (answered < totalQ) {
      showToast('Répondez à toutes les questions (' + answered + '/' + totalQ + ')', 'warning');
      return;
    }

    const btn = document.getElementById('quizSubmitBtn');
    btn.disabled = true;
    btn.textContent = 'Envoi...';

    try {
      const res = await fetch('/api/courses/lessons/' + currentLesson.id + '/submit', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ answers: currentAnswers })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      showResult(data.result);
    } catch (e) {
      showToast(e.message, 'error');
      btn.disabled = false;
      btn.textContent = 'Valider mes réponses';
    }
  }

  function showResult(r) {
    const isWin = r.net >= 0;
    let bonusHTML = '';
    if (r.path_completed) {
      bonusHTML = '<div class="result-bonus">🎉 Parcours terminé !<br>Bonus final : +' + fmt(r.bonus) + ' F</div>';
    }

    document.getElementById('quizBox').innerHTML = `
      <div class="result-box">
        <div class="result-icon">${isWin ? '🎉' : '😢'}</div>
        <div class="result-title ${isWin ? 'win' : 'lose'}">${isWin ? 'Bravo !' : 'Dommage...'}</div>
        <div class="result-stats">
          <div class="result-stat"><div class="v" style="color:#2e7d32;">${r.correct}</div><div class="l">Correct</div></div>
          <div class="result-stat"><div class="v" style="color:#d32f2f;">${r.total - r.correct}</div><div class="l">Faux</div></div>
          <div class="result-stat"><div class="v">${r.total}</div><div class="l">Total</div></div>
        </div>
        <div class="result-net ${isWin ? 'up' : 'down'}">
          ${r.net >= 0 ? '+' : ''}${fmt(r.net)} F
        </div>
        ${bonusHTML}
        <button class="quiz-submit" onclick="closeQuizAndReload()">Continuer</button>
      </div>
    `;

    if (navigator.vibrate) navigator.vibrate(isWin ? [30, 50, 30] : [100, 50, 100]);
  }

  function closeQuizAndReload() {
    closeQuiz();
    loadPath();
  }

  // ===== INIT =====
  (async function() {
    await loadProfile();
    if (!isActivated) {
      renderLocked();
    } else {
      loadPath();
    }
  })();
</script>
</body>
</html>
"""
)