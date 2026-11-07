# Zyrostyle website

A multi-page static website for **Zyrostyle**, an award-winning content marketing, SEO and digital marketing agency in Patna, Bihar. It is built for SEO, local SEO with geo tags, GEO (AI search) and AEO (answer engines).

## Pages

| URL | Purpose |
|---|---|
| `/` | Home: hero, services, SEO/GEO/AEO, why us, industries, process, locations, FAQ, enquiry form |
| `/services/` | Hub page for all services |
| `/seo-services-patna/` | SEO, local SEO, Google Business Profile |
| `/content-creation-services-patna/` | Copywriting, Reels, video, design |
| `/content-strategy-patna/` | Positioning, personas, calendars |
| `/content-marketing-services-patna/` | SEO content, B2B content, email, inbound marketing |
| `/digital-marketing-agency-patna/` | Google Ads, Meta Ads, lead generation |
| `/social-media-marketing-patna/` | Instagram, Facebook, LinkedIn, influencers |
| `/ai-search-optimisation-geo-aeo/` | GEO and AEO |
| `/industries/` | Healthcare, real estate, education, hospitality, retail, travel, B2B |
| `/areas-we-serve/` | Patna neighbourhoods and Bihar cities |
| `/about/`, `/contact/`, `/privacy-policy/`, `404.html` | |

The build also produces `sitemap.xml`, `robots.txt` and `llms.txt`. The keyword strategy is in [`docs/seo-keyword-map.md`](docs/seo-keyword-map.md).

## Editing

All copy, keywords, FAQs and business details are in `build/content.py`. The templates are in `build/build.py`. After editing, rebuild:

```bash
python3 build/build.py
```

Before launch, fill in the `SITE` block: domain, phone, WhatsApp, address, PIN code, map coordinates, social links and form endpoint. Any field left empty is omitted from both the pages and the structured data.

## Hosting

The output is plain static HTML, CSS and JS, so it works on GitHub Pages, Netlify, Vercel, Cloudflare Pages or any web host. Internal links use clean directory URLs (`/seo-services-patna/`), which need a web server. Opening the files directly with `file://` won't follow those links.
