"""
Photo assignments and alt text.

All photos are from Unsplash (https://unsplash.com/license — free for commercial
use, no attribution required), downloaded, checked and converted to WebP in
assets/img/photos/ as <name>.webp (1800px) and <name>-sm.webp (900px).
Replace any image with your own shoot photography by keeping the same file name.
"""

ALT = {
    "marketing-strategy-team-patna": "Marketing strategists planning a campaign with sticky notes on a glass wall",
    "creative-team-collaboration": "Creative team collaborating around laptops on a content marketing project",
    "agency-presentation-workshop": "Digital marketing agency presenting a growth strategy to a client team",
    "seo-analytics-dashboard": "Laptop showing an SEO and website analytics dashboard",
    "video-editing-content-creation": "Video editing timeline for Reels and commercial video content creation",
    "content-strategy-wireframes": "Strategist sketching content plans and website wireframes on paper",
    "content-marketing-writing-desk": "Writer's desk with laptop and notebook for blog and content marketing",
    "digital-marketing-performance-data": "Performance marketing dashboard with campaign charts and conversion data",
    "social-media-content-studio": "Studio microphone for podcast, video and social media content production",
    "ai-search-optimisation-workspace": "Team working on laptops on AI search and answer engine optimisation",
    "healthcare-doctor-digital": "Doctor using a smartphone — digital marketing for hospitals and clinics",
    "hospital-reception": "Modern hospital reception — healthcare marketing and local SEO",
    "real-estate-home-keys": "House keys and model home — real estate lead generation",
    "real-estate-modern-home": "Modern residential property at dusk — real estate digital marketing",
    "education-coaching-books": "Books and learning blocks — marketing for coaching institutes and schools",
    "restaurant-hospitality-interior": "Restaurant interior — social media marketing for restaurants and cafés",
    "retail-fashion-store": "Fashion retail store interior — retail and e-commerce marketing",
    "travel-tourism-planning": "Travel planning with map and camera — tourism and hotel marketing in Bihar",
    "b2b-modern-office": "Modern corporate office — B2B digital marketing and LinkedIn marketing",
    "team-laptops-top-view": "Top view of a digital marketing team working on laptops",
    "client-success-celebration": "Client and strategist celebrating marketing results with a high five",
    "expert-whiteboard-session": "Digital marketing expert leading a whiteboard strategy session",
    "digital-marketing-classroom": "Digital marketing training session in a classroom",
    "workshop-group-discussion": "Group discussion during a digital marketing workshop",
    "freelancer-laptop-typing": "Digital marketer working on a laptop",
    "lead-generation-laptop-review": "Reviewing a lead generation landing page on a laptop",
    "full-service-agency-floor": "Full-service digital marketing agency office floor",
    "small-business-checkout": "Small business checkout counter with a tablet point-of-sale",
    "online-business-team": "Small business owners taking their business online",
    "local-business-meeting": "Local business owner in a marketing meeting",
    "open-office-workspace": "Open-plan office workspace",
    "startup-team-working": "Startup team working together in a meeting room",
    "creative-idea-bulb": "Light bulb idea note pinned on a cork board",
    "design-studio-screens": "Design studio screens showing website and brand creatives",
    "brainstorm-office-loft": "Team brainstorming in a bright loft office",
    "photographer-landscape-creative": "Photographer capturing a landscape — creative content production",
}

# slug -> (hero photo, full-bleed band photo)
PAGE_PHOTOS = {
    "": ("marketing-strategy-team-patna", "creative-team-collaboration"),
    "services": ("team-laptops-top-view", "agency-presentation-workshop"),
    "seo-services-patna": ("seo-analytics-dashboard", "open-office-workspace"),
    "content-creation-services-patna": ("video-editing-content-creation", "photographer-landscape-creative"),
    "content-strategy-patna": ("content-strategy-wireframes", "brainstorm-office-loft"),
    "content-marketing-services-patna": ("content-marketing-writing-desk", "creative-idea-bulb"),
    "digital-marketing-agency-patna": ("digital-marketing-performance-data", "agency-presentation-workshop"),
    "social-media-marketing-patna": ("social-media-content-studio", "workshop-group-discussion"),
    "ai-search-optimisation-geo-aeo": ("ai-search-optimisation-workspace", "design-studio-screens"),
    "industries": ("startup-team-working", "creative-team-collaboration"),
    "areas-we-serve": ("local-business-meeting", "open-office-workspace"),
    "about": ("creative-team-collaboration", "agency-presentation-workshop"),
    "contact": ("client-success-celebration", "brainstorm-office-loft"),
    "privacy-policy": ("b2b-modern-office", None),
    "404": ("creative-idea-bulb", None),
    "digital-marketing-patna-guide": ("brainstorm-office-loft", "team-laptops-top-view"),
    "best-digital-marketing-company-patna": ("client-success-celebration", "agency-presentation-workshop"),
    "digital-marketing-institute-patna": ("digital-marketing-classroom", "workshop-group-discussion"),
    "top-digital-marketing-agencies-patna": ("agency-presentation-workshop", "startup-team-working"),
    "digital-marketing-course-patna": ("workshop-group-discussion", "digital-marketing-classroom"),
    "digital-marketing-expert-patna": ("expert-whiteboard-session", "brainstorm-office-loft"),
    "online-marketing-agency-patna": ("online-business-team", "small-business-checkout"),
    "digital-marketing-agency-near-me-patna": ("local-business-meeting", "open-office-workspace"),
    "cheap-digital-marketing-services-patna": ("small-business-checkout", "creative-idea-bulb"),
    "digital-marketing-packages-cost-patna": ("content-marketing-writing-desk", "digital-marketing-performance-data"),
    "digital-marketing-company-boring-road-patna": ("retail-fashion-store", "restaurant-hospitality-interior"),
    "digital-marketing-small-business-patna": ("small-business-checkout", "retail-fashion-store"),
    "b2b-digital-marketing-agency-patna": ("b2b-modern-office", "expert-whiteboard-session"),
    "digital-marketing-company-kankarbagh-patna": ("healthcare-doctor-digital", "education-coaching-books"),
    "lead-generation-agency-patna": ("lead-generation-laptop-review", "digital-marketing-performance-data"),
    "freelance-digital-marketer-patna": ("freelancer-laptop-typing", "team-laptops-top-view"),
    "full-service-digital-marketing-firm-patna": ("full-service-agency-floor", "creative-team-collaboration"),
}

INDUSTRY_PHOTOS = {
    "healthcare": "healthcare-doctor-digital",
    "real-estate": "real-estate-modern-home",
    "education": "education-coaching-books",
    "hospitality": "restaurant-hospitality-interior",
    "retail": "retail-fashion-store",
    "travel": "travel-tourism-planning",
    "b2b": "b2b-modern-office",
}
