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

  .inactive-banner { margin: 0 16px 16px; background: linear-gradient(135deg, #fff3e0, #ffe0b2); border: 1.5px solid #ffb74d; border-radius: 16px; padding: 14px 16px; display: flex; align-items: center; gap: 12px; }
  .inactive-banner .icon { width: 40px; height: 40px; border-radius: 12px; background: #ffe0b2; color: #e65100; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 20px; }
  .inactive-banner .text { flex: 1; min-width: 0; }
  .inactive-banner .title { font-size: 13px; font-weight: 800; color: #e65100; margin-bottom: 2px; }
  .inactive-banner .desc { font-size: 11px; color: #bf360c; }
  .inactive-banner .action { background: #e65100; color: #fff; border: none; padding: 8px 12px; border-radius: 10px; font-size: 11px; font-weight: 700; cursor: pointer; flex-shrink: 0; font-family: inherit; }

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

  .preview-note { margin: 0 16px 16px; background: #e3f2fd; border-left: 3px solid #1976d2; border-radius: 10px; padding: 10px 14px; font-size: 12px; color: #0d47a1; font-weight: 600; line-height: 1.5; }

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
  .chapter.open .chapter-lessons { max-height: 3000px; }

  .lesson-item { padding: 14px 16px; border-top: 1px solid #f5f5f5; display: flex; align-items: center; gap: 12px; transition: background 0.2s; }
  .lesson-item:active { background: #f9f9f9; }
  .lesson-status { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 15px; font-weight: 900; }
  .lesson-status.done { background: var(--green); color: #fff; }
  .lesson-status.today { background: var(--gold); color: #212121; animation: pulse-gold 1.5s infinite; }
  .lesson-status.locked { background: #f5f5f5; color: #9e9e9e; }
  @keyframes pulse-gold { 0%,100% { box-shadow: 0 0 0 0 rgba(251,192,45,0.5); } 50% { box-shadow: 0 0 0 8px rgba(251,192,45,0); } }
  .lesson-info { flex: 1; min-width: 0; }
  .lesson-title { font-size: 13px; font-weight: 700; color: var(--text-dark); }
  .lesson-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
  .lesson-btn { background: var(--green); color: #fff; border: none; padding: 8px 14px; border-radius: 10px; font-size: 11px; font-weight: 800; font-family: inherit; cursor: pointer; white-space: nowrap; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; }
  .lesson-btn.locked { background: #f5f5f5; color: #9e9e9e; cursor: not-allowed; }
  .lesson-btn.today { background: linear-gradient(135deg, var(--gold), #f57c00); color: #212121; box-shadow: 0 4px 12px rgba(245,124,0,0.3); }

  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
  .empty-state .icon { font-size: 60px; margin-bottom: 12px; }
  .empty-state h3 { font-size: 15px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  .toast-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; display: flex; flex-direction: column; gap: 10px; width: 340px; max-width: 90vw; }
  .toast { padding: 16px 20px; border-radius: 16px; color: #fff; font-size: 14px; font-weight: 700; box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: toastIn 0.3s ease; line-height: 1.4; }
  .toast.success { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
  .toast.error { background: linear-gradient(135deg, #d32f2f, #b71c1c); }
  .toast.warning { background: linear-gradient(135deg, #f57c00, #e65100); }
  .toast.info { background: linear-gradient(135deg, #1976d2, #0d47a1); }
  @keyframes toastIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

  .section-label { padding: 0 16px 8px; font-size: 14px; font-weight: 800; color: var(--text-dark); }

  @media (min-width: 768px) {
    body { background: linear-gradient(135deg, #f0f4f0, #e8f5e9); padding: 20px 0; }
    .app { max-width: 900px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); overflow: hidden; }
    .hero { padding: 40px 32px; }
    .hero-title { font-size: 32px; }
    .stats-row { grid-template-columns: repeat(3, 1fr); }
  }
</style>
</head>
<body>

<div class="toast-container" id="toastContainer"></div>

<div class="app">
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
    const isUnlocked = p.is_unlocked || false;
    const totalLessons = (p.chapters || []).reduce((sum, c) => sum + (c.lessons || []).length, 0);

    // Bannière inactif
    let inactiveBannerHTML = '';
    if (!isActivated) {
      inactiveBannerHTML = `
        <div class="inactive-banner">
          <div class="icon">🔒</div>
          <div class="text">
            <div class="title">Compte non activé</div>
            <div class="desc">Activez pour débloquer ce parcours</div>
          </div>
          <button class="action" onclick="location.href='/activation'">Activer</button>
        </div>
      `;
    }

    // Progress
    let progressHTML = '';
    if (isUnlocked) {
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

    // Unlock
    let unlockHTML = '';
    if (!isUnlocked) {
      let btnDisabled = isActivated ? '' : 'disabled';
      let btnText = isActivated ? '🔓 Débloquer maintenant' : '🔒 Activez votre compte d\\'abord';

      unlockHTML = `
        <div class="unlock-card">
          <div style="font-size: 40px;">🔒</div>
          <div style="font-size: 13px; color: #6d4c00; font-weight: 700; margin-top: 8px;">Débloquez ce parcours pour</div>
          <div class="unlock-price">${fmt(p.unlock_price || 5000)} <span>FCFA</span></div>
          <div class="unlock-sub">${totalLessons} leçons · ${fmt(p.final_bonus || 500)} F de bonus final</div>
          <button class="btn-unlock" id="unlockBtn" onclick="unlockPath()" ${btnDisabled}>${btnText}</button>
        </div>
      `;
    }

    // Preview note
    let previewNoteHTML = '';
    if (!isUnlocked) {
      previewNoteHTML = `
        <div class="preview-note">
          👁️ Aperçu du contenu · Les leçons sont visibles mais restent verrouillées jusqu'au déblocage.
        </div>
      `;
    }

    // Chapitres
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
                <div class="chapter-meta">${lessons.length} leçon(s)${isUnlocked ? ' · ' + completed + ' terminée(s)' : ''}</div>
              </div>
              <div class="chapter-arrow">▾</div>
            </div>
            <div class="chapter-lessons">${lessonsHTML}</div>
          </div>
        `;
      }).join('');
    } else {
      chaptersHTML = '<div class="empty-state"><div class="icon">📚</div><h3>Aucune leçon</h3><p>Le contenu sera bientôt disponible.</p></div>';
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

      ${inactiveBannerHTML}
      ${progressHTML}
      ${unlockHTML}
      ${previewNoteHTML}

      <div class="section-label">📖 Contenu du parcours</div>

      ${chaptersHTML}

      <div style="height: 40px;"></div>
    `;
  }

  // ===== RENDER LEÇON =====
  function renderLesson(l, p) {
    const isUnlocked = p.is_unlocked || false;
    const isDone = (p.completed_lesson_ids || []).indexOf(l.id) !== -1;
    const lastDay = p.last_day || 0;
    const isToday = isUnlocked && !isDone && l.day_number === lastDay + 1;

    let statusClass = 'locked';
    let statusIcon = '🔒';
    let btnHTML = '';

    if (isDone) {
      statusClass = 'done';
      statusIcon = '✓';
      btnHTML = '<span class="lesson-btn locked">✓ Terminé</span>';
    } else if (isToday) {
      statusClass = 'today';
      statusIcon = '▶';
      btnHTML = `<a href="/parcours/${pathId}/lecon/${l.id}" class="lesson-btn today">Commencer →</a>`;
    } else if (isUnlocked) {
      statusClass = 'locked';
      statusIcon = '🔒';
      btnHTML = `<span class="lesson-btn locked">🔒 Jour ${l.day_number}</span>`;
    } else {
      btnHTML = '<span class="lesson-btn locked">🔒</span>';
    }

    return `
      <div class="lesson-item">
        <div class="lesson-status ${statusClass}">${statusIcon}</div>
        <div class="lesson-info">
          <div class="lesson-title">${escapeHtml(l.title)}</div>
          <div class="lesson-meta">Jour ${l.day_number} · ⏱ ${l.duration_minutes || 30} min · +${fmt(l.gain_amount)} / -${fmt(l.loss_amount)} F</div>
        </div>
        ${btnHTML}
      </div>
    `;
  }

  // ===== TOGGLE CHAPITRE =====
  function toggleChapter(id) {
    const el = document.getElementById('chapter-' + id);
    if (el) el.classList.toggle('open');
    if (navigator.vibrate) navigator.vibrate(5);
  }

  // ===== DÉBLOQUER =====
  async function unlockPath() {
    if (!isActivated) {
      showToast('Activez votre compte d\\'abord', 'error');
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
      btn.textContent = '🔓 Débloquer maintenant';
    }
  }

  // ===== INIT =====
  (async function() {
    await loadProfile();
    loadPath();
  })();
</script>
</body>
</html>
"""
)