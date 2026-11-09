# SEO measurement and release notes — 9 November 2026

## Host configuration

Production is Cloudflare Pages project `zyro` (`zyro-7ax.pages.dev`), connected to GitHub main. The canonical host is https://zyrostyle.com. Cloudflare has a proxied www CNAME and a zone redirect rule: www, or HTTP on apex, redirects 301 to HTTPS apex, preserving path and query. Do not change this back in page metadata. Rule ID: 9eae904f67504befa1516307d568a32e. DNS record ID: 3f565b6e77ada902d59dadf8402a4ac1.

## Content and freshness

The main homepage owns broad brand/agency discovery. `/digital-marketing-agency-patna/` focuses on Google/Meta paid campaigns. The selection guide is a checklist, not a fabricated top-ten ranking. Existing URLs remain stable. The package page compares proposed scope and explicitly states that no fixed rates are published. Add fees, taxes and contract terms only after business verification. Unsupported awards have been removed; publish case studies only with client permission, dates, scope, source data and evidence.

Sitemap `lastmod` is omitted because no reliable per-page change history exists. Rebuilds must not invent freshness. Privacy policy review date is explicit in SITE, independent of build time.

## Collection readiness

`assets/js/measurement.js` prepares `contact_handoff` events for WhatsApp links, chat chips, form handoffs, phone and email links. It NEVER emits `generate_lead` or `qualify_lead`. No form content, contact details, message text or URL query parameters are sent. `page_path` and `landing_page` contain paths only; `acquisition_channel` is a coarse first-landing classification, not authoritative attribution.

Optional analytics defaults to off. Allow/decline controls are on the privacy page. Consent and attribution persist only for the current browser session when allowed. A consent manager can call `ZyroMeasurement.setConsent(true/false)`. Without consent there is no optional event collection or attribution storage. Without a verified `SITE.ga4_measurement_id`, there is no GA4 network collection. With consent but no ID, events are available in `window.dataLayer` for integration/testing only, not stored remotely. No real traffic metrics have been fabricated.

Set the verified GA4 G-... ID in `build/content.py` and rebuild. Use the direct gtag integration OR a GTM adapter, not both. Disable enhanced-measurement form interactions and outbound click collection if they would be misread as leads or expose full URLs. Configure landing_page, acquisition_channel, contact_method and placement as event-scoped custom dimensions. Leave `contact_handoff` out of key-event/lead totals. Validate network payloads and DebugView before treating collection as operational. Declining stops future events; it does not erase past collected data.

## Confirming and qualifying leads

Record an enquiry only when an actual message, call or backend submission is received. Staff must then confirm genuine business fit, service need, contactability and next step before marking it qualified. Deduplicate by an internal lead_id. Do not put personal information in analytics. Record source/medium from consented attribution or a documented client answer; use unknown when unavailable. Do not infer organic acquisition from visiting an SEO page.

Keep one current reviewed row per lead with these CSV headers:

`lead_id,received_date,landing_page,source,medium,status,qualified_date`

Dates use YYYY-MM-DD. Status: received, qualified, won, unqualified or lost. Qualified/won requires qualified_date. Preserve the original qualification date after later loss; use a separate CRM field for current sales stage if needed. Empty landing_page remains unattributed. Source google and medium organic are aligned with GSC; other search engines are excluded from this Google-only report. Use pseudonymous internal IDs; export no names, email addresses, phone numbers or message bodies.

## Weekly report

Export Search Console Search results → Pages for the exact reporting date window, Web search type, without extra query/country/device filters unless corresponding lead records are filtered identically. Retain headers `Top pages,Clicks,Impressions`. Include both old www and new apex data in a domain property when available. Confirm canonical selection through URL Inspection; submit https://zyrostyle.com/sitemap.xml.

Run:

```sh
python3 scripts/seo_report.py --gsc /private/Pages.csv --leads /private/leads.csv --start 2026-11-09 --end 2026-11-15 --out /private/weekly-seo.csv
```

The report normalizes old/new host URLs, removes query strings, deduplicates by requiring one row per lead ID, and shows Google clicks, impressions, CTR, received organic enquiries and qualified organic leads by landing page. Handoffs remain a separate GA4 interaction report, never a lead input. Qualification is counted on qualified_date, receipt on received_date. GSC cannot identify individual leads; the report compares aggregates, not person-level joins. Different attribution windows and consent coverage mean qualified leads divided by Search Console clicks is not a session conversion rate. No data means unavailable, not proven zero performance. Keep CRM/export files outside the website repository.

## Outstanding business inputs

Verified GA4 property ID, access to Search Console performance data and a staff-reviewed CRM/export are required to activate remote measurement and produce real metrics. Prices, awards, office address and case-study results must be supplied and verified by the business; the site does not invent them.
