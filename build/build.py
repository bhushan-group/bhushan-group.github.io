import json, os, shutil
from jinja2 import Environment, DictLoader
from markupsafe import Markup, escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # the top of the repository
OUT = os.path.join(ROOT, "_site")  # what GitHub publishes; never committed

# Stop with a clear message if a hand edit broke either data file. A failed
# build leaves the previous version of the site live.
for _f in ("news.json", "people.json"):
    try:
        json.load(open(os.path.join(ROOT, "data", _f), encoding="utf-8"))
    except ValueError as e:
        raise SystemExit(f"data/{_f} is not valid JSON ({e}). Usually a missing or extra comma.")
# ---------------------------------------------------------------------------
# Visitor analytics. Paste the two IDs below and rebuild; leave a value empty
# and that service's tag is simply left out of every page.
#   UMAMI_WEBSITE_ID  the data-website-id from Umami Cloud -> Settings -> Websites
#   CF_BEACON_TOKEN   the token from Cloudflare -> Web Analytics -> Manage site
# ---------------------------------------------------------------------------
UMAMI_WEBSITE_ID = "7a71e7ea-a7a3-4c17-883f-4831fe021e8a"
CF_BEACON_TOKEN = "f63998ee8e5a4acb979db13249c20d64"

data = json.load(open(os.path.join(HERE, "data.json")))

BASE_URL = "https://bhushan-group.github.io/"

# Google Search Console ownership verification. Leave empty to omit the tag.
# Removing this breaks verification, which stops the sitemap being read.
GSC_VERIFICATION = "zZIlCNRtoEToZO5fepvjEdKskch8Lbat7TbngFcFmrY"

# The PI bio lives here rather than in data.json, which is regenerated from the
# old site by extract.py and would overwrite it.
PI_PROSE = """\
<p>I am an engineer who works on biological questions. My lab builds microfluidic devices and biosensors because the questions we care about \u2014 how gut microbes change the way a drug behaves, how tissue and bacteria shape each other over days \u2014 cannot be answered in a dish or by an endpoint assay. They need an environment you can control and a measurement you can keep taking.</p>
<p>I came to this from mechanical engineering. I earned my PhD at Louisiana State University and trained as a postdoc at the University of California, Davis and at Massachusetts General Hospital, Harvard Medical School and Shriners Boston. As an NIH K30 scholar at UC Davis I took a second MS in advanced clinical research, which shaped how I think about what these models have to predict before anyone should trust them.</p>
<p>My work has been recognized with the NIH K99/R00, an NSF CAREER Award and the CMBE Young Innovator Award. I serve on the Editorial Board of <em>Scientific Reports</em>.</p>
<p>The lab spans microfabrication in both polymer and metal, cell and molecular biology, and computation. Through the NSF I-Corps program I worked on whether one of our technologies had a market, which changed how I think about translation. In 2026 I spent time at KTH Royal Institute of Technology and Stockholm University as a Digital Futures Scholar-in-Residence.</p>
<p>I teach biofluid mechanics, medical devices and synthetic biology. I care a great deal about student success and about building unusual learning opportunities \u2014 I helped start <a href="http://www.thecrimson.com/article/2014/4/21/sustainability-hackathon-first/">the first Sustainability Hackathon at Harvard</a> \u2014 and about finding good ways of <a href="https://youtu.be/Cr_b1ZUAp-g">communicating science</a> to people outside the field.</p>
"""

PUBS = data["pubs"]
def citation_tail(p):
    """The ", 15(5): 493-504, 2022" that follows the journal name."""
    bits = ""
    if p.get("volume"):
        bits += " " + p["volume"]
        if p.get("issue"):
            bits += "(" + p["issue"] + ")"
    if p.get("pages"):
        bits += (": " if bits else " ") + p["pages"].replace("-", "\u2013")
    if not bits and p.get("details"):
        bits = " " + p["details"]
    return Markup(escape(bits + (", " if bits else " ") + str(p["year"])))


for p in PUBS:
    p["citation"] = citation_tail(p)
    p["title_html"] = Markup(p["title_html"])
    p["authors_html"] = Markup(str(escape(p["authors"])).replace("Bhushan A", "<strong>Bhushan A</strong>"))

def tagged(keywords):
    return [p for p in PUBS if any(k.lower() in str(p["title_html"]).lower() for k in keywords)]

GLYPH_ARROW = Markup('<svg width="20" height="24" viewBox="0 0 20 24" aria-hidden="true"><path d="M5 4 L14 12 L5 20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></svg>')

THEMES = [
 dict(id="crc", name="Microbes and colorectal cancer", link_text="Colon and microbiome projects", tint="app-teal",
      img="assets/img/photos/organoid-bacteria.jpg", alt="Brightfield image of an organoid with fluorescent bacteria nearby",
      short="Colon organoids and chips that host living bacteria, to test how bile acids and microbial metabolites change tumor epithelium.",
      paras=["The colon is lined by epithelium that lives in constant contact with bacteria and the molecules they make. We build colon organoid models and microfluidic chips in which living bacteria and human epithelium share the same space, so their interactions can be controlled and measured.",
             "Current work asks how bile salts, bacterial enzymes such as bile salt hydrolase, and other microbial metabolites influence bacterial colonization, host signaling and tumor behavior in colorectal cancer organoids."],
      pubs=tagged(["Bile salts and bacterial", "Engineered bacterial therapeutics", "Tiny Organs", "microfluidic colon with an extracellular"])),
 dict(id="liver-fat", name="Liver–fat crosstalk", link_text="Liver and adipose projects", tint="app-rose",
      img="assets/img/photos/adipocytes.jpg", alt="Fluorescence image of adipocytes cultured on a chip",
      short="Linked adipose and liver tissues on chip for studying insulin resistance and fatty liver disease in human cells.",
      paras=["Fat tissue and the liver signal to each other constantly, and that conversation goes wrong in insulin resistance and fatty liver disease. We culture adipose and liver tissues on chip to study it with human and primary cells under flow.",
             "Our perfused adipose tissue-chips carry preadipocytes differentiated into adipocytes, and adipocytes made insulin resistant. The insulin-resistant adipocytes take up less fatty acid, and rosiglitazone restores uptake. Our liver constructs combine several cell types, stay functional for weeks, and can be made insulin resistant to test strategies that restore insulin response."],
      pubs=tagged(["insulin resistance through", "3D human adipose", "insulin resistant adipose", "primary murine adipose", "liver sinusoid", "flow and collagen"])),
 dict(id="drug", name="Microbiome and drug response", link_text="Drug response projects", tint="app-sand",
      img="assets/img/photos/bacteria-colonization.jpg", alt="Fluorescence image of bacteria colonizing intestinal cells",
      short="Intestine chips and pharmacokinetic models of how gut bacteria alter drug absorption and metabolism.",
      paras=["Gut bacteria change how drugs are absorbed and metabolized. Our intestine tissue chip grows a tight epithelial monolayer on a collagen membrane instead of the usual Transwell membrane, and we use it to study how gut bacteria modulate cytochrome P450 drug-metabolizing enzymes. Because many gut bacteria need low oxygen, we also built chips with local control of oxygen tension.",
             "We pair these experiments with pharmacokinetic models to understand how bacteria alter drug exposure, for example for tacrolimus and sulfasalazine."],
      pubs=tagged(["pharmacokinetics of tacrolimus", "anoxic environment", "local control of oxygen", "organ-to-organ interaction", "predicting drug efficacy"])),
 dict(id="sensing", name="On-chip sensing", link_text="Sensing projects", tint="app-teal",
      img="assets/img/photos/sensor-bead-assay.jpg", alt="Diagram of a microfluidic bead assay: a cell culture chamber feeds bead and antibody inlets, two serpentine mixers and a detection region",
      short="Continuous on-chip sensors that track what tissue secretes, such as albumin and cholesterol, over time.",
      paras=["Tissue on a chip changes over days and weeks, and the small volumes make proteins and small molecules hard to measure. We build assays into the chip that read out what cells secrete in real time, without stopping the experiment. Bead-based assays run in line with the culture chamber and measure secreted proteins and metabolites, such as albumin and cholesterol.",
             "Measuring over time turns an organ-on-chip from a single snapshot into a record of how tissue responds to drugs, microbes and nutrients."],
      pubs=tagged(["cholesterol secreted", "in-line ELISA", "microsphere-based assay", "Microparticles and Microfluidics"])),
]
APPS = THEMES[:3]

PILLARS = [
 dict(name="Engineer", img="assets/img/photos/chip-in-hand.jpg", alt="A small transparent microfluidic chip held in a palm next to a quarter",
      text="Microfluidic and organ-on-chip platforms that set the conditions living tissue experiences."),
 dict(name="Model", img="assets/img/photos/spheroids.jpg", alt="Fluorescence image of multicellular spheroids",
      text="Human tissues and organoids, grown alone or with microbes."),
 dict(name="Measure", img="assets/img/photos/sensor-albumin.jpg", alt="Diagram of on-chip albumin sensing: cells in a culture chamber feed antibody-coated beads that give a measurement over time",
      text="Continuous on-chip sensors that track what tissue secretes, such as albumin and cholesterol, over time."),
]

FEATURED_DOIS = ["10.1007/s10439-026-04226-2", "10.1002/adtp.202300449", "10.1016/j.trecan.2024.04.001"]
FEATURED = [next(p for p in PUBS if p["doi"] == d) for d in FEATURED_DOIS]
VIDEOS = [
 dict(id="uscxFoseJmY", title="Finding your best medicine with an intestine on a chip"),
 dict(id="E4ay9wufZkc", title="Fighting obesity by growing more fat cells"),
 dict(id="BoVCGA8Iv-M", title="Fighting diabetes through a liver–adipose organ-chip"),
 dict(id="4gC0glk5DKs", title="Personalized organ-chip to battle one of the deadliest cancers"),
]
# Workshops in the BIOMIC menu. Add a line here when the next one has a page.
BIOMIC = [("BIOMIC 2024", "https://sites.google.com/iit.edu/eng-bio-workshop-2024/")]

NAV = [("research", "Research", "research.html"), ("publications", "Publications", "publications.html"),
       ("news", "News", "news.html"), ("people", "People", "people.html"), ("teaching", "Teaching", "teaching.html")]

def initials(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper()
GROUPS = data["groups"]
for g in GROUPS:
    for m in g["members"]:
        m["initials"] = initials(m["name"])

T = {}
T["base.html"] = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>document.documentElement.className += " js";</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ description }}">
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://bhushan-group.github.io/assets/img/photos/organoids-crc.jpg">
{% if gsc %}<meta name="google-site-verification" content="{{ gsc }}">
{% endif %}<link rel="canonical" href="{{ canonical }}">
<link rel="icon" href="{{ root }}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&amp;family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&amp;display=swap">
<link rel="stylesheet" href="{{ root }}assets/css/style.css">
{% if umami_id %}<script defer src="https://cloud.umami.is/script.js" data-website-id="{{ umami_id }}"></script>
{% endif %}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
<div class="wrap">
<a class="brand" href="{{ root }}index.html">
<svg width="36" height="26" viewBox="0 0 36 26" aria-hidden="true"><rect x="1" y="1" width="34" height="24" rx="6" fill="#E1F0EF" stroke="#9FB3BC" stroke-width="1.5"></rect><path d="M7 9 H17 V17 H29" fill="none" stroke="#0E7C86" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path><circle cx="7" cy="9" r="2.6" fill="#0E7C86"></circle><circle cx="29" cy="17" r="2.6" fill="#C1121F"></circle></svg>
<span class="brand-text"><span class="brand-name">Bhushan Research Group</span><span class="brand-sub">Biomedical Engineering, Illinois Institute of Technology</span></span>
</a>
<nav class="site-nav" aria-label="Main">
<ul>
{% for key, label, href in nav %}<li><a href="{{ root }}{{ href }}"{% if key == page %} aria-current="page"{% endif %}>{{ label }}</a></li>
{% endfor %}{% if biomic %}<li class="nav-menu">
<button type="button" class="nav-menu-btn" aria-expanded="false" aria-controls="biomic-menu">BIOMIC<svg width="11" height="7" viewBox="0 0 11 7" aria-hidden="true"><path d="M1 1.5 L5.5 5.5 L10 1.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg></button>
<ul class="nav-menu-list" id="biomic-menu">
{% for label, href in biomic %}<li><a href="{{ href }}">{{ label }}</a></li>
{% endfor %}</ul>
</li>
{% endif %}<li><a class="nav-cta" href="{{ root }}join.html"{% if page == 'join' %} aria-current="page"{% endif %}>Join the lab</a></li>
</ul>
</nav>
</div>
</header>

<main id="main">
{% block content %}{% endblock %}
</main>

<footer class="site-footer">
<div class="wrap">
<div class="footer-grid">
<div>
<h2>Bhushan Research Group</h2>
<p>Department of Biomedical Engineering<br>Illinois Institute of Technology<br>10 West 35th Street<br>Chicago, IL 60616</p>
</div>
<div>
<h2>Contact</h2>
<p>Abhinav Bhushan<br><a href="mailto:abhushan@iit.edu">abhushan@iit.edu</a><br><a href="https://www.linkedin.com/in/abhinavphd">LinkedIn</a></p>
</div>
<div>
<h2>More</h2>
<ul class="footer-links">
<li><a href="{{ root }}news.html">Lab news</a></li>
<li><a href="{{ root }}join.html">Join the lab</a></li>
<li><a href="{{ root }}teaching.html">Teaching</a></li>
</ul>
</div>
</div>
</div>
</footer>
<script src="{{ root }}assets/js/nav.js" defer></script>
{% if page == 'people' %}<script src="{{ root }}assets/js/people.js" defer></script>
{% endif %}
{% if page in ('home', 'news') %}<script src="{{ root }}assets/js/news.js" defer></script>
{% endif %}{% if cf_token %}<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "{{ cf_token }}"}'></script>
{% endif %}</body>
</html>
'''

T["macros.html"] = r'''{% macro pub_item(p) -%}
<li class="pub">
<span class="pub-year">{{ p.year }}</span>
<div class="pub-body">
<p class="pub-title">{% if p.link %}<a href="{{ p.link }}">{{ p.title_html }}</a>{% else %}{{ p.title_html }}{% endif %}</p>
<p class="pub-authors">{{ p.authors_html }}</p>
<p class="pub-venue"><em>{{ p.venue }}</em>{{ p.citation }}</p>
{% if p.doi %}<p class="pub-doi"><a href="https://doi.org/{{ p.doi }}">doi.org/{{ p.doi }}</a></p>{% endif %}
</div>
</li>
{%- endmacro %}
{% macro play_icon() -%}
<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="none" stroke="#FFFFFF" stroke-width="1.5"></circle><path d="M13 10.5 L22 16 L13 21.5 Z" fill="#FFFFFF"></path></svg>
{%- endmacro %}
{% macro person_item(p) -%}
<article class="person">
<span class="avatar avatar-sm" aria-hidden="true">{{ p.initials }}</span>
<div>
<h3>{{ p.name }}</h3>
<p class="person-role">{{ p.role }}</p>
<p class="bio">{{ p.bio }}</p>
</div>
</article>
{%- endmacro %}
'''

T["index.html"] = r'''{% extends "base.html" %}{% from "macros.html" import pub_item, play_icon %}
{% block content %}
<section class="hero">
<div class="wrap">
<div class="hero-text">
<h1>We engineer microphysiological systems and biosensors to understand how living tissue responds to microbes, nutrients and drugs</h1>
<p class="lede">Our microfluidic platforms, organ-on-chip models and sensors let us control, perturb and measure living biology with high spatial and temporal resolution.</p>
<div class="actions">
<a class="btn btn-light" href="research.html">Explore our research</a>
<a class="btn btn-outline-light" href="publications.html">Browse publications</a>
</div>
<p class="byline">Led by <a href="people.html">Abhinav Bhushan</a>, Associate Professor of Biomedical Engineering at Illinois Institute of Technology.</p>
</div>
<figure class="mosaic">
<img class="wide" src="assets/img/photos/chip-perspective.svg" alt="A microfluidic organ-on-chip device with fluid in its channels and tubing at each port">
<img class="tile" src="assets/img/photos/organoids-crc.jpg" alt="Fluorescence image of colorectal cancer organoids">
<img class="tile" src="assets/img/photos/organoids-ecadherin.jpg" alt="Fluorescence image of organoids">
<figcaption>A microfluidic device of the kind we build, and organoids imaged in the lab.</figcaption>
</figure>
</div>
</section>

<section class="news-band" data-news-section aria-labelledby="latest-news">
<div class="wrap">
<div class="section-head">
<h2 id="latest-news">Latest from the lab</h2>
<div class="news-controls">
<a class="text-link" href="news.html">All news</a>
<button class="scroll-btn" type="button" data-scroll="prev" aria-controls="news-track" aria-label="Earlier items"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 4 L6.5 10 L12.5 16" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></svg></button>
<button class="scroll-btn" type="button" data-scroll="next" aria-controls="news-track" aria-label="Later items"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4 L13.5 10 L7.5 16" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></svg></button>
</div>
</div>
<div class="news-track" id="news-track" data-news data-layout="strip" data-limit="8" tabindex="0" aria-label="Latest news, scrolls sideways"></div>
<noscript><p class="news-status"><a href="news.html">See lab news</a></p></noscript>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head">
<div>
<h2>Engineer, model, measure</h2>
<p class="section-intro">We build reusable engineering platforms and apply them to questions where spatial control and measurement over time matter.</p>
</div>
<a class="text-link" href="research.html">How we work</a>
</div>
<div class="pillars">
{% for p in pillars %}<article class="pillar">
<img src="{{ p.img }}" alt="{{ p.alt }}" loading="lazy">
<h3>{{ p.name }}</h3>
<p>{{ p.text }}</p>
</article>
{% if not loop.last %}<div class="pillar-arrow" aria-hidden="true">{{ arrow }}</div>
{% endif %}{% endfor %}</div>
</div>
</section>

<section class="section section-wash">
<div class="wrap">
<div class="section-head">
<h2>Where we apply the platforms</h2>
<a class="text-link" href="research.html">All research</a>
</div>
<div class="apps">
{% for t in apps %}<article class="app {{ t.tint }}">
<img src="{{ t.img }}" alt="{{ t.alt }}" loading="lazy">
<div class="app-body">
<h3>{{ t.name }}</h3>
<p>{{ t.short }}</p>
<a class="text-link" href="research.html#{{ t.id }}">{{ t.link_text }}</a>
</div>
</article>
{% endfor %}</div>
</div>
</section>

<section class="section">
<div class="wrap split">
<div class="stack">
<h2>Recent publications</h2>
<ol class="pub-list">
{% for p in featured %}{{ pub_item(p) }}
{% endfor %}</ol>
<div class="links-row"><a class="text-link" href="publications.html">All publications</a></div>
</div>
<div class="stack">
<h2>On video</h2>
<ul class="videos">
{% for v in videos %}<li><a class="video" href="https://youtu.be/{{ v.id }}">
<span class="video-thumb"><img src="https://i.ytimg.com/vi/{{ v.id }}/mqdefault.jpg" alt="" loading="lazy" onerror="this.remove()">{{ play_icon() }}</span>
<span class="video-title">{{ v.title }}</span>
</a></li>
{% endfor %}</ul>
<div class="links-row"><a class="text-link" href="https://www.iit.edu/news/chip-sized-device-mighty-tool-finding-colon-cancer-treatment">Illinois Tech News story on our colon chip</a></div>
</div>
</div>
</section>

<section class="join-band">
<div class="wrap">
<img src="assets/img/photos/group-dinner.jpg" alt="Lab members sharing a meal together" loading="lazy">
<div>
<h2>Join the lab</h2>
<p>We welcome PhD, master's and undergraduate researchers who want to work where engineering, biology and computation meet, in a lab built on academic freedom and room to follow your own scientific curiosity.</p>
<div class="actions">
<a class="btn btn-light" href="join.html">See open positions</a>
<a class="btn btn-outline-light" href="people.html">Meet the team</a>
</div>
</div>
</div>
</section>
{% endblock %}
'''

T["research.html"] = r'''{% extends "base.html" %}{% from "macros.html" import pub_item %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>Research</h1>
<p class="lede">Rather than treating each disease or tissue as a separate technology, we build reusable engineering platforms and apply them where spatial control and measurement over time matter.</p>
</div>
</section>
<section class="section" style="padding-top: 56px; padding-bottom: 24px">
<div class="wrap">
<div class="research-intro">
{% for p in pillars %}<div>
<h3>{{ p.name }}</h3>
<p>{{ p.text }}</p>
</div>
{% endfor %}</div>
<figure class="figure-wide">
<img src="assets/img/photos/chip-cross-section.svg" alt="Cross-section of a two-compartment organ-on-chip: tissue lining the upper channel, a perfused channel carrying microbes below, and a porous membrane between them" loading="lazy">
<figcaption>Inside a two-compartment chip: tissue lines the upper channel, a perfused channel runs below, and a porous membrane between them lets molecules cross.</figcaption>
</figure>
</div>
</section>
<div class="wrap">
{% for t in themes %}<section class="theme-block" id="{{ t.id }}">
<div>
<img class="theme-img" src="{{ t.img }}" alt="{{ t.alt }}" loading="lazy">
<h2>{{ t.name }}</h2>
<div class="prose">
{% for para in t.paras %}<p>{{ para }}</p>
{% endfor %}</div>
</div>
<div>
<p class="label">Selected papers</p>
<ol class="pub-list compact">
{% for p in t.pubs[:5] %}{{ pub_item(p) }}
{% endfor %}</ol>
</div>
</section>
{% endfor %}<section class="theme-block" id="earlier">
<div>
<img class="theme-img" src="assets/img/photos/gc-column.jpg" alt="A microfabricated metal gas chromatography column next to a penny" loading="lazy">
<h2>Other and earlier projects</h2>
<div class="prose">
<p>Past and collaborative projects include a patient-derived pancreatic cancer-on-a-chip for testing combination drugs, a point-of-care saliva test for periodontitis, analysis of volatile compounds in breath and other samples, and microfabricated columns for gas chromatography.</p>
</div>
</div>
<div>
<p class="label">Watch and read</p>
<ul class="plain-list">
<li><a href="https://youtu.be/4gC0glk5DKs">Video: personalized organ-chip to battle one of the deadliest cancers</a></li>
<li><a href="https://www.nature.com/articles/s41378-022-00370-6">Paper: patient-derived pancreatic cancer-on-a-chip</a></li>
<li><a href="https://www.youtube.com/watch?v=8fOIGsyLICQ">Video: stopping gum disease with a spit test</a></li>
<li><a href="https://spj.science.org/doi/10.34133/bmef.0002">Paper: diagnostic potential of VOC profiling for noninfectious diseases</a></li>
<li><a href="https://ieeexplore.ieee.org/document/4147573">Paper: LIGA-fabricated nickel micro gas chromatograph columns</a></li>
</ul>
</div>
</section>
</div>
{% endblock %}
'''

T["publications.html"] = r'''{% extends "base.html" %}{% from "macros.html" import pub_item %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>Publications</h1>
<p class="lede">Journal articles and preprints from the lab and its collaborations, newest first.</p>
</div>
</section>
<section class="section" style="padding-top: 48px">
<div class="wrap">
<ol class="pub-list">
{% for p in pubs %}{{ pub_item(p) }}
{% endfor %}</ol>
</div>
</section>
{% endblock %}
'''

T["news.html"] = r'''{% extends "base.html" %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>News</h1>
<p class="lede">Papers, talks, awards and people: what is happening in the lab.</p>
</div>
</section>
<section class="section" style="padding-top: 56px">
<div class="wrap">
<div class="news-archive" data-news data-layout="archive"></div>
<noscript><p class="news-status">News needs JavaScript to display. The items are also listed in <a href="data/news.json">data/news.json</a>.</p></noscript>
</div>
</section>
{% endblock %}
'''

T["people.html"] = r'''{% extends "base.html" %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>People</h1>
<p class="lede">Students and staff working across engineering, biology and computation.</p>
</div>
</section>
<section class="section" style="padding-top: 56px">
<div class="wrap">
<figure class="banner">
<img src="assets/img/photos/group-outdoors.jpg" alt="Members of the Bhushan lab standing together outdoors">
</figure>
<div class="pi" style="margin-top: 64px">
<span class="avatar avatar-lg"><img src="assets/img/people/abhinav-bhushan.jpg" alt="" width="180" height="180"></span>
<div>
<h2>Abhinav Bhushan</h2>
<p class="pi-role">Associate Professor, Biomedical Engineering</p>
<div class="links-row">
<a class="text-link" href="mailto:abhushan@iit.edu">abhushan@iit.edu</a>
<a class="text-link" href="https://www.linkedin.com/in/abhinavphd">LinkedIn</a>
</div>
<div class="prose">
{{ pi_prose }}
</div>
</div>
</div>
</div>
</section>
<section class="section section-wash">
<div class="wrap">
<div data-people></div>
<noscript><p class="news-status">The list of lab members needs JavaScript to display. The names are also in <a href="data/people.json">data/people.json</a>.</p></noscript>
</div>
</section>
<section class="join-band">
<div class="wrap">
<img src="assets/img/photos/group-conference.jpg" alt="Lab members at a conference" loading="lazy">
<div>
<h2>Want to work with us?</h2>
<p>We welcome students and postdocs who want to work where engineering, biology and computation meet.</p>
<div class="actions">
<a class="btn btn-light" href="join.html">See open positions</a>
</div>
</div>
</div>
</section>
{% endblock %}
'''

T["join.html"] = r'''{% extends "base.html" %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>Join the lab</h1>
<p class="lede">We welcome PhD, master's and undergraduate researchers and postdocs who want to work where engineering, biology and computation meet.</p>
<div class="actions"><a class="btn btn-light" href="mailto:abhushan@iit.edu">Email Prof. Bhushan</a></div>
</div>
</section>
<section class="section" style="padding-top: 64px">
<div class="wrap">
<div class="block two-col center">
<div>
<h2 style="margin-bottom: 24px">Positions</h2>
<div class="prose">
<p>The lab has positions for highly motivated undergraduate and graduate students and postdocs interested in multidisciplinary training at the intersection of engineering, biology and medicine. Projects center on microfluidic platforms and biomedical devices for diagnostic and therapeutic applications, and span a wide range of research topics.</p>
<p>To ask about openings, <a href="mailto:abhushan@iit.edu">email Prof. Bhushan</a> with a short description of your background and the kind of work you would like to do.</p>
</div>
</div>
<img src="assets/img/photos/group-dinner.jpg" alt="Lab members sharing a meal together" loading="lazy">
</div>
{{ credit_block }}
</div>
</section>
{% endblock %}
'''

T["teaching.html"] = r'''{% extends "base.html" %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>Teaching</h1>
<p class="lede">Courses I teach or have taught at Illinois Tech.</p>
</div>
</section>
<section class="section" style="padding-top: 56px">
<div class="wrap">
<div class="two-col center" style="margin-bottom: 72px">
<img src="assets/img/photos/teaching-bhushan.jpg" alt="Abhinav Bhushan teaching" loading="lazy">
<div class="prose">
<p>My teaching runs from the first-year introduction to biomedical engineering through to graduate courses on medical devices, microfluidics and synthetic biology.</p>
<p>The emphasis is on building and testing real things: students design and fabricate devices, work through the primary literature, and in the synthetic biology course take a project all the way to an international competition.</p>
</div>
</div>
{{ teaching_body }}
</div>
</section>
{% endblock %}
'''

T["404.html"] = r'''{% extends "base.html" %}
{% block content %}
<section class="page-head">
<div class="wrap">
<h1>Page not found</h1>
<p class="lede">That page doesn't exist or has moved.</p>
<div class="actions"><a class="btn btn-light" href="/index.html">Go to the homepage</a></div>
</div>
</section>
{% endblock %}
'''

# Course lists for the Join and Teaching pages. Edit these two HTML files directly.
FRAG = os.path.join(HERE, "fragments")
credit_block = Markup(open(os.path.join(FRAG, "join_credit.html")).read())
teaching_body = Markup(open(os.path.join(FRAG, "teaching_body.html")).read())

env = Environment(loader=DictLoader(T), autoescape=True, keep_trailing_newline=True)
PAGES = [
 ("index.html", "home", "Bhushan Research Group | Illinois Tech", "We engineer microphysiological systems and biosensors to understand how living tissue responds to microbes, nutrients and drugs. Biomedical Engineering at Illinois Institute of Technology."),
 ("research.html", "research", "Research | Bhushan Research Group", "Engineer, model, measure: organ-on-chip platforms applied to microbes and colorectal cancer, liver–fat crosstalk, drug response and on-chip sensing."),
 ("publications.html", "publications", "Publications | Bhushan Research Group", "Journal articles and preprints from the Bhushan Research Group at Illinois Tech."),
 ("news.html", "news", "News | Bhushan Research Group", "Lab news from the Bhushan Research Group at Illinois Tech: papers, talks, awards and people."),
 ("people.html", "people", "People | Bhushan Research Group", "Students, staff and principal investigator of the Bhushan Research Group."),
 ("join.html", "join", "Join the lab | Bhushan Research Group", "Research positions and course-credit opportunities in the Bhushan Research Group."),
 ("teaching.html", "teaching", "Teaching | Bhushan Research Group", "Courses taught by Abhinav Bhushan at Illinois Tech."),
 ("404.html", "none", "Page not found | Bhushan Research Group", "Page not found."),
]
ctx = dict(nav=NAV, themes=THEMES, apps=APPS, pillars=PILLARS, featured=FEATURED, videos=VIDEOS, pubs=PUBS,
           groups=GROUPS, pi_prose=Markup(PI_PROSE), arrow=GLYPH_ARROW,
           credit_block=credit_block, teaching_body=teaching_body)

if os.path.exists(OUT):
    shutil.rmtree(OUT)
for d in ("assets/img", "assets/css", "assets/js", "data"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
shutil.copy(os.path.join(HERE, "static", "favicon.svg"), os.path.join(OUT, "assets/img/favicon.svg"))
os.makedirs(os.path.join(OUT, "assets/img/photos"), exist_ok=True)
os.makedirs(os.path.join(OUT, "assets/img/news"), exist_ok=True)
os.makedirs(os.path.join(OUT, "assets/img/people"), exist_ok=True)
for sub in ("photos", "news", "people"):
    # images live in assets/img; Pages CMS uploads news photos and headshots there
    src = os.path.join(ROOT, "assets", "img", sub)
    for f in os.listdir(src):
        if f.endswith(".txt"):
            continue
        shutil.copy(os.path.join(src, f), os.path.join(OUT, "assets/img", sub, f))
shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "assets/css/style.css"))
shutil.copy(os.path.join(HERE, "news.js"), os.path.join(OUT, "assets/js/news.js"))
shutil.copy(os.path.join(HERE, "nav.js"), os.path.join(OUT, "assets/js/nav.js"))
shutil.copy(os.path.join(HERE, "people.js"), os.path.join(OUT, "assets/js/people.js"))
for fname, page, title, desc in PAGES:
    root = "/" if fname == "404.html" else ""
    html = env.get_template(fname).render(page=page, title=title, description=desc, root=root,
                                          umami_id=UMAMI_WEBSITE_ID, cf_token=CF_BEACON_TOKEN, biomic=BIOMIC,
                                          canonical=BASE_URL + ("" if fname == "index.html" else fname),
                                          gsc=GSC_VERIFICATION, **ctx)
    open(os.path.join(OUT, fname), "w").write(html)
print("built", [p[0] for p in PAGES])
print({t["id"]: len(t["pubs"]) for t in THEMES})
shutil.copy(os.path.join(ROOT, "data", "news.json"), os.path.join(OUT, "data/news.json"))
shutil.copy(os.path.join(ROOT, "data", "people.json"), os.path.join(OUT, "data/people.json"))

# build/siteroot holds files that must sit at the top level of the site and
# survive every re-upload, such as search-engine verification files.
ROOTDIR = os.path.join(HERE, "siteroot")
if os.path.isdir(ROOTDIR):
    for f in sorted(os.listdir(ROOTDIR)):
        if f == "README.txt":
            continue
        shutil.copy(os.path.join(ROOTDIR, f), os.path.join(OUT, f))
        print("site root:", f)

# Search engines find pages far faster when handed a list of them.
import datetime
today = datetime.date.today().isoformat()
urls = []
for fname, page, title, desc in PAGES:
    if fname == "404.html":
        continue
    loc = BASE_URL + ("" if fname == "index.html" else fname)
    priority = "1.0" if fname == "index.html" else "0.8"
    urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
                f"    <priority>{priority}</priority>\n  </url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls) + "\n</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(
    "User-agent: *\nAllow: /\n\nSitemap: " + BASE_URL + "sitemap.xml\n")
print("wrote sitemap.xml with", len(urls), "urls, and robots.txt")
