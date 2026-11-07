/* Zytrostyle — site behaviour (progressive enhancement; the site works without JS) */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Scroll reveal
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    reveals.forEach(function (r) { obs.observe(r); });
  } else {
    reveals.forEach(function (r) { r.classList.add('visible'); });
  }

  // Contact form: if no backend endpoint is configured (data-endpoint empty),
  // hand the enquiry to WhatsApp (if a number is set) or the visitor's email client.
  var form = document.getElementById('enquiry-form');
  if (form) {
    form.addEventListener('submit', function (ev) {
      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint) return; // a real form handler (e.g. Formspree / Netlify Forms) takes over
      ev.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var services = d.getAll('services').join(', ');
      var lines = [
        'New enquiry from zytrostyle website',
        'Name: ' + (d.get('name') || ''),
        'Company / Brand: ' + (d.get('company') || ''),
        'Website: ' + (d.get('website') || '-'),
        'Mobile / WhatsApp: ' + (d.get('phone') || ''),
        'Email: ' + (d.get('email') || ''),
        'Services: ' + (services || d.get('service') || ''),
        'Monthly budget: ' + (d.get('budget') || '-'),
        'Goals: ' + (d.get('goals') || '')
      ];
      var body = lines.join('\n');
      var wa = form.getAttribute('data-whatsapp');
      var mail = form.getAttribute('data-email');
      var status = document.getElementById('form-status');
      if (wa) {
        window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(body), '_blank', 'noopener');
      } else if (mail) {
        window.location.href = 'mailto:' + mail + '?subject=' +
          encodeURIComponent('Marketing consultation request — ' + (d.get('company') || d.get('name') || '')) +
          '&body=' + encodeURIComponent(body);
      }
      if (status) status.textContent = 'Thank you — your enquiry is ready to send. Our strategists respond within one working day.';
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
