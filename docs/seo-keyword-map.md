# Zyrostyle: SEO, GEO and AEO keyword map (Patna and Bihar)

Each page gets one main keyword cluster, so pages don't compete with each other for the same search. Main keywords go in the `<title>`, H1, first paragraph, meta description and URL. Secondary keywords appear naturally in the body copy, the FAQs and the "What's included" lists.

| Page (URL) | Primary keyword | Secondary / long-tail keywords |
|---|---|---|
| `/` Home | digital marketing agency in patna | best digital marketing company in patna, seo company in patna, content marketing agency in patna, award winning marketing agency patna |
| `/seo-services-patna/` | best seo company in patna / seo services in patna | seo agency in patna, local seo services patna, gmb optimization services patna, google map ranking expert patna, seo consultant in patna, affordable seo services in patna, technical seo company patna, ecommerce seo agency patna, website ranking agency patna, link building services in patna, google business profile setup patna, on page off page seo patna, organic traffic growth services patna |
| `/content-creation-services-patna/` | content creation services in patna | content writing agency in patna, video content creation agency patna, blog writing services patna, website content creation services patna, copywriter / ad copywriter in patna, reels video shoot patna, corporate video creation in patna, product photography and video patna, flyer and catalog design patna, content creation packages patna |
| `/content-strategy-patna/` | content strategy consultant patna | digital content strategy services patna, content plan for small businesses patna, content calendar creation patna, brand storytelling services patna, content strategy for coaching institutes patna, ecommerce content strategy patna |
| `/content-marketing-services-patna/` | content marketing agency in patna | content marketing services in patna, b2b content marketing agency patna, seo content marketing services patna, content distribution agency patna, inbound marketing agency patna, lead conversion content marketing patna, content marketing pricing in patna |
| `/digital-marketing-agency-patna/` | digital marketing agency in patna | best / top 10 digital marketing agency in patna, digital marketing services patna, digital marketing expert in patna, online marketing agency patna, digital marketing package cost in patna, digital marketing services for small business patna, b2b digital marketing agency patna, lead generation agency in patna, google ads agency in patna, full service digital marketing firm patna, best agency for lead generation in bihar |
| `/social-media-marketing-patna/` | social media marketing agency in patna | social media management services patna, instagram marketing agency patna, meta ads agency in patna, facebook ads expert patna, instagram reels creation service patna, social media handle manager patna, influencer marketing agency in patna, smm packages cost in patna, youtube channel promotion agency patna, restaurant social media marketing patna |
| `/ai-search-optimisation-geo-aeo/` | generative engine optimisation patna | answer engine optimisation, ai search optimisation, google ai overviews optimisation, llm seo agency bihar |
| `/industries/` | industry digital marketing patna | digital marketing services for doctors in patna, hospital digital marketing services patna, real estate digital marketing agency patna, coaching institute marketing agency patna, school promotion agency in patna, social media management for real estate patna |
| `/areas-we-serve/` | digital marketing agency patna & bihar | digital marketing company in boring road / kankarbagh / patliputra colony / saguna more patna, digital marketing services in boring canal road, Gaya / Muzaffarpur / Bhagalpur |
| `/about/`, `/contact/` | brand and conversion pages | digital marketing strategy consultation patna, free seo consultation patna |

## High-intent agency and training pages (round 2)

| # | Keyword | Page | Angle that keeps it distinct |
|---|---|---|---|
| 1 | digital marketing agency in patna | `/digital-marketing-agency-patna/` (existing) | Main service page, now linking to the new pages |
| 2 | best digital marketing company in patna | `/best-digital-marketing-company-patna/` | 8 criteria for choosing an agency, comparison table |
| 3 | digital marketing services patna | `/services/` (existing, strengthened) | New H1 and FAQ block (FAQPage schema) |
| 4 | digital marketing institute in patna | `/digital-marketing-institute-patna/` | Academy run by a working agency, training formats |
| 5 | top 10 digital marketing agency in patna | `/top-digital-marketing-agencies-patna/` | 10-point test plus red flags (Article schema) |
| 6 | digital marketing course in patna | `/digital-marketing-course-patna/` | 12-module curriculum (Course schema) |
| 7 | digital marketing expert in patna | `/digital-marketing-expert-patna/` | Audits, consultation, part-time marketing lead |
| 8 | online marketing agency patna | `/online-marketing-agency-patna/` | Getting an offline business online, 7-step checklist |
| 9 | digital marketing agency near me patna | `/digital-marketing-agency-near-me-patna/` | In-person meetings, neighbourhoods, how "near me" search works |
| 10 | cheap digital marketing services in patna | `/cheap-digital-marketing-services-patna/` | Cheap vs affordable, starter packages |
| 11 | digital marketing package cost in patna | `/digital-marketing-packages-cost-patna/` | Packages, what affects cost, budget guide |
| 12 | digital marketing company in boring road patna | `/digital-marketing-company-boring-road-patna/` | Playbooks for the street's business types |
| 13 | digital marketing services for small business patna | `/digital-marketing-small-business-patna/` | 90-day plan |
| 14 | b2b digital marketing agency patna | `/b2b-digital-marketing-agency-patna/` | B2B funnel table, LinkedIn |
| 15 | digital marketing company in kankarbagh patna | `/digital-marketing-company-kankarbagh-patna/` | Residential-area playbooks |
| 16 | lead generation agency in patna | `/lead-generation-agency-patna/` | Channel × intent table, lead system |
| 17 | freelance digital marketer in patna | `/freelance-digital-marketer-patna/` | Freelancer vs agency, project-based options |
| 18 | full service digital marketing firm patna | `/full-service-digital-marketing-firm-patna/` | Capability map |
| — | (hub) | `/digital-marketing-patna-guide/` | Hub page linking every page above, ItemList schema |

**Fill in before publishing:**
- `PACKAGES[*].price` in `build/landing_content.py`. Real starting prices make the cost and cheap pages much stronger.
- `COURSE` details (duration, fee, next batch). Publish the course and institute pages only if Zyrostyle actually runs training.

## Keywords left out on purpose

- **Election campaigns** (`election banner and digital campaign agency patna`): this is a high-volume search in Bihar but a brand-risk decision. Add a dedicated page only if leadership wants political clients.

## Technical SEO, GEO and AEO already built in

- Every page has its own `<title>`, meta description, canonical URL, `hreflang en-IN` and Open Graph / Twitter tags.
- **Geo tags** on every page: `geo.region=IN-BR`, `geo.placename=Patna, Bihar, India`, `geo.position` and `ICBM`.
- **JSON-LD on every page:** `ProfessionalService` (a LocalBusiness type) with address, geo coordinates, areaServed (Patna and 12 Bihar cities), opening hours and an offer catalogue. Pages also carry `WebSite`, `WebPage`, `BreadcrumbList`, and where relevant `Service`, `FAQPage` and `ItemList` markup.
- **AEO:** every service page has 4 to 6 FAQs, written answer-first. They render as `<details>` and are mirrored in the `FAQPage` schema.
- **GEO:** `llms.txt` gives AI crawlers a short, citable summary of the business and its services. The business name and description are worded the same way on every page.
- `sitemap.xml` and `robots.txt` are included, plus clean URLs, one H1 per page, a strong internal-link structure (dropdown menu, related services, footer) and fast pages that load no images (good for Core Web Vitals).

## Launch checklist (do these first)

1. Fill in the `SITE` block in `build/content.py`: domain, phone, WhatsApp, street address, PIN code, office coordinates and social profile links. Then run `python3 build/build.py`.
2. Make the name, address and phone match **exactly** across the website, Google Business Profile, Justdial, IndiaMART and the social profiles.
3. Replace "award-winning" with the **specific awards** (name, year, awarding body), or remove the claim until you can back it up. Google's E-E-A-T guidelines and AI engines both reward claims that can be verified.
4. Connect a form backend (Formspree, Netlify Forms or a CRM) through `form_endpoint`.
5. Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools. Add GA4 and Google Tag Manager.
6. Content roadmap: publish 2 to 4 Patna-focused blog posts a month (for example "Digital marketing cost in Patna 2026", "How to rank on Google Maps in Patna", "Admission marketing for coaching institutes in Patna"), plus case studies with real numbers.
