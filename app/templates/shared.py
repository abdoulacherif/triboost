"""CSS et scripts partagés par toutes les pages."""

HTML_HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#2e7d32">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="format-detection" content="telephone=no">
<title>{title}</title>
"""

CSS_COMMUN = """
<style>
  :root {
    --green: #2e7d32;
    --green-dark: #1b5e20;
    --green-light: #e8f5e9;
    --gold: #fbc02d;
    --red: #d32f2f;
    --red-light: #ffebee;
    --text-dark: #212121;
    --text-muted: #757575;
    --border: #e0e0e0;
    --bg: #fcfcfc;
    --safe-top: env(safe-area-inset-top, 0px);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
  }
  html, body {
    font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text-dark);
    min-height: 100vh;
    min-height: 100dvh;
    overscroll-behavior: none;
    -webkit-font-smoothing: antialiased;
  }
  body {
    display: flex;
    justify-content: center;
    padding-top: var(--safe-top);
    padding-bottom: var(--safe-bottom);
  }
  .wrap {
    width: 100%;
    max-width: 480px;
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 100vh;
    min-height: 100dvh;
    animation: pageIn 0.3s ease-out;
  }
  @keyframes pageIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .logo {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: var(--green);
    margin-bottom: 6px;
    letter-spacing: -0.5px;
  }
  .logo span { color: var(--gold); }
  .subtitle {
    text-align: center;
    color: var(--text-muted);
    font-size: 14px;
    margin-bottom: 32px;
    line-height: 1.4;
  }
  .form-group {
    margin-bottom: 14px;
    position: relative;
  }
  .form-group label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
  }
  .form-group input {
    width: 100%;
    height: 52px;
    padding: 0 16px;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    font-size: 16px;
    font-family: inherit;
    background: #fff;
    color: var(--text-dark);
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    -webkit-appearance: none;
    appearance: none;
  }
  .form-group input:focus {
    border-color: var(--green);
    box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.12);
  }
  .form-group input::placeholder { color: #bdbdbd; font-size: 15px; }
  .btn-primary {
    position: relative;
    width: 100%;
    height: 54px;
    background: var(--green);
    color: #fff;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    font-size: 16px;
    font-family: inherit;
    cursor: pointer;
    margin-top: 8px;
    overflow: hidden;
    transition: background 0.2s, transform 0.1s;
    box-shadow: 0 4px 14px rgba(46, 125, 50, 0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .btn-primary:active:not(:disabled) {
    transform: scale(0.98);
    background: var(--green-dark);
  }
  .btn-primary:disabled { opacity: 0.7; cursor: not-allowed; }
  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.5);
    transform: scale(0);
    animation: rippleAnim 0.6s linear;
    pointer-events: none;
  }
  @keyframes rippleAnim {
    to { transform: scale(4); opacity: 0; }
  }
  .spinner {
    width: 20px;
    height: 20px;
    border: 2.5px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .alert {
    padding: 14px 16px;
    border-radius: 14px;
    font-size: 14px;
    margin-bottom: 16px;
    display: none;
    line-height: 1.4;
  }
  .alert.error {
    background: var(--red-light);
    color: var(--red);
    border-left: 4px solid var(--red);
  }
  .alert.success {
    background: var(--green-light);
    color: var(--green);
    border-left: 4px solid var(--green);
  }
  .referral-info {
    background: var(--green-light);
    color: var(--green);
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 13px;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 600;
  }
  .footer {
    text-align: center;
    margin-top: 28px;
    font-size: 14px;
    color: var(--text-muted);
  }
  .footer a {
    color: var(--green);
    font-weight: 700;
    text-decoration: none;
    padding: 8px;
    display: inline-block;
  }
  .pw-toggle {
    position: absolute;
    right: 14px;
    top: 38px;
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    color: var(--text-muted);
    display: flex;
  }
  .progress-bar {
    position: fixed;
    top: var(--safe-top);
    left: 0; right: 0;
    height: 3px;
    z-index: 9999;
    display: none;
  }
  .progress-bar.active { display: block; }
  .progress-bar::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    height: 100%;
    width: 40%;
    background: linear-gradient(90deg, var(--green), var(--gold));
    animation: progressAnim 1.2s ease-in-out infinite;
  }
  @keyframes progressAnim {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(300%); }
  }
  .back-btn {
    position: absolute;
    top: calc(16px + var(--safe-top));
    left: 16px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--green-light);
    color: var(--green);
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10;
  }
  .back-btn:active {
    transform: scale(0.92);
    background: #c8e6c9;
  }
</style>
"""

JS_COMMUN = """
<script>
  // ===== RIPPLE EFFECT =====
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('.btn-primary');
    if (!btn || btn.disabled) return;
    const rect = btn.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    const size = Math.max(rect.width, rect.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
    ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });

  function showProgress() {
    document.getElementById('progressBar')?.classList.add('active');
  }
  function hideProgress() {
    document.getElementById('progressBar')?.classList.remove('active');
  }
  function vibrate(d) {
    if (navigator.vibrate) navigator.vibrate(d || 10);
  }
  function togglePassword(id) {
    const input = document.getElementById(id);
    input.type = input.type === 'password' ? 'text' : 'password';
    vibrate(5);
  }
  function setButtonLoading(btn, loading, text) {
    btn.disabled = loading;
    const span = btn.querySelector('span');
    if (!span) return;
    if (loading) {
      span.innerHTML = '<div class="spinner"></div>';
    } else {
      span.textContent = text;
    }
  }
  function showError(msg) {
    const el = document.getElementById('errorMsg');
    el.textContent = '⚠ ' + msg;
    el.style.display = 'block';
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  function showSuccess(msg) {
    const el = document.getElementById('successMsg');
    el.textContent = '✓ ' + msg;
    el.style.display = 'block';
  }
</script>
"""