/* Contact interactions are handoffs, never confirmed leads.
   No network analytics or attribution storage until optional analytics consent. */
(function () {
  'use strict';
  var consent = false, attribution;
  var engines = /(^|\.)(google\.[a-z.]+|bing\.com|duckduckgo\.com|search\.yahoo\.com|search\.brave\.com)$/i;
  function currentAttribution() {
    var ref = ''; try { ref = new URL(document.referrer).hostname; } catch (_) {}
    var medium = new URLSearchParams(location.search).get('utm_medium');
    return { landing_page: location.pathname, channel: medium ? (/^(cpc|ppc|paid|paid_social)$/i.test(medium) ? 'paid' : 'campaign') : (engines.test(ref) ? 'organic' : (ref && ref !== location.hostname && ref !== 'www.zyrostyle.com' ? 'referral' : 'direct_or_unknown')) };
  }
  attribution = currentAttribution();
  function restoreAttribution() {
    try {
      var saved = JSON.parse(sessionStorage.getItem('zs-attribution'));
      if (saved && /^\/(?!\/)[a-z0-9\-/]*$/i.test(saved.landing_page) && /^(organic|paid|campaign|referral|direct_or_unknown)$/.test(saved.channel)) attribution = saved;
      sessionStorage.setItem('zs-attribution', JSON.stringify(attribution));
    } catch (_) {}
  }
  function track(name, method, placement) {
    if (!consent) return;
    var event = { event: name, contact_method: method, placement: placement, page_path: location.pathname, landing_page: attribution.landing_page, acquisition_channel: attribution.channel };
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(event);
    if (window.gtag && analyticsId()) window.gtag('event', name, { contact_method: method, placement: placement, page_path: location.pathname, landing_page: attribution.landing_page, acquisition_channel: attribution.channel });
  }
  function analyticsId() {
    var meta = document.querySelector('meta[name="ga4-measurement-id"]');
    var id = meta ? meta.content : '';
    return /^G-[A-Z0-9]+$/.test(id) ? id : '';
  }
  function startAnalytics() {
    var id = analyticsId(); if (!id || window.zsGaStarted) return;
    window.zsGaStarted = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id, { send_page_view: false, page_location: location.origin + location.pathname, page_referrer: '', allow_google_signals: false, allow_ad_personalization_signals: false });
    window.gtag('event', 'page_view', { page_location: location.origin + location.pathname, page_referrer: '' });
    var script = document.createElement('script'); script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id; document.head.appendChild(script);
  }
  function setConsent(allowed) {
    consent = allowed === true;
    try {
      sessionStorage.setItem('zs-analytics-consent', consent ? 'granted' : 'denied');
      if (!consent) sessionStorage.removeItem('zs-attribution');
    } catch (_) {}
    var id = analyticsId(); if (id) window['ga-disable-' + id] = !consent;
    if (consent) { restoreAttribution(); startAnalytics(); }
    else attribution = currentAttribution();
    var status = document.getElementById('analytics-consent-status');
    if (status) status.textContent = consent ? 'Optional analytics allowed for this browser session.' : 'Optional analytics declined.';
  }
  window.ZyroMeasurement = { handoff: function (method, placement) { track('contact_handoff', method, placement); }, setConsent: setConsent };
  document.addEventListener('click', function (ev) {
    var button = ev.target.closest('[data-analytics-consent]');
    if (button) { setConsent(button.getAttribute('data-analytics-consent') === 'grant'); return; }
    var a = ev.target.closest('a[href]'); if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^https:\/\/wa\.me\//i.test(href)) track('contact_handoff', 'whatsapp', 'link');
    else if (/^mailto:/i.test(href)) track('contact_handoff', 'email', 'link');
    else if (/^tel:/i.test(href)) track('contact_handoff', 'phone', 'link');
  });
  try { if (sessionStorage.getItem('zs-analytics-consent') === 'granted') setConsent(true); } catch (_) {}
})();
