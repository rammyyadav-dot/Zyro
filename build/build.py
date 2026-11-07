#!/usr/bin/env python3
"""
Static site generator for zyrostyle.

    python3 build/build.py

Writes clean-URL pages (slug/index.html), sitemap.xml, robots.txt and llms.txt
into the repository root. All copy lives in build/content.py.
"""
import html
import json
import os
from datetime import date

from photos import ALT, INDUSTRY_PHOTOS, PAGE_PHOTOS
from clusters_a import SEO_PAGES, SMM_PAGES
from clusters_b import CREATION_PAGES, NICHE_PAGES, STRATEGY_PAGES
from landing_content import COURSE, COURSE_MODULES, LANDINGS, PACKAGES
from content import (AI_SEARCH, AREAS, BIHAR_CITIES, HOME_FAQS, INDUSTRIES, PATNA_AREAS,
                     PILLARS, PROCESS, SERVICES, SITE, TICKER, WHY)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = SITE["url"].rstrip("/")
TODAY = date.today().isoformat()


def _ver(rel):
    import hashlib
    with open(os.path.join(ROOT, "assets", rel), "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;"
         "1,300;1,400&family=Barlow:wght@300;400;500&family=Barlow+Condensed:wght@400;500"
         "&family=Inter+Tight:wght@400;500;600;700;800&display=swap")
SVC = {s["slug"]: s for s in SERVICES}
NAMES = {**{s["slug"]: s["nav"] for s in SERVICES}, AI_SEARCH["slug"]: AI_SEARCH["nav"],
         "industries": "Industries", "services": "Services", "areas-we-serve": "Areas We Serve",
         "about": "About", "contact": "Contact", "": "Home", "privacy-policy": "Privacy Policy",
         "digital-marketing-patna-guide": "Patna Marketing Hub"}
NAMES.update({l["slug"]: l["primary"].title().replace(" In ", " in ") for l in LANDINGS})

ORG_ID = BASE + "/#organization"

# ── Service clusters: group key -> (menu title, parent pillar slug, pages) ──
_by = {p["slug"]: p for p in NICHE_PAGES}
CLUSTERS = [
    ("seo", "SEO", "seo-services-patna", SEO_PAGES),
    ("social", "Social Media", "social-media-marketing-patna", SMM_PAGES),
    ("creation", "Content Creation", "content-creation-services-patna", CREATION_PAGES),
    ("content", "Content Marketing", "content-marketing-services-patna", STRATEGY_PAGES),
    ("ads", "Ads &amp; Web", "digital-marketing-agency-patna", [_by["google-ads-agency-patna"], _by["website-design-seo-patna"]]),
    ("industry", "Industries", "industries", [_by[k] for k in ("healthcare-digital-marketing-patna", "real-estate-digital-marketing-patna",
        "coaching-institute-marketing-patna", "school-promotion-agency-patna", "restaurant-social-media-marketing-patna",
        "election-campaign-digital-marketing-patna")]),
    ("local", "Patna Areas", "areas-we-serve", [_by["digital-marketing-company-saguna-more-patna"], _by["digital-marketing-company-patliputra-colony-patna"]]),
]
CLUSTER_PAGES = []
for _key, _title, _parent, _pages in CLUSTERS:
    for _p in _pages:
        _p.setdefault("schema", "service")
        _p["parent"] = _parent
        _p["cluster"] = _key
        PAGE_PHOTOS[_p["slug"]] = _p["photo"]
        CLUSTER_PAGES.append(_p)
CHILDREN = {_parent: _pages for _key, _title, _parent, _pages in CLUSTERS}
NAMES.update({p["slug"]: p["nav"] for p in CLUSTER_PAGES})
PAGES = []  # (slug, priority) for the sitemap


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    out, skip = [], False
    for ch in s:
        if ch == "<":
            skip = True
        elif ch == ">":
            skip = False
        elif not skip:
            out.append(ch)
    return "".join(out)


class Ctx:
    """Per-page context: knows its depth so every internal link is relative."""

    def __init__(self, slug):
        self.slug = slug
        self.pre = "../" * (slug.count("/") + 1) if slug else ""

    def href(self, slug):
        if slug.startswith(("http", "#", "mailto:", "tel:")):
            return slug
        target = (slug + "/") if slug else ""
        return (self.pre + target) or "./"

    def asset(self, path):
        return self.pre + "assets/" + path


def canonical(slug):
    return BASE + "/" + (slug + "/" if slug else "")


# ── STRUCTURED DATA ──────────────────────────────────────────────────────────
def org_schema():
    addr = {"@type": "PostalAddress", "addressLocality": SITE["locality"],
            "addressRegion": SITE["region"], "addressCountry": SITE["country"]}
    if SITE["street"]:
        addr["streetAddress"] = SITE["street"]
    if SITE["postal_code"]:
        addr["postalCode"] = SITE["postal_code"]
    org = {
        "@type": ["ProfessionalService", "Organization"],
        "@id": ORG_ID,
        "name": SITE["name"],
        "legalName": SITE["legal_name"],
        "url": BASE + "/",
        "logo": BASE + "/assets/img/logo.svg",
        "image": BASE + "/assets/img/og-image.png",
        "slogan": SITE["slogan"],
        "description": ("Zyrostyle is an award-winning content marketing and SEO agency in Patna, Bihar, "
                        "helping brands build organic growth engines that drive traffic, leads and revenue."),
        "email": SITE["email"],
        "address": addr,
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
        "openingHours": SITE["hours"],
        "priceRange": "₹₹",
        "areaServed": [{"@type": "City", "name": "Patna"}, {"@type": "State", "name": "Bihar"},
                       {"@type": "Country", "name": "India"}]
                      + [{"@type": "City", "name": c} for c in BIHAR_CITIES],
        "knowsAbout": ["Search Engine Optimization", "Local SEO", "Generative Engine Optimization",
                       "Answer Engine Optimization", "Content Marketing", "Content Strategy",
                       "Content Creation", "Digital Marketing", "Social Media Marketing",
                       "Google Ads", "Meta Ads", "Lead Generation"],
        "knowsLanguage": ["en-IN", "hi-IN"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Digital marketing services in Patna",
            "itemListElement": [{"@type": "Offer", "itemOffered": {
                "@type": "Service", "name": s["card_title"], "url": canonical(s["slug"])}}
                for s in SERVICES],
        },
    }
    if SITE["phone"]:
        org["telephone"] = SITE["phone"]
    if SITE["founded"]:
        org["foundingDate"] = SITE["founded"]
    if SITE["social"]:
        org["sameAs"] = SITE["social"]
    return org


def page_schema(ctx, title, desc, crumbs, extra=None, faqs=None, page_type="WebPage"):
    url = canonical(ctx.slug)
    graph = [
        org_schema(),
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": SITE["name"],
         "inLanguage": "en-IN", "publisher": {"@id": ORG_ID}},
        {"@type": page_type, "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": "en-IN", "isPartOf": {"@id": BASE + "/#website"},
         "about": {"@id": ORG_ID}, "dateModified": TODAY},
    ]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": canonical(s)}
            for i, (n, s) in enumerate(crumbs)]})
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs]})
    if extra:
        graph.extend(extra)
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")


def service_schema(name, slug, service_type, desc):
    return {
        "@type": "Service", "@id": canonical(slug) + "#service", "name": name,
        "serviceType": service_type, "description": desc, "url": canonical(slug),
        "provider": {"@id": ORG_ID},
        "areaServed": [{"@type": "City", "name": "Patna"}, {"@type": "State", "name": "Bihar"}],
        "audience": {"@type": "BusinessAudience", "name": "Businesses in Patna and Bihar"},
    }


# ── LAYOUT ───────────────────────────────────────────────────────────────────
def head(ctx, title, desc, keywords, schema, robots="index, follow, max-image-preview:large"):
    url = canonical(ctx.slug)
    og_img = BASE + "/assets/img/og-image.png"
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<meta name="robots" content="{robots}">
<meta name="author" content="{SITE['name']}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-IN" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<!-- GEO tags: Patna, Bihar, India -->
<meta name="geo.region" content="{SITE['region_code']}">
<meta name="geo.placename" content="{SITE['locality']}, {SITE['region']}, India">
<meta name="geo.position" content="{SITE['lat']};{SITE['lng']}">
<meta name="ICBM" content="{SITE['lat']}, {SITE['lng']}">
<meta name="language" content="English">
<meta name="distribution" content="global">
<!-- Open Graph / social -->
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="business:contact_data:locality" content="{SITE['locality']}">
<meta property="business:contact_data:region" content="{SITE['region']}">
<meta property="business:contact_data:country_name" content="India">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="{ctx.asset('img/favicon.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{ctx.asset('css/style.css')}?v={_ver('css/style.css')}">
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


MENU_EXTRA = {
    "seo": [("ai-search-optimisation-geo-aeo", "AI Search (GEO & AEO)")],
    "content": [("content-strategy-patna", "Content Strategy")],
    "ads": [("lead-generation-agency-patna", "Lead Generation"), ("full-service-digital-marketing-firm-patna", "Full-Service Marketing"),
            ("digital-marketing-packages-cost-patna", "Packages & Pricing")],
}
PATNA_MENU = [("digital-marketing-patna-guide", "Patna Hub"), ("areas-we-serve", "All Areas We Serve"),
              ("digital-marketing-company-boring-road-patna", "Boring Road"), ("digital-marketing-company-kankarbagh-patna", "Kankarbagh"),
              ("digital-marketing-company-saguna-more-patna", "Saguna More"), ("digital-marketing-company-patliputra-colony-patna", "Patliputra Colony"),
              ("digital-marketing-agency-near-me-patna", "Agency Near Me"), ("best-digital-marketing-company-patna", "Best Agency Guide"),
              ("digital-marketing-course-patna", "Digital Marketing Course"), ("digital-marketing-institute-patna", "Zyrostyle Academy")]


def nav(ctx):
    def cur(sl):
        return ' aria-current="page"' if ctx.slug == sl else ""

    def link(sl, label):
        return f'<li><a href="{ctx.href(sl)}"{cur(sl)}>{label}</a></li>'

    cols = []
    for key, title, parent, pages in CLUSTERS:
        if key in ("industry", "local"):
            continue
        items = "".join(link(p["slug"], p["nav"]) for p in pages)
        items += "".join(link(sl, lb) for sl, lb in MENU_EXTRA.get(key, []))
        cols.append(f'<div class="mega-col"><a class="mega-h" href="{ctx.href(parent)}"{cur(parent)}>{title}</a><ul>{items}</ul></div>')
    services_mega = (f'<div class="mega" id="mega-services"><div class="mega-inner">{"".join(cols)}'
                     f'<div class="mega-foot"><a href="{ctx.href("services")}">All services →</a>'
                     f'<a href="{ctx.href("contact")}">Free consultation →</a></div></div></div>')
    ind = "".join(link(p["slug"], p["nav"]) for p in CHILDREN["industries"]) + link("industries", "All Industries")
    pat = "".join(link(sl, lb) for sl, lb in PATNA_MENU)

    def toggle(label, target):
        return f'<button class="sub-toggle" aria-expanded="false" aria-controls="{target}" aria-label="Show {label} menu"><span></span></button>'

    return f"""<div class="scroll-progress" aria-hidden="true"><span></span></div>
<header class="site-header">
  <nav class="nav" aria-label="Main">
    <a class="nav-logo" href="{ctx.href('')}" aria-label="Zyrostyle home">Zyrostyle</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu">Menu</button>
    <div class="nav-menu" id="nav-menu">
      <ul class="nav-links">
        <li class="has-mega"><a href="{ctx.href('services')}"{cur('services')}>Services</a>{toggle('Services', 'mega-services')}{services_mega}</li>
        <li class="has-sub"><a href="{ctx.href('industries')}"{cur('industries')}>Industries</a>{toggle('Industries', 'sub-industries')}<ul class="subnav" id="sub-industries">{ind}</ul></li>
        <li class="has-sub"><a href="{ctx.href('digital-marketing-patna-guide')}"{cur('digital-marketing-patna-guide')}>Patna</a>{toggle('Patna', 'sub-patna')}<ul class="subnav" id="sub-patna">{pat}</ul></li>
        <li><a href="{ctx.href('about')}"{cur('about')}>About</a></li>
        <li><a class="btn btn-dark btn-sm nav-cta" href="{ctx.href('contact')}">Free Consultation</a></li>
      </ul>
    </div>
  </nav>
</header>
"""


def wa_widget():
    chips = [("🔎", "SEO &amp; Google Maps", "Hi Zyrostyle! I'd like help with SEO and ranking on Google Maps."),
             ("📱", "Social Media &amp; Reels", "Hi Zyrostyle! I'd like help with social media marketing and Reels."),
             ("🎯", "Ads &amp; Leads", "Hi Zyrostyle! I'd like to generate more leads with Google and Meta ads."),
             ("✨", "Free Consultation", "Hi Zyrostyle! I'd like a free marketing consultation for my business.")]
    chip_html = "".join(f'<button type="button" class="wa-chip" data-msg="{esc(m)}"><span aria-hidden="true">{e}</span> {t}</button>'
                        for e, t, m in chips)
    default = esc("Hi Zyrostyle! I'd like to know more about your digital marketing services.")
    return f"""<div class="wa" data-wa="{SITE['whatsapp']}">
  <div class="wa-panel" id="wa-panel" role="dialog" aria-modal="false" aria-labelledby="wa-title" hidden>
    <div class="wa-head">
      <span class="wa-avatar" aria-hidden="true">ZS</span>
      <div><p class="wa-name" id="wa-title">Zyrostyle</p><p class="wa-status"><span class="wa-dot"></span>Replies within minutes</p></div>
      <button type="button" class="wa-close" aria-label="Close chat">&times;</button>
    </div>
    <div class="wa-body">
      <div class="wa-bubble"><p><span aria-hidden="true">👋</span> Hi! Looking to grow your business in <strong>Patna or Bihar</strong>? Our strategists are here to help — ask us anything.</p><span class="wa-time">Just now ✓✓</span></div>
      <div class="wa-chips">{chip_html}</div>
    </div>
    <a class="wa-cta" href="https://wa.me/{SITE['whatsapp']}?text={default}" data-msg="{default}" rel="noopener" target="_blank">
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.3-1.4A9.9 9.9 0 1 0 12.04 2zm0 18.1c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7.1 3.9zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4.1c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>
      Chat on WhatsApp</a>
  </div>
  <button type="button" class="wa-fab" aria-expanded="false" aria-controls="wa-panel" aria-label="Chat with Zyrostyle on WhatsApp">
    <svg class="wa-ico" viewBox="0 0 24 24" width="30" height="30" aria-hidden="true"><path fill="currentColor" d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.3-1.4A9.9 9.9 0 1 0 12.04 2zm0 18.1c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7.1 3.9zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4.1c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>
    <span class="wa-x" aria-hidden="true">&times;</span>
    <span class="wa-badge" aria-hidden="true">1</span>
  </button>
</div>
"""


def footer(ctx):
    svc = "".join(f'<li><a href="{ctx.href(s["slug"])}">{s["nav"]}</a></li>' for s in SERVICES)
    svc += f'<li><a href="{ctx.href(AI_SEARCH["slug"])}">GEO &amp; AEO</a></li>'
    contact = f'<li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>'
    if SITE["phone"]:
        contact += f'<li><a href="tel:{SITE["phone"].replace(" ", "")}">{SITE["phone"]}</a></li>'
    addr = ", ".join(x for x in [SITE["street"], SITE["locality"], SITE["region"], SITE["postal_code"]] if x)
    contact += f"<li><a href=\"{ctx.href('contact')}\">{esc(addr)}, India</a></li>"
    social = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{u.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0].title()}</a></li>' for u in SITE["social"])
    popular = " · ".join(f'<a href="{ctx.href(l["slug"])}">{esc(l["primary"].title())}</a>' for l in LANDINGS)
    popular += f' · <a href="{ctx.href("digital-marketing-patna-guide")}">All Patna Guides</a>'
    wa = wa_widget() if SITE["whatsapp"] else ""
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <p class="footer-brand">Zyrostyle</p>
        <p class="footer-strap">{SITE['tagline']}</p>
        <p class="footer-about">Zyrostyle is an award-winning digital marketing, SEO, content strategy, content creation and social media marketing agency serving businesses in Patna, Bihar and across India.</p>
      </div>
      <div>
        <p class="footer-title">Services</p>
        <ul class="footer-links">{svc}</ul>
      </div>
      <div>
        <p class="footer-title">Quick Links</p>
        <ul class="footer-links">
          <li><a href="{ctx.href('')}">Home</a></li>
          <li><a href="{ctx.href('about')}">About Zyrostyle</a></li>
          <li><a href="{ctx.href('services')}">Services</a></li>
          <li><a href="{ctx.href('industries')}">Industries</a></li>
          <li><a href="{ctx.href('areas-we-serve')}">Areas We Serve</a></li>
          <li><a href="{ctx.href('contact')}">Contact</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-title">Contact</p>
        <ul class="footer-links">{contact}{social}</ul>
      </div>
    </div>
    <p class="footer-services footer-popular">Popular in Patna: {popular}</p>
    <p class="footer-services">SEO · Local SEO · GEO · AEO · Content Creation · Content Strategy · Content Marketing · Digital Marketing · Social Media Marketing · Lead Generation · Google Ads · Meta Ads<br>Service location: Patna, Bihar, India — serving {", ".join(PATNA_AREAS[:6])} &amp; all of Bihar</p>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Zyrostyle. All rights reserved.</span>
      <span>Photography: Unsplash</span>
      <span><a href="{ctx.href('privacy-policy')}">Privacy Policy</a> · <a href="{ctx.pre}sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>
{wa}
<script src="{ctx.asset('js/main.js')}?v={_ver('js/main.js')}" defer></script>
</body>
</html>
"""


# ── COMPONENTS ───────────────────────────────────────────────────────────────
def breadcrumb(ctx, crumbs):
    items = []
    for i, (name, slug) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            items.append(f'<li><a href="{ctx.href(slug)}">{esc(name)}</a></li>')
    return f'<ol class="breadcrumb">{"".join(items)}</ol>'


def pic(ctx, name, cls="", eager=False, sizes="100vw", alt=None):
    base = ctx.asset(f"img/photos/{name}")
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="{base}.webp" srcset="{base}-sm.webp 900w, {base}.webp 1800w" sizes="{sizes}" '
            f'alt="{esc(alt if alt is not None else ALT[name])}" width="1800" height="1200" {load} decoding="async">')


def img_band(ctx, text, photo=None, label=""):
    photo = photo or (PAGE_PHOTOS.get(ctx.slug) or (None, None))[1]
    if not photo:
        return ""
    lab = f'<span class="label on-dark">{label}</span>' if label else ""
    return f"""<section class="img-band" aria-label="{esc(strip_tags(text))}">
  <div class="img-band-media" data-speed="0.18">{pic(ctx, photo, "img-band-img")}</div>
  <div class="img-band-shade"></div>
  <div class="wrap img-band-copy">{lab}<p class="img-band-text split">{text}</p></div>
</section>
"""


def mega_marquee(rows=None):
    rows = rows or [("Get Found", "Get Noticed", "Get Chosen"), ("SEO", "GEO", "AEO", "Content", "Social", "Performance")]
    out = []
    for i, words in enumerate(rows):
        seq = "".join(f'<span class="mm-word{" outline" if (j + i) % 2 else ""}">{w}</span><span class="mm-dot">◆</span>' for j, w in enumerate(words)) * 3
        out.append(f'<div class="mm-row" data-dir="{-1 if i % 2 else 1}"><div class="mm-track">{seq}</div></div>')
    return f'<section class="mega-marquee" aria-hidden="true">{"".join(out)}</section>\n'


def showcase(ctx):
    slides = []
    for s in SERVICES:
        slides.append(f"""<a class="hs-slide" href="{ctx.href(s['slug'])}">
  <div class="hs-media">{pic(ctx, PAGE_PHOTOS[s['slug']][0], sizes="(max-width: 960px) 85vw, 40vw")}</div>
  <div class="hs-copy"><span class="num">{s['num']}</span><h3>{s['card_title']}</h3><p>{s['card_sub']}</p><span class="link-arrow">Explore {s['nav']}</span></div>
</a>""")
    return f"""<section class="hs dark" id="services">
  <div class="hs-sticky">
    <div class="wrap hs-head">
      <div><span class="label">Our Services — Everything Your Brand Needs to Grow</span><h2 class="h-lg">One growth partner. <em>Six connected capabilities.</em></h2></div>
      <p class="lead">Scroll to explore how we connect content, search, creativity and paid media into one growth engine.</p>
    </div>
    <div class="hs-track">{"".join(slides)}<div class="hs-end"><p class="tagline">Everything connected. Nothing wasted.</p><a class="btn btn-light" href="{ctx.href('services')}">All Services</a></div></div>
  </div>
</section>
"""


def x3d_home(ctx):
    """Home hero: sticky WebGL particle scene + scroll-driven story chapters.
    The H1 and all copy are real HTML (indexable); the canvas is decoration."""
    chapters = [
        ("01", "Discover", "Get Found.", "SEO, local SEO and AI-search optimisation put your business in front of customers the moment they search — on Google, Google Maps and AI assistants.", "seo-services-patna", "SEO Services"),
        ("02", "Connect", "Get Noticed.", "Content, storytelling and social media connect your brand to the right audience in Patna and Bihar — in English, Hindi and Hinglish.", "content-marketing-services-patna", "Content Marketing"),
        ("03", "Grow", "Get Chosen.", "Performance ads, landing pages and conversion tracking turn attention into enquiries, admissions, bookings and revenue.", "digital-marketing-agency-patna", "Digital Marketing"),
    ]
    ch = "".join(f"""<div class="x3d-chapter" data-index="{i+1}">
      <span class="x3d-num">{n} — {k}</span>
      <h2 class="x3d-ch-title">{t}</h2>
      <p>{d}</p>
      <a class="link-arrow" href="{ctx.href(sl)}">{lbl}</a>
    </div>""" for i, (n, k, t, d, sl, lbl) in enumerate(chapters))
    return f"""<section class="x3d" id="top" aria-label="Zyrostyle — digital marketing and SEO agency in Patna">
  <div class="x3d-sticky">
    <div class="x3d-fallback">{pic(ctx, "marketing-strategy-team-patna", "hero-img", eager=True)}</div>
    <canvas class="x3d-canvas" aria-hidden="true"></canvas>
    <div class="x3d-vignette"></div>
    <div class="x3d-hud" aria-hidden="true"><span>Patna · 25.59°N 85.13°E</span><span class="x3d-hud-step">00 / 03</span></div>
    <div class="wrap x3d-intro">
      <span class="eyebrow">Award-Winning Marketing Agency in Patna · SEO · GEO · Content · Creative Growth</span>
      <h1 class="h-xl x3d-title"><span class="kt">Digital Marketing &amp; SEO Agency in Patna</span> <span class="kt">That Turns Visibility <em>Into Growth.</em></span></h1>
      <p class="x3d-rotator" aria-label="Get Found. Get Noticed. Get Chosen.">Get <span class="rot"><span class="rot-w is-on">Found.</span><span class="rot-w">Noticed.</span><span class="rot-w">Chosen.</span></span></p>
      <p class="lead">We are an award-winning content marketing and SEO agency, helping brands build organic growth engines that drive traffic, leads and revenue across Patna, Bihar and India.</p>
      <div class="btn-row"><a class="btn btn-light" href="{ctx.href('contact')}">Get Your Free Marketing Consultation</a><a class="btn btn-line" href="#services">Explore Our Services</a></div>
    </div>
    <div class="wrap x3d-chapters">{ch}</div>
    <div class="x3d-scroll" aria-hidden="true"><span class="scroll-line"></span>Scroll to explore the growth engine</div>
  </div>
</section>
"""


def kinetic_statement():
    words = "We don't just market brands. We make them matter.".split()
    spans = "".join(f'<span class="k3-w" style="--k:{i}">{w}</span> ' for i, w in enumerate(words))
    return f"""<section class="k3" aria-label="We don't just market brands. We make them matter.">
  <div class="k3-sticky"><p class="k3-text">{spans}</p></div>
</section>
"""


def hero(ctx, eyebrow, h1, lead, crumbs=None, strap=None, ctas=None, meta=None, sub=True, photo=None):
    bc = f'<nav aria-label="Breadcrumb">{breadcrumb(ctx, crumbs)}</nav>' if crumbs else ""
    strap_html = f'<p class="hero-strap">{strap}</p>' if strap else ""
    ctas = ctas or [("Get Your Free Marketing Consultation", "contact", "btn-light"),
                    ("Explore Our Services", "services", "btn-line")]
    btns = "".join(f'<a class="btn {c}" href="{ctx.href(s)}">{t}</a>' for t, s, c in ctas)
    meta_html = ("<div class=\"hero-meta\">" + "".join(f"<span>{m}</span>" for m in meta) + "</div>") if meta else ""
    photo = photo or (PAGE_PHOTOS.get(ctx.slug) or (None,))[0]
    media = (f'<div class="hero-media" data-speed="0.3">{pic(ctx, photo, "hero-img", eager=True)}</div><div class="hero-shade"></div>'
             if photo else "")
    return f"""<section class="hero dark{' sub' if sub else ''}{' has-img' if photo else ''}">
  {media}
  <div class="wrap hero-inner">
    {bc}
    <span class="eyebrow">{eyebrow}</span>
    <h1 class="h-xl split">{h1}</h1>
    {strap_html}
    <p class="lead">{lead}</p>
    <div class="btn-row">{btns}</div>
    {meta_html}
  </div>
</section>
"""


def ticker():
    items = "".join(f'<span class="ticker-item">{esc(t)}</span>' for t in TICKER * 2)
    return f'<div class="ticker-wrap" aria-hidden="true"><div class="ticker">{items}</div></div>\n'


def faq_section(faqs, title="Frequently asked <em>questions.</em>", label="FAQ", cls="warm"):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="answer"><p>{esc(a)}</p></div></details>'
                    for q, a in faqs)
    return f"""<section class="section {cls}" id="faq">
  <div class="wrap">
    <div class="section-head single reveal"><div><span class="label">{label}</span><h2 class="h-lg">{title}</h2></div></div>
    <div class="faq reveal">{items}</div>
  </div>
</section>
"""


def service_cards(ctx, cls=""):
    cards = []
    for s in SERVICES:
        pts = "".join(f"<li>{p}</li>" for p in s["card_points"])
        cards.append(f"""<article class="card service-card reveal">
  <a class="card-media" href="{ctx.href(s['slug'])}" tabindex="-1">{pic(ctx, PAGE_PHOTOS[s['slug']][0], sizes="(max-width: 640px) 100vw, 33vw")}</a>
  <span class="num">{s['num']}</span>
  <h3><a href="{ctx.href(s['slug'])}" style="text-decoration:none">{s['card_title']}</a></h3>
  <p class="sub">{s['card_sub']}</p>
  <p>{s['card_text']}</p>
  <ul>{pts}</ul>
  <a class="link-arrow" href="{ctx.href(s['slug'])}">Explore {s['nav']}</a>
</article>""")
    return f'<div class="grid-3 {cls}">{"".join(cards)}</div>'


def triad_section(ctx, link=True):
    more = (f'<div class="btn-row"><a class="btn btn-line" href="{ctx.href(AI_SEARCH["slug"])}">Discover AI Search Optimisation</a></div>'
            if link else "")
    return f"""<section class="section dark">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">SEO + GEO + AEO</span><h2 class="h-lg">Built for the next generation <em>of search.</em></h2></div>
      <p class="lead">Your customers search everywhere — Google Search, Google Maps, YouTube, social networks and conversational AI tools. Your brand should be discoverable in all of them.</p>
    </div>
    <div class="triad reveal">
      <div><span class="abbr">SEO</span><h3>Search Engine Optimisation</h3><p>Improve how search engines discover, understand and rank your website for relevant queries.</p></div>
      <div><span class="abbr">GEO</span><h3>Generative Engine Optimisation</h3><p>Structure useful, credible and clearly attributed information so AI-powered search and discovery systems can better understand your brand and services.</p></div>
      <div><span class="abbr">AEO</span><h3>Answer Engine Optimisation</h3><p>Develop clear, direct answers to real customer questions through well-structured service pages, FAQs, explainers and knowledge content.</p></div>
    </div>
    <p class="tagline reveal">Be Found. Be Understood. Be Remembered.</p>
    {more}
  </div>
</section>
"""


def process_section():
    steps = "".join(f'<div class="process-step"><span class="n">Step {i+1:02d}</span><h3>{n}</h3><p>{d}</p></div>'
                    for i, (n, d) in enumerate(PROCESS))
    return f"""<section class="section dark">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">Our Approach</span><h2 class="h-lg">From strategy to <em>measurable growth.</em></h2></div>
      <p class="lead">A better process creates better marketing. Every engagement follows six connected steps.</p>
    </div>
    <div class="process reveal">{steps}</div>
    <p class="tagline reveal">Your growth isn't a one-time campaign. It's a system we help you build.</p>
  </div>
</section>
"""


def why_section(cls=""):
    items = "".join(f'<li><span class="n">{i+1:02d}</span><div><h3>{n}</h3><p>{d}</p></div></li>'
                    for i, (n, d) in enumerate(WHY))
    return f"""<section class="section {cls}">
  <div class="wrap grid-2">
    <div class="reveal">
      <span class="label">Why Choose Zyrostyle</span>
      <h2 class="h-lg">Creative thinking. Search intelligence. <em>Commercial focus.</em></h2>
      <p class="tagline">We don't chase vanity metrics. We build marketing around business outcomes.</p>
    </div>
    <ul class="num-list reveal">{items}</ul>
  </div>
</section>
"""


def industries_cards(ctx, limit=None):
    cards = []
    for i, (key, name, short, _long, _pts) in enumerate(INDUSTRIES[:limit]):
        cards.append(f"""<article class="card reveal"><a class="card-media" href="{ctx.href('industries')}#{key}" tabindex="-1">{pic(ctx, INDUSTRY_PHOTOS[key], sizes="(max-width: 640px) 100vw, 33vw")}</a><span class="num">{i+1:02d}</span><h3>{name}</h3><p>{short}</p>
<a class="link-arrow" href="{ctx.href('industries')}#{key}">Learn more</a></article>""")
    return f'<div class="grid-3">{"".join(cards)}</div>'


def locations_section(ctx, cls="stone"):
    p = "".join(f"<li>{a}</li>" for a in PATNA_AREAS)
    b = "".join(f"<li>{c}</li>" for c in BIHAR_CITIES)
    return f"""<section class="section {cls}">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">Digital Marketing Agency Serving Patna &amp; Bihar</span><h2 class="h-lg">Local understanding. <em>Bigger ambitions.</em></h2></div>
      <p class="lead">Zyrostyle provides digital marketing, content creation, SEO and social media marketing for businesses targeting Patna and wider Bihar — in English, Hindi or Hinglish.</p>
    </div>
    <div class="loc-cols reveal">
      <div><h3 class="h-sm">Patna</h3><ul class="loc-tags">{p}</ul></div>
      <div><h3 class="h-sm">Bihar</h3><ul class="loc-tags">{b}</ul></div>
    </div>
    <p class="tagline reveal">Patna Ki Soch. Brand Ki Badi Udaan.</p>
    <div class="btn-row reveal"><a class="btn btn-dark" href="{ctx.href('areas-we-serve')}">See Areas We Serve</a><a class="btn btn-line" href="{ctx.href('contact')}">Talk to a Marketing Strategist</a></div>
  </div>
</section>
"""


def enquiry_form(ctx, heading=True):
    opts = "".join(f'<option>{s["card_title"]}</option>' for s in SERVICES)
    opts += "<option>AI Search Optimisation (GEO &amp; AEO)</option><option>Not sure yet — need advice</option>"
    endpoint = SITE["form_endpoint"]
    action = f'action="{endpoint}" method="POST"' if endpoint else 'action="#" method="POST"'
    head_html = ""
    if heading:
        head_html = """<span class="label">Free Marketing Consultation</span>
<h2 class="h-md" style="margin-bottom:36px">Tell us about <em>your business.</em></h2>"""
    return f"""{head_html}
<form class="form" id="enquiry-form" {action} data-endpoint="{endpoint}" data-email="{SITE['email']}" data-whatsapp="{SITE['whatsapp']}">
  <div class="field"><label for="f-name">Full Name *</label><input id="f-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="f-company">Company / Brand Name *</label><input id="f-company" name="company" autocomplete="organization" required></div>
  <div class="field"><label for="f-website">Business Website (Optional)</label><input id="f-website" name="website" type="url" placeholder="https://"></div>
  <div class="field"><label for="f-phone">Mobile / WhatsApp *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" pattern="[0-9+ ()-]{{8,16}}" required></div>
  <div class="field"><label for="f-email">Email Address *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="f-service">Services Required *</label><select id="f-service" name="service" required><option value="">Select a service</option>{opts}</select></div>
  <div class="field full"><label for="f-budget">Monthly Marketing Budget (Optional)</label><select id="f-budget" name="budget"><option value="">Prefer not to say</option><option>Under ₹25,000</option><option>₹25,000 – ₹50,000</option><option>₹50,000 – ₹1,00,000</option><option>₹1,00,000 – ₹3,00,000</option><option>Above ₹3,00,000</option></select></div>
  <div class="field full"><label for="f-goals">Tell Us About Your Business Goals *</label><textarea id="f-goals" name="goals" required></textarea></div>
  <div class="full"><button class="btn btn-dark" type="submit">Let's Grow My Business</button></div>
  <p class="full form-status" id="form-status" role="status" aria-live="polite"></p>
  <p class="full form-note">We respect your privacy. Your details are used only to respond to your enquiry. See our <a href="{ctx.href('privacy-policy')}">Privacy Policy</a>.</p>
</form>"""


def cta_section(ctx, title="Ready to turn your business into a brand <em>people choose?</em>",
                text="Your next customer could already be searching for a business like yours. Make every search, every impression and every interaction count with a connected marketing strategy."):
    return f"""<section class="section dark cta-band">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">Let's Build Your Next Growth Story</span><h2 class="h-lg">{title}</h2></div>
    <div class="reveal">
      <p class="lead">{text}</p>
      <p class="tagline">Zyrostyle — Make Your Brand Impossible to Ignore.</p>
      <div class="btn-row"><a class="btn btn-light" href="{ctx.href('contact')}">Request Your Free Marketing Consultation</a><a class="btn btn-line" href="{ctx.href('contact')}">Get a Custom Proposal</a></div>
    </div>
  </div>
</section>
"""


def write(slug, body, priority="0.8"):
    path = os.path.join(ROOT, slug, "index.html") if slug else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    if priority:
        PAGES.append((slug, priority))


# ── PAGES ────────────────────────────────────────────────────────────────────
def build_home():
    ctx = Ctx("")
    title = "Zyrostyle | Award-Winning Digital Marketing & SEO Agency in Patna"
    desc = ("Award-winning content marketing & SEO agency in Patna, Bihar. SEO, GEO, content, social media & Google Ads "
            "that drive traffic, leads and revenue.")
    kw = ("digital marketing agency in patna, best digital marketing company in patna, seo company in patna, "
          "content marketing agency in patna, social media marketing agency in patna, digital marketing services patna, "
          "seo services in patna, top digital marketing agency in patna, lead generation agency in patna, bihar")
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, None, faqs=HOME_FAQS)) + nav(ctx)
    body = body.replace("<body>", '<body class="home">', 1)

    def pill(name, cls=""):
        return f'<span class="bh-pill {cls}" aria-hidden="true">{pic(ctx, name, eager=True, sizes="30vw", alt="")}</span>'

    # 1 ── HERO
    body += f"""<main id="main">
<section class="bh">
  <div class="bh-wrap">
    <p class="bh-eyebrow">Award-winning digital marketing, SEO &amp; content agency · Patna, Bihar</p>
    <div class="bh-grid">
      <h1 class="bh-title" aria-label="We are Zyrostyle. We do big things.">
        <span class="bh-row" data-shift="-0.06"><span class="bh-w">We are</span> {pill("creative-team-collaboration")}</span>
        <span class="bh-row" data-shift="0.05">{pill("video-editing-content-creation", "wide")} <span class="bh-w">Zyrostyle</span></span>
        <span class="bh-row" data-shift="-0.04"><span class="bh-w">We</span> {pill("client-success-celebration", "wide")} <span class="bh-w">do</span></span>
        <span class="bh-row" data-shift="0.07"><span class="bh-w">Big things</span></span>
      </h1>
      <div class="bh-side">
        <p>We solve big growth problems with strategy, search and creative that make a measurable impact.</p>
        <p>We partner with brands across Patna and Bihar that have the biggest ambitions.</p>
        <p>We hire big talent and give it big opportunities to build boundless careers.</p>
        <div class="bh-cta"><p class="bh-ask">Ready to do big things?</p><a class="pill-btn" href="{ctx.href('contact')}">Contact us</a></div>
      </div>
    </div>
  </div>
</section>
"""
    # 2 ── WHAT WE DO (compact image grid)
    tiles = []
    for i, sv in enumerate(SERVICES):
        tiles.append(f"""<a class="bw-tile t{i+1} reveal" href="{ctx.href(sv['slug'])}">
  <span class="bw-img">{pic(ctx, PAGE_PHOTOS[sv['slug']][0], sizes="(max-width: 760px) 100vw, 30vw")}</span>
  <span class="bw-cap"><strong>{sv['nav']}</strong><i></i><em>{sv['card_sub'].split('.')[0]}</em></span>
</a>""")
    body += f"""<section class="bw" id="services">
  <div class="bw-wrap">
    <p class="bw-vert" aria-hidden="true" data-speed="-0.12">What we do</p>
    <div>
      <h2 class="bw-h">Six connected capabilities. <em>One growth engine.</em></h2>
      <div class="bw-grid">{"".join(tiles)}</div>
      <div class="bw-more"><a class="pill-btn pill-dark" href="{ctx.href('services')}">View all services</a></div>
    </div>
  </div>
</section>
"""
    # 3 ── GIANT MARQUEE
    body += """<section class="bm" aria-hidden="true">
  <div class="mm-row" data-dir="1"><div class="mm-track">""" + ("<span>Do big things</span><span class='bm-dot'></span>" * 6) + """</div></div>
  <div class="mm-row outline" data-dir="-1"><div class="mm-track">""" + ("<span>Do big things</span><span class='bm-dot'></span>" * 6) + """</div></div>
</section>
"""
    # 4 ── SEO / GEO / AEO positioning (keyword-rich, clean)
    body += f"""<section class="bs">
  <div class="bs-wrap">
    <div class="bs-head reveal">
      <span class="label">Digital marketing &amp; SEO agency in Patna</span>
      <h2 class="bs-h">Your customers are searching. <em>Make sure they find you.</em></h2>
    </div>
    <div class="bs-body reveal">
      <p class="bs-lead">Zyrostyle is a content-led digital marketing and SEO agency in Patna, Bihar. We bring together SEO, content, social media and performance advertising to help ambitious brands compete, connect and convert — across Patna, Bihar and India.</p>
      <div class="bs-cols">
        <div><span>SEO</span><p>Rank on Google and Google Maps for the searches that bring customers.</p></div>
        <div><span>GEO</span><p>Be understood and cited by AI-powered search and assistants.</p></div>
        <div><span>AEO</span><p>Own the answers to your customers' real questions.</p></div>
      </div>
      <a class="link-arrow" href="{ctx.href(AI_SEARCH['slug'])}">How we optimise for AI search</a>
    </div>
  </div>
</section>
"""
    # 5 ── WHO WE HELP (compact image row)
    inds = "".join(f"""<a class="bi-card" href="{ctx.href('industries')}#{key}">
  <span class="bi-img">{pic(ctx, INDUSTRY_PHOTOS[key], sizes="260px")}</span>
  <span class="bi-name">{name.split(',')[0].split('&')[0].strip()}</span>
</a>""" for key, name, _s, _l, _p in INDUSTRIES)
    body += f"""<section class="bi">
  <div class="bi-head"><h2 class="bi-h">Who we help</h2><a class="link-arrow" href="{ctx.href('industries')}">All industries</a></div>
  <div class="bi-row">{inds}</div>
</section>
"""
    # 6 ── HOW WE WORK (compact)
    steps = "".join(f'<li><span>{i+1:02d}</span><strong>{n}</strong><p>{d}</p></li>' for i, (n, d) in enumerate(PROCESS))
    body += f"""<section class="bp">
  <div class="bp-wrap">
    <h2 class="bp-h">How we work</h2>
    <ol class="bp-list reveal">{steps}</ol>
  </div>
</section>
"""
    # 7 ── FAQ (AEO)
    body += faq_section(HOME_FAQS, title="Questions, <em>answered.</em>", cls="")
    # 8 ── FINAL CTA (gold field)
    areas = " · ".join(PATNA_AREAS[:8])
    body += f"""<section class="bc">
  <div class="bc-wrap">
    <h2 class="bc-h">Want to do<br>big things?</h2>
    <div class="bc-side">
      <p>Tell us about your business. A Zyrostyle strategist will reply within one working day with ideas for your growth.</p>
      <a class="pill-btn pill-dark" href="{ctx.href('contact')}">Contact us</a>
      <p class="bc-areas">Serving {areas} &amp; all of Bihar.</p>
    </div>
  </div>
</section>
"""
    body += "</main>\n" + footer(ctx)
    write("", body, "1.0")


def cluster_grid(ctx, parent, title=None):
    kids = CHILDREN.get(parent)
    if not kids:
        return ""
    cards = "".join(f"""<a class="cg-card reveal" href="{ctx.href(p['slug'])}">
  <span class="cg-img">{pic(ctx, p['photo'][0], sizes="(max-width: 640px) 100vw, 25vw")}</span>
  <span class="cg-name">{p['nav']}</span><span class="cg-desc">{esc(strip_tags(p['strap']))}</span>
</a>""" for p in kids)
    title = title or f"Specialist {NAMES[parent].replace('Services', '').strip()} services <em>in Patna.</em>"
    return f"""<section class="section cg">
  <div class="wrap">
    <div class="section-head single reveal"><div><span class="label">Explore</span><h2 class="h-lg">{title}</h2></div></div>
    <div class="cg-grid">{cards}</div>
  </div>
</section>
"""


def build_service(s):
    ctx = Ctx(s["slug"])
    crumbs = [("Home", ""), ("Services", "services"), (s["nav"], s["slug"])]
    extra = [service_schema(s["card_title"] + " in Patna", s["slug"], s["service_type"], s["description"])]
    body = head(ctx, s["title"], s["description"], s["keywords"],
                page_schema(ctx, s["title"], s["description"], crumbs, extra, s["faqs"])) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, s["eyebrow"], s["h1"], s["lead"], crumbs, strap=s["strap"],
                 ctas=[("Get Your Free Consultation", "contact", "btn-light"), ("Read FAQs", "#faq", "btn-line")],
                 meta=["Patna, Bihar", "Award-Winning Agency", "Transparent Reporting"])
    intro = "".join(f"<p>{p}</p>" for p in s["intro"])
    inc = "".join(f"<li>{i}</li>" for i in s["includes"])
    feats = "".join(f'<li><span class="n">{i+1:02d}</span><div><h3>{n}</h3><p>{d}</p></div></li>'
                    for i, (n, d) in enumerate(s["features"]))
    local = "".join(f"<p>{p}</p>" for p in s["local"])
    rel = "".join(f'<li><a href="{ctx.href(r)}">{NAMES[r]}</a></li>' for r in s["related"])
    rel += f'<li><a href="{ctx.href("services")}">All Services</a></li>'
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">{s['intro_label']}</span><h2 class="h-lg">{s['intro_h2']}</h2></div>
    <div class="prose reveal">{intro}</div>
  </div>
</section>
{img_band(ctx, s['strap'], label=s['nav'] + ' in Patna')}<section class="section warm">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">What's Included</span><h2 class="h-lg">{s['includes_h2']}</h2></div>
      <p class="lead">Every engagement is tailored after a free consultation, so you invest only in what moves your business forward.</p>
    </div>
    <ul class="check-list reveal">{inc}</ul>
  </div>
</section>
<section class="section">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">How We Deliver</span><h2 class="h-lg">{s['features_h2']}</h2>
      <div class="btn-row"><a class="btn btn-dark" href="{ctx.href('contact')}">Get a Custom Proposal</a></div></div>
    <ul class="num-list reveal">{feats}</ul>
  </div>
</section>
<section class="section stone">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">Patna &amp; Bihar</span><h2 class="h-lg">{s['local_h2']}</h2></div>
    <div class="prose reveal">{local}<p class="tagline">{s['closing']}</p></div>
  </div>
</section>
"""
    body += cluster_grid(ctx, s["slug"])
    body += process_section()
    body += faq_section(s["faqs"], title=f"{s['nav']} in Patna — <em>your questions answered.</em>")
    body += f"""<section class="section tight">
  <div class="wrap">
    <span class="label reveal">Related Services</span>
    <ul class="related reveal">{rel}</ul>
  </div>
</section>
"""
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write(s["slug"], body, "0.9")


def build_services_hub():
    ctx = Ctx("services")
    title = "Digital Marketing Services in Patna | SEO, Content & Social"
    desc = ("Explore Zyrostyle's services in Patna: SEO, content creation, content strategy, content marketing, "
            "digital marketing, social media marketing, GEO and AEO.")
    kw = "digital marketing services patna, seo services in patna, content marketing services in patna, social media marketing services patna, content creation services in patna"
    crumbs = [("Home", ""), ("Services", "services")]
    extra = [{"@type": "ItemList", "name": "Zyrostyle services", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": canonical(s["slug"]), "name": s["card_title"]}
        for i, s in enumerate(SERVICES)]}]
    faqs = [
        ("What digital marketing services do you offer in Patna?", "Zyrostyle offers SEO and local SEO, GEO and AEO (AI search optimisation), content creation, content strategy, content marketing, social media marketing, Google Ads, Meta Ads, lead generation, landing pages and analytics for businesses in Patna and across Bihar."),
        ("Can I choose only one digital marketing service?", "Yes. You can start with a single service such as SEO or social media and add more as results grow, or choose a full-service plan with everything connected."),
        ("Which digital marketing service should my business start with?", "Most local businesses get the fastest return from Google Business Profile optimisation and local SEO, followed by social media and targeted ads. We recommend priorities after a free audit."),
        ("Do you serve businesses outside Patna?", "Yes. We serve clients across Bihar — including Gaya, Muzaffarpur, Bhagalpur and Darbhanga — and across India."),
    ]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, extra, faqs, page_type="CollectionPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Digital Marketing Services in Patna", "Digital marketing services in Patna — <em>everything your brand needs to grow.</em>",
                 "One growth partner. Six connected marketing capabilities. We connect content, search, creativity and paid media to build a complete digital growth engine for businesses in Patna, Bihar and across India.",
                 crumbs, ctas=[("Get Your Free Consultation", "contact", "btn-light"), ("Explore Industries", "industries", "btn-line")])
    body += f'<section class="section"><div class="wrap">{service_cards(ctx)}</div></section>\n'
    groups = []
    for key, title, parent, pages in CLUSTERS:
        items = "".join(f'<li><a href="{ctx.href(p["slug"])}">{p["nav"]}</a></li>' for p in pages)
        items += "".join(f'<li><a href="{ctx.href(sl)}">{lb}</a></li>' for sl, lb in MENU_EXTRA.get(key, []))
        groups.append(f'<div class="reveal"><h3><a href="{ctx.href(parent)}">{title}</a></h3><ul>{items}</ul></div>')
    body += f"""<section class="section warm"><div class="wrap">
<div class="section-head single reveal"><div><span class="label">Service Directory</span><h2 class="h-lg">Every service, <em>one place.</em></h2></div></div>
<div class="dir">{"".join(groups)}</div></div></section>
"""
    body += mega_marquee()
    body += triad_section(ctx)
    body += why_section("warm")
    body += faq_section(faqs, title="Digital marketing services in Patna — <em>FAQs.</em>", cls="")
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write("services", body, "0.9")


def build_ai_search():
    a = AI_SEARCH
    ctx = Ctx(a["slug"])
    crumbs = [("Home", ""), ("Services", "services"), (a["nav"], a["slug"])]
    extra = [service_schema("Generative & Answer Engine Optimisation (GEO / AEO)", a["slug"], a["service_type"], a["description"])]
    body = head(ctx, a["title"], a["description"], a["keywords"],
                page_schema(ctx, a["title"], a["description"], crumbs, extra, a["faqs"])) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, a["eyebrow"], a["h1"], a["lead"], crumbs, strap="Be Found. Be Understood. Be Remembered.",
                 ctas=[("Discover AI Search Optimisation", "contact", "btn-light"), ("Read FAQs", "#faq", "btn-line")])
    body += img_band(ctx, "Search is changing. <em>Your visibility shouldn't.</em>", label="AI Search")
    body += triad_section(ctx, link=False)
    steps = [
        ("Entity clarity", "Consistent name, address, services and descriptions across your website, Google Business Profile, directories and social profiles, so machines know exactly who you are."),
        ("Structured data", "Organisation, LocalBusiness, Service, FAQ and Breadcrumb schema that make your pages machine-readable."),
        ("Answer-first content", "Service pages and FAQs that answer real customer questions directly in the first lines, then expand with depth and evidence."),
        ("Credibility signals", "Author expertise, clear sourcing, reviews, case studies and authoritative mentions that support trust (E-E-A-T)."),
        ("Crawl & access hygiene", "Fast, crawlable pages, clean sitemaps, sensible robots rules and an llms.txt summary for AI crawlers."),
        ("Measurement", "Tracking of brand mentions, AI Overview presence, featured snippets and referral traffic from AI tools where available."),
    ]
    li = "".join(f'<li><span class="n">{i+1:02d}</span><div><h3>{n}</h3><p>{d}</p></div></li>' for i, (n, d) in enumerate(steps))
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">How We Optimise for AI Search</span><h2 class="h-lg">Six building blocks of <em>AI discoverability.</em></h2>
      <div class="prose" style="margin-top:28px"><p>Search behaviour is changing. Customers discover businesses through Google Search, Google Maps, video platforms, social networks and conversational AI tools. Our goal is to help your business build stronger discoverability, credibility and customer confidence across all relevant search experiences.</p></div></div>
    <ul class="num-list reveal">{li}</ul>
  </div>
</section>
"""
    body += faq_section(a["faqs"], title="GEO &amp; AEO — <em>your questions answered.</em>")
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write(a["slug"], body, "0.8")


def build_industries():
    ctx = Ctx("industries")
    title = "Industry Marketing in Patna | Healthcare, Real Estate, Education"
    desc = ("Digital marketing in Patna for doctors & hospitals, real estate, coaching institutes, schools, "
            "restaurants, retail, travel and B2B brands.")
    kw = ("digital marketing services for doctors in patna, hospital digital marketing services patna, real estate digital marketing agency patna, "
          "coaching institute marketing agency patna, school promotion agency in patna, restaurant social media marketing patna, "
          "social media management for real estate patna, ecommerce seo agency patna")
    crumbs = [("Home", ""), ("Industries", "industries")]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs)) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Industries We Serve in Patna &amp; Bihar",
                 "Every industry has a different audience. <em>Every brand deserves a smarter strategy.</em>",
                 "From hospitals on Bailey Road to coaching institutes on Boring Road and real-estate projects near Saguna More, Zyrostyle builds marketing strategies around how your specific customers search, compare and decide.",
                 crumbs, ctas=[("Discuss Your Industry", "contact", "btn-light"), ("Explore Services", "services", "btn-line")])
    for i, (key, name, short, long, pts) in enumerate(INDUSTRIES):
        cls = "warm" if i % 2 == 0 else ""
        li = "".join(f"<li>{p}</li>" for p in pts)
        body += f"""<section class="section {cls}" id="{key}">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">{i+1:02d} — Industry</span><h2 class="h-lg">{name}</h2><p class="tagline">{short}</p>
      <figure class="media-frame img-reveal">{pic(ctx, INDUSTRY_PHOTOS[key], sizes="(max-width: 960px) 100vw, 50vw")}</figure></div>
    <div class="reveal"><div class="prose"><p>{long}</p></div><ul class="check-list" style="columns:1;margin-top:20px">{li}</ul>
      <div class="btn-row"><a class="btn btn-dark btn-sm" href="{ctx.href('contact')}">Plan My {name.split(',')[0].split('&')[0].strip()} Marketing</a></div></div>
  </div>
</section>
"""
    body += cluster_grid(ctx, "industries", title="Industry marketing <em>in Patna.</em>")
    body += cta_section(ctx, title="Don't see your industry? <em>Let's talk.</em>",
                        text="We work with manufacturers, NGOs, professional firms, automobile dealers, jewellers, interior designers and many more. Tell us about your market and we'll build a strategy around it.")
    body += "</main>\n" + footer(ctx)
    write("industries", body, "0.8")


def build_areas():
    ctx = Ctx("areas-we-serve")
    title = "Digital Marketing Agency Serving Patna & Bihar | Areas We Serve"
    desc = ("Digital marketing across Patna — Boring Road, Kankarbagh, Patliputra Colony, Saguna More — and Bihar "
            "cities like Gaya, Muzaffarpur & Bhagalpur.")
    kw = ("digital marketing company in boring road patna, digital marketing company in kankarbagh patna, digital marketing services in boring canal road, "
          "digital marketing company in saguna more, digital marketing company in patliputra colony, seo company in bihar, "
          "best agency for lead generation in bihar, digital marketing agency gaya, digital marketing agency muzaffarpur")
    crumbs = [("Home", ""), ("Areas We Serve", "areas-we-serve")]
    extra = [{"@type": "Place", "name": "Patna, Bihar", "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
              "containedInPlace": {"@type": "State", "name": "Bihar"}}]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, extra)) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Patna &amp; Bihar", "Local understanding. <em>Bigger ambitions.</em>",
                 "Zyrostyle provides digital marketing, SEO, content creation and social media marketing for businesses targeting Patna and wider Bihar. Whether your customers search in English, Hindi or Hinglish, we build content around their language, interests and intent.",
                 crumbs, strap="Patna Ki Soch. Brand Ki Badi Udaan.",
                 ctas=[("Talk to a Marketing Strategist", "contact", "btn-light"), ("Explore Services", "services", "btn-line")])
    blocks = "".join(f'<div class="area-block reveal"><h3>Digital marketing in {n}</h3><p>{d}</p></div>' for n, d in AREAS)
    band = img_band(ctx, "Patna Ki Soch. <em>Brand Ki Badi Udaan.</em>", label="Patna &amp; Bihar")
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal" style="position:sticky;top:110px"><span class="label">Patna Neighbourhoods</span><h2 class="h-lg">From Boring Road <em>to Danapur.</em></h2>
      <div class="prose" style="margin-top:24px"><p>Every Patna neighbourhood has its own customer mix. Our local SEO, Google Maps optimisation and geo-targeted advertising are tuned to the localities where your customers actually live, work and shop.</p></div></div>
    <div>{blocks}</div>
  </div>
</section>
"""
    body += band
    cities = [
        ("Gaya &amp; Bodh Gaya", "Tourism, hospitality, pilgrimage and education brands reaching domestic and international visitors."),
        ("Muzaffarpur", "Retail, trade, healthcare and education businesses in North Bihar's commercial hub."),
        ("Bhagalpur", "Textile and silk businesses, retailers and institutions building regional and national reach."),
        ("Darbhanga", "Healthcare, education and local service providers growing visibility across Mithila."),
        ("Hajipur &amp; Begusarai", "Industrial, manufacturing and B2B companies generating qualified leads beyond Bihar."),
        ("Purnia, Arrah, Bihar Sharif &amp; more", "Local businesses building their first strong digital presence with local SEO and social media."),
    ]
    cards = "".join(f'<article class="card reveal"><h3>{n}</h3><p>{d}</p></article>' for n, d in cities)
    body += f"""<section class="section warm">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="label">Across Bihar</span><h2 class="h-lg">Marketing for <em>every Bihar market.</em></h2></div>
      <p class="lead">Based in Patna, we run SEO, content and lead-generation campaigns for businesses targeting customers across Bihar's districts — and help Bihar brands scale nationally.</p></div>
    <div class="grid-3">{cards}</div>
  </div>
</section>
"""
    faqs = [
        ("Do you only work with businesses in Patna?", "No. Zyrostyle is based in Patna and works with businesses across Bihar and India. Many of our strategies help Patna businesses reach customers in other Bihar districts and help Bihar brands scale nationally."),
        ("Can you help my business rank in a specific Patna locality?", "Yes. Through Google Business Profile optimisation, locality-relevant content, local citations and review strategy, we help businesses improve visibility for searches in specific areas such as Boring Road, Kankarbagh or Patliputra Colony."),
        ("Do you create Hindi and Hinglish content for Bihar audiences?", "Yes. We create English, Hindi and Hinglish content depending on how your audience searches and engages."),
    ]
    body += cluster_grid(ctx, "areas-we-serve", title="Neighbourhood <em>guides.</em>")
    body += faq_section(faqs, cls="")
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write("areas-we-serve", body, "0.8")


def build_about():
    ctx = Ctx("about")
    title = "About Zyrostyle | Award-Winning Content Marketing Agency, Patna"
    desc = ("Zyrostyle is an award-winning content marketing and SEO agency in Patna, Bihar, building organic "
            "growth engines for ambitious brands.")
    kw = "about zyrostyle, content marketing agency patna, award winning marketing agency patna, seo agency bihar, digital marketing expert in patna"
    crumbs = [("Home", ""), ("About", "about")]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, page_type="AboutPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "About Zyrostyle", "We don't just market brands. <em>We make them matter.</em>",
                 "Zyrostyle is an award-winning content marketing and SEO agency in Patna, helping brands build organic growth engines that drive traffic, leads and revenue.",
                 crumbs, ctas=[("Work With Us", "contact", "btn-light"), ("Explore Services", "services", "btn-line")])
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">Our Story</span><h2 class="h-lg">Born in Patna. <em>Built for growth.</em></h2></div>
    <div class="prose reveal">
      <p>Zyrostyle was founded on a simple belief: businesses in Patna and Bihar deserve marketing that is as strategic, creative and measurable as anything produced in India's biggest metros.</p>
      <p>Too many local businesses were stuck with disconnected vendors — one for the website, another for social media, someone else for ads — and no one accountable for growth. We built Zyrostyle as <strong>one connected growth partner</strong>: strategy, content, search, social and performance working together.</p>
      <p>Today we help startups, local businesses and established companies across healthcare, education, real estate, hospitality, retail, travel and B2B get found, get noticed and get chosen.</p>
      <p class="tagline">Built for Visibility. Designed for Growth.</p>
    </div>
  </div>
</section>
{img_band(ctx, "Born in Patna. <em>Built for growth.</em>", label="Our Story")}<section class="section dark manifesto">
  <div class="wrap reveal">
    <span class="label">The Zyrostyle Philosophy</span>
    <h2 class="h-lg scrub">"Great marketing doesn't just attract attention. It creates commercial momentum."</h2>
    <a class="link-arrow" href="{ctx.href('services')}" style="color:var(--white)">See how we do it</a>
  </div>
</section>
"""
    body += why_section()
    body += process_section()
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write("about", body, "0.7")


def build_contact():
    ctx = Ctx("contact")
    title = "Contact Zyrostyle | Free Marketing Consultation in Patna, Bihar"
    desc = ("Request a free digital marketing, SEO or social media consultation with Zyrostyle in Patna, Bihar. "
            "Get a custom marketing proposal for your business.")
    kw = "contact digital marketing agency patna, free seo consultation patna, digital marketing strategy consultation patna, marketing agency near me patna"
    crumbs = [("Home", ""), ("Contact", "contact")]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, page_type="ContactPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Free Marketing Consultation", "Let's build your next <em>growth story.</em>",
                 "Your next customer could already be searching for a business like yours. Tell us about your goals and a Zyrostyle strategist will respond within one working day.",
                 crumbs, ctas=[("Start Below", "#consultation", "btn-light")])
    rows = f'<dt>Email</dt><dd><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></dd>'
    if SITE["phone"]:
        rows += f'<dt>Phone</dt><dd><a href="tel:{SITE["phone"].replace(" ", "")}">{SITE["phone"]}</a></dd>'
    if SITE["whatsapp"]:
        rows += f'<dt>WhatsApp</dt><dd><a href="https://wa.me/{SITE["whatsapp"]}" rel="noopener" target="_blank">Chat with us</a></dd>'
    addr = ", ".join(x for x in [SITE["street"], SITE["locality"], SITE["region"], SITE["postal_code"]] if x)
    rows += f'<dt>Office</dt><dd>{esc(addr)}, India</dd>'
    rows += '<dt>Hours</dt><dd>Monday – Saturday, 10:00 – 19:00</dd>'
    maps = f"https://www.google.com/maps/search/?api=1&query={SITE['lat']},{SITE['lng']}"
    body += f"""<section class="section" id="consultation">
  <div class="wrap grid-2">
    <div class="reveal">{enquiry_form(ctx)}</div>
    <aside class="contact-aside reveal">
      <span class="label">Reach Us</span>
      <dl>{rows}</dl>
      <div class="btn-row"><a class="btn btn-line" href="{maps}" rel="noopener" target="_blank">Open in Google Maps</a></div>
      <p class="tagline">Patna Ki Soch. Brand Ki Badi Udaan.</p>
    </aside>
  </div>
</section>
"""
    faqs = [
        ("What happens after I submit the form?", "A Zyrostyle strategist reviews your details, may run a quick audit of your website and online presence, and contacts you within one working day to schedule a free consultation call."),
        ("Is the consultation really free?", "Yes. The initial consultation is free and comes with no obligation. If there is a fit, we follow up with a custom marketing proposal."),
        ("Can we meet in person in Patna?", "Yes. We are happy to meet clients in Patna, and we also work remotely with businesses across Bihar and India."),
    ]
    body += faq_section(faqs)
    body += "</main>\n" + footer(ctx)
    write("contact", body, "0.7")


def build_privacy():
    ctx = Ctx("privacy-policy")
    title = "Privacy Policy | Zyrostyle"
    desc = "How Zyrostyle collects, uses and protects the personal information you share through our website."
    crumbs = [("Home", ""), ("Privacy Policy", "privacy-policy")]
    body = head(ctx, title, desc, "zyrostyle privacy policy", page_schema(ctx, title, desc, crumbs)) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Legal", "Privacy <em>Policy.</em>", "Last updated: " + date.today().strftime("%d %B %Y"), crumbs,
                 ctas=[("Contact Us", "contact", "btn-light")])
    body += f"""<section class="section"><div class="wrap prose">
<p><strong>Who we are.</strong> Zyrostyle is a digital marketing agency based in Patna, Bihar, India. This policy explains how we handle personal information submitted through this website.</p>
<p><strong>Information we collect.</strong> When you submit an enquiry, we collect the details you provide — such as your name, company, website, phone/WhatsApp number, email address, services of interest, budget range and business goals.</p>
<p><strong>How we use it.</strong> We use this information only to respond to your enquiry, prepare proposals and provide services you request. We do not sell your personal information.</p>
<p><strong>Analytics and cookies.</strong> We may use privacy-respecting analytics (such as Google Analytics) to understand how visitors use our website. You can control cookies through your browser settings.</p>
<p><strong>Data retention and security.</strong> We keep enquiry information only as long as needed for the purposes above and apply reasonable safeguards to protect it, in line with applicable Indian law, including the Digital Personal Data Protection Act, 2023.</p>
<p><strong>Your rights.</strong> You may request access to, correction of, or deletion of your personal information by emailing <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
<p><strong>Changes.</strong> We may update this policy from time to time. The latest version will always be available on this page.</p>
</div></section>
"""
    body += "</main>\n" + footer(ctx)
    write("privacy-policy", body, "0.3")


def build_404():
    ctx = Ctx("")
    ctx.pre = "/"  # served from any depth by the host, so use root-relative links
    title = "Page Not Found | Zyrostyle"
    desc = "The page you were looking for could not be found."
    body = head(ctx, title, desc, "", page_schema(ctx, title, desc, None), robots="noindex, follow") + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "404", "This page got lost. <em>Your customers shouldn't.</em>",
                 "The page you were looking for doesn't exist or has moved. Let's get you back on track.",
                 ctas=[("Back to Home", "", "btn-light"), ("Explore Services", "services", "btn-line")], sub=False, photo="creative-idea-bulb")
    body += "</main>\n" + footer(ctx)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(body)


def build_meta_files():
    urls = "".join(f"  <url><loc>{canonical(s)}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n"
                   for s, p in PAGES)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /build/\nDisallow: /docs/\n\nSitemap: {BASE}/sitemap.xml\n")
    # llms.txt — concise, citable summary for AI crawlers (GEO)
    lines = [f"# {SITE['name']}", "",
             f"> {SITE['name']} is an award-winning content marketing, SEO and digital marketing agency based in Patna, Bihar, India. "
             "It helps brands build organic growth engines that drive traffic, leads and revenue through SEO, GEO, AEO, "
             "content creation, content strategy, content marketing, social media marketing and performance advertising.", "",
             f"- Location: {SITE['locality']}, {SITE['region']}, India (serving all of Bihar and India)",
             f"- Contact: {SITE['email']}" + (f", {SITE['phone']}" if SITE["phone"] else ""),
             "- Languages: English, Hindi, Hinglish",
             "- Industries: healthcare, real estate, education & coaching, hospitality, retail & e-commerce, travel, startups & B2B", "",
             "## Services", ""]
    lines += [f"- [{s['card_title']}]({canonical(s['slug'])}): {s['card_text']}" for s in SERVICES]
    lines += [f"- [{AI_SEARCH['nav']}]({canonical(AI_SEARCH['slug'])}): {AI_SEARCH['description']}", "", "## Patna guides", ""]
    lines += [f"- [{l['primary'].title()}]({canonical(l['slug'])}): {l['hub']}" for l in LANDINGS]
    for key, title, parent, pages in CLUSTERS:
        lines += ["", f"## {strip_tags(title).replace('&amp;', '&')}", ""]
        lines += [f"- [{p['nav']}]({canonical(p['slug'])}): {p['description']}" for p in pages]
    lines += ["", "## Company", "",
              f"- [About]({canonical('about')})", f"- [Industries]({canonical('industries')})",
              f"- [Areas we serve]({canonical('areas-we-serve')})", f"- [Contact]({canonical('contact')})", ""]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── HIGH-INTENT LANDING PAGES ────────────────────────────────────────────────
def packages_html(ctx):
    cards = []
    for p in PACKAGES:
        price = f'<p class="pkg-price">{esc(p["price"])}</p>' if p["price"] else '<p class="pkg-price muted">Custom quote</p>'
        pts = "".join(f"<li>{x}</li>" for x in p["points"])
        cards.append(f"""<article class="card pkg reveal"><span class="num">{p['sub']}</span><h3>{p['name']}</h3>{price}
<p>{p['for']}</p><ul>{pts}</ul><a class="btn btn-dark btn-sm" href="{ctx.href('contact')}">Get {p['name']} Quote</a></article>""")
    return f'<div class="grid-3">{"".join(cards)}</div>'


def section_html(ctx, sec, idx):
    t = sec["type"]
    cls = ["", "warm", "", "stone"][idx % 4]
    label = sec.get("label", "")
    h2 = sec.get("h2", "")
    lead = f'<p class="lead">{sec["lead"]}</p>' if sec.get("lead") else "<div></div>"
    headblock = f'<div class="section-head reveal"><div><span class="label">{label}</span><h2 class="h-lg">{h2}</h2></div>{lead}</div>'
    if t == "process":
        return process_section()
    if t == "prose":
        paras = "".join(f"<p>{p}</p>" for p in sec["paras"])
        return f"""<section class="section {cls}"><div class="wrap grid-2">
<div class="reveal"><span class="label">{label}</span><h2 class="h-lg">{h2}</h2></div><div class="prose reveal">{paras}</div></div></section>
"""
    if t == "checklist":
        items = "".join(f"<li>{i}</li>" for i in sec["items"])
        return f'<section class="section {cls}"><div class="wrap">{headblock}<ul class="check-list reveal">{items}</ul></div></section>\n'
    if t == "numlist":
        items = "".join(f'<li><span class="n">{i+1:02d}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(sec["items"]))
        return f"""<section class="section {cls}"><div class="wrap grid-2">
<div class="reveal"><span class="label">{label}</span><h2 class="h-lg">{h2}</h2>{('<p class="lead" style="margin-top:24px">' + sec['lead'] + '</p>') if sec.get('lead') else ''}
<div class="btn-row"><a class="btn btn-dark" href="{ctx.href('contact')}">Get Your Free Consultation</a></div></div>
<ul class="num-list reveal">{items}</ul></div></section>
"""
    if t == "cards":
        cards = []
        for c in sec["cards"]:
            pts = "".join(f"<li>{x}</li>" for x in (c[2] if len(c) > 2 else []))
            cards.append(f'<article class="card reveal"><h3>{c[0]}</h3><p>{c[1]}</p>{"<ul>" + pts + "</ul>" if pts else ""}</article>')
        grid = "grid-4" if len(cards) == 4 else "grid-3"
        return f'<section class="section {cls}"><div class="wrap">{headblock}<div class="{grid}">{"".join(cards)}</div></div></section>\n'
    if t == "table":
        th = "".join(f'<th scope="col">{h}</th>' for h in sec["head"])
        rows = "".join("<tr>" + "".join((f'<th scope="row">{c}</th>' if j == 0 else f"<td>{c}</td>") for j, c in enumerate(r)) + "</tr>" for r in sec["rows"])
        return f"""<section class="section {cls}"><div class="wrap">{headblock}
<div class="table-wrap reveal"><table class="data-table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div></div></section>
"""
    if t == "packages":
        note = '<p class="form-note reveal" style="margin-top:20px">Ad spend is paid directly to Google/Meta and is not included in management fees. All packages are customised after a free consultation.</p>'
        return f'<section class="section {cls}"><div class="wrap">{headblock}{packages_html(ctx)}{note}</div></section>\n'
    if t == "tiers":
        cards = []
        for p in sec["tiers"]:
            pts = "".join(f"<li>{x}</li>" for x in p["points"])
            cards.append(f"""<article class="card pkg reveal"><span class="num">{p['sub']}</span><h3>{p['name']}</h3><p class="pkg-price muted">Custom quote</p>
<p>{p['for']}</p><ul>{pts}</ul><a class="btn btn-dark btn-sm" href="{ctx.href('contact')}">Get {p['name']} Quote</a></article>""")
        note = '<p class="form-note reveal" style="margin-top:20px">Every plan is customised after a free consultation. Ad budgets are paid directly to the platform and kept separate from fees.</p>'
        return f'<section class="section {cls}"><div class="wrap">{headblock}<div class="grid-3">{"".join(cards)}</div>{note}</div></section>\n'
    if t == "curriculum":
        mods = "".join(f'<li><span class="n">Module {i+1:02d}</span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(COURSE_MODULES))
        return f'<section class="section {cls}"><div class="wrap">{headblock}<ol class="curriculum reveal">{mods}</ol></div></section>\n'
    if t == "coursefacts":
        facts = [("Duration", COURSE["duration"] or "Contact us for batch options"),
                 ("Format", COURSE["mode"]),
                 ("Fee", COURSE["fee"] or "Contact us for current fees"),
                 ("Next batch", COURSE["next_batch"] or "Enquire for the next start date")]
        f = "".join(f"<div><span>{a}</span><strong>{b}</strong></div>" for a, b in facts)
        return f'<section class="section tight"><div class="wrap"><div class="strip facts reveal">{f}</div></div></section>\n'
    if t == "areas":
        blocks = "".join(f'<div class="area-block reveal"><h3>{a}</h3><p>{b}</p></div>' for a, b in sec["items"])
        return f"""<section class="section {cls}"><div class="wrap grid-2">
<div class="reveal"><span class="label">{label}</span><h2 class="h-lg">{h2}</h2></div><div>{blocks}</div></div></section>
"""
    raise ValueError(t)


def landing_schema_extra(l):
    url = canonical(l["slug"])
    kind = l.get("schema")
    if kind == "service":
        sv = service_schema(l["primary"].title(), l["slug"], l["service_type"], l["description"])
        if l.get("area"):
            sv["areaServed"] = [{"@type": "Place", "name": l["area"]}, {"@type": "City", "name": "Patna"}]
        return [sv]
    if kind == "course":
        c = {"@type": "Course", "@id": url + "#course", "name": proper(l["primary"]) if l.get("cluster") else "Digital Marketing Course in Patna",
             "description": l["description"], "url": url, "inLanguage": ["en-IN", "hi-IN"],
             "provider": {"@id": ORG_ID},
             "syllabusSections": [{"@type": "Syllabus", "name": a, "description": b} for a, b in COURSE_MODULES],
             "hasCourseInstance": [{"@type": "CourseInstance", "courseMode": m, "location": "Patna, Bihar"}
                                   for m in ("Onsite", "Online")]}
        if COURSE["fee"]:
            c["offers"] = {"@type": "Offer", "category": "Paid", "priceCurrency": "INR", "description": COURSE["fee"]}
        return [c]
    if kind == "article":
        return [{"@type": "Article", "@id": url + "#article", "headline": strip_tags(l["h1"]), "description": l["description"],
                 "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "dateModified": TODAY, "mainEntityOfPage": url}]
    if kind == "org":
        return [{"@type": "EducationalOrganization", "@id": url + "#academy", "name": "Zyrostyle Academy",
                 "url": url, "parentOrganization": {"@id": ORG_ID},
                 "address": {"@type": "PostalAddress", "addressLocality": "Patna", "addressRegion": "Bihar", "addressCountry": "IN"}}]
    return []


def proper(kw):
    out = kw[0].upper() + kw[1:]
    for a, b in [("patna", "Patna"), ("b2b", "B2B"), ("boring road", "Boring Road"), ("kankarbagh", "Kankarbagh"), ("bihar", "Bihar")]:
        out = out.replace(a, b)
    return out


def build_landing(l):
    ctx = Ctx(l["slug"])
    if l.get("parent"):
        par = l["parent"]
        crumbs = [("Home", ""), ("Services", "services"), (NAMES[par], par), (l["nav"], l["slug"])]
        if par in ("industries", "areas-we-serve"):
            crumbs = [("Home", ""), (NAMES[par], par), (l["nav"], l["slug"])]
        if not l.get("related"):
            sib = [p["slug"] for p in CHILDREN[par] if p["slug"] != l["slug"]]
            i0 = [p["slug"] for p in CHILDREN[par]].index(l["slug"])
            l["related"] = [par] + (sib[i0:] + sib[:i0])[:4]
    else:
        crumbs = [("Home", ""), ("Patna Hub", "digital-marketing-patna-guide"), (l["primary"].title(), l["slug"])]
    schema = page_schema(ctx, l["title"], l["description"], crumbs, landing_schema_extra(l), l["faqs"])
    body = head(ctx, l["title"], l["description"], l["keywords"], schema) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, l["eyebrow"], l["h1"], l["lead"], crumbs, strap=l.get("strap"),
                 ctas=l.get("ctas") or [("Get Your Free Consultation", "contact", "btn-light"), ("Read FAQs", "#faq", "btn-line")],
                 meta=["Patna, Bihar", "Award-Winning Agency", "Transparent Reporting"])
    for i, sec in enumerate(l["sections"]):
        body += section_html(ctx, sec, i)
        if i == 0:
            body += img_band(ctx, l.get("strap") or "Get Found. Get Noticed. Get Chosen.", label=proper(l["primary"]))
    body += faq_section(l["faqs"], title=f"{esc(proper(l['primary']))} — <em>FAQs.</em>")
    rel = "".join(f'<li><a href="{ctx.href(r)}">{esc(NAMES[r])}</a></li>' for r in l["related"])
    if not l.get("parent"):
        rel += f'<li><a href="{ctx.href("digital-marketing-patna-guide")}">All Patna Guides</a></li>'
    body += f'<section class="section tight"><div class="wrap"><span class="label reveal">Related</span><ul class="related reveal">{rel}</ul></div></section>\n'
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write(l["slug"], body, "0.8")


HUB_GROUPS = [
    ("Choosing an Agency", ["digital-marketing-agency-patna", "best-digital-marketing-company-patna", "top-digital-marketing-agencies-patna",
                            "full-service-digital-marketing-firm-patna", "online-marketing-agency-patna", "digital-marketing-expert-patna"]),
    ("Pricing &amp; Small Business", ["digital-marketing-packages-cost-patna", "cheap-digital-marketing-services-patna",
                                     "digital-marketing-small-business-patna", "freelance-digital-marketer-patna"]),
    ("Leads &amp; B2B", ["lead-generation-agency-patna", "b2b-digital-marketing-agency-patna", "services"]),
    ("Near You in Patna", ["digital-marketing-agency-near-me-patna", "digital-marketing-company-boring-road-patna",
                           "digital-marketing-company-kankarbagh-patna", "areas-we-serve"]),
    ("Learn Digital Marketing", ["digital-marketing-course-patna", "digital-marketing-institute-patna"]),
]


def build_hub():
    ctx = Ctx("digital-marketing-patna-guide")
    title = "Patna Digital Marketing Hub | Agencies, Costs, Courses & Local Guides"
    desc = "Everything Patna businesses search for in digital marketing — choosing an agency, package costs, lead generation, local services and courses, in one place."
    kw = ", ".join(l["primary"] for l in LANDINGS)
    crumbs = [("Home", ""), ("Patna Hub", "digital-marketing-patna-guide")]
    by = {l["slug"]: l for l in LANDINGS}
    order = [sl for _, g in HUB_GROUPS for sl in g]
    extra = [{"@type": "ItemList", "name": "Digital marketing in Patna — guides and services", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": canonical(sl), "name": NAMES[sl]} for i, sl in enumerate(order)]}]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, extra, page_type="CollectionPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Patna Digital Marketing Hub", "Everything Patna searches for <em>in digital marketing.</em>",
                 "Agencies, costs, local services, lead generation and courses — answered honestly by Zyrostyle, an award-winning content marketing and SEO agency in Patna, Bihar.",
                 crumbs, strap="Get Found. Get Noticed. Get Chosen.")
    for i, (gname, slugs) in enumerate(HUB_GROUPS):
        cards = []
        for sl in slugs:
            if sl in by:
                blurb = by[sl]["hub"]
            elif sl in SVC:
                blurb = SVC[sl]["card_text"]
            else:
                blurb = {"services": "All Zyrostyle digital marketing services in Patna — SEO, content, social, ads, GEO & AEO.",
                         "areas-we-serve": "Every Patna neighbourhood and Bihar city we serve."}.get(sl, "")
            cards.append(f'<article class="card service-card reveal"><h3><a href="{ctx.href(sl)}" style="text-decoration:none">{esc(NAMES[sl])}</a></h3><p>{blurb}</p><a class="link-arrow" href="{ctx.href(sl)}">Read more</a></article>')
        cls = "warm" if i % 2 else ""
        body += f'<section class="section {cls}"><div class="wrap"><div class="section-head single reveal"><div><span class="label">{i+1:02d}</span><h2 class="h-lg">{gname}</h2></div></div><div class="grid-3">{"".join(cards)}</div></div></section>\n'
    body += mega_marquee()
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write("digital-marketing-patna-guide", body, "0.8")


if __name__ == "__main__":
    build_home()
    build_services_hub()
    for svc in SERVICES:
        build_service(svc)
    build_ai_search()
    for land in LANDINGS:
        build_landing(land)
    for cp in CLUSTER_PAGES:
        build_landing(cp)
    build_hub()
    build_industries()
    build_areas()
    build_about()
    build_contact()
    build_privacy()
    build_404()
    build_meta_files()
    print(f"Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt, llms.txt")
