// ADR-009: size demo iframes from their own height messages.
// Messages are only accepted from a demo iframe's own window, only as a number,
// and clamped. Message data never reaches the DOM.
(function () {
  var frames = Array.prototype.slice.call(document.querySelectorAll('iframe[data-demo]'));
  if (!frames.length) return;
  window.addEventListener('message', function (e) {
    var frame = frames.find(function (f) { return f.contentWindow === e.source; });
    if (!frame || !e.data || e.data.type !== 'cs-demo-height') return;
    var h = Number(e.data.height);
    if (!isFinite(h)) return;
    frame.style.height = Math.min(Math.max(Math.round(h), 120), 2000) + 'px';
  });
  frames.forEach(function (f) {
    f.addEventListener('load', function () {
      var paused = document.documentElement.getAttribute('data-motion') === 'paused';
      f.contentWindow.postMessage({ type: 'cs-motion', paused: paused }, '*');
    });
  });
})();
