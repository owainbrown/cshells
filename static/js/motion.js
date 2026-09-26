// ADR-007: a pause control for the page's animation. It only exists when this
// script runs, and it remembers the choice where storage is available.
(function () {
  var root = document.documentElement;
  var slot = document.getElementById('motion-slot');
  var saved = null;
  try { saved = localStorage.getItem('cs-motion'); } catch (e) {}

  function tellDemos(paused) {
    document.querySelectorAll('iframe[data-demo]').forEach(function (f) {
      if (f.contentWindow) f.contentWindow.postMessage({ type: 'cs-motion', paused: paused }, '*');
    });
  }
  function apply(paused) {
    if (paused) root.setAttribute('data-motion', 'paused'); else root.removeAttribute('data-motion');
    tellDemos(paused);
  }
  apply(saved === 'paused');
  if (!slot) return;

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'cs-button cs-button--quiet';
  slot.appendChild(btn);
  var PAUSE = '<svg class="cs-button__icon" viewBox="0 0 3 3" aria-hidden="true"><path d="M0 0H1V3H0ZM2 0H3V3H2Z"/></svg>Pause waves';
  var PLAY = '<svg class="cs-button__icon" viewBox="0 0 3 3" aria-hidden="true"><path d="M0 0H1V3H0ZM1 0.5H2V2.5H1ZM2 1H3V2H2Z"/></svg>Play waves';
  function render(paused) {
    btn.setAttribute('aria-pressed', String(paused));
    btn.innerHTML = paused ? PLAY : PAUSE;
  }
  render(saved === 'paused');
  btn.addEventListener('click', function () {
    var paused = btn.getAttribute('aria-pressed') !== 'true';
    apply(paused);
    render(paused);
    try { localStorage.setItem('cs-motion', paused ? 'paused' : 'playing'); } catch (e) {}
  });
})();
