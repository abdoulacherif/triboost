from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_LESSON_DETAIL = (
    HTML_HEAD.format(title="Leçon — TriBoost")
    + CSS_COMMUN
    + """
<style>
  body { display: block !important; background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #fff; min-height: 100vh; margin: 0 auto; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; border-bottom: 1px solid #f0f0f0; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 14px; font-weight: 700; color: var(--text-muted); flex: 1; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; }
  .spacer { width: 40px; }

  /* TIMER STICKY */
  .timer-bar { position: sticky; top: 73px; z-index: 49; background: linear-gradient(135deg, #1a1a1a, #333); color: #fff; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; }
  .timer-display { font-size: 18px; font-weight: 900; font-family: 'Courier New', monospace; }
  .timer-label { font-size: 11px; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.5px; }
  .timer-progress { flex: 1; margin: 0 16px; height: 6px; background: rgba(255,255,255,0.2); border-radius: 3px; overflow: hidden; }
  .timer-fill { height: 100%; background: linear-gradient(90deg, #fbc02d, #00ff88); border-radius: 3px; transition: width 1s linear; }
  .timer-icon { font-size: 20px; }

  /* CONTENU */
  .lesson-header { padding: 20px; border-bottom: 1px solid #f0f0f0; }
  .lesson-day { display: inline-block; background: var(--gold); color: #212121; font-size: 10px; font-weight: 900; padding: 4px 10px; border-radius: 8px; letter-spacing: 0.5px; margin-bottom: 10px; text-transform: uppercase; }
  .lesson-title { font-size: 22px; font-weight: 900; color: var(--text-dark); line-height: 1.3; margin-bottom: 12px; }
  .lesson-objectives { background: #e3f2fd; border-left: 3px solid #1976d2; border-radius: 10px; padding: 12px 14px; font-size: 13px; color: #0d47a1; line-height: 1.6; }

  .content-area { padding: 20px; }
  .content-block { margin-bottom: 24px; animation: fadeIn 0.4s ease-out; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  .block-heading { font-size: 20px; font-weight: 900; color: var(--text-dark); margin-bottom: 12px; line-height: 1.3; }
  .block-text { font-size: 15px; line-height: 1.7; color: #424242; margin-bottom: 12px; }
  .block-text p { margin-bottom: 12px; }
  .block-image { width: 100%; border-radius: 14px; margin: 12px 0; }
  .block-video { width: 100%; aspect-ratio: 16 / 9; border-radius: 14px; background: #000; margin: 12px 0; }
  .block-code { background: #1a1a1a; color: #00ff88; font-family: 'Courier New', monospace; font-size: 13px; padding: 16px; border-radius: 12px; overflow-x: auto; line-height: 1.6; margin: 12px 0; white-space: pre-wrap; }
  .block-quote { background: #f3e5f5; border-left: 3px solid #7b1fa2; border-radius: 10px; padding: 14px 16px; font-style: italic; font-size: 14px; color: #4a148c; line-height: 1.6; }
  .block-tip { background: linear-gradient(135deg, #fff8e1, #fffde7); border: 1.5px solid var(--gold); border-radius: 12px; padding: 14px 16px; font-size: 13px; color: #6d4c00; line-height: 1.6; display: flex; gap: 10px; }
  .block-tip .icon { font-size: 20px; flex-shrink: 0; }

  /* EXERCICES */
  .exercises-area { padding: 20px; background: #f9f9f9; border-top: 1px solid #f0f0f0; }
  .ex-head { font-size: 18px; font-weight: 900; color: var(--text-dark); margin-bottom: 6px; }
  .ex-sub { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; line-height: 1.5; }
  .ex-item { background: #fff; border: 1.5px solid #e0e0e0; border-radius: 16px; padding: 18px; margin-bottom: 14px; }
  .ex-title { font-size: 14px; font-weight: 800; color: var(--text-dark); margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
  .ex-num { background: var(--green); color: #fff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 900; }
  .ex-instructions { font-size: 13px; color: #616161; line-height: 1.6; margin-bottom: 12px; }
  .ex-input { width: 100%; padding: 14px; border: 1.5px solid #e0e0e0; border-radius: 12px; font-size: 15px; font-family: inherit; outline: none; box-sizing: border-box; }
  .ex-input:focus { border-color: var(--green); }
  .ex-textarea { width: 100%; padding: 14px; border: 1.5px solid #e0e0e0; border-radius: 12px; font-size: 14px; font-family: monospace; outline: none; min-height: 100px; resize: vertical; box-sizing: border-box; }
  .ex-textarea:focus { border-color: var(--green); }
  .ex-choice { display: flex; flex-direction: column; gap: 8px; }
  .ex-opt { padding: 12px 14px; border: 1.5px solid #e0e0e0; border-radius: 10px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
  .ex-opt.selected { border-color: var(--green); background: var(--green-light); font-weight: 700; }

  /* FOOTER */
  .finish-area { padding: 20px; background: #fff; border-top: 1px solid #f0f0f0; }
  .btn-finish { width: 100%; background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; border: none; padding: 18px; border-radius: 16px; font-weight: 900; font-size: 16px; font-family: inherit; cursor: pointer; box-shadow: 0 6px 20px rgba(46,125,50,0.3); display: flex; align-items: center; justify-content: center; gap: 8px; }
  .btn-finish:disabled { background: #bdbdbd; box-shadow: none; cursor: not-allowed; }
  .finish-note { text-align: center; font-size: 12px; color: var(--text-muted); margin-top: 10px; }
  .finish-note.locked { color: #e65100; font-weight: 700; }

  /* ÉCRAN 24H */
  .wait-screen { padding: 60px 24px; text-align: center; min-height: 60vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
  .wait-icon { width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #e3f2fd, #bbdefb); color: #1976d2; display: flex; align-items: center; justify-content: center; font-size: 60px; margin-bottom: 24px; animation: pulse-wait 2s infinite; }
  @keyframes pulse-wait { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
  .wait-title { font-size: 22px; font-weight: 900; color: var(--text-dark); margin-bottom: 12px; }
  .wait-text { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin-bottom: 24px; max-width: 320px; }
  .wait-countdown { background: linear-gradient(135deg, #1a1a1a, #333); color: #00ff88; font-family: 'Courier New', monospace; font-size: 32px; font-weight: 900; padding: 20px 32px; border-radius: 16px; letter-spacing: 2px; margin-bottom: 24px; }
  .wait-btn { background: linear-gradient(135deg, #2e7d32, #1b5e20); color: #fff; padding: 16px 32px; border-radius: 14px; text-decoration: none; font-weight: 900; font-size: 15px; box-shadow: 0 6px 20px rgba(46,125,50,0.3); display: inline-flex; align-items: center; gap: 8px; }

  /* RESULT MODAL */
  #resultOverlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 99999; align-items: center; justify-content: center; padding: 16px; }
  #resultOverlay.open { display: flex; }
  .result-card { background: #fff; border-radius: 24px; padding: 30px 24px; max-width: 400px; width: 100%; text-align: center; animation: popIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
  @keyframes popIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  .result-emoji { font-size: 72px; margin-bottom: 12px; }
  .result-headline { font-size: 24px; font-weight: 900; margin-bottom: 6px; }
  .result-headline.win { color: var(--green); }
  .result-headline.lose { color: #d32f2f; }
  .result-sub { font-size: 14px; color: var(--text-muted); margin-bottom: 20px; }
  .result-score { background: #f9f9f9; border-radius: 14px; padding: 16px; margin-bottom: 16px; }
  .result-score .v { font-size: 28px; font-weight: 900; color: var(--green); }
  .result-score .l { font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }
  .result-earn { font-size: 20px; font-weight: 900; color: var(--green); margin-bottom: 20px; }
  .result-btn { width: 100%; background: var(--green); color: #fff; border: none; padding: 16px; border-radius: 14px; font-weight: 900; font-size: 15px; font-family: inherit; cursor: pointer; }

  .toast-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; display: flex; flex-direction: column; gap: 10px; width: 340px; max-width: 90vw; }
  .toast { padding: 16px 20px; border-radius: 16px; color: #fff; font-size: 14px; font-weight: 700; box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: toastIn 0.3s ease; }
  .toast.success { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .toast.error { background: linear-gradient(135deg, #d32f2f, #b71c1c); }
  .toast.warning { background: linear-gradient(135deg, #f57c00, #e65100); }
  @keyframes toastIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

  @media (min-width: 768px) {
    body { background: linear-gradient(135deg, #f0f4f0, #e8f5e9); padding: 20px 0; }
    .app { max-width: 900px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); overflow: hidden; }
    .content-area { padding: 40px 60px; }
    .lesson-header { padding: 40px 60px; }
    .exercises-area { padding: 40px 60px; }
    .lesson-title { font-size: 32px; }
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
    <div class="page-title" id="topbarTitle">Leçon</div>
    <div class="spacer"></div>
  </header>

  <div id="loading" style="text-align:center;padding:80px 20px;color:#757575;">Chargement...</div>

  <div id="content" style="display:none;"></div>
</div>

<div id="resultOverlay">
  <div class="result-card" id="resultCard"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');
  if (!token || !userId) window.location.href = '/login';

  const pathParts = window.location.pathname.split('/');
  const lessonId = pathParts[pathParts.length - 1];

  let lesson = null;
  let sessionId = null;
  let timerInterval = null;
  let elapsedSeconds = 0;
  let requiredSeconds = 1800; // 30 min par défaut
  let answers = {};

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

  function formatTime(sec) {
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    const s = sec % 60;
    if (h > 0) return String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
  }

  // ===== CHARGER LA LEÇON =====
  async function loadLesson() {
    try {
      const res = await fetch('/api/lesson/lesson/' + lessonId, { headers: headers() });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Erreur');
      }
      const data = await res.json();
      lesson = data.lesson;

      // Vérifier si terminée
      if (data.is_done) {
        renderAlreadyDone();
        return;
      }

      // Vérifier la règle 24h
      if (!data.can_start && data.remaining_seconds > 0) {
        renderWaitScreen(data.remaining_seconds);
        return;
      }

      requiredSeconds = (lesson.duration_minutes || 30) * 60;

      renderLessonView(data);

      // Démarrer la session
      await startSession();
    } catch (e) {
      document.getElementById('loading').innerHTML = '<div style="text-align:center;padding:60px 20px;color:#d32f2f;font-size:14px;">' + escapeHtml(e.message) + '</div>';
    }
  }

  // ===== ÉCRAN D'ATTENTE 24H =====
  function renderWaitScreen(seconds) {
    document.getElementById('loading').style.display = 'none';
    const c = document.getElementById('content');
    c.style.display = 'block';

    c.innerHTML = `
      <div class="wait-screen">
        <div class="wait-icon">⏰</div>
        <div class="wait-title">Prochaine leçon dans...</div>
        <div class="wait-text">Vous avez déjà fait votre leçon du jour. Revenez demain pour continuer.</div>
        <div class="wait-countdown" id="countdown">${formatTime(seconds)}</div>
        <a href="/formation" class="wait-btn">← Retour aux parcours</a>
      </div>
    `;

    let remaining = seconds;
    setInterval(function() {
      remaining--;
      if (remaining < 0) remaining = 0;
      const el = document.getElementById('countdown');
      if (el) el.textContent = formatTime(remaining);
    }, 1000);
  }

  // ===== DÉJÀ TERMINÉE =====
  function renderAlreadyDone() {
    document.getElementById('loading').style.display = 'none';
    const c = document.getElementById('content');
    c.style.display = 'block';

    c.innerHTML = `
      <div class="wait-screen">
        <div class="wait-icon" style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); color: #2e7d32;">✓</div>
        <div class="wait-title">Leçon déjà terminée</div>
        <div class="wait-text">Bravo ! Vous avez déjà validé cette leçon.</div>
        <a href="/formation" class="wait-btn">← Retour aux parcours</a>
      </div>
    `;
  }

  // ===== RENDER LA VUE LEÇON =====
  function renderLessonView(data) {
    document.getElementById('loading').style.display = 'none';
    const c = document.getElementById('content');
    c.style.display = 'block';

    document.getElementById('topbarTitle').textContent = 'Jour ' + lesson.day_number;

    // Contenu
    let contentHTML = '';
    if (data.blocks && data.blocks.length > 0) {
      contentHTML = data.blocks.map(function(b) {
        const type = b.block_type || 'text';
        if (type === 'heading') {
          return '<div class="content-block"><div class="block-heading">' + escapeHtml(b.content) + '</div></div>';
        } else if (type === 'text') {
          return '<div class="content-block"><div class="block-text">' + escapeHtml(b.content).replace(/\\n/g, '<br>') + '</div></div>';
        } else if (type === 'image') {
          return '<div class="content-block"><img class="block-image" src="' + escapeHtml(b.media_url || b.content) + '" alt=""></div>';
        } else if (type === 'video') {
          return '<div class="content-block"><video class="block-video" controls src="' + escapeHtml(b.media_url || b.content) + '"></video></div>';
        } else if (type === 'code') {
          return '<div class="content-block"><pre class="block-code">' + escapeHtml(b.content) + '</pre></div>';
        } else if (type === 'quote') {
          return '<div class="content-block"><div class="block-quote">"' + escapeHtml(b.content) + '"</div></div>';
        } else if (type === 'tip') {
          return '<div class="content-block"><div class="block-tip"><div class="icon">💡</div><div>' + escapeHtml(b.content) + '</div></div></div>';
        }
        return '<div class="content-block"><div class="block-text">' + escapeHtml(b.content) + '</div></div>';
      }).join('');
    } else if (lesson.content) {
      contentHTML = '<div class="content-block"><div class="block-text">' + escapeHtml(lesson.content).replace(/\\n/g, '<br>') + '</div></div>';
    }

    // Exercices
    let exercisesHTML = '';
    if (data.exercises && data.exercises.length > 0) {
      exercisesHTML = data.exercises.map(function(ex, i) {
        let inputHTML = '';
        if (ex.exercise_type === 'choice') {
          const opts = ex.options || [];
          inputHTML = '<div class="ex-choice" data-ex="' + ex.id + '">' +
            opts.map(function(o, j) {
              return '<div class="ex-opt" onclick="selectExercise(\\'' + ex.id + '\\', \\'' + escapeHtml(o).replace(/'/g, '') + '\\', this)">' + escapeHtml(o) + '</div>';
            }).join('') +
            '</div>';
        } else if (ex.exercise_type === 'code') {
          inputHTML = '<textarea class="ex-textarea" id="ex-' + ex.id + '" placeholder="Écrivez votre code..."></textarea>';
        } else {
          inputHTML = '<input class="ex-input" id="ex-' + ex.id + '" placeholder="Votre réponse...">';
        }

        return '<div class="ex-item">' +
          '<div class="ex-title"><div class="ex-num">' + (i + 1) + '</div>' + escapeHtml(ex.title) + '</div>' +
          (ex.instructions ? '<div class="ex-instructions">' + escapeHtml(ex.instructions) + '</div>' : '') +
          inputHTML +
          '</div>';
      }).join('');
    }

    c.innerHTML = `
      <div class="timer-bar">
        <div class="timer-icon">⏱️</div>
        <div class="timer-display" id="timerDisplay">00:00</div>
        <div class="timer-progress"><div class="timer-fill" id="timerFill" style="width:0%"></div></div>
        <div class="timer-label" id="timerLabel">MIN 30</div>
      </div>

      <div class="lesson-header">
        <div class="lesson-day">Jour ${lesson.day_number} · Leçon</div>
        <h1 class="lesson-title">${escapeHtml(lesson.title)}</h1>
        ${lesson.objectives ? '<div class="lesson-objectives"><strong>🎯 Objectifs :</strong> ' + escapeHtml(lesson.objectives) + '</div>' : ''}
      </div>

      <div class="content-area">
        ${contentHTML}
      </div>

      ${exercisesHTML ? '<div class="exercises-area">' +
        '<div class="ex-head">🎯 Exercice final</div>' +
        '<div class="ex-sub">Répondez aux exercices pour valider la leçon.</div>' +
        exercisesHTML +
        '</div>' : ''}

      <div class="finish-area">
        <button class="btn-finish" id="finishBtn" onclick="finishLesson()" disabled>
          ⏱️ Patientez...
        </button>
        <div class="finish-note locked" id="finishNote">Vous devez passer au moins <strong id="requiredMin">30 minutes</strong> sur cette leçon.</div>
      </div>
    `;
  }

  // ===== SÉLECTIONNER UNE RÉPONSE =====
  function selectExercise(exId, answer, el) {
    answers[exId] = answer;
    el.parentElement.querySelectorAll('.ex-opt').forEach(function(o) { o.classList.remove('selected'); });
    el.classList.add('selected');
    if (navigator.vibrate) navigator.vibrate(5);
  }

  // ===== DÉMARRER LA SESSION =====
  async function startSession() {
    try {
      const res = await fetch('/api/lesson/lesson/' + lessonId + '/start', {
        method: 'POST', headers: headers()
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      sessionId = data.result.session_id;
      startTimer();
    } catch (e) {
      showToast(e.message, 'error');
    }
  }

  // ===== TIMER =====
  function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    elapsedSeconds = 0;

    timerInterval = setInterval(function() {
      elapsedSeconds++;
      const remaining = Math.max(0, requiredSeconds - elapsedSeconds);
      document.getElementById('timerDisplay').textContent = formatTime(elapsedSeconds);

      const pct = Math.min(100, (elapsedSeconds / requiredSeconds) * 100);
      document.getElementById('timerFill').style.width = pct + '%';

      if (elapsedSeconds >= requiredSeconds) {
        document.getElementById('timerLabel').textContent = '✓ OK';
        document.getElementById('finishBtn').disabled = false;
        document.getElementById('finishBtn').innerHTML = '✓ Terminer la leçon';
        document.getElementById('finishNote').classList.remove('locked');
        document.getElementById('finishNote').innerHTML = 'Vous pouvez maintenant valider.';
      } else {
        document.getElementById('timerLabel').textContent = 'RESTE ' + formatTime(remaining);
      }
    }, 1000);
  }

  // ===== TERMINER =====
  async function finishLesson() {
    if (elapsedSeconds < requiredSeconds) {
      showToast('Attendez encore ' + formatTime(requiredSeconds - elapsedSeconds), 'warning');
      return;
    }

    if (!sessionId) {
      showToast('Session introuvable', 'error');
      return;
    }

    const btn = document.getElementById('finishBtn');
    btn.disabled = true;
    btn.textContent = 'Validation...';

    // Récupérer les réponses textuelles
    document.querySelectorAll('.ex-input, .ex-textarea').forEach(function(el) {
      const id = el.id.replace('ex-', '');
      if (el.value.trim()) answers[id] = el.value.trim();
    });

    try {
      const res = await fetch('/api/lesson/lesson/' + lessonId + '/finish', {
        method: 'POST', headers: headers(),
        body: JSON.stringify({ session_id: sessionId, answers: answers })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');
      if (!data.result.success) throw new Error(data.result.message);

      // Arrêter le timer
      if (timerInterval) clearInterval(timerInterval);

      showResult(data);
    } catch (e) {
      showToast(e.message, 'error');
      btn.disabled = false;
      btn.textContent = '✓ Terminer la leçon';
    }
  }

  function showResult(data) {
    const overlay = document.getElementById('resultOverlay');
    const card = document.getElementById('resultCard');
    const score = data.score || { earned: 0, total: 0 };
    const isWin = score.earned >= score.total * 0.5;

    card.innerHTML = `
      <div class="result-emoji">${isWin ? '🎉' : '😢'}</div>
      <div class="result-headline ${isWin ? 'win' : 'lose'}">${isWin ? 'Leçon terminée !' : 'Essaie encore'}</div>
      <div class="result-sub">${isWin ? 'Excellent travail !' : 'Vous pouvez réviser et recommencer dans 24h.'}</div>

      ${score.total > 0 ? `
        <div class="result-score">
          <div class="v">${score.earned} / ${score.total}</div>
          <div class="l">Points obtenus</div>
        </div>
      ` : ''}

      <div class="result-earn">⏱️ Temps passé : ${formatTime(elapsedSeconds)}</div>

      <button class="result-btn" onclick="goBack()">Retour aux parcours</button>
    `;

    overlay.classList.add('open');

    if (navigator.vibrate) navigator.vibrate(isWin ? [30, 50, 30] : [100, 50, 100]);
  }

  function goBack() {
    history.back();
  }

  // ===== INIT =====
  loadLesson();
</script>
</body>
</html>
"""
)