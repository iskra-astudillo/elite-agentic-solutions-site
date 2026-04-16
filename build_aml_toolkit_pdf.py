#!/usr/bin/env python3
"""Generate the AML Automation Toolkit PDF lead magnet."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, ListFlowable, ListItem,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from pathlib import Path

OUT = Path("/Users/berylusllc/elite-agentic-solutions-site/downloads/lead_magnet_aml_toolkit.pdf")

PRIMARY = HexColor("#8B5CF6")
ACCENT = HexColor("#00D4AA")
DARK = HexColor("#0A0A1A")
TEXT = HexColor("#1a1a2e")
TEXT_DIM = HexColor("#505070")
CARD_BG = HexColor("#F4F4FA")


def build():
    styles = getSampleStyleSheet()
    base = styles['Normal']
    base.fontName = 'Helvetica'
    base.fontSize = 10.5
    base.leading = 15
    base.textColor = TEXT

    title_style = ParagraphStyle(
        'Title', parent=base, fontName='Helvetica-Bold',
        fontSize=24, leading=28, textColor=PRIMARY, spaceAfter=12, alignment=TA_LEFT,
    )
    subtitle_style = ParagraphStyle(
        'Sub', parent=base, fontName='Helvetica', fontSize=13, leading=18,
        textColor=TEXT_DIM, spaceAfter=18,
    )
    h1 = ParagraphStyle(
        'H1', parent=base, fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=PRIMARY, spaceBefore=14, spaceAfter=8,
    )
    h2 = ParagraphStyle(
        'H2', parent=base, fontName='Helvetica-Bold', fontSize=12.5, leading=17,
        textColor=DARK, spaceBefore=10, spaceAfter=4,
    )
    body = ParagraphStyle(
        'Body', parent=base, fontName='Helvetica', fontSize=10.5, leading=15, spaceAfter=8,
    )
    bullet = ParagraphStyle(
        'Bullet', parent=body, leftIndent=16, bulletIndent=4, spaceAfter=4,
    )
    cta_style = ParagraphStyle(
        'CTA', parent=base, fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=ACCENT, spaceBefore=8, spaceAfter=6, alignment=TA_CENTER,
    )
    cover_big = ParagraphStyle(
        'Big', parent=base, fontName='Helvetica-Bold', fontSize=32, leading=36,
        textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=14,
    )

    doc = SimpleDocTemplate(
        str(OUT), pagesize=LETTER,
        leftMargin=0.9*inch, rightMargin=0.9*inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch,
        title="AML Automation Toolkit for Community Banks",
        author="Elite Agentic Solutions",
    )

    story = []

    # COVER
    story.append(Paragraph("ELITE AGENTIC SOLUTIONS", ParagraphStyle(
        'eyebrow', parent=base, fontName='Helvetica-Bold', fontSize=10,
        textColor=ACCENT, spaceAfter=18,
    )))
    story.append(Paragraph("AML Automation Toolkit", cover_big))
    story.append(Paragraph("for Community & Regional Banks", ParagraphStyle(
        'subcover', parent=base, fontName='Helvetica', fontSize=16, textColor=TEXT_DIM, spaceAfter=30,
    )))
    story.append(Paragraph(
        "The alert triage framework, SAR narrative template, KYC acceleration playbook, and ROI "
        "calculator that BSA officers are using to cut compliance cost 80% without adding headcount.",
        body,
    ))
    story.append(Spacer(1, 0.35*inch))

    # Stats grid
    stats = [
        ["95%", "Typical false positive rate on rule-based AML alerts"],
        ["60-70%", "Alert volume reduction after agentic triage"],
        ["10 min", "SAR narrative drafting time (was 2-4 hours)"],
        ["$2-5M", "Annual AML spend at a typical community bank"],
    ]
    stat_table = Table(
        [[Paragraph(f"<b>{n}</b>", ParagraphStyle('n', fontName='Helvetica-Bold', fontSize=22, textColor=PRIMARY)),
          Paragraph(d, ParagraphStyle('d', fontName='Helvetica', fontSize=10, textColor=TEXT_DIM, leading=13))]
         for n, d in stats],
        colWidths=[1.2*inch, 4.8*inch],
    )
    stat_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#DDDDEE')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#DDDDEE')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("&copy; 2026 Elite Agentic Solutions &middot; eliteagenticsolutions.com", ParagraphStyle(
        'foot', parent=base, fontSize=8, textColor=TEXT_DIM,
    )))
    story.append(PageBreak())

    # SECTION 1: ALERT TRIAGE
    story.append(Paragraph("Part 1 &middot; Alert Triage Framework", h1))
    story.append(Paragraph(
        "A $2B community bank running standard transaction monitoring rules generates 200-500 alerts per "
        "week, ~95% of which are false positives. Every alert, regardless of outcome, requires review and "
        "documentation. The result: 3-4 full-time analysts on triage alone.",
        body,
    ))
    story.append(Paragraph("The 4-Stage Agentic Triage Model", h2))
    for stage_title, stage_desc in [
        ("Stage 1: Context aggregation",
         "Agent pulls 12-24 months of customer transaction history, KYC profile, business type, peer "
         "comparisons, and prior alert history before any disposition logic runs."),
        ("Stage 2: Typology matching",
         "Agent compares the flagged pattern against 80+ FinCEN typologies and the bank's historical "
         "disposition patterns for similar customer profiles."),
        ("Stage 3: Risk-tiered recommendation",
         "Agent produces one of: auto-close (with full audit trail), analyst review (with context "
         "pre-packaged), or escalate to SAR drafting (with narrative pre-drafted)."),
        ("Stage 4: Explainability artifact",
         "Every disposition ships with a reasoning chain, data points cited, and risk factors weighed "
         "&mdash; examiner-ready, case-by-case."),
    ]:
        story.append(Paragraph(stage_title, ParagraphStyle(
            'stg', parent=body, fontName='Helvetica-Bold', textColor=ACCENT, spaceAfter=2,
        )))
        story.append(Paragraph(stage_desc, body))
    story.append(PageBreak())

    # SECTION 2: SAR NARRATIVE TEMPLATE
    story.append(Paragraph("Part 2 &middot; SAR Narrative Template", h1))
    story.append(Paragraph(
        "FinCEN-compliant SAR narratives follow a well-defined structure. The agentic system drafts all "
        "five sections automatically from the flagged transaction data, customer profile, and alert context. "
        "Use this template as a baseline for manual drafting or agent output review.",
        body,
    ))
    sar_sections = [
        ("1. Subject identification",
         "Full legal name, account numbers, TIN/SSN redacted per FinCEN rules, DOB, address, "
         "occupation/business type, relationship tenure with bank."),
        ("2. Account information",
         "Account types, open dates, signers, average balance, related accounts, cross-ownership flags."),
        ("3. Transaction description",
         "Chronological list of suspicious transactions with dates, amounts, counterparties, channels, "
         "and locations. Aggregate totals by pattern type."),
        ("4. Suspicious activity explanation",
         "Plain-English description of the pattern, typology classification (structuring, layering, "
         "smurfing, etc.), and why it deviates from the customer's expected profile."),
        ("5. Recommended action",
         "Continued monitoring, relationship exit, or law-enforcement referral. Include the decision "
         "rationale and supervisor sign-off."),
    ]
    for t, d in sar_sections:
        story.append(Paragraph(t, ParagraphStyle('sn', parent=body, fontName='Helvetica-Bold', textColor=ACCENT, spaceAfter=2)))
        story.append(Paragraph(d, body))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Time savings: 2-4 hours per SAR &rarr; ~10 minutes (including officer review). "
                           "For 10 SARs/month, that recovers 30+ analyst hours.", ParagraphStyle(
        'savings', parent=body, fontName='Helvetica-Oblique', textColor=TEXT_DIM,
    )))
    story.append(PageBreak())

    # SECTION 3: KYC ACCELERATION PLAYBOOK
    story.append(Paragraph("Part 3 &middot; KYC / CDD Acceleration Playbook", h1))
    story.append(Paragraph(
        "Community banks typically take 3-4 weeks to onboard a new business customer through full KYC "
        "and CDD. Agentic orchestration cuts this to 3-5 days without reducing diligence depth.",
        body,
    ))
    play_steps = [
        ("Day 1: Automated intake",
         "Agent ingests application, runs entity verification, pulls beneficial ownership from state "
         "registries, sanctions/PEP screening, adverse media scan."),
        ("Day 2: Risk tiering",
         "Agent scores customer against risk model (industry, geography, transaction profile, ownership "
         "opacity). Low-risk customers progress automatically; higher-risk routed to EDD queue."),
        ("Day 3-4: Enhanced due diligence (if needed)",
         "Agent drafts EDD questionnaire, collects required documents, validates corporate docs, and "
         "packages everything into the compliance case record."),
        ("Day 5: Approval + monitoring setup",
         "BSA officer reviews packaged case, approves/declines, and agent provisions transaction "
         "monitoring profile calibrated to this customer type."),
    ]
    for t, d in play_steps:
        story.append(Paragraph(t, ParagraphStyle('kyc', parent=body, fontName='Helvetica-Bold', textColor=ACCENT, spaceAfter=2)))
        story.append(Paragraph(d, body))

    story.append(PageBreak())

    # SECTION 4: ROI CALCULATOR
    story.append(Paragraph("Part 4 &middot; Agentic AML ROI Calculator", h1))
    story.append(Paragraph(
        "Plug in your bank's numbers. The template below uses a $2B community bank baseline.",
        body,
    ))
    roi_table_data = [
        ["Metric", "Before", "After Agentic AML", "Impact"],
        ["Weekly alerts to analysts", "400", "120-160", "60-70% reduction"],
        ["Hours/wk on alert triage", "~133 hrs", "~40-50 hrs", "~85 hrs/wk freed"],
        ["FTEs on triage", "3.5", "1.0-1.5", "2+ FTE capacity freed"],
        ["Avg SAR drafting time", "3 hrs", "10 min", "~94% time cut"],
        ["SAR analyst hrs/month (10 SARs)", "30 hrs", "2-3 hrs", "~27 hrs/mo freed"],
        ["KYC onboarding time", "4 weeks", "5 days", "~80% faster"],
        ["Annual compliance cost", "$2.0-5.0M", "$0.4-1.0M", "~80% reduction"],
    ]
    roi_table = Table(roi_table_data, colWidths=[2.0*inch, 1.2*inch, 1.6*inch, 1.6*inch])
    roi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9.5),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#DDDDEE')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), CARD_BG]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (3, 1), (3, -1), ACCENT),
        ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
    ]))
    story.append(roi_table)
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Payback timeline: most deployments break even in weeks, not quarters. The "
                           "FTE capacity freed in the first month typically covers annual platform cost.",
                           body))
    story.append(PageBreak())

    # SECTION 5: EXAMINER-READY DOCUMENTATION
    story.append(Paragraph("Part 5 &middot; Examiner-Ready Documentation Checklist", h1))
    story.append(Paragraph(
        "What examiners expect to see for agentic AML workflows:",
        body,
    ))
    checklist = [
        "Model risk management documentation (SR 11-7 alignment) for the agent's decision logic",
        "Ongoing validation report: sample case reviews, false positive/negative analysis",
        "Explainability artifact per disposition: reasoning chain, data cited, risk factors weighed",
        "Escalation protocol: defined thresholds for human review, SAR drafting, relationship exit",
        "Change control: every agent logic update versioned, reviewed, documented",
        "Independent testing program covering the agent layer quarterly or after material changes",
        "Board and committee reporting cadence: monthly MI on agent disposition patterns and outcomes",
        "Data lineage: where each data point in an alert decision originated and when it was pulled",
    ]
    for item in checklist:
        story.append(Paragraph(f"&#9744; &nbsp; {item}", bullet))

    story.append(PageBreak())

    # SECTION 6: VENDOR COMPARISON
    story.append(Paragraph("Part 6 &middot; Vendor Comparison Scorecard", h1))
    vcmp = [
        ["Capability", "Rule Engines\n(Actimize, Oracle)", "RPA\n(UiPath, Automation Anywhere)", "Agentic AI\n(Elite Agentic Solutions)"],
        ["Detection", "Strong", "None (orchestration only)", "Layered above rules"],
        ["False positive reduction", "None", "None", "60-70%"],
        ["Contextual reasoning", "No", "No", "Yes"],
        ["SAR narrative drafting", "Manual", "Manual (templated)", "Auto, FinCEN-formatted"],
        ["Adapts to portal/UI changes", "N/A", "Breaks", "Self-adapts"],
        ["Unstructured docs", "No", "OCR pre-processing", "Native"],
        ["Learns from outcomes", "No", "No", "Yes"],
        ["Licensing cost (mid-size)", "$200K-850K+/yr", "$200K+ (w/ maint.)", "Fraction of enterprise"],
        ["Implementation", "6-18 months", "3-9 months", "Weeks"],
    ]
    vtbl = Table(vcmp, colWidths=[1.6*inch, 1.7*inch, 1.7*inch, 1.7*inch])
    vtbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#DDDDEE')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), CARD_BG]),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (3, 1), (3, -1), ACCENT),
    ]))
    story.append(vtbl)

    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("Ready to pilot?", h1))
    story.append(Paragraph(
        "Book a 30-minute operations assessment. We'll map your current alert volume and compliance cost "
        "baseline, and show you exactly what a 60-70% reduction looks like for your bank &mdash; with no "
        "commitment.",
        body,
    ))
    story.append(Paragraph("eliteagenticsolutions.com/#demo", cta_style))
    story.append(Paragraph(
        "&copy; 2026 Elite Agentic Solutions. For informational use by compliance professionals. Not legal "
        "or regulatory advice. Consult your BSA officer and regulators before deploying any compliance "
        "automation.",
        ParagraphStyle('disc', parent=body, fontSize=8, textColor=TEXT_DIM, alignment=TA_CENTER, spaceBefore=20),
    ))

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == '__main__':
    build()
