// Puts the header sun where the real sun is over Seaham.
// Sets --sun-y (in art pixels from the top of the home sea) on every .sun from the
// solar elevation. Light theme only: in the dark theme the same shape is the
// moon, which stays where the stylesheet puts it.
(function () {
  var suns = document.querySelectorAll('.sun');
  if (!suns.length) return;

  var LAT = 54.84, LON = -1.34;          // Seaham North Pier
  var rad = Math.PI / 180;
  var dark = window.matchMedia('(prefers-color-scheme: dark)');
  var root = document.documentElement;

  function elevation(d) {
    var start = Date.UTC(d.getUTCFullYear(), 0, 0);
    var n = (d - start) / 864e5;                           // day of year
    var decl = 23.44 * Math.sin(rad * (360 / 365) * (n - 81));
    var b = rad * (360 / 365) * (n - 81);
    var eot = 9.87 * Math.sin(2 * b) - 7.53 * Math.cos(b) - 1.5 * Math.sin(b); // minutes
    var utcHours = d.getUTCHours() + d.getUTCMinutes() / 60;
    var solar = utcHours + LON / 15 + eot / 60;             // local solar time
    var h = rad * 15 * (solar - 12);                        // hour angle
    var s = Math.sin(rad * LAT) * Math.sin(rad * decl) +
            Math.cos(rad * LAT) * Math.cos(rad * decl) * Math.cos(h);
    return Math.asin(s) / rad;
  }

  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return dark.matches;
  }

  // Row 0 is the top of the sea block; the back swell sits around rows 12-20.
  // 50 degrees or more puts the sun at the top; the horizon half-sinks it;
  // below -8 degrees it is under the water.
  function rowFor(e) {
    if (e < -8) return 26;
    return Math.max(0, 16 - Math.min(e, 50) * 0.32);
  }

  function update() {
    var row = isDark() ? null : String(Math.round(rowFor(elevation(new Date()))));  // whole art pixels
    for (var i = 0; i < suns.length; i++) {
      if (row === null) suns[i].style.removeProperty('--sun-y');
      else suns[i].style.setProperty('--sun-y', row);
    }
  }

  update();
  setInterval(update, 5 * 60 * 1000);
  if (dark.addEventListener) dark.addEventListener('change', update);
  new MutationObserver(update).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
})();
