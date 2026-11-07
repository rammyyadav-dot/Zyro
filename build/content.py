"""
Zyrostyle website content.

Every page's SEO copy, keyword targets, FAQs (AEO) and schema hints live here so
marketing can edit copy without touching templates. Run `python3 build/build.py`
after editing to regenerate the static HTML.
"""

# ─────────────────────────────────────────────────────────────────────────────
# BUSINESS DETAILS — fill in the blanks before launch.
# Empty values are simply left out of the pages and the structured data, so no
# placeholder phone numbers or addresses are ever published.
# ─────────────────────────────────────────────────────────────────────────────
SITE = {
    "name": "Zyrostyle",
    "legal_name": "Zyrostyle",
    "url": "https://www.zyrostyle.com",          # TODO: confirm live domain
    "email": "hello@zyrostyle.com",              # TODO: confirm inbox
    "phone": "",                                   # e.g. "+91 98XXXXXXXX" — shown + added to schema when set
    "whatsapp": "",                                # digits only, e.g. "9198XXXXXXXX" — enables WhatsApp button
    "street": "",                                  # e.g. "2nd Floor, ..., Boring Road"
    "locality": "Patna",
    "region": "Bihar",
    "region_code": "IN-BR",
    "postal_code": "",                             # e.g. "800001"
    "country": "IN",
    "lat": "25.5941",                              # Patna city centre — replace with office pin
    "lng": "85.1376",
    "hours": "Mo-Sa 10:00-19:00",
    "founded": "",
    "form_endpoint": "",                           # e.g. Formspree URL; empty = WhatsApp / email hand-off
    "social": [                                    # add profile URLs; used for schema sameAs + footer
        # "https://www.instagram.com/zyrostyle",
        # "https://www.linkedin.com/company/zyrostyle",
        # "https://www.facebook.com/zyrostyle",
        # "https://www.youtube.com/@zyrostyle",
    ],
    "tagline": "Built for Visibility. Designed for Growth.",
    "slogan": "Get Found. Get Noticed. Get Chosen.",
    "short": "Award-winning content marketing, SEO and digital marketing agency in Patna, Bihar.",
}

PATNA_AREAS = [
    "Boring Road", "Boring Canal Road", "Kankarbagh", "Patliputra Colony", "Bailey Road",
    "Saguna More", "Danapur", "Rajendra Nagar", "Fraser Road", "Exhibition Road",
    "Gandhi Maidan", "Raja Bazar", "Ashiana Nagar", "Anisabad", "Patna City",
]
BIHAR_CITIES = [
    "Gaya", "Muzaffarpur", "Darbhanga", "Bhagalpur", "Hajipur", "Begusarai",
    "Purnia", "Arrah", "Bihar Sharif", "Chapra", "Samastipur", "Motihari",
]

TICKER = [
    "Get Found. Get Noticed. Get Chosen.",
    "SEO · GEO · AEO",
    "Content That Converts",
    "Patna Ki Soch. Brand Ki Badi Udaan.",
    "We Don't Just Market Brands. We Make Them Matter.",
    "Built for Patna. Ready for India.",
    "Less Guesswork. More Growth Intelligence.",
]

# ─────────────────────────────────────────────────────────────────────────────
# SERVICES — one landing page each
# ─────────────────────────────────────────────────────────────────────────────
SERVICES = [
    {
        "slug": "seo-services-patna",
        "num": "01",
        "nav": "SEO Services",
        "card_title": "Search Engine Optimisation (SEO)",
        "card_sub": "Rank for What Matters. Grow Organically.",
        "card_text": "Technical SEO, local SEO, Google Business Profile optimisation and search-intent content that put your business in front of customers who are ready to buy.",
        "card_points": ["Technical & on-page SEO audits", "Local SEO & Google Maps ranking", "Keyword & competitor research", "E-commerce & B2B SEO"],
        "service_type": "Search Engine Optimization",
        "title": "Best SEO Company in Patna | SEO Services & Local SEO — Zyrostyle",
        "description": "Zyrostyle is an award-winning SEO agency in Patna. Technical SEO, local SEO, Google Business Profile & Google Maps ranking that drive leads across Bihar.",
        "keywords": "best seo company in patna, seo services in patna, seo agency in patna, local seo services patna, gmb optimization services patna, google map ranking expert patna, seo consultant in patna, affordable seo services in patna, technical seo company patna, ecommerce seo agency patna, website ranking agency patna, link building services in patna, google business profile setup patna",
        "eyebrow": "SEO Agency in Patna, Bihar",
        "h1": "SEO Services in Patna That Put You <em>on Page One.</em>",
        "lead": "Looking for the best SEO company in Patna? Zyrostyle helps businesses across Patna and Bihar rank higher on Google, appear in the Google Maps local pack and turn organic traffic into enquiries, calls and revenue.",
        "strap": "Rank for What Matters. Grow Organically.",
        "intro_label": "Why SEO, why now",
        "intro_h2": "Your customers are already searching. <em>Are they finding you?</em>",
        "intro": [
            "Every day, people in Patna search for doctors in Kankarbagh, coaching institutes on Boring Road, flats near Saguna More and restaurants on Boring Canal Road. The businesses that appear first win the click, the call and the customer.",
            "Our <strong>SEO services in Patna</strong> combine technical excellence, search-intent research and genuinely useful content. We fix what holds your website back, build the pages your customers are searching for and strengthen the signals Google uses to decide who deserves to rank.",
            "Whether you need <strong>local SEO</strong> to win the map pack in your neighbourhood, <strong>e-commerce SEO</strong> to grow online sales, or <strong>B2B SEO</strong> to reach decision-makers across India, we build a search strategy around your commercial goals — not vanity rankings.",
        ],
        "includes_h2": "Our SEO services include",
        "includes": [
            "On-page and technical SEO audits", "Keyword research and competitor analysis",
            "Local SEO and Google Business Profile optimisation", "Google Maps ranking and local citations",
            "Website architecture and internal linking", "SEO content writing and optimisation",
            "Core Web Vitals and page-speed improvements", "Schema markup and structured data",
            "E-commerce and B2B SEO strategies", "Ethical link building and digital PR",
            "Google Search Console and GA4 reporting", "Search visibility and conversion improvements",
        ],
        "features_h2": "Four pillars of <em>search growth.</em>",
        "features": [
            ("Technical SEO", "Crawlability, indexation, site speed, mobile experience, schema markup and site architecture — the foundations that help Google discover and trust your website."),
            ("Local SEO & Google Maps", "Google Business Profile setup and optimisation, local citations, review strategy and location pages that help you rank in the Patna map pack for 'near me' searches."),
            ("Content & On-Page SEO", "Search-intent mapping, service-page optimisation, topic clusters and SEO blogs written for people first and optimised for search engines."),
            ("Authority & Off-Page SEO", "Ethical link building, digital PR, local business listings and brand mentions that build the credibility your rankings depend on."),
        ],
        "local_h2": "Local SEO built for <em>Patna searches.</em>",
        "local": [
            "Most local buying decisions in Patna start with Google Search or Google Maps. We optimise your Google Business Profile, categories, services, photos, posts and reviews so you appear when nearby customers search for what you offer.",
            "We create location-relevant content for areas such as Boring Road, Kankarbagh, Patliputra Colony, Bailey Road and Saguna More, and help businesses expand visibility to Gaya, Muzaffarpur, Bhagalpur, Darbhanga and other Bihar markets.",
        ],
        "closing": "SEO isn't just about rankings. It's about getting discovered by people ready to become your customers.",
        "faqs": [
            ("How much do SEO services cost in Patna?", "SEO pricing in Patna depends on your website size, competition and goals. Local SEO for a single-location business typically needs a smaller monthly retainer than a multi-city or e-commerce SEO programme. Zyrostyle shares a transparent, custom proposal after a free audit, so you only pay for the work your business actually needs."),
            ("How long does SEO take to show results?", "Most businesses see early improvements in visibility and local rankings within 8–12 weeks, while competitive keywords usually take 4–6 months or more. SEO compounds over time: the content and authority you build keep generating traffic long after the work is done."),
            ("What is local SEO and why does my Patna business need it?", "Local SEO helps your business appear in Google Maps and 'near me' searches in your area. For clinics, coaching institutes, restaurants, showrooms and service businesses in Patna, it is often the fastest route to calls, direction requests and walk-ins."),
            ("Can you optimise my Google Business Profile?", "Yes. We set up or audit your Google Business Profile, fix categories and service details, add photos and posts, build consistent local citations and create a review-generation process to improve your Google Maps ranking in Patna."),
            ("Do you guarantee first-page rankings?", "No ethical SEO agency can guarantee rankings, because Google controls its algorithm. What we do guarantee is transparent work, white-hat methods, clear reporting and a strategy focused on traffic, leads and revenue rather than vanity metrics."),
            ("Do you offer SEO for e-commerce and B2B websites?", "Yes. We provide e-commerce SEO (category and product optimisation, technical fixes, structured data) and B2B SEO (thought-leadership content, service pages and lead-generation landing pages) for businesses in Patna and across India."),
        ],
        "related": ["content-marketing-services-patna", "ai-search-optimisation-geo-aeo", "digital-marketing-agency-patna"],
    },
    {
        "slug": "content-creation-services-patna",
        "num": "02",
        "nav": "Content Creation",
        "card_title": "Content Creation Services",
        "card_sub": "Content That Captures Attention. Creativity That Converts.",
        "card_text": "Website copy, SEO blogs, social creatives, Instagram Reels, ad copy, brochures and brand storytelling — every piece made with a purpose.",
        "card_points": ["Website & landing page copywriting", "SEO blogs & thought leadership", "Reels & short-form video", "Brochures, catalogues & profiles"],
        "service_type": "Content Creation",
        "title": "Content Creation Services in Patna | Copywriting, Reels & Video",
        "description": "Content creation agency in Patna for website copy, SEO blogs, Instagram Reels, video, ad copy and brochures. Content that captures attention and converts.",
        "keywords": "content creation services in patna, content writing agency in patna, video content creation agency patna, blog writing services patna, website content creation services patna, ad copywriter in patna, copywriter in patna, reels video shoot patna, instagram reels creation service patna, corporate video creation in patna, graphic design and content creation patna, product photography and video patna, content creation packages patna",
        "eyebrow": "Content Creation Agency in Patna",
        "h1": "Content Creation Services in Patna That <em>Influence Decisions.</em>",
        "lead": "From a powerful brand headline to a scroll-stopping Instagram Reel, Zyrostyle creates content for businesses in Patna and Bihar that communicates with clarity, originality and commercial impact.",
        "strap": "Content That Captures Attention. Creativity That Converts.",
        "intro_label": "Content with a purpose",
        "intro_h2": "We don't create content to fill feeds. <em>We create content to win customers.</em>",
        "intro": [
            "Your content is often the first conversation a customer has with your brand. A vague website, generic posts or a poorly scripted video quietly costs you enquiries every single day.",
            "Our <strong>content creation services in Patna</strong> bring writers, designers, video creators and SEO strategists together, so every asset is on-brand, search-friendly and built to move your audience one step closer to choosing you.",
            "We create in <strong>English, Hindi and Hinglish</strong> — because the best content speaks the way your customers actually think, search and talk.",
        ],
        "includes_h2": "Our content creation capabilities",
        "includes": [
            "Website content and landing page copywriting", "SEO blogs, articles and thought leadership",
            "Social media creatives, posters and campaign assets", "Instagram Reels and short-form video content",
            "Corporate and commercial video scripting & production", "Advertising copy and promotional campaigns",
            "Corporate profiles, catalogues and brochures", "Brand messaging and creative storytelling",
            "Product photography and promotional content", "Flyers, catalogue and print design",
            "Email newsletters and sales copy", "Hindi, English and Hinglish content",
        ],
        "features_h2": "Formats that <em>work hard.</em>",
        "features": [
            ("Words that sell", "Website copy, landing pages, ad copy and sales collateral written by experienced copywriters who understand persuasion, search intent and your audience."),
            ("Video & Reels", "Concepts, scripts, shoots and edits for Instagram Reels, YouTube Shorts, corporate films and commercial videos that stop the scroll and tell your story."),
            ("Design & visual assets", "Social creatives, campaign graphics, brochures, catalogues and flyers designed to a consistent brand system so your business looks as good as it is."),
            ("SEO content", "Blogs, guides and service pages researched around real Patna and Bihar search demand, structured to rank on Google and be cited by AI search."),
        ],
        "local_h2": "Content that speaks <em>Bihar's language.</em>",
        "local": [
            "A coaching institute on Boring Road, a hospital on Bailey Road and a real-estate developer near Saguna More all need very different content. We research your audience before we write a single line.",
            "Our team understands regional context, festivals, admission cycles, wedding seasons and local buying behaviour — so your content feels relevant to Patna while remaining polished enough to compete nationally.",
        ],
        "closing": "We don't create content to fill feeds. We create content to influence decisions.",
        "faqs": [
            ("What content creation services do you offer in Patna?", "Zyrostyle offers website copywriting, SEO blog writing, social media creatives, Instagram Reels and short-form video, corporate and commercial video, ad copy, brochures, catalogues, corporate profiles and brand storytelling for businesses in Patna and across Bihar."),
            ("Do you create Instagram Reels and video content?", "Yes. We plan concepts, write scripts, coordinate shoots and edit Reels, YouTube Shorts, product videos and corporate films. We can shoot on location in Patna or create content from footage you provide."),
            ("Can you write content in Hindi and Hinglish?", "Yes. We create content in English, Hindi and Hinglish, depending on how your audience searches and engages. Many Patna businesses get the best results from a bilingual mix."),
            ("Do you offer monthly content creation packages?", "Yes. We offer monthly content creation packages that combine social creatives, Reels, blogs and copy, tailored to your goals and budget. Contact us for a custom quote."),
            ("Will the content be SEO-friendly?", "Every website page and blog we create is researched around search intent, structured with clear headings and answers, and optimised for both Google and AI-powered search tools."),
        ],
        "related": ["content-strategy-patna", "social-media-marketing-patna", "content-marketing-services-patna"],
    },
    {
        "slug": "content-strategy-patna",
        "num": "03",
        "nav": "Content Strategy",
        "card_title": "Content Strategy",
        "card_sub": "Every Great Brand Starts With a Better Strategy.",
        "card_text": "Positioning, audience personas, search-intent research, topic clusters and content calendars that connect every message to a business goal.",
        "card_points": ["Brand positioning & messaging", "Audience personas & journeys", "Content-gap & intent analysis", "Monthly content calendars"],
        "service_type": "Content Strategy",
        "title": "Content Strategy Consultant in Patna | Brand & Content Planning",
        "description": "Content strategy services in Patna: brand positioning, audience research, topic clusters, content calendars and distribution plans that drive business growth.",
        "keywords": "content strategy consultant patna, digital content strategy services patna, content plan for small businesses patna, content calendar creation patna, brand storytelling services patna, content strategy for coaching institutes patna, ecommerce content strategy patna, digital marketing strategy consultation patna",
        "eyebrow": "Content Strategy Consultants in Patna",
        "h1": "Content Strategy That Turns Random Posting Into <em>Real Growth.</em>",
        "lead": "Zyrostyle builds content strategies for Patna and Bihar businesses based on customer search intent, competitor research, buyer behaviour and commercial objectives — so every piece of content has a job to do.",
        "strap": "Right Message. Right Audience. Right Moment.",
        "intro_label": "Strategy before execution",
        "intro_h2": "Random posting doesn't build a brand. <em>Connected communication does.</em>",
        "intro": [
            "Many businesses publish content without a plan: a festival post here, a blog there, a Reel when someone has time. The result is inconsistent messaging, wasted budget and very little to show for it.",
            "As a <strong>content strategy consultant in Patna</strong>, we start with the questions that matter: Who exactly are your customers? What are they searching for? What makes you different? Which content will move them from awareness to enquiry?",
            "The outcome is a clear, documented roadmap — positioning, messaging, topics, formats, channels and calendars — that your team or ours can execute with confidence.",
        ],
        "includes_h2": "Our content strategy approach covers",
        "includes": [
            "Brand positioning and messaging frameworks", "Audience personas and customer journeys",
            "Search-intent and content-gap analysis", "Competitor content benchmarking",
            "Editorial planning and topic clusters", "Monthly content calendars",
            "Multi-platform content distribution", "Conversion-focused website content architecture",
            "Brand storytelling and tone-of-voice guides", "Content measurement and optimisation",
        ],
        "features_h2": "From insight to <em>editorial plan.</em>",
        "features": [
            ("Positioning & messaging", "Define what you stand for, who you serve and why customers should choose you — then turn it into a messaging framework every channel can use."),
            ("Audience & search insight", "Personas, buyer journeys and keyword research reveal what your customers in Patna and Bihar are asking at every stage of the decision."),
            ("Topic clusters & calendars", "Pillar pages, supporting topics and monthly calendars aligned with seasons, launches, admissions and festivals."),
            ("Distribution & measurement", "Decide where each piece lives — website, Instagram, LinkedIn, YouTube, WhatsApp, email — and how success will be measured."),
        ],
        "local_h2": "Strategy shaped by <em>local insight.</em>",
        "local": [
            "We build content plans around Bihar's real calendar — admission seasons for coaching institutes and schools, wedding and festive seasons for retail and hospitality, and property-buying cycles for developers.",
            "Small businesses get a practical, achievable content plan; growing brands get a scalable editorial system ready for expansion beyond Patna.",
        ],
        "closing": "Right Message. Right Audience. Right Moment.",
        "faqs": [
            ("What is a content strategy?", "A content strategy is a documented plan that defines who your audience is, what they need, which topics and formats you will create, where you will publish them and how you will measure results. It connects every piece of content to a business objective."),
            ("Do small businesses in Patna need a content strategy?", "Yes — arguably more than large brands, because small businesses have limited time and budget. A focused content plan ensures every post, page and video works toward more enquiries instead of being produced at random."),
            ("Do you create content strategies for coaching institutes and schools?", "Yes. We build admission-focused content strategies for coaching institutes and schools in Patna, covering results-led storytelling, faculty content, student testimonials, exam-season topics and local SEO."),
            ("What will I receive at the end of the strategy engagement?", "You receive a positioning and messaging framework, audience personas, a keyword and topic map, a content calendar, channel recommendations and a measurement plan — ready for your team or ours to execute."),
        ],
        "related": ["content-marketing-services-patna", "content-creation-services-patna", "seo-services-patna"],
    },
    {
        "slug": "content-marketing-services-patna",
        "num": "04",
        "nav": "Content Marketing",
        "card_title": "Content Marketing",
        "card_sub": "Turn Great Content Into Your Most Valuable Growth Asset.",
        "card_text": "SEO-led content programmes, lead-generation content, email marketing and distribution that attract, nurture and convert customers.",
        "card_points": ["SEO-led content campaigns", "Lead-generation landing pages", "Email marketing & newsletters", "B2B thought leadership"],
        "service_type": "Content Marketing",
        "title": "Content Marketing Agency in Patna | SEO Content & Lead Generation",
        "description": "Award-winning content marketing agency in Patna. SEO content, B2B thought leadership, email marketing and inbound lead generation that builds organic growth.",
        "keywords": "content marketing services in patna, content marketing agency in patna, b2b content marketing agency patna, seo content marketing services patna, content distribution agency patna, content marketing company near me patna, lead conversion content marketing patna, inbound marketing agency patna, content marketing pricing in patna",
        "eyebrow": "Content Marketing Agency in Patna",
        "h1": "Content Marketing That Builds <em>Demand, Not Just Traffic.</em>",
        "lead": "Zyrostyle is an award-winning content marketing agency in Patna, helping brands build organic growth engines that attract qualified traffic, earn trust and convert readers into leads and revenue.",
        "strap": "Don't Just Publish Content. Build Demand.",
        "intro_label": "Content as a growth engine",
        "intro_h2": "Customers trust you <em>before</em> <em>they ever call you.</em>",
        "intro": [
            "Today's customers research before they buy. They read articles, compare options, watch videos and ask AI tools for recommendations. Content marketing makes sure your brand is part of that research — and the most credible voice in it.",
            "Our <strong>content marketing services in Patna</strong> combine SEO, editorial excellence and conversion thinking. We build content ecosystems that attract organic traffic, support brand credibility and nurture customers through every stage of the buying journey.",
            "Unlike paid ads that stop the moment you stop paying, great content keeps working — compounding into a durable, low-cost source of enquiries for years.",
        ],
        "includes_h2": "Our content marketing services include",
        "includes": [
            "SEO-led content marketing campaigns", "Blog and editorial content programmes",
            "Lead-generation content and landing pages", "Email marketing and newsletters",
            "Content distribution and amplification", "B2B thought leadership",
            "Case studies, guides and e-books", "Industry-specific content campaigns",
            "Inbound marketing funnels", "Content performance and conversion analysis",
        ],
        "features_h2": "Attract. Nurture. <em>Convert.</em>",
        "features": [
            ("Attract", "Search-optimised articles, guides and videos answer the questions your customers in Patna and Bihar are already asking on Google and AI search."),
            ("Engage", "Thought leadership, case studies and social distribution build familiarity and authority so prospects remember you when it is time to decide."),
            ("Convert", "Landing pages, lead magnets, clear CTAs and WhatsApp-ready enquiry paths turn interest into qualified leads."),
            ("Nurture", "Email newsletters and remarketing content keep you top of mind, shortening the sales cycle for high-value services."),
        ],
        "local_h2": "Content marketing for <em>Patna's growth brands.</em>",
        "local": [
            "We help hospitals explain treatments clearly, coaching institutes showcase results, real-estate developers build buyer confidence and B2B companies win trust beyond Bihar.",
            "Every programme is measured against outcomes that matter: organic visibility, qualified enquiries, conversion rate and cost per lead.",
        ],
        "closing": "Don't Just Publish Content. Build Demand.",
        "faqs": [
            ("What is the difference between content marketing and content creation?", "Content creation is producing individual assets such as blogs, videos or creatives. Content marketing is the strategic system around them — research, distribution, SEO, lead capture and measurement — designed to attract and convert customers over time."),
            ("How much does content marketing cost in Patna?", "Content marketing pricing in Patna depends on the volume and type of content, the competitiveness of your industry and whether distribution and email are included. Zyrostyle offers monthly programmes tailored to your goals; request a free consultation for a custom proposal."),
            ("Do you offer B2B content marketing?", "Yes. We create B2B thought leadership, LinkedIn content, case studies, whitepapers and lead-generation landing pages for B2B companies in Patna that sell across Bihar and India."),
            ("How do you measure content marketing success?", "We track organic traffic, keyword visibility, engagement, leads generated, conversion rate and, where possible, revenue influenced by content — reported in clear monthly dashboards."),
        ],
        "related": ["content-strategy-patna", "seo-services-patna", "ai-search-optimisation-geo-aeo"],
    },
    {
        "slug": "digital-marketing-agency-patna",
        "num": "05",
        "nav": "Digital Marketing",
        "card_title": "Digital Marketing & Performance Advertising",
        "card_sub": "Reach the Right People. Make Every Marketing Rupee Work Harder.",
        "card_text": "Google Ads, Meta Ads, lead-generation campaigns, landing pages, remarketing and conversion tracking focused on measurable outcomes.",
        "card_points": ["Google Ads & search advertising", "Facebook & Instagram ads", "Lead-generation campaigns", "Conversion tracking & analytics"],
        "service_type": "Digital Marketing",
        "title": "Digital Marketing Agency in Patna | Google Ads & Lead Generation",
        "description": "Top digital marketing agency in Patna for Google Ads, Meta Ads, lead generation and full-service digital marketing for small businesses and brands across Bihar.",
        "keywords": "digital marketing agency in patna, best digital marketing company in patna, digital marketing services patna, top 10 digital marketing agency in patna, digital marketing expert in patna, online marketing agency patna, digital marketing agency near me patna, digital marketing package cost in patna, digital marketing services for small business patna, b2b digital marketing agency patna, lead generation agency in patna, full service digital marketing firm patna, google ads agency in patna, best agency for lead generation in bihar",
        "eyebrow": "Digital Marketing Agency in Patna",
        "h1": "The Digital Marketing Agency in Patna Built for <em>Measurable Growth.</em>",
        "lead": "Zyrostyle is a full-service digital marketing company in Patna combining SEO, content, Google Ads, Meta Ads and conversion-focused landing pages to generate qualified leads for businesses across Bihar.",
        "strap": "Less Guesswork. More Growth Intelligence.",
        "intro_label": "Performance with purpose",
        "intro_h2": "Make every marketing rupee <em>work harder.</em>",
        "intro": [
            "Running ads is easy. Running profitable campaigns is not. Without the right targeting, landing pages and tracking, budgets disappear into clicks that never become customers.",
            "As a <strong>digital marketing agency in Patna</strong>, we connect organic visibility with targeted paid campaigns — Google Search, Performance Max, YouTube, Facebook and Instagram — and measure everything against the outcomes that matter: enquiries, calls, WhatsApp messages, admissions, bookings and sales.",
            "From <strong>small businesses</strong> seeking their first consistent leads to growing companies entering new markets, we build campaigns around clearly defined goals and transparent reporting.",
        ],
        "includes_h2": "Our digital marketing capabilities",
        "includes": [
            "Google Ads and search advertising", "Facebook and Instagram advertising",
            "YouTube and Performance Max campaigns", "Paid lead-generation campaigns",
            "Campaign landing pages and conversion optimisation", "Remarketing and audience segmentation",
            "Digital campaign strategy and media planning", "Conversion tracking, GA4 and Tag Manager",
            "WhatsApp and call-tracking integration", "Performance reporting and optimisation",
            "Website design and development support", "Monthly digital marketing packages",
        ],
        "features_h2": "One partner. <em>Every channel connected.</em>",
        "features": [
            ("Google Ads", "Search, Maps, Display, YouTube and Performance Max campaigns that capture high-intent demand the moment customers search in Patna and Bihar."),
            ("Meta Ads", "Facebook and Instagram campaigns with sharp creatives, precise audience targeting and lead forms or WhatsApp click-to-chat built in."),
            ("Lead generation", "Dedicated landing pages, offers and follow-up journeys designed to lower your cost per lead and lift lead quality."),
            ("Analytics & CRO", "GA4, conversion tracking and continuous A/B testing so decisions are driven by data, not guesswork."),
        ],
        "local_h2": "Digital marketing for <em>businesses across Bihar.</em>",
        "local": [
            "We serve businesses on Boring Road, Kankarbagh, Patliputra Colony, Saguna More and Bailey Road, as well as brands targeting customers in Gaya, Muzaffarpur, Bhagalpur and beyond.",
            "Geo-targeted campaigns let you reach customers by locality, radius or district — ideal for clinics, showrooms, coaching institutes, real-estate projects and multi-branch businesses.",
        ],
        "closing": "Less Guesswork. More Growth Intelligence.",
        "faqs": [
            ("Which is the best digital marketing agency in Patna?", "The best digital marketing agency for you is one that understands your industry, combines SEO, content and paid media, and reports transparently on leads and revenue. Zyrostyle is an award-winning, content-led digital marketing agency in Patna built around exactly these principles."),
            ("What does a digital marketing package cost in Patna?", "Digital marketing package costs in Patna vary by channels, content volume and ad spend. Small businesses often start with a focused package (for example local SEO plus social media), while growth brands combine SEO, content and paid advertising. We provide a custom quote after understanding your goals."),
            ("Do you provide digital marketing services for small businesses?", "Yes. We design affordable, focused digital marketing plans for small businesses in Patna — typically starting with Google Business Profile, local SEO, social media and a simple lead-generation campaign."),
            ("Do you manage Google Ads in Patna?", "Yes. We plan, build and optimise Google Search, Display, YouTube and Performance Max campaigns, with conversion tracking set up so you can see exactly which campaigns generate enquiries."),
            ("Can you generate leads for businesses outside Patna?", "Yes. While we are based in Patna, we run lead-generation campaigns for businesses targeting customers anywhere in Bihar and across India."),
        ],
        "related": ["best-digital-marketing-company-patna", "digital-marketing-packages-cost-patna", "lead-generation-agency-patna", "full-service-digital-marketing-firm-patna", "social-media-marketing-patna", "seo-services-patna"],
    },
    {
        "slug": "social-media-marketing-patna",
        "num": "06",
        "nav": "Social Media Marketing",
        "card_title": "Social Media Marketing",
        "card_sub": "Stop Scrolling. Start Connecting.",
        "card_text": "Instagram, Facebook, LinkedIn and YouTube management, Reels, influencer collaborations and Meta Ads that make your brand impossible to ignore.",
        "card_points": ["Social media account management", "Instagram Reels & creatives", "Meta Ads campaigns", "LinkedIn & B2B social"],
        "service_type": "Social Media Marketing",
        "title": "Social Media Marketing Agency in Patna | Instagram & Meta Ads",
        "description": "Social media marketing agency in Patna for Instagram & Facebook management, Reels, Meta Ads, influencer marketing and LinkedIn. Build attention, earn trust.",
        "keywords": "social media marketing agency in patna, social media management services patna, instagram marketing agency patna, meta ads agency in patna, facebook ads expert patna, social media handle manager patna, influencer marketing agency in patna, smm packages cost in patna, youtube channel promotion agency patna, social media content creator patna, b2b social media marketing patna, facebook marketing company in patna, social media advertising services patna, restaurant social media marketing patna",
        "eyebrow": "Social Media Marketing Agency in Patna",
        "h1": "Social Media Marketing in Patna That Makes People <em>Stop Scrolling.</em>",
        "lead": "Zyrostyle manages Instagram, Facebook, LinkedIn and YouTube for brands in Patna and Bihar — combining creative storytelling, Reels, audience insight and Meta Ads to turn followers into customers.",
        "strap": "Build Attention. Earn Trust. Inspire Action.",
        "intro_label": "Social that sells",
        "intro_h2": "Looking good on social isn't enough. <em>It has to make you memorable.</em>",
        "intro": [
            "Your social media presence should do more than look attractive. It should make your brand recognisable, relevant and worth remembering — and it should bring in enquiries.",
            "Our <strong>social media marketing services in Patna</strong> combine strategy, content creation, community management and paid social, so organic content builds trust while targeted <strong>Meta Ads</strong> reach new customers in exactly the right localities.",
            "We handle everything from monthly content calendars and Reels production to influencer collaborations and brand launches, with clear reporting on reach, engagement and leads.",
        ],
        "includes_h2": "Our social media services",
        "includes": [
            "Instagram and Facebook marketing", "LinkedIn and B2B social media marketing",
            "Social media account management", "Meta Ads campaign strategy and management",
            "Reels, short-form video and creative content", "YouTube channel management and promotion",
            "Influencer marketing and creator collaborations", "Campaign calendars and brand launches",
            "Brand page and profile optimisation", "Community engagement and response management",
            "Social listening and competitor tracking", "Social performance analytics",
        ],
        "features_h2": "Content, community <em>and conversion.</em>",
        "features": [
            ("Strategy & calendars", "Platform-specific strategies and monthly calendars built around your audience, festivals, launches and business goals."),
            ("Reels & creatives", "Thumb-stopping Reels, carousels and stories produced by our creators — designed for Patna audiences and on-brand every time."),
            ("Meta Ads", "Facebook and Instagram ad campaigns with locality targeting, lead forms and click-to-WhatsApp to generate measurable enquiries."),
            ("Influencers & community", "Collaborations with relevant Bihar creators and proactive community management that turns followers into advocates."),
        ],
        "local_h2": "Social media for <em>Patna's favourite brands.</em>",
        "local": [
            "Restaurants and cafés on Boring Canal Road, fashion boutiques in Patliputra Colony, coaching institutes on Boring Road and real-estate projects near Saguna More all compete for attention on the same feeds.",
            "We craft content that reflects local culture and Hinglish conversation while keeping your brand polished — and we target ads precisely by locality, interest and intent.",
        ],
        "closing": "Build Attention. Earn Trust. Inspire Action.",
        "faqs": [
            ("How much do social media marketing packages cost in Patna?", "SMM package costs in Patna depend on the number of platforms, posts and Reels per month, and whether ad management is included. Zyrostyle offers flexible monthly social media packages; contact us for a quote based on your goals."),
            ("Do you manage Instagram and Facebook accounts?", "Yes. We handle complete social media management — strategy, content calendars, creatives, Reels, captions, posting, community engagement and monthly reporting — for Instagram, Facebook, LinkedIn and YouTube."),
            ("Do you run Meta Ads (Facebook and Instagram ads)?", "Yes. We plan, create and optimise Meta Ads campaigns for awareness, traffic, lead generation and WhatsApp enquiries, targeted precisely to localities in Patna and districts across Bihar."),
            ("Do you offer influencer marketing in Patna?", "Yes. We identify relevant creators in Patna and Bihar, manage briefs and collaborations and measure the results of influencer campaigns."),
            ("Which social platform is best for my business?", "It depends on your audience. Instagram and Facebook work well for restaurants, retail, real estate, healthcare and education; LinkedIn is best for B2B; YouTube suits brands that benefit from explainer and long-form content. We recommend a mix after reviewing your goals."),
        ],
        "related": ["content-creation-services-patna", "digital-marketing-agency-patna", "content-strategy-patna"],
    },
]

AI_SEARCH = {
    "slug": "ai-search-optimisation-geo-aeo",
    "nav": "AI Search (GEO & AEO)",
    "service_type": "Generative Engine Optimization",
    "title": "GEO & AEO Agency in Patna | AI Search Optimisation — Zyrostyle",
    "description": "GEO and AEO services in Patna. Help Google AI Overviews, AI search and chat assistants understand, trust and cite your brand.",
    "keywords": "generative engine optimisation patna, geo agency india, answer engine optimisation patna, aeo services, ai search optimisation patna, google ai overviews optimisation, chatgpt seo patna, llm seo agency bihar",
    "eyebrow": "SEO + GEO + AEO — Patna, Bihar",
    "h1": "Be Found on Google. <em>Be Understood by AI.</em>",
    "lead": "Search behaviour is changing. Customers now discover businesses through Google Search, Google Maps, AI Overviews and conversational AI assistants. Zyrostyle helps Patna and Bihar businesses become discoverable, understandable and trusted across all of them.",
    "faqs": [
        ("What is Generative Engine Optimisation (GEO)?", "Generative Engine Optimisation (GEO) is the practice of structuring useful, credible and clearly attributed information so AI-powered search and discovery systems — such as Google AI Overviews and conversational AI assistants — can accurately understand, summarise and reference your brand and services."),
        ("What is Answer Engine Optimisation (AEO)?", "Answer Engine Optimisation (AEO) means creating clear, direct answers to real customer questions through well-structured service pages, FAQs, explainers and knowledge content, so search engines and voice or AI assistants can surface your answer."),
        ("Is GEO replacing SEO?", "No. GEO and AEO build on strong SEO foundations. AI search systems still rely on crawlable, authoritative, well-structured websites. The most resilient strategy combines all three: SEO, GEO and AEO."),
        ("Can you guarantee my business will appear in AI answers?", "No one can guarantee inclusion in AI-generated answers, because those systems are controlled by their providers. We improve the factors that make your brand easier to understand and cite: clear entity information, structured data, consistent business listings, credible content and authoritative mentions."),
        ("Which businesses in Patna benefit most from GEO and AEO?", "Businesses whose customers research before buying — hospitals and clinics, coaching institutes and schools, real-estate developers, B2B companies, travel and hospitality brands — benefit most, because their customers increasingly ask AI tools for recommendations and explanations."),
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# INDUSTRIES
# ─────────────────────────────────────────────────────────────────────────────
INDUSTRIES = [
    ("healthcare", "Healthcare, Hospitals & Doctors",
     "Patient-focused content, local SEO, hospital website optimisation and responsible healthcare advertising.",
     "Patients in Patna search for specialists, hospitals and diagnostic centres on Google Maps before they book. We help hospitals, clinics and doctors build trustworthy, medically accurate content, optimise Google Business Profiles for every location and department, and run compliant awareness campaigns that respect patient sensitivity.",
     ["Hospital & clinic local SEO", "Doctor profile & department pages", "Google Business Profile for each branch", "Patient education content & FAQs", "Responsible healthcare ads", "Review & reputation management"]),
    ("real-estate", "Real Estate & Property Developers",
     "Property campaign creatives, lead-generation landing pages, Google Ads and location-based marketing.",
     "From new launches near Saguna More and Danapur to premium projects on Bailey Road, property buyers research for months. We build project landing pages, walkthrough videos, Google and Meta lead campaigns and nurture journeys that deliver site visits — not just form fills.",
     ["Project launch campaigns", "Lead-generation landing pages", "Google Ads & Meta lead ads", "Walkthrough videos & Reels", "Location-based targeting", "Lead nurturing via WhatsApp & email"]),
    ("education", "Education, Schools & Coaching Institutes",
     "Admission-focused digital campaigns, local search visibility, social media storytelling and enquiry generation.",
     "Patna is one of India's great coaching and education hubs, and competition for admissions on Boring Road, Kankarbagh and Rajendra Nagar is intense. We plan admission-season campaigns, showcase results and faculty, optimise local search and generate counselling enquiries for coaching institutes, schools and colleges.",
     ["Admission-season campaigns", "Results & topper storytelling", "Local SEO for each centre", "YouTube & Reels for faculty", "Lead forms & counselling funnels", "School promotion & brand building"]),
    ("hospitality", "Restaurants, Cafés & Hospitality",
     "Google Maps visibility, local discovery, brand content, menu promotions and social media advertising.",
     "Diners decide where to eat with a quick Google Maps or Instagram search. We make restaurants and cafés on Boring Canal Road, Fraser Road and beyond irresistible online with food photography, Reels, menu promotions, review strategy and hyper-local ads.",
     ["Google Maps & 'near me' visibility", "Food photography & Reels", "Instagram & influencer campaigns", "Menu, festive & event promotions", "Review generation", "Hyper-local Meta Ads"]),
    ("retail", "Retail, Fashion & E-commerce",
     "Product campaigns, online store SEO, creative advertising and customer acquisition strategies.",
     "Whether you run a boutique in Patliputra Colony or ship across India, we combine e-commerce SEO, product content, catalogue shoots and performance advertising to grow footfall and online sales.",
     ["E-commerce & category SEO", "Product photography & video", "Catalogue & lookbook design", "Shopping & Performance Max ads", "Festive & wedding-season campaigns", "Customer retention email & WhatsApp"]),
    ("travel", "Travel, Tourism & Hotels",
     "Destination content, B2B travel marketing, hotel promotions, search visibility and digital lead generation.",
     "Bihar is home to globally significant heritage — Bodh Gaya, Nalanda, Rajgir and Vaishali. We help hotels, tour operators and travel brands reach domestic and international travellers with destination content, OTA-friendly search visibility and lead generation.",
     ["Destination & itinerary content", "Hotel SEO & Google Hotel visibility", "B2B travel marketing", "Pilgrimage & heritage tour campaigns", "Multilingual content", "Booking-focused landing pages"]),
    ("b2b", "Startups & B2B Businesses",
     "Brand positioning, website content, LinkedIn marketing, thought leadership and demand generation.",
     "Bihar's startup and B2B ecosystem is growing fast. We help founders and B2B companies sharpen positioning, build credible websites, publish thought leadership on LinkedIn and generate qualified pipeline across India.",
     ["Brand positioning & messaging", "Website content & UX copy", "LinkedIn marketing & founder branding", "Thought leadership & case studies", "B2B SEO & demand generation", "Account-based campaigns"]),
]

PROCESS = [
    ("Discover", "We understand your business, target audience, current digital presence and growth opportunities."),
    ("Audit", "We review your website, search, content, competitor and marketing performance information."),
    ("Strategise", "We build a marketing roadmap around your audience, channels, objectives, budget and priorities."),
    ("Create", "Our creative and content process translates strategy into campaigns, pages, messaging and assets."),
    ("Launch", "We implement prioritised activities across search, content, social media and paid advertising."),
    ("Measure & Improve", "We track meaningful performance indicators, identify opportunities and optimise based on results."),
]

WHY = [
    ("Strategy Before Execution", "Every campaign begins by understanding your business, competition, audience and growth objectives."),
    ("Content at the Core", "We combine valuable content with search and advertising to create consistent brand communication."),
    ("Built for Patna. Ready for India.", "We understand local relevance, regional-language communication and scalable strategies for businesses targeting Bihar and beyond."),
    ("Brand and Performance Together", "We connect brand positioning, creative campaigns and measurable digital marketing outcomes."),
    ("Transparent, Insight-Led Marketing", "We focus on meaningful indicators: qualified enquiries, organic visibility, conversions and customer-acquisition performance."),
    ("One Connected Growth Partner", "From positioning and strategy to production, distribution and optimisation, your brand experience stays consistent."),
]

PILLARS = [
    ("Get Discovered", "Improve your search visibility across Google and relevant AI-powered discovery platforms."),
    ("Build Authority", "Establish credibility through valuable content, brand storytelling and a consistent digital presence."),
    ("Generate Demand", "Reach high-intent audiences through organic search, social campaigns and targeted advertising."),
    ("Convert Customers", "Turn website visitors, enquiries and campaign interactions into qualified business opportunities."),
    ("Grow Sustainably", "Build scalable marketing processes driven by insights, measurement and continuous improvement."),
]

HOME_FAQS = [
    ("What does Zyrostyle do?", "Zyrostyle is an award-winning content marketing, SEO and digital marketing agency in Patna, Bihar. We help brands build organic growth engines through SEO, GEO, AEO, content creation, content strategy, content marketing, social media marketing and performance advertising."),
    ("Where is Zyrostyle located?", "Zyrostyle is based in Patna, Bihar, and serves businesses across Patna — including Boring Road, Kankarbagh, Patliputra Colony, Bailey Road and Saguna More — as well as clients throughout Bihar and India."),
    ("Which is the best SEO and digital marketing company in Patna?", "Look for an agency that combines strategy, content, SEO and paid media, understands your industry and reports transparently on leads and revenue. Zyrostyle is a content-led, award-winning agency in Patna that builds marketing around business outcomes rather than vanity metrics."),
    ("How much does digital marketing cost in Patna?", "Costs depend on the services, channels and scale you need. Small businesses can start with a focused local SEO and social media package, while growing brands typically combine SEO, content marketing and paid advertising. We provide a free consultation and a custom proposal."),
    ("Do you work with small businesses and startups?", "Yes. We work with startups, local businesses and established companies. Every plan is scaled to your goals and budget."),
    ("Do you create content in Hindi?", "Yes. We create content in English, Hindi and Hinglish to match how your customers search and engage."),
]

# Areas served — unique copy per locality to avoid thin, duplicated content.
AREAS = [
    ("Boring Road", "One of Patna's busiest commercial and coaching corridors. We help coaching institutes, retail showrooms, clinics and restaurants on Boring Road win local search, Google Maps visibility and admission-season enquiries."),
    ("Boring Canal Road", "Home to many of the city's cafés, restaurants, showrooms and lifestyle brands. Our social media marketing, Reels and hyper-local Meta Ads help Boring Canal Road businesses stand out in crowded feeds."),
    ("Kankarbagh", "A large residential and commercial hub with dense demand for healthcare, education and everyday services. We build local SEO and Google Business Profile strategies that capture Kankarbagh's high volume of 'near me' searches."),
    ("Patliputra Colony", "A premium neighbourhood known for clinics, boutiques and professional services. We create polished brand content and targeted campaigns that reach Patliputra Colony's discerning customers."),
    ("Bailey Road", "A key arterial road with hospitals, corporate offices, institutions and retail. We support Bailey Road organisations with reputation-led content, SEO and lead-generation campaigns."),
    ("Saguna More & Danapur", "Patna's fast-growing real-estate and retail corridor. We help developers, showrooms and new businesses here generate leads with project landing pages, Google Ads and location-targeted advertising."),
    ("Rajendra Nagar & Kadamkuan", "Established residential and education neighbourhoods. We help coaching centres, schools and local retailers build trust and enquiries through local search and community-focused content."),
    ("Fraser Road & Exhibition Road", "Central commercial districts with hotels, offices, retailers and restaurants. We drive footfall and bookings through Google Maps optimisation, search ads and brand content."),
]
