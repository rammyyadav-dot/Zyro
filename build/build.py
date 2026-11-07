#!/usr/bin/env python3
"""
Static site generator for zytrostyle.

    python3 build/build.py

Writes clean-URL pages (slug/index.html), sitemap.xml, robots.txt and llms.txt
into the repository root. All copy lives in build/content.py.
"""
import html
import json
import os
from datetime import date

from content import (AI_SEARCH, AREAS, BIHAR_CITIES, HOME_FAQS, INDUSTRIES, PATNA_AREAS,
                     PILLARS, PROCESS, SERVICES, SITE, TICKER, WHY)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = SITE["url"].rstrip("/")
TODAY = date.today().isoformat()
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;"
         "1,300;1,400&family=Barlow:wght@300;400;500&family=Barlow+Condensed:wght@400;500&display=swap")
SVC = {s["slug"]: s for s in SERVICES}
NAMES = {**{s["slug"]: s["nav"] for s in SERVICES}, AI_SEARCH["slug"]: AI_SEARCH["nav"],
         "industries": "Industries", "services": "Services", "areas-we-serve": "Areas We Serve",
         "about": "About", "contact": "Contact", "": "Home", "privacy-policy": "Privacy Policy"}
ORG_ID = BASE + "/#organization"
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
        "description": ("Zytrostyle is an award-winning content marketing and SEO agency in Patna, Bihar, "
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
<link rel="stylesheet" href="{ctx.asset('css/style.css')}">
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def nav(ctx):
    def cur(s):
        return ' aria-current="page"' if ctx.slug == s else ""
    sub = "".join(f'<li><a href="{ctx.href(s["slug"])}"{cur(s["slug"])}>{s["nav"]}</a></li>' for s in SERVICES)
    sub += f'<li><a href="{ctx.href(AI_SEARCH["slug"])}"{cur(AI_SEARCH["slug"])}>{AI_SEARCH["nav"]}</a></li>'
    return f"""<header class="site-header">
  <nav class="nav" aria-label="Main">
    <a class="nav-logo" href="{ctx.href('')}" aria-label="Zytrostyle home">Zytrostyle</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu">Menu</button>
    <div class="nav-menu" id="nav-menu">
      <ul class="nav-links">
        <li class="has-sub"><a href="{ctx.href('services')}"{cur('services')}>Services</a><ul class="subnav">{sub}</ul></li>
        <li><a href="{ctx.href('industries')}"{cur('industries')}>Industries</a></li>
        <li><a href="{ctx.href('areas-we-serve')}"{cur('areas-we-serve')}>Patna &amp; Bihar</a></li>
        <li><a href="{ctx.href('about')}"{cur('about')}>About</a></li>
        <li><a class="btn btn-dark btn-sm nav-cta" href="{ctx.href('contact')}">Free Consultation</a></li>
      </ul>
    </div>
  </nav>
</header>
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
    wa = ""
    if SITE["whatsapp"]:
        wa = (f'<a class="float-wa" href="https://wa.me/{SITE["whatsapp"]}?text='
              f'{esc("Hi Zytrostyle, I would like a free marketing consultation.")}" '
              f'rel="noopener" target="_blank">WhatsApp Us</a>')
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <p class="footer-brand">Zytrostyle</p>
        <p class="footer-strap">{SITE['tagline']}</p>
        <p class="footer-about">Zytrostyle is an award-winning digital marketing, SEO, content strategy, content creation and social media marketing agency serving businesses in Patna, Bihar and across India.</p>
      </div>
      <div>
        <p class="footer-title">Services</p>
        <ul class="footer-links">{svc}</ul>
      </div>
      <div>
        <p class="footer-title">Quick Links</p>
        <ul class="footer-links">
          <li><a href="{ctx.href('')}">Home</a></li>
          <li><a href="{ctx.href('about')}">About Zytrostyle</a></li>
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
    <p class="footer-services">SEO · Local SEO · GEO · AEO · Content Creation · Content Strategy · Content Marketing · Digital Marketing · Social Media Marketing · Lead Generation · Google Ads · Meta Ads<br>Service location: Patna, Bihar, India — serving {", ".join(PATNA_AREAS[:6])} &amp; all of Bihar</p>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Zytrostyle. All rights reserved.</span>
      <span><a href="{ctx.href('privacy-policy')}">Privacy Policy</a> · <a href="{ctx.pre}sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>
{wa}
<script src="{ctx.asset('js/main.js')}" defer></script>
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


def hero(ctx, eyebrow, h1, lead, crumbs=None, strap=None, ctas=None, meta=None, sub=True):
    bc = f'<nav aria-label="Breadcrumb">{breadcrumb(ctx, crumbs)}</nav>' if crumbs else ""
    strap_html = f'<p class="hero-strap">{strap}</p>' if strap else ""
    ctas = ctas or [("Get Your Free Marketing Consultation", "contact", "btn-light"),
                    ("Explore Our Services", "services", "btn-line")]
    btns = "".join(f'<a class="btn {c}" href="{ctx.href(s)}">{t}</a>' for t, s, c in ctas)
    meta_html = ("<div class=\"hero-meta\">" + "".join(f"<span>{m}</span>" for m in meta) + "</div>") if meta else ""
    return f"""<section class="hero dark{' sub' if sub else ''}">
  <div class="wrap hero-inner">
    {bc}
    <span class="eyebrow">{eyebrow}</span>
    <h1 class="h-xl">{h1}</h1>
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
      <span class="label">Why Choose Zytrostyle</span>
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
        cards.append(f"""<article class="card reveal"><span class="num">{i+1:02d}</span><h3>{name}</h3><p>{short}</p>
<a class="link-arrow" href="{ctx.href('industries')}#{key}">Learn more</a></article>""")
    return f'<div class="grid-3">{"".join(cards)}</div>'


def locations_section(ctx, cls="stone"):
    p = "".join(f"<li>{a}</li>" for a in PATNA_AREAS)
    b = "".join(f"<li>{c}</li>" for c in BIHAR_CITIES)
    return f"""<section class="section {cls}">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">Digital Marketing Agency Serving Patna &amp; Bihar</span><h2 class="h-lg">Local understanding. <em>Bigger ambitions.</em></h2></div>
      <p class="lead">Zytrostyle provides digital marketing, content creation, SEO and social media marketing for businesses targeting Patna and wider Bihar — in English, Hindi or Hinglish.</p>
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
      <p class="tagline">Zytrostyle — Make Your Brand Impossible to Ignore.</p>
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
    title = "Zytrostyle | Award-Winning Digital Marketing & SEO Agency in Patna"
    desc = ("Award-winning content marketing & SEO agency in Patna, Bihar. SEO, GEO, content, social media & Google Ads "
            "that drive traffic, leads and revenue.")
    kw = ("digital marketing agency in patna, best digital marketing company in patna, seo company in patna, "
          "content marketing agency in patna, social media marketing agency in patna, digital marketing services patna, "
          "seo services in patna, top digital marketing agency in patna, lead generation agency in patna, bihar")
    pillars = "".join(f'<div class="pillar"><h3>{n}</h3><p>{d}</p></div>' for n, d in PILLARS)
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, None, faqs=HOME_FAQS)) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Award-Winning Marketing Agency in Patna · Digital Marketing • SEO • Content Marketing • Creative Growth",
                 "Digital Marketing &amp; SEO Agency in Patna That Turns Visibility <em>Into Growth.</em>",
                 "We are an award-winning content marketing and SEO agency, helping brands build organic growth engines that drive traffic, leads and revenue. Zytrostyle helps businesses in Patna and across Bihar get discovered, earn trust and turn marketing into a powerful engine for sustainable growth.",
                 strap="Get Found. Get Noticed. Get Chosen.",
                 meta=["Patna, Bihar", "SEO · GEO · AEO", "Content-Led Growth", "English · Hindi · Hinglish"],
                 sub=False)
    body += ticker()
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <span class="label">We Don't Just Market Brands. We Make Them Matter.</span>
      <h2 class="h-lg">A content-led growth partner <em>for ambitious brands.</em></h2>
    </div>
    <div class="prose reveal">
      <p>Zytrostyle is a content-led <strong>digital marketing and SEO agency in Patna, Bihar</strong>, helping businesses increase their online visibility, attract qualified customers and turn marketing into a powerful engine for sustainable growth.</p>
      <p>We bring together <strong>Search Engine Optimisation (SEO)</strong>, <strong>Generative Engine Optimisation (GEO)</strong>, <strong>Answer Engine Optimisation (AEO)</strong>, content marketing, creative storytelling, social media and performance advertising to help ambitious brands compete, connect and convert.</p>
      <p>Whether you are a startup building your first digital presence, a local business looking for more customers, or an established company ready to scale across Bihar and India, we create marketing strategies aligned with your business goals.</p>
      <p class="tagline">Your customers are searching. Make sure they find you.</p>
    </div>
  </div>
</section>
<section class="section warm">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">Your Brand Deserves More Than Just Visibility</span><h2 class="h-lg">It deserves <em>market leadership.</em></h2></div>
      <div class="prose"><p>Every day, potential customers search Google, explore social media, compare brands, read reviews and increasingly turn to AI-powered search tools before making purchasing decisions. The real challenge is not simply appearing online — it's being discovered by the right audience, trusted at the right moment and chosen over your competitors.</p></div>
    </div>
    <div class="pillars reveal">{pillars}</div>
    <p class="tagline reveal">Because great marketing doesn't just attract attention. It creates commercial momentum.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">Our Services — Everything Your Brand Needs to Grow</span><h2 class="h-lg">One growth partner. <em>Six connected capabilities.</em></h2></div>
      <p class="lead">We connect content, search, creativity and paid media to build a complete digital growth engine for businesses in Patna, Bihar and across India.</p>
    </div>
    {service_cards(ctx)}
  </div>
</section>
"""
    body += triad_section(ctx)
    body += why_section()
    body += f"""<section class="section warm">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="label">Digital Marketing Solutions for Patna's Growing Businesses</span><h2 class="h-lg">Every industry has a different audience. <em>Every brand deserves a smarter strategy.</em></h2></div>
      <p class="lead">From Boring Road to Kankarbagh, from Patna to markets across Bihar — we help businesses communicate, compete and grow.</p>
    </div>
    {industries_cards(ctx, 6)}
    <div class="btn-row reveal"><a class="btn btn-dark" href="{ctx.href('industries')}">Discuss Your Industry</a></div>
  </div>
</section>
"""
    body += process_section()
    body += locations_section(ctx)
    body += faq_section(HOME_FAQS, cls="")
    body += cta_section(ctx)
    body += f"""<section class="section warm" id="consultation">
  <div class="wrap grid-2">
    <div class="reveal">
      <span class="label">Request Your Free Marketing Consultation</span>
      <h2 class="h-lg">Let's grow <em>your business.</em></h2>
      <p class="lead" style="margin-top:24px">Share a few details and a Zytrostyle strategist will get back to you with ideas tailored to your business, audience and goals.</p>
    </div>
    <div class="reveal">{enquiry_form(ctx, heading=False)}</div>
  </div>
</section>
"""
    body += "</main>\n" + footer(ctx)
    write("", body, "1.0")


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
<section class="section warm">
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
    desc = ("Explore Zytrostyle's services in Patna: SEO, content creation, content strategy, content marketing, "
            "digital marketing, social media marketing, GEO and AEO.")
    kw = "digital marketing services patna, seo services in patna, content marketing services in patna, social media marketing services patna, content creation services in patna"
    crumbs = [("Home", ""), ("Services", "services")]
    extra = [{"@type": "ItemList", "name": "Zytrostyle services", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": canonical(s["slug"]), "name": s["card_title"]}
        for i, s in enumerate(SERVICES)]}]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, extra, page_type="CollectionPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Our Services", "Everything your brand needs <em>to grow.</em>",
                 "One growth partner. Six connected marketing capabilities. We connect content, search, creativity and paid media to build a complete digital growth engine for businesses in Patna, Bihar and across India.",
                 crumbs, ctas=[("Get Your Free Consultation", "contact", "btn-light"), ("Explore Industries", "industries", "btn-line")])
    body += f'<section class="section"><div class="wrap">{service_cards(ctx)}</div></section>\n'
    body += triad_section(ctx)
    body += why_section("warm")
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
                 "From hospitals on Bailey Road to coaching institutes on Boring Road and real-estate projects near Saguna More, Zytrostyle builds marketing strategies around how your specific customers search, compare and decide.",
                 crumbs, ctas=[("Discuss Your Industry", "contact", "btn-light"), ("Explore Services", "services", "btn-line")])
    for i, (key, name, short, long, pts) in enumerate(INDUSTRIES):
        cls = "warm" if i % 2 == 0 else ""
        li = "".join(f"<li>{p}</li>" for p in pts)
        body += f"""<section class="section {cls}" id="{key}">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">{i+1:02d} — Industry</span><h2 class="h-lg">{name}</h2><p class="tagline">{short}</p></div>
    <div class="reveal"><div class="prose"><p>{long}</p></div><ul class="check-list" style="columns:1;margin-top:20px">{li}</ul>
      <div class="btn-row"><a class="btn btn-dark btn-sm" href="{ctx.href('contact')}">Plan My {name.split(',')[0].split('&')[0].strip()} Marketing</a></div></div>
  </div>
</section>
"""
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
                 "Zytrostyle provides digital marketing, SEO, content creation and social media marketing for businesses targeting Patna and wider Bihar. Whether your customers search in English, Hindi or Hinglish, we build content around their language, interests and intent.",
                 crumbs, strap="Patna Ki Soch. Brand Ki Badi Udaan.",
                 ctas=[("Talk to a Marketing Strategist", "contact", "btn-light"), ("Explore Services", "services", "btn-line")])
    blocks = "".join(f'<div class="area-block reveal"><h3>Digital marketing in {n}</h3><p>{d}</p></div>' for n, d in AREAS)
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal" style="position:sticky;top:110px"><span class="label">Patna Neighbourhoods</span><h2 class="h-lg">From Boring Road <em>to Danapur.</em></h2>
      <div class="prose" style="margin-top:24px"><p>Every Patna neighbourhood has its own customer mix. Our local SEO, Google Maps optimisation and geo-targeted advertising are tuned to the localities where your customers actually live, work and shop.</p></div></div>
    <div>{blocks}</div>
  </div>
</section>
"""
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
        ("Do you only work with businesses in Patna?", "No. Zytrostyle is based in Patna and works with businesses across Bihar and India. Many of our strategies help Patna businesses reach customers in other Bihar districts and help Bihar brands scale nationally."),
        ("Can you help my business rank in a specific Patna locality?", "Yes. Through Google Business Profile optimisation, locality-relevant content, local citations and review strategy, we help businesses improve visibility for searches in specific areas such as Boring Road, Kankarbagh or Patliputra Colony."),
        ("Do you create Hindi and Hinglish content for Bihar audiences?", "Yes. We create English, Hindi and Hinglish content depending on how your audience searches and engages."),
    ]
    body += faq_section(faqs, cls="")
    body += cta_section(ctx)
    body += "</main>\n" + footer(ctx)
    write("areas-we-serve", body, "0.8")


def build_about():
    ctx = Ctx("about")
    title = "About Zytrostyle | Award-Winning Content Marketing Agency, Patna"
    desc = ("Zytrostyle is an award-winning content marketing and SEO agency in Patna, Bihar, building organic "
            "growth engines for ambitious brands.")
    kw = "about zytrostyle, content marketing agency patna, award winning marketing agency patna, seo agency bihar, digital marketing expert in patna"
    crumbs = [("Home", ""), ("About", "about")]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, page_type="AboutPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "About Zytrostyle", "We don't just market brands. <em>We make them matter.</em>",
                 "Zytrostyle is an award-winning content marketing and SEO agency in Patna, helping brands build organic growth engines that drive traffic, leads and revenue.",
                 crumbs, ctas=[("Work With Us", "contact", "btn-light"), ("Explore Services", "services", "btn-line")])
    body += f"""<section class="section">
  <div class="wrap grid-2">
    <div class="reveal"><span class="label">Our Story</span><h2 class="h-lg">Born in Patna. <em>Built for growth.</em></h2></div>
    <div class="prose reveal">
      <p>Zytrostyle was founded on a simple belief: businesses in Patna and Bihar deserve marketing that is as strategic, creative and measurable as anything produced in India's biggest metros.</p>
      <p>Too many local businesses were stuck with disconnected vendors — one for the website, another for social media, someone else for ads — and no one accountable for growth. We built Zytrostyle as <strong>one connected growth partner</strong>: strategy, content, search, social and performance working together.</p>
      <p>Today we help startups, local businesses and established companies across healthcare, education, real estate, hospitality, retail, travel and B2B get found, get noticed and get chosen.</p>
      <p class="tagline">Built for Visibility. Designed for Growth.</p>
    </div>
  </div>
</section>
<section class="section dark manifesto">
  <div class="wrap reveal">
    <span class="label">The Zytrostyle Philosophy</span>
    <h2 class="h-lg">"Great marketing doesn't just attract attention. <em>It creates commercial momentum."</em></h2>
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
    title = "Contact Zytrostyle | Free Marketing Consultation in Patna, Bihar"
    desc = ("Request a free digital marketing, SEO or social media consultation with Zytrostyle in Patna, Bihar. "
            "Get a custom marketing proposal for your business.")
    kw = "contact digital marketing agency patna, free seo consultation patna, digital marketing strategy consultation patna, marketing agency near me patna"
    crumbs = [("Home", ""), ("Contact", "contact")]
    body = head(ctx, title, desc, kw, page_schema(ctx, title, desc, crumbs, page_type="ContactPage")) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Free Marketing Consultation", "Let's build your next <em>growth story.</em>",
                 "Your next customer could already be searching for a business like yours. Tell us about your goals and a Zytrostyle strategist will respond within one working day.",
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
        ("What happens after I submit the form?", "A Zytrostyle strategist reviews your details, may run a quick audit of your website and online presence, and contacts you within one working day to schedule a free consultation call."),
        ("Is the consultation really free?", "Yes. The initial consultation is free and comes with no obligation. If there is a fit, we follow up with a custom marketing proposal."),
        ("Can we meet in person in Patna?", "Yes. We are happy to meet clients in Patna, and we also work remotely with businesses across Bihar and India."),
    ]
    body += faq_section(faqs)
    body += "</main>\n" + footer(ctx)
    write("contact", body, "0.7")


def build_privacy():
    ctx = Ctx("privacy-policy")
    title = "Privacy Policy | Zytrostyle"
    desc = "How Zytrostyle collects, uses and protects the personal information you share through our website."
    crumbs = [("Home", ""), ("Privacy Policy", "privacy-policy")]
    body = head(ctx, title, desc, "zytrostyle privacy policy", page_schema(ctx, title, desc, crumbs)) + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "Legal", "Privacy <em>Policy.</em>", "Last updated: " + date.today().strftime("%d %B %Y"), crumbs,
                 ctas=[("Contact Us", "contact", "btn-light")])
    body += f"""<section class="section"><div class="wrap prose">
<p><strong>Who we are.</strong> Zytrostyle is a digital marketing agency based in Patna, Bihar, India. This policy explains how we handle personal information submitted through this website.</p>
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
    title = "Page Not Found | Zytrostyle"
    desc = "The page you were looking for could not be found."
    body = head(ctx, title, desc, "", page_schema(ctx, title, desc, None), robots="noindex, follow") + nav(ctx)
    body += '<main id="main">\n'
    body += hero(ctx, "404", "This page got lost. <em>Your customers shouldn't.</em>",
                 "The page you were looking for doesn't exist or has moved. Let's get you back on track.",
                 ctas=[("Back to Home", "", "btn-light"), ("Explore Services", "services", "btn-line")], sub=False)
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
    lines += [f"- [{AI_SEARCH['nav']}]({canonical(AI_SEARCH['slug'])}): {AI_SEARCH['description']}", "", "## Company", "",
              f"- [About]({canonical('about')})", f"- [Industries]({canonical('industries')})",
              f"- [Areas we serve]({canonical('areas-we-serve')})", f"- [Contact]({canonical('contact')})", ""]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    build_home()
    build_services_hub()
    for svc in SERVICES:
        build_service(svc)
    build_ai_search()
    build_industries()
    build_areas()
    build_about()
    build_contact()
    build_privacy()
    build_404()
    build_meta_files()
    print(f"Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt, llms.txt")
