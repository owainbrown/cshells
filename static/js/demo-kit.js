// Included by every demo. Reports the demo's height to the post, and follows
// the page's pause control. Demos run sandboxed with an opaque origin, so
// there is no storage and no access to the parent page.
(function () {
  function report() {
    parent.postMessage({ type: 'cs-demo-height', height: document.documentElement.scrollHeight }, '*');
  }
  if ('ResizeObserver' in window) new ResizeObserver(report).observe(document.documentElement);
  window.addEventListener('load', report);
  window.addEventListener('message', function (e) {
    if (e.source !== parent || !e.data || e.data.type !== 'cs-motion') return;
    if (e.data.paused) document.documentElement.setAttribute('data-motion', 'paused');
    else document.documentElement.removeAttribute('data-motion');
  });
})();
