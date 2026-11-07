/* Zyrostyle — site behaviour & scroll motion.
   Progressive enhancement: content is fully readable without JS, and all motion
   is skipped for visitors who prefer reduced motion. */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var vh = window.innerHeight, vw = window.innerWidth;
  function setHdr() { var h = document.querySelector('.site-header'); if (h) root.style.setProperty('--hdr', h.offsetHeight + 'px'); }
  setHdr(); window.addEventListener('resize', setHdr);

  // ── Mobile navigation ────────────────────────────────────────────────
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Mobile sub-menus (accordion)
  document.querySelectorAll('.sub-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
      var li = b.parentNode, open = li.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // ── Split headings into words (keeps <em> and other inline markup) ───
  function splitWords(el) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (ch) {
        if (ch.nodeType === 3) {
          var parts = ch.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span'); w.className = 'w';
            var wi = document.createElement('span'); wi.className = 'wi'; wi.textContent = p;
            wi.style.setProperty('--i', i++); w.appendChild(wi); frag.appendChild(w);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1 && ch.tagName !== 'BR') { walk(ch); }
      });
    })(el);
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
  }
  var splits = Array.prototype.slice.call(document.querySelectorAll('.split, .section .h-lg, .manifesto h2, .bw-h, .bs-h'));
  splits = splits.filter(function (el) { return !el.classList.contains('scrub'); });
  if (!reduce) splits.forEach(function (el) { el.classList.add('split'); splitWords(el); });

  // ── Scroll-lit text: wrap words so they brighten with scroll ─────────
  var scrubs = Array.prototype.slice.call(document.querySelectorAll('.scrub'));
  var scrubWords = [];
  scrubs.forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.innerHTML = words.map(function (w) { return '<span class="sw" aria-hidden="true">' + w + '</span>'; }).join(' ');
    scrubWords.push({ el: el, words: el.querySelectorAll('.sw') });
  });

  // ── Reveal on enter (fade-ups, image clip reveals, split headings) ───
  var revealables = document.querySelectorAll('.reveal, .img-reveal, .split');
  if ('IntersectionObserver' in window && !reduce) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible', 'in'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealables.forEach(function (r) { obs.observe(r); });
  } else {
    revealables.forEach(function (r) { r.classList.add('visible', 'in'); });
  }

  // ── Bold hero: entrance + rows that slide sideways on scroll ─────────
  var bh = document.querySelector('.bh');
  if (bh) requestAnimationFrame(function () { requestAnimationFrame(function () { bh.classList.add('in'); }); });
  var shifters = Array.prototype.slice.call(document.querySelectorAll('[data-shift]'));

  // ── Horizontal pinned showcase ───────────────────────────────────────
  var hs = document.querySelector('.hs');
  var hsTrack = hs && hs.querySelector('.hs-track');
  function setupShowcase() {
    if (!hs || !hsTrack) return;
    var enable = !reduce && vw > 960 && vh >= 680;
    hs.classList.toggle('pinned', enable);
    if (enable) {
      var dist = hsTrack.scrollWidth - vw;
      hs.style.height = (vh + Math.max(dist, 0)) + 'px';
    } else {
      hs.style.height = ''; hsTrack.style.transform = '';
    }
  }

  // ── Scroll-driven frame loop ─────────────────────────────────────────
  var progress = document.querySelector('.scroll-progress span');
  var parallax = Array.prototype.slice.call(document.querySelectorAll('[data-speed]'));
  var rows = Array.prototype.slice.call(document.querySelectorAll('.mm-row'));
  var ticking = false, lastScroll = window.scrollY || 0, velocity = 0;

  function frame() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    velocity += ((y - lastScroll) - velocity) * 0.35; lastScroll = y;
    var skew = Math.max(-12, Math.min(12, velocity * -0.12));
    var docH = root.scrollHeight - vh;
    if (progress) progress.style.transform = 'scaleX(' + (docH > 0 ? y / docH : 0) + ')';

    if (!reduce) {
      parallax.forEach(function (el) {
        var r = el.parentNode.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var center = r.top + r.height / 2 - vh / 2;
        el.style.transform = 'translate3d(0,' + (-center * parseFloat(el.getAttribute('data-speed'))).toFixed(1) + 'px,0)';
      });
      rows.forEach(function (row) {
        var r = row.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var dir = parseFloat(row.getAttribute('data-dir')) || 1;
        var shift = (r.top - vh) * 0.45 * dir - (dir > 0 ? vw * 0.6 : vw * 0.2);
        row.firstElementChild.style.transform = 'translate3d(' + shift.toFixed(1) + 'px,0,0) skewX(' + skew.toFixed(2) + 'deg)';
      });
      shifters.forEach(function (el) {
        var f = parseFloat(el.getAttribute('data-shift'));
        el.style.transform = 'translate3d(' + (y * f * 4).toFixed(1) + 'px,0,0)';
      });
      if (hs && hs.classList.contains('pinned')) {
        var hr = hs.getBoundingClientRect();
        var max = hsTrack.scrollWidth - vw;
        var p = Math.min(Math.max(-hr.top / (hr.height - vh), 0), 1);
        hsTrack.style.transform = 'translate3d(' + (-p * max).toFixed(1) + 'px,0,0)';
      }
    }
    scrubWords.forEach(function (s) {
      var r = s.el.getBoundingClientRect();
      var p = reduce ? 1 : Math.min(Math.max((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0), 1);
      var lit = Math.round(p * s.words.length);
      for (var i = 0; i < s.words.length; i++) s.words[i].classList.toggle('on', i < lit);
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  var settle; window.addEventListener('scroll', function () { clearTimeout(settle); settle = setTimeout(function () { velocity = 0; lastScroll = window.scrollY; onScroll(); }, 120); }, { passive: true });
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { vh = window.innerHeight; vw = window.innerWidth; setupShowcase(); onScroll(); });
  window.addEventListener('load', function () { setupShowcase(); onScroll(); });
  setupShowcase(); frame();

  // ── Contact form: WhatsApp / email hand-off when no backend endpoint ──
  var form = document.getElementById('enquiry-form');
  if (form) {
    form.addEventListener('submit', function (ev) {
      if (form.getAttribute('data-endpoint')) return;
      ev.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var body = [
        'New enquiry from the Zyrostyle website',
        'Name: ' + (d.get('name') || ''),
        'Company / Brand: ' + (d.get('company') || ''),
        'Website: ' + (d.get('website') || '-'),
        'Mobile / WhatsApp: ' + (d.get('phone') || ''),
        'Email: ' + (d.get('email') || ''),
        'Service: ' + (d.get('service') || ''),
        'Monthly budget: ' + (d.get('budget') || '-'),
        'Goals: ' + (d.get('goals') || '')
      ].join('\n');
      var wa = form.getAttribute('data-whatsapp'), mail = form.getAttribute('data-email');
      if (wa) window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(body), '_blank', 'noopener');
      else if (mail) window.location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent('Marketing consultation request — ' + (d.get('company') || d.get('name') || '')) + '&body=' + encodeURIComponent(body);
      var status = document.getElementById('form-status');
      if (status) status.textContent = 'Thank you — your enquiry is ready to send. Our strategists respond within one working day.';
    });
  }

  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();
})();
