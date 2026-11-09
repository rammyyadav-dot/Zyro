# Zyrostyle website

A multi-page static website for **Zyrostyle**, a content marketing, SEO and digital marketing agency in Patna, Bihar. It is built for SEO, local SEO with geo tags, GEO (AI search) and AEO (answer engines).

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

## Home page design and motion

- The home page is a bold editorial layout. The hero reads "We are Zyrostyle / We do big things", with photos set into the lines of type, next to the agency statements.
- Below the hero: a compact "What we do" image grid, a giant moving text band, the SEO/GEO/AEO positioning, a "Who we help" image row, the six-step process, FAQs and a gold "Want to do big things?" closing band.
- Type: Inter Tight for display headings, Cormorant italic for accents, Barlow for body text.
- `assets/js/main.js` handles all motion: hero entrance, rows that slide sideways on scroll, word reveals, moving text bands with velocity skew, parallax and the scroll progress bar. Motion turns off for visitors who set their device to reduce motion.
- CSS and JS links include a content hash (`?v=…`), so browsers never pair a new page with a cached old stylesheet.
- Photography combines the original Unsplash library with uploaded replacements; assignments and alt text live in `build/photos.py`.
- To reprocess uploaded images, install Pillow (`python3 -m pip install Pillow`), run `python3 build/prepare_images.py`, then rebuild. This preserves source files, honors image orientation, strips metadata, and creates WebP variants without upscaling. Commit the generated `assets/img/photos/uploaded.json` along with the images; normal site builds do not require Pillow.

## SEO operations

Production is Cloudflare Pages (`zyro`), deployed automatically from GitHub main. Canonical host: https://zyrostyle.com. See `docs/seo-measurement.md` for host redirects, event collection readiness, lead qualification and weekly Search Console reporting. Run `python3 scripts/check_seo.py` after rebuilding.
