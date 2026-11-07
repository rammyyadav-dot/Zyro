/* Zyrostyle — 3D home: WebGL "growth engine", kinetic typography and 3D motion.
   Requires three.min.js (self-hosted, MIT). Everything here is decorative: the
   page is fully readable without JS/WebGL, and motion is skipped when the
   visitor prefers reduced motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  var stage = document.querySelector('.x3d');
  var k3 = document.querySelector('.k3');
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function sectionProgress(el) {
    var hdr = el === stage ? (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--hdr')) || 0) : 0;
    var r = el.getBoundingClientRect(), span = r.height - (window.innerHeight - hdr);
    return span > 0 ? clamp((hdr - r.top) / span, 0, 1) : 0;
  }

  // ── Kinetic characters in the hero title (keeps <em> markup) ──────────
  if (stage) {
    var c = 0;
    stage.querySelectorAll('.x3d-title .kt').forEach(function (line) {
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (ch) {
          if (ch.nodeType === 3) {
            var frag = document.createDocumentFragment();
            ch.textContent.split(/(\s+)/).forEach(function (word) {
              if (!word) return;
              if (/^\s+$/.test(word)) { frag.appendChild(document.createTextNode(' ')); return; }
              var w = document.createElement('span'); w.style.display = 'inline-block'; w.style.whiteSpace = 'nowrap';
              word.split('').forEach(function (chr) {
                var s = document.createElement('span'); s.className = 'kc'; s.textContent = chr;
                s.style.setProperty('--c', c++); w.appendChild(s);
              });
              frag.appendChild(w);
            });
            node.replaceChild(frag, ch);
          } else if (ch.nodeType === 1) { walk(ch); }
        });
      })(line);
    });
    var title = stage.querySelector('.x3d-title');
    if (title) title.setAttribute('aria-label', title.textContent.replace(/\s+/g, ' ').trim());
    requestAnimationFrame(function () { requestAnimationFrame(function () { stage.classList.add('ready'); }); });

    // 3D word flip: Get Found. / Noticed. / Chosen.
    var words = stage.querySelectorAll('.rot-w'), wi = 0;
    if (words.length && !reduce) {
      setInterval(function () {
        var cur = words[wi]; wi = (wi + 1) % words.length; var nxt = words[wi];
        cur.classList.remove('is-on'); cur.classList.add('is-out');
        nxt.classList.remove('is-out'); nxt.classList.add('is-on');
        setTimeout(function () { cur.classList.remove('is-out'); }, 900);
      }, 2300);
    }
  }

  // ── 3D tilt cards with glare (desktop pointers only) ──────────────────
  if (finePointer && !reduce) {
    document.querySelectorAll('.card, .hs-slide').forEach(function (el) {
      el.classList.add('tilt');
      var glare = document.createElement('span'); glare.className = 'tilt-glare'; el.appendChild(glare);
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.transform = 'perspective(900px) rotateY(' + ((x - .5) * 10).toFixed(2) + 'deg) rotateX(' + ((.5 - y) * 8).toFixed(2) + 'deg) translateZ(6px)';
        el.style.setProperty('--gx', (x * 100) + '%'); el.style.setProperty('--gy', (y * 100) + '%');
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  if (reduce) return;

  // ── 3D kinetic statement: words fly in from depth ─────────────────────
  if (k3) {
    k3.classList.add('live');
    var kw = k3.querySelectorAll('.k3-w');
    var kUpdate = function () {
      var r = k3.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var q = sectionProgress(k3), n = kw.length;
      for (var i = 0; i < n; i++) {
        var e = ease(clamp((q * 1.5 - (i / n) * 0.75) / 0.42, 0, 1));
        kw[i].style.transform = 'translate3d(0,' + ((1 - e) * 80).toFixed(1) + 'px,' + ((1 - e) * -650).toFixed(0) + 'px) rotateX(' + ((1 - e) * -60).toFixed(1) + 'deg)';
        kw[i].style.filter = e > 0.98 ? 'none' : 'blur(' + ((1 - e) * 10).toFixed(1) + 'px)';
        kw[i].style.opacity = e.toFixed(3);
      }
    };
    window.addEventListener('scroll', kUpdate, { passive: true });
    window.addEventListener('resize', kUpdate);
    kUpdate();
  }

  // ── WebGL growth engine ───────────────────────────────────────────────
  if (!stage || typeof THREE === 'undefined') return;
  var canvas = stage.querySelector('.x3d-canvas');
  var renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
  } catch (err) { return; }
  stage.classList.add('live', 'gl-on');

  var mobile = window.innerWidth < 960;
  var N = mobile ? 3600 : 7200;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.setClearColor(0x000000, 1);
  var scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x000000, 0.055);
  var camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
  camera.position.set(0, 0, 8.5);

  // Shape generators (each returns N xyz positions)
  function rnd() { return Math.random() * 2 - 1; }
  function sphere() {
    var a = new Float32Array(N * 3), g = Math.PI * (3 - Math.sqrt(5));
    for (var i = 0; i < N; i++) {
      var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = g * i, R = 2.45 + rnd() * 0.06;
      // latitude bands to read like a search "globe"
      if (i % 7 === 0) R = 2.45 + 0.35;
      a[i * 3] = Math.cos(th) * r * R; a[i * 3 + 1] = y * R; a[i * 3 + 2] = Math.sin(th) * r * R;
    }
    return a;
  }
  function torus() {
    var a = new Float32Array(N * 3), R = 2.2, r = 0.78;
    for (var i = 0; i < N; i++) {
      var u = Math.random() * Math.PI * 2, v = Math.random() * Math.PI * 2, rr = r * (0.92 + Math.random() * 0.12);
      a[i * 3] = (R + rr * Math.cos(v)) * Math.cos(u);
      a[i * 3 + 1] = rr * Math.sin(v);
      a[i * 3 + 2] = (R + rr * Math.cos(v)) * Math.sin(u);
    }
    return a;
  }
  function vortex() {
    var a = new Float32Array(N * 3);
    for (var i = 0; i < N; i++) {
      var t = i / N, arm = i % 3, ang = t * Math.PI * 14 + arm * (Math.PI * 2 / 3);
      var rad = 0.25 + Math.pow(t, 1.15) * 2.6 + Math.random() * 0.18;
      a[i * 3] = Math.cos(ang) * rad + rnd() * 0.05;
      a[i * 3 + 1] = -2.9 + t * 5.6 + rnd() * 0.08;
      a[i * 3 + 2] = Math.sin(ang) * rad + rnd() * 0.05;
    }
    return a;
  }
  function zed() {
    var a = new Float32Array(N * 3), W = 2.1, H = 2.0, segs = [[-W, H, W, H], [W, H, -W, -H], [-W, -H, W, -H]];
    var lens = segs.map(function (s) { return Math.hypot(s[2] - s[0], s[3] - s[1]); }), tot = lens[0] + lens[1] + lens[2];
    for (var i = 0; i < N; i++) {
      var pick = Math.random() * tot, k = pick < lens[0] ? 0 : pick < lens[0] + lens[1] ? 1 : 2, s = segs[k], t = Math.random();
      a[i * 3] = s[0] + (s[2] - s[0]) * t + rnd() * 0.22;
      a[i * 3 + 1] = s[1] + (s[3] - s[1]) * t + rnd() * 0.22;
      a[i * 3 + 2] = rnd() * 0.45;
    }
    return a;
  }
  var shapes = [sphere(), torus(), vortex(), zed()];
  var keys = [0.0, 0.34, 0.64, 0.92];

  var geo = new THREE.BufferGeometry();
  var pos = new Float32Array(N * 3), col = new Float32Array(N * 3), delay = new Float32Array(N), seed = new Float32Array(N * 3);
  var gold = new THREE.Color(0xc8a882), deep = new THREE.Color(0x8a6a45), white = new THREE.Color(0xfff6ea), tmp = new THREE.Color();
  for (var i = 0; i < N; i++) {
    pos[i * 3] = shapes[0][i * 3]; pos[i * 3 + 1] = shapes[0][i * 3 + 1]; pos[i * 3 + 2] = shapes[0][i * 3 + 2];
    var m = Math.random();
    tmp.copy(m < 0.6 ? gold : m < 0.85 ? white : deep);
    col[i * 3] = tmp.r; col[i * 3 + 1] = tmp.g; col[i * 3 + 2] = tmp.b;
    delay[i] = Math.random();
    seed[i * 3] = rnd(); seed[i * 3 + 1] = rnd(); seed[i * 3 + 2] = rnd();
  }
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));

  var spr = document.createElement('canvas'); spr.width = spr.height = 64;
  var sx = spr.getContext('2d'), grd = sx.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, 'rgba(255,255,255,1)'); grd.addColorStop(0.35, 'rgba(255,255,255,.55)'); grd.addColorStop(1, 'rgba(255,255,255,0)');
  sx.fillStyle = grd; sx.fillRect(0, 0, 64, 64);
  var mat = new THREE.PointsMaterial({ size: mobile ? 0.075 : 0.06, map: new THREE.CanvasTexture(spr), vertexColors: true,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
  var points = new THREE.Points(geo, mat);

  var group = new THREE.Group(); group.add(points); scene.add(group);

  // wireframe core + orbit rings
  var core = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(1.05, 1)),
    new THREE.LineBasicMaterial({ color: 0xc8a882, transparent: true, opacity: 0.35 }));
  group.add(core);
  var rings = [];
  [3.3, 3.9].forEach(function (rad, k) {
    var pts = []; for (var j = 0; j <= 128; j++) { var t = j / 128 * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(t) * rad, 0, Math.sin(t) * rad)); }
    var ring = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: k ? 0xffffff : 0xc8a882, transparent: true, opacity: 0.16 }));
    ring.rotation.x = k ? 1.2 : 1.45; ring.rotation.z = k ? 0.5 : -0.3; group.add(ring); rings.push(ring);
  });

  // dust field for depth
  var dustN = mobile ? 500 : 1100, dpos = new Float32Array(dustN * 3);
  for (var d = 0; d < dustN; d++) { dpos[d * 3] = rnd() * 16; dpos[d * 3 + 1] = rnd() * 10; dpos[d * 3 + 2] = -Math.random() * 18 + 2; }
  var dgeo = new THREE.BufferGeometry(); dgeo.setAttribute('position', new THREE.BufferAttribute(dpos, 3));
  var dust = new THREE.Points(dgeo, new THREE.PointsMaterial({ size: 0.03, color: 0x8a7a66, transparent: true, opacity: 0.6, depthWrite: false }));
  scene.add(dust);

  // state
  var mouse = { x: 0, y: 0, tx: 0, ty: 0 }, visible = true, lastY = window.scrollY, vel = 0;
  var chapters = stage.querySelectorAll('.x3d-chapter'), hudStep = stage.querySelector('.x3d-hud-step');
  window.addEventListener('pointermove', function (e) {
    mouse.tx = (e.clientX / window.innerWidth) * 2 - 1; mouse.ty = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });

  function resize() {
    var w = canvas.clientWidth, h = canvas.clientHeight;
    mobile = window.innerWidth < 960;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) loop(); }).observe(stage);
  }

  var clock = new THREE.Clock(), running = false;
  function loop() { if (running) return; running = true; requestAnimationFrame(tick); }
  function tick() {
    if (!visible) { running = false; return; }
    requestAnimationFrame(tick);
    var time = clock.getElapsedTime();
    var p = sectionProgress(stage);
    stage.style.setProperty('--p', p.toFixed(4));
    var y = window.scrollY; vel += ((y - lastY) - vel) * 0.1; lastY = y;

    // morph between keyframed shapes with per-particle stagger + mid-flight scatter
    var seg = 0; while (seg < keys.length - 2 && p > keys[seg + 1]) seg++;
    var local = clamp((p - keys[seg]) / (keys[seg + 1] - keys[seg]), 0, 1);
    var A = shapes[seg], B = shapes[seg + 1];
    var scatter = Math.sin(Math.PI * local) * 0.9;
    for (var i = 0; i < N; i++) {
      var t = ease(clamp(local * 1.35 - delay[i] * 0.35, 0, 1)), i3 = i * 3;
      var wob = Math.sin(time * 0.8 + delay[i] * 12) * 0.03;
      pos[i3] = A[i3] + (B[i3] - A[i3]) * t + seed[i3] * scatter + wob;
      pos[i3 + 1] = A[i3 + 1] + (B[i3 + 1] - A[i3 + 1]) * t + seed[i3 + 1] * scatter + wob;
      pos[i3 + 2] = A[i3 + 2] + (B[i3 + 2] - A[i3 + 2]) * t + seed[i3 + 2] * scatter;
    }
    geo.attributes.position.needsUpdate = true;

    // composition: shape sits right of the copy on desktop, above it on mobile
    mouse.x += (mouse.tx - mouse.x) * 0.05; mouse.y += (mouse.ty - mouse.y) * 0.05;
    var targetX = mobile ? 0 : 2.6, targetY = mobile ? 1.35 : 0.1;
    group.position.x += (targetX - group.position.x) * 0.08;
    group.position.y += (targetY - group.position.y) * 0.08;
    var zedFace = clamp((p - 0.8) / 0.12, 0, 1); // the final "Z" turns to face the viewer
    group.rotation.y = (time * 0.12 + p * Math.PI * 2.2 + vel * 0.002) * (1 - zedFace) + mouse.x * 0.35;
    group.rotation.x = mouse.y * 0.22 + Math.sin(time * 0.3) * 0.05 * (1 - zedFace);
    var sc = mobile ? 0.72 : 1; group.scale.setScalar(sc * (1 + Math.sin(time * 1.2) * 0.012));
    core.rotation.x = time * 0.35; core.rotation.y = time * 0.5;
    core.material.opacity = (0.35 * (1 - clamp(p * 3, 0, 1)) + 0.08) * (1 - zedFace);
    rings.forEach(function (r, k) { r.rotation.y = time * (k ? -0.08 : 0.06); r.material.opacity = 0.16 * (1 - zedFace); });
    dust.rotation.y = time * 0.01; dust.position.y = -p * 3;
    camera.position.x += (mouse.x * 0.6 - camera.position.x) * 0.04;
    camera.position.y += (-mouse.y * 0.4 - camera.position.y) * 0.04;
    camera.lookAt(group.position.x * 0.35, 0, 0);
    mat.size = (mobile ? 0.075 : 0.06) * (1 + Math.min(Math.abs(vel) * 0.004, 0.6));

    // story chapters
    var step = p < 0.17 ? 0 : p < 0.43 ? 1 : p < 0.69 ? 2 : 3;
    for (var c2 = 0; c2 < chapters.length; c2++) chapters[c2].classList.toggle('is-active', c2 + 1 === step);
    if (hudStep) hudStep.textContent = '0' + step + ' / 03';

    renderer.render(scene, camera);
  }
  loop();
})();
