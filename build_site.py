#!/usr/bin/env python3
"""Build Elite Agentic Solutions site pages from markdown sources."""
import os
import re
import shutil
import markdown
from pathlib import Path

SITE_ROOT = Path("/Users/berylusllc/elite-agentic-solutions-site")
DOWNLOADS = Path("/Users/berylusllc/Downloads")
VAULT = Path("/Users/berylusllc/Documents/Obsidian Vault/elite-agentic-master-package")

# Tracking pixel / analytics snippet (shared with elite-ai-empire-site)
HEAD_TRACKING = """<!-- Google Analytics (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RNPW0BFLCF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-RNPW0BFLCF');
</script>
<!-- Facebook Pixel -->
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '506606013454412');
  fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=506606013454412&ev=PageView&noscript=1"/></noscript>"""

SHARED_CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0A0A1A;--bg2:#111128;--bg3:#1A1A3E;--primary:#8B5CF6;--primary-glow:#8B5CF640;--accent:#00D4AA;--accent-glow:#00D4AA40;--text:#E8E8F0;--text-dim:#9090B0;--card-bg:#12122A;--card-border:#1E1E40;--radius:16px;--radius-sm:10px}
html{scroll-behavior:smooth}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;overflow-x:hidden;font-weight:400}
a{color:var(--primary);text-decoration:none;transition:color .2s}
a:hover{color:var(--accent)}
::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--primary)}

/* Nav */
nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:1rem 2rem;background:rgba(10,10,26,.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(139,92,246,.1)}
.nav-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem}
.nav-logo{font-weight:800;font-size:1.15rem;background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.nav-links{display:flex;gap:1.5rem;align-items:center}
.nav-links a{color:var(--text-dim);font-size:.9rem;font-weight:500}
.nav-links a:hover{color:var(--text)}
.nav-cta{padding:.55rem 1.25rem;border-radius:50px;background:linear-gradient(135deg,var(--primary),#6D28D9);color:#fff !important;font-weight:600;font-size:.85rem;transition:all .3s;border:none;cursor:pointer;white-space:nowrap}
.nav-cta:hover{transform:translateY(-2px);box-shadow:0 4px 20px var(--primary-glow);color:#fff !important}

/* Article layout */
.page-wrap{max-width:820px;margin:0 auto;padding:8rem 1.5rem 4rem}
.page-wrap-wide{max-width:1100px;margin:0 auto;padding:8rem 1.5rem 4rem}
.article-header{margin-bottom:3rem;padding-bottom:2rem;border-bottom:1px solid var(--card-border)}
.eyebrow{display:inline-block;padding:.35rem 1rem;border-radius:50px;background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.3);color:var(--primary);font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1.25rem}
h1{font-size:clamp(2rem,5vw,3.25rem);font-weight:900;line-height:1.1;margin-bottom:1.5rem;background:linear-gradient(135deg,#fff 0%,#E8E8F0 50%,var(--primary) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.article-meta{color:var(--text-dim);font-size:.9rem}
.prose h2{font-size:clamp(1.5rem,3vw,2rem);font-weight:800;margin:3rem 0 1rem;color:#fff;line-height:1.25}
.prose h3{font-size:1.3rem;font-weight:700;margin:2rem 0 .75rem;color:var(--accent)}
.prose h4{font-size:1.1rem;font-weight:700;margin:1.5rem 0 .5rem;color:#fff}
.prose p{margin-bottom:1.25rem;color:#D0D0E0;font-size:1.05rem}
.prose ul,.prose ol{margin:1rem 0 1.5rem 1.5rem;color:#D0D0E0}
.prose li{margin-bottom:.5rem;font-size:1.05rem}
.prose strong{color:#fff;font-weight:700}
.prose em{color:var(--accent);font-style:italic}
.prose blockquote{border-left:3px solid var(--primary);padding:.75rem 1.25rem;margin:1.5rem 0;background:rgba(139,92,246,.05);color:var(--text-dim);font-style:italic}
.prose code{background:var(--card-bg);padding:.15rem .45rem;border-radius:5px;font-size:.9em;color:var(--accent);border:1px solid var(--card-border)}
.prose pre{background:var(--card-bg);padding:1.25rem;border-radius:var(--radius-sm);overflow-x:auto;margin:1.5rem 0;border:1px solid var(--card-border)}
.prose pre code{background:transparent;border:none;padding:0;color:var(--text)}
.prose hr{border:none;border-top:1px solid var(--card-border);margin:2.5rem 0}
.prose a{color:var(--primary);text-decoration:underline;text-decoration-color:rgba(139,92,246,.4);text-underline-offset:3px}
.prose a:hover{color:var(--accent);text-decoration-color:var(--accent)}
.prose table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:.95rem}
.prose th{background:var(--card-bg);padding:.85rem 1rem;text-align:left;font-weight:700;color:#fff;border:1px solid var(--card-border)}
.prose td{padding:.75rem 1rem;border:1px solid var(--card-border);color:#D0D0E0;vertical-align:top}
.prose tr:nth-child(even) td{background:rgba(18,18,42,.4)}

/* CTA block */
.cta-block{margin:3.5rem 0 1rem;padding:2.5rem;border-radius:var(--radius);background:linear-gradient(135deg,rgba(139,92,246,.12),rgba(0,212,170,.08));border:1px solid rgba(139,92,246,.3);text-align:center}
.cta-block h3{font-size:1.6rem;font-weight:800;color:#fff;margin-bottom:.75rem}
.cta-block p{color:var(--text-dim);margin-bottom:1.5rem;font-size:1.05rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.9rem 2rem;border-radius:50px;background:linear-gradient(135deg,var(--primary),#6D28D9);color:#fff !important;font-weight:700;font-size:1rem;transition:all .3s;border:none;cursor:pointer;text-decoration:none !important}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 28px var(--primary-glow);color:#fff !important}
.btn-secondary{background:transparent;border:1px solid var(--card-border);color:var(--text) !important}
.btn-secondary:hover{border-color:var(--primary);color:var(--primary) !important}
.btn-group{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}

/* Blog index */
.blog-grid{display:grid;gap:1.5rem;margin-top:2rem}
.blog-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius);padding:2rem;transition:all .3s;display:block}
.blog-card:hover{transform:translateY(-3px);border-color:var(--primary);box-shadow:0 8px 30px rgba(0,0,0,.3)}
.blog-card h3{font-size:1.4rem;font-weight:800;color:#fff;margin-bottom:.75rem;line-height:1.3}
.blog-card p{color:var(--text-dim);margin-bottom:1rem;font-size:1rem}
.blog-card .read-more{color:var(--primary);font-weight:600;font-size:.9rem}
.blog-card:hover .read-more{color:var(--accent)}

/* Compare table */
.compare-hero{text-align:center;margin-bottom:3rem}
.compare-table{width:100%;border-collapse:collapse;margin:2rem 0;background:var(--card-bg);border-radius:var(--radius);overflow:hidden;border:1px solid var(--card-border)}
.compare-table th{background:linear-gradient(135deg,rgba(139,92,246,.2),rgba(0,212,170,.1));padding:1rem;text-align:left;font-weight:700;color:#fff;border-bottom:1px solid var(--card-border)}
.compare-table td{padding:1rem;border-bottom:1px solid var(--card-border);color:#D0D0E0;vertical-align:top}
.compare-table tr:last-child td{border-bottom:none}
.check{color:var(--accent);font-weight:700}
.cross{color:#E0526E;font-weight:700}
.winner-tag{display:inline-block;padding:.2rem .6rem;border-radius:4px;background:rgba(0,212,170,.15);color:var(--accent);font-size:.75rem;font-weight:700;margin-left:.5rem}

/* Gated download form */
.download-hero{text-align:center;margin-bottom:3rem}
.download-form{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius);padding:2.5rem;max-width:520px;margin:0 auto}
.download-form label{display:block;color:var(--text);font-weight:600;margin-bottom:.5rem;font-size:.9rem}
.download-form input,.download-form select{width:100%;padding:.85rem 1rem;border-radius:var(--radius-sm);background:var(--bg);border:1px solid var(--card-border);color:var(--text);font-size:1rem;margin-bottom:1.25rem;font-family:inherit}
.download-form input:focus,.download-form select:focus{outline:none;border-color:var(--primary)}
.download-form button{width:100%;padding:1rem;border-radius:50px;background:linear-gradient(135deg,var(--primary),#6D28D9);color:#fff;font-weight:700;font-size:1rem;border:none;cursor:pointer;transition:all .3s}
.download-form button:hover{transform:translateY(-2px);box-shadow:0 8px 28px var(--primary-glow)}
.download-preview{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius);padding:2rem;margin:2rem 0}
.download-preview h3{color:var(--accent);font-size:1.2rem;margin-bottom:1rem}
.download-preview ul{margin-left:1.25rem;color:#D0D0E0}
.download-preview li{margin-bottom:.35rem}

/* Footer */
footer{background:var(--bg2);border-top:1px solid var(--card-border);padding:3rem 2rem;margin-top:4rem}
.footer-inner{max-width:1200px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1.5rem}
.footer-brand{font-weight:800;font-size:1rem;background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.footer-copy{color:var(--text-dim);font-size:.8rem}
.footer-links{display:flex;gap:1.25rem;flex-wrap:wrap}
.footer-links a{color:var(--text-dim);font-size:.85rem}
.footer-links a:hover{color:var(--primary)}

@media(max-width:768px){
  .page-wrap,.page-wrap-wide{padding:6.5rem 1rem 3rem}
  .nav-links{display:none}
  nav{padding:.75rem 1rem}
  .cta-block{padding:1.75rem}
  .compare-table th,.compare-table td{padding:.65rem .5rem;font-size:.85rem}
}"""


def page_header(title, description, og_url, og_image=None, extra_head=""):
    og_image = og_image or "https://eliteagenticsolutions.com/assets/og-image.png"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{HEAD_TRACKING}
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{og_url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{og_image}">
<meta property="og:site_name" content="Elite Agentic Solutions">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{SHARED_CSS}</style>
{extra_head}
</head>
<body>
<nav id="nav">
  <div class="nav-inner">
    <a href="/" class="nav-logo">Elite Agentic Solutions</a>
    <div class="nav-links">
      <a href="/#platform">Platform</a>
      <a href="/#pricing">Pricing</a>
      <a href="/blog/">Blog</a>
      <a href="/#demo">Demo</a>
    </div>
    <a href="/#demo" class="nav-cta">Book a Demo</a>
  </div>
</nav>
"""


FOOTER = """<footer>
  <div class="footer-inner">
    <div>
      <div class="footer-brand">Elite Agentic Solutions</div>
      <div class="footer-copy">Agentic operations platform for regulated industries &copy; 2026</div>
    </div>
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/blog/">Blog</a>
      <a href="/downloads/aml-toolkit.html">AML Toolkit</a>
      <a href="/downloads/rcm-checklist.html">RCM Checklist</a>
      <a href="/#demo">Book a Demo</a>
    </div>
  </div>
</footer>
</body>
</html>"""


CTA_DEMO = """<div class="cta-block">
  <h3>See Your Workflow Automated in 48 Hours</h3>
  <p>Get a free operations assessment. We map your highest-ROI automation opportunity and calculate expected savings before you commit to anything.</p>
  <div class="btn-group">
    <a href="/#demo" class="btn">Book a Demo</a>
    <a href="/#pricing" class="btn btn-secondary">See Pricing</a>
  </div>
</div>"""


def md_to_html(md_text):
    md = markdown.Markdown(extensions=['extra', 'tables', 'toc', 'sane_lists'])
    # Strip YAML front matter if present
    if md_text.lstrip().startswith('---'):
        parts = md_text.lstrip().split('---', 2)
        if len(parts) >= 3:
            md_text = parts[2]
    html = md.convert(md_text)
    return html


def build_blog_post(src_file, out_file, title, description, slug, eyebrow="Blog Post"):
    md_text = src_file.read_text()
    # Strip the first H1 from md (we render it separately)
    lines = md_text.splitlines()
    h1_text = None
    body_lines = []
    for line in lines:
        if h1_text is None and line.startswith('# '):
            h1_text = line[2:].strip()
            continue
        body_lines.append(line)
    body_md = "\n".join(body_lines)
    # Remove Meta description / Target keyword metadata scaffolding that appears at top of some posts
    body_md = re.sub(r'^\*\*(Meta description|Target keyword|URL slug|Word count|Internal links|Secondary keywords|Author)[^\n]*\n', '', body_md, flags=re.MULTILINE)

    body_html = md_to_html(body_md)
    og_url = f"https://eliteagenticsolutions.com/blog/{slug}.html"

    headline = (h1_text or title).replace('"', '\\"')
    desc_esc = description.replace('"', '\\"')
    ld_json = (
        '<script type="application/ld+json">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "BlogPosting",\n'
        f'  "headline": "{headline}",\n'
        f'  "description": "{desc_esc}",\n'
        f'  "url": "{og_url}",\n'
        '  "datePublished": "2026-04-10",\n'
        '  "dateModified": "2026-04-15",\n'
        '  "author": {"@type":"Organization","name":"Elite Agentic Solutions"},\n'
        '  "publisher": {"@type":"Organization","name":"Elite Agentic Solutions","logo":{"@type":"ImageObject","url":"https://eliteagenticsolutions.com/assets/og-image.png"}}\n'
        '}\n'
        '</script>'
    )

    html = page_header(title, description, og_url, extra_head=ld_json)
    html += f"""<main class="page-wrap">
  <article>
    <header class="article-header">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1_text or title}</h1>
      <div class="article-meta">Elite Agentic Solutions &middot; April 2026</div>
    </header>
    <div class="prose">
      {body_html}
    </div>
    {CTA_DEMO}
  </article>
</main>
"""
    html += FOOTER
    out_file.write_text(html)
    return h1_text or title


def build_blog_index(posts, out_file):
    og_url = "https://eliteagenticsolutions.com/blog/"
    html = page_header(
        "Blog — Elite Agentic Solutions",
        "Agentic AI, compliance automation, and operations insights for regulated industries.",
        og_url,
    )
    cards = []
    for p in posts:
        cards.append(f"""<a href="/blog/{p['slug']}.html" class="blog-card">
      <h3>{p['title']}</h3>
      <p>{p['excerpt']}</p>
      <span class="read-more">Read article &rarr;</span>
    </a>""")
    cards_html = "\n    ".join(cards)
    html += f"""<main class="page-wrap-wide">
  <header class="article-header">
    <span class="eyebrow">Insights</span>
    <h1>Agentic Operations Blog</h1>
    <div class="article-meta">Research, frameworks, and case studies for regulated-industry operations leaders.</div>
  </header>
  <div class="blog-grid">
    {cards_html}
  </div>
  {CTA_DEMO}
</main>
"""
    html += FOOTER
    out_file.write_text(html)


def build_compare_waystar(out_file):
    title = "Elite Agentic Solutions vs Waystar | Healthcare RCM Comparison"
    description = "Compare Elite Agentic Solutions and Waystar for revenue cycle automation. See how agentic AI beats traditional RCM platforms on cost, ROI, and adaptability."
    og_url = "https://eliteagenticsolutions.com/compare/waystar.html"
    html = page_header(title, description, og_url)
    html += f"""<main class="page-wrap-wide">
  <header class="article-header compare-hero">
    <span class="eyebrow">Comparison</span>
    <h1>Elite Agentic Solutions vs Waystar</h1>
    <div class="article-meta">Agentic AI vs legacy RCM platform &mdash; head-to-head for healthcare operations leaders</div>
  </header>
  <div class="prose">
    <h2>The Short Answer</h2>
    <p>Waystar is a capable revenue cycle management clearinghouse and analytics platform with a two-decade track record serving hospitals, physician groups, and RCM outsourcers. It handles claim submission, eligibility verification, remits processing, and denial analytics at scale.</p>
    <p><strong>What it is not:</strong> an adaptive automation platform. Waystar's underlying workflow logic is rule-based. When a payer redesigns its portal, when a denial code changes meaning, when a new prior-auth format appears &mdash; Waystar's response is a software release. Yours.</p>
    <p>Elite Agentic Solutions is purpose-built for the gap Waystar leaves: <em>the adaptive, decision-capable automation layer above the clearinghouse.</em> The five-agent engine handles prior auth appeals, denial rework, ERA reconciliation, and payer-specific workflow logic &mdash; and improves with every outcome.</p>

    <h2>Head-to-Head</h2>
    <table class="compare-table">
      <thead>
        <tr>
          <th>Capability</th>
          <th>Waystar</th>
          <th>Elite Agentic Solutions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Core architecture</strong></td>
          <td>Rule-based clearinghouse + analytics</td>
          <td>Five-agent engine with adaptive reasoning <span class="winner-tag">BETTER FIT</span></td>
        </tr>
        <tr>
          <td><strong>Handles payer portal changes</strong></td>
          <td><span class="cross">&#10007;</span> Vendor release cycle</td>
          <td><span class="check">&#10003;</span> Agent adapts automatically</td>
        </tr>
        <tr>
          <td><strong>Denial appeal drafting</strong></td>
          <td>Analytics + human team</td>
          <td><span class="check">&#10003;</span> Agents draft, submit, track</td>
        </tr>
        <tr>
          <td><strong>Unstructured document handling</strong></td>
          <td>Limited (requires pre-processing)</td>
          <td><span class="check">&#10003;</span> Native LLM document understanding</td>
        </tr>
        <tr>
          <td><strong>Implementation time</strong></td>
          <td>3&ndash;9 months typical</td>
          <td><span class="check">&#10003;</span> 2&ndash;4 weeks to pilot ROI</td>
        </tr>
        <tr>
          <td><strong>Pricing model</strong></td>
          <td>Enterprise contract + per-claim fees</td>
          <td>Tiered SaaS + outcomes-based add-ons</td>
        </tr>
        <tr>
          <td><strong>Learning over time</strong></td>
          <td><span class="cross">&#10007;</span> Static rule sets</td>
          <td><span class="check">&#10003;</span> Agents improve with every appeal outcome</td>
        </tr>
        <tr>
          <td><strong>Audit-ready decision logs</strong></td>
          <td>Transaction-level logs</td>
          <td><span class="check">&#10003;</span> Full agent reasoning + timestamp trail</td>
        </tr>
        <tr>
          <td><strong>Human-in-the-loop escalation</strong></td>
          <td>All exceptions to humans</td>
          <td><span class="check">&#10003;</span> Risk-scored routing, only real edge cases</td>
        </tr>
        <tr>
          <td><strong>Customization cost</strong></td>
          <td>Professional services engagements</td>
          <td>Self-configured SectorForge pack</td>
        </tr>
        <tr>
          <td><strong>Typical net ROI timeline</strong></td>
          <td>6&ndash;12 months</td>
          <td>Weeks &mdash; the first recovered denial pays for deployment</td>
        </tr>
      </tbody>
    </table>

    <h2>When Waystar Is the Right Choice</h2>
    <ul>
      <li>You need a primary clearinghouse and don't yet have one.</li>
      <li>Your claim volume is high and clean-claim rate is your bottleneck.</li>
      <li>You want a known, long-standing vendor with deep payer connectivity.</li>
      <li>Your IT team is comfortable absorbing rule-set maintenance and vendor release cycles.</li>
    </ul>

    <h2>When Elite Agentic Solutions Wins</h2>
    <ul>
      <li>Your denial rate is above 8% and you're losing revenue to unappealed denials.</li>
      <li>Prior authorization is eating 15+ hours per week of your billing team.</li>
      <li>You've already tried RPA or a clearinghouse's "automation" module and it broke with the first payer portal update.</li>
      <li>You want automation that <em>improves</em> with every claim, not stays static.</li>
      <li>You need sector-specific workflows that don't require six months of custom development.</li>
    </ul>

    <h2>They Can Work Together</h2>
    <p>Elite Agentic Solutions is not a clearinghouse. It sits above your clearinghouse &mdash; Waystar, Availity, Change Healthcare, or your EHR's native submission layer &mdash; and handles the adaptive work your clearinghouse cannot: navigating payer portals, reading unstructured denial letters, drafting appeals, reconciling complex ERAs, and escalating only genuinely ambiguous cases to your team.</p>
    <p>If you already use Waystar for claim submission, Elite Agentic Solutions layers on top to capture the 65% of denials that never get reworked. The ROI isn't about replacing your clearinghouse &mdash; it's about recovering the revenue your clearinghouse wasn't built to chase.</p>

    <h2>Real Numbers</h2>
    <ul>
      <li><strong>$47,000+ recovered per deployment</strong> in systematically reworked denials that billing staff had deprioritized.</li>
      <li><strong>73% reduction</strong> in denial rates by pre-submission agentic validation.</li>
      <li><strong>95% time savings</strong> on prior auth processing, ERA reconciliation, and denial rework.</li>
      <li><strong>Weeks to ROI</strong> &mdash; the first recovered denial pays for the deployment.</li>
    </ul>
  </div>
  {CTA_DEMO}
</main>
"""
    html += FOOTER
    out_file.write_text(html)


def build_compare_nice(out_file):
    title = "Elite Agentic Solutions vs NICE Actimize | AML & Compliance Comparison"
    description = "Compare Elite Agentic Solutions and NICE Actimize for AML transaction monitoring. See how agentic AI cuts false positives 60-70% without replacing your detection layer."
    og_url = "https://eliteagenticsolutions.com/compare/nice-actimize.html"
    html = page_header(title, description, og_url)
    html += f"""<main class="page-wrap-wide">
  <header class="article-header compare-hero">
    <span class="eyebrow">Comparison</span>
    <h1>Elite Agentic Solutions vs NICE Actimize</h1>
    <div class="article-meta">Agentic AI vs legacy AML platform &mdash; for BSA officers, compliance heads, and credit union risk leaders</div>
  </header>
  <div class="prose">
    <h2>The Short Answer</h2>
    <p>NICE Actimize is a mature, enterprise-grade transaction monitoring and financial crimes platform used by many of the largest banks globally. Its rule-based detection engine is sophisticated and well-understood by examiners.</p>
    <p><strong>What it is not:</strong> a solution for the <em>volume</em> problem. NICE Actimize will faithfully flag transactions that match its rule thresholds &mdash; including the 95% that are false positives. Every alert still requires a human analyst to triage, document, and dispose of.</p>
    <p>Elite Agentic Solutions does not replace NICE Actimize. It sits above it, adding the contextual reasoning and documentation automation layer that rule engines cannot provide.</p>

    <h2>Head-to-Head</h2>
    <table class="compare-table">
      <thead>
        <tr>
          <th>Capability</th>
          <th>NICE Actimize</th>
          <th>Elite Agentic Solutions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Detection architecture</strong></td>
          <td>Rule-based + statistical scoring</td>
          <td>Agentic triage layer above detection <span class="winner-tag">COMPLEMENTARY</span></td>
        </tr>
        <tr>
          <td><strong>Licensing cost (mid-size bank)</strong></td>
          <td>$200K&ndash;$850K/yr + implementation</td>
          <td>SaaS tiers starting at a fraction of enterprise platforms</td>
        </tr>
        <tr>
          <td><strong>False positive reduction</strong></td>
          <td><span class="cross">&#10007;</span> None &mdash; detection only</td>
          <td><span class="check">&#10003;</span> 60&ndash;70% alert volume reduction</td>
        </tr>
        <tr>
          <td><strong>SAR narrative drafting</strong></td>
          <td>Manual (2&ndash;4 hours per SAR)</td>
          <td><span class="check">&#10003;</span> FinCEN-formatted draft in &lt; 10 min</td>
        </tr>
        <tr>
          <td><strong>Alert context aggregation</strong></td>
          <td>Analyst pulls manually</td>
          <td><span class="check">&#10003;</span> 12&ndash;24mo history + peer comparisons auto</td>
        </tr>
        <tr>
          <td><strong>KYC/CDD onboarding orchestration</strong></td>
          <td>Separate module + integration</td>
          <td><span class="check">&#10003;</span> Included in Banking Compliance Pack</td>
        </tr>
        <tr>
          <td><strong>Explainability for examiners</strong></td>
          <td>Rule reference + disposition notes</td>
          <td><span class="check">&#10003;</span> Full reasoning chain + data cited per case</td>
        </tr>
        <tr>
          <td><strong>Implementation time</strong></td>
          <td>6&ndash;18 months</td>
          <td><span class="check">&#10003;</span> Weeks to pilot</td>
        </tr>
        <tr>
          <td><strong>Ongoing maintenance burden</strong></td>
          <td>Dedicated tuning staff required</td>
          <td>Learner agent calibrates to your customer base</td>
        </tr>
        <tr>
          <td><strong>Fits community/regional banks</strong></td>
          <td>Cost-prohibitive for most &lt; $5B banks</td>
          <td><span class="check">&#10003;</span> Built for $500M&ndash;$20B asset tier</td>
        </tr>
      </tbody>
    </table>

    <h2>When NICE Actimize Is the Right Choice</h2>
    <ul>
      <li>You are a global top-20 bank with dedicated quant teams and a seven-figure AML platform budget.</li>
      <li>You need multi-jurisdiction, multi-product detection rule libraries out of the box.</li>
      <li>Your regulators are already familiar with NICE's audit trail format.</li>
    </ul>

    <h2>When Elite Agentic Solutions Wins</h2>
    <ul>
      <li>You're a community bank, credit union, or regional bank paying enterprise licensing fees you can't justify.</li>
      <li>Your BSA team is drowning in 95% false positive alert volume.</li>
      <li>SAR narrative drafting consumes 30+ analyst hours per month.</li>
      <li>You want audit-ready automation that examiners can interrogate case-by-case.</li>
      <li>You'd rather layer agentic automation on your existing detection than rip and replace.</li>
    </ul>

    <h2>They Can Work Together</h2>
    <p>If you already run NICE Actimize, Elite Agentic Solutions adds the agentic triage and documentation layer on top. Alerts generated by NICE flow into the agentic system, which aggregates context, produces a disposition recommendation, and routes only genuinely ambiguous cases to your BSA analysts. Documented examiner-ready reasoning for every alert &mdash; automatically.</p>
    <p>The economics: you keep your existing detection investment and cut the labor cost of alert triage by 60&ndash;70% without adding headcount.</p>

    <h2>Real Numbers</h2>
    <ul>
      <li><strong>60&ndash;70% fewer alerts</strong> reach human analysts after agentic triage.</li>
      <li><strong>SAR drafting time: 2&ndash;4 hours &rarr; 10 minutes</strong>, inclusive of officer review.</li>
      <li><strong>Audit-ready reasoning</strong> logged for every case disposition.</li>
      <li><strong>KYC onboarding: 4 weeks &rarr; 5 days</strong> with KYC orchestration module.</li>
    </ul>
  </div>
  {CTA_DEMO}
</main>
"""
    html += FOOTER
    out_file.write_text(html)


def build_gated_download(out_file, pdf_name, toolkit_title, toolkit_desc, bullets, cta_hero):
    title = f"{toolkit_title} | Elite Agentic Solutions"
    description = toolkit_desc
    og_url = f"https://eliteagenticsolutions.com/downloads/{out_file.name}"
    html = page_header(title, description, og_url)
    bullets_html = "\n        ".join(f"<li>{b}</li>" for b in bullets)
    html += f"""<main class="page-wrap">
  <header class="article-header download-hero">
    <span class="eyebrow">Free Download</span>
    <h1>{toolkit_title}</h1>
    <div class="article-meta">{cta_hero}</div>
  </header>
  <div class="download-preview">
    <h3>Inside the toolkit</h3>
    <ul>
        {bullets_html}
    </ul>
  </div>
  <form class="download-form" action="BREVO_FORM_URL" method="POST" id="download-form">
    <label for="firstname">First name</label>
    <input type="text" id="firstname" name="FIRSTNAME" required>
    <label for="email">Work email</label>
    <input type="email" id="email" name="EMAIL" required>
    <label for="company">Company</label>
    <input type="text" id="company" name="COMPANY">
    <label for="role">Role</label>
    <select id="role" name="ROLE">
      <option value="">Select your role</option>
      <option>BSA / AML Officer</option>
      <option>Compliance / Risk</option>
      <option>Rev Cycle Director</option>
      <option>CFO / COO</option>
      <option>IT / Automation Lead</option>
      <option>Other</option>
    </select>
    <input type="hidden" name="SOURCE" value="{pdf_name}">
    <input type="hidden" name="redirect_url" value="/downloads/{pdf_name}">
    <button type="submit">Email Me The Toolkit &rarr;</button>
    <p style="color:var(--text-dim);font-size:.8rem;text-align:center;margin-top:1rem">No spam. Unsubscribe anytime. Your email is never sold.</p>
  </form>
  <script>
  // Track conversion + direct-download fallback. Replace BREVO_FORM_URL in production to POST to Brevo.
  document.getElementById('download-form').addEventListener('submit', function(e){{
    if(typeof fbq==='function') fbq('track','Lead',{{content_name:'{pdf_name}'}});
    if(typeof gtag==='function') gtag('event','generate_lead',{{value:1,currency:'USD',content_name:'{pdf_name}'}});
    // If Brevo URL hasn't been wired, fall back to direct download so users still get the asset.
    if(this.action.indexOf('BREVO_FORM_URL')>-1){{
      e.preventDefault();
      window.location.href='/downloads/{pdf_name}';
    }}
  }});
  </script>
</main>
"""
    html += FOOTER
    out_file.write_text(html)


def main():
    # 1. Blog posts
    blog_meta = [
        {
            'slug': '265-billion-problem',
            'src': DOWNLOADS / 'blog_post_1_265b_problem.md',
            'title': 'The $265B Problem: Why Healthcare Still Runs on Fax Machines',
            'description': 'Healthcare wastes $265B/year on admin complexity. Learn why RPA failed and how agentic AI finally closes the gap in revenue cycle automation.',
            'excerpt': 'One out of every four dollars spent on U.S. healthcare goes to paperwork. $265B/yr in administrative waste. Here is why RPA failed, and what actually works for revenue cycle.',
        },
        {
            'slug': 'agentic-ai-vs-rpa',
            'src': DOWNLOADS / 'blog_post_2_agentic_vs_rpa.md',
            'title': 'Agentic AI vs RPA: Why Bots That Think Beat Bots That Click',
            'description': 'RPA costs enterprises 30-40% of TCO in maintenance alone and 50% of projects fail to scale. Here is why agentic AI replaces your entire RPA stack.',
            'excerpt': 'RPA was a $3.6B industry built on a flawed premise. Maintenance eats 30-40% of TCO. 50% of projects fail to scale. Here is why bots that think beat bots that click.',
        },
        {
            'slug': 'small-banks-aml-automation',
            'src': DOWNLOADS / 'blog_post_3_small_banks_aml.md',
            'title': 'How Small Banks Can Automate AML Without Hiring a 10-Person Team',
            'description': 'Community banks spend $2-5M/yr on AML compliance, mostly on 95% false positive alerts. See how agentic AI cuts costs 80% and SAR time by 90%.',
            'excerpt': 'Community banks spend $2-5M/yr on AML compliance. 95% of alerts are false positives. See how agentic triage cuts alert volume 60-70% and SAR drafting time by 90%.',
        },
    ]

    for m in blog_meta:
        build_blog_post(
            m['src'],
            SITE_ROOT / 'blog' / f"{m['slug']}.html",
            m['title'],
            m['description'],
            m['slug'],
            eyebrow="Blog Post",
        )
        print(f"Built blog/{m['slug']}.html")

    # 2. Blog index
    build_blog_index(
        [{'slug': m['slug'], 'title': m['title'], 'excerpt': m['excerpt']} for m in blog_meta],
        SITE_ROOT / 'blog' / 'index.html',
    )
    print("Built blog/index.html")

    # 3. Compare pages
    build_compare_waystar(SITE_ROOT / 'compare' / 'waystar.html')
    print("Built compare/waystar.html")
    build_compare_nice(SITE_ROOT / 'compare' / 'nice-actimize.html')
    print("Built compare/nice-actimize.html")

    # 4. Copy PDFs (RCM checklist already exists in Downloads; AML toolkit not present, we'll generate it later)
    rcm_src = DOWNLOADS / 'lead_magnet_rcm_checklist.pdf'
    if rcm_src.exists():
        shutil.copy(rcm_src, SITE_ROOT / 'downloads' / 'lead_magnet_rcm_checklist.pdf')
        print("Copied lead_magnet_rcm_checklist.pdf")

    # 5. Gated download pages
    build_gated_download(
        SITE_ROOT / 'downloads' / 'aml-toolkit.html',
        'lead_magnet_aml_toolkit.pdf',
        'AML Automation Toolkit for Community Banks',
        'Free toolkit for BSA officers and community bank compliance leaders: alert triage framework, SAR narrative template, KYC acceleration playbook, and an agentic ROI calculator.',
        [
            'The 95% false positive problem &mdash; and the triage framework that cuts alert volume 60&ndash;70%',
            'FinCEN-compliant SAR narrative template that drops drafting time from 2&ndash;4 hours to 10 minutes',
            'KYC onboarding acceleration playbook (4 weeks &rarr; 5 days)',
            'Agentic-AML ROI calculator: headcount savings, examiner readiness, payback timeline',
            'Examiner-ready documentation checklist for agentic workflows',
            'Vendor comparison scorecard: rule engines, RPA, agentic AI',
        ],
        'For BSA officers, compliance directors, and risk leaders at community and regional banks.',
    )
    print("Built downloads/aml-toolkit.html")

    build_gated_download(
        SITE_ROOT / 'downloads' / 'rcm-checklist.html',
        'lead_magnet_rcm_checklist.pdf',
        'Revenue Cycle Automation Readiness Checklist',
        'Free 25-point checklist for hospital Rev Cycle Directors: where to automate first, which payer workflows pay back in weeks, and the metrics to track.',
        [
            'The 25 RCM workflows ranked by automation ROI &mdash; start with what pays back fastest',
            'Prior auth automation readiness assessment &mdash; is your stack ready?',
            'Denial rework prioritization matrix (appeal vs. resubmit vs. write-off)',
            'ERA/EOB reconciliation automation scorecard',
            'Payer portal workflow inventory template',
            'KPI framework: cost-to-collect, clean claim rate, appeal success by payer',
            'Baseline metrics worksheet for your first 90 days',
        ],
        'For Rev Cycle Directors, CFOs, and practice administrators serious about cutting cost-to-collect.',
    )
    print("Built downloads/rcm-checklist.html")


if __name__ == '__main__':
    main()
