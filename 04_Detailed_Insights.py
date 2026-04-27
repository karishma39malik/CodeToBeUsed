# ── GLOBAL PDF (ALL CANDIDATES) ──────────────────────────────────────────────
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
import os


import streamlit as st

st.set_page_config(
    page_title="TalentScan · Detailed Insights",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard")
def build_all_candidates_pdf(results, role_name="Role"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("<b>TalentScan AI – Full Candidate Report</b>", styles["Title"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Role: {role_name}", styles["Normal"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Loop candidates
    for idx, r in enumerate(results, 1):
        name = r.get("full_name") or r.get("original_filename") or "Unknown"

        comp = int((r.get("composite_score", 0)) * 100)
        rel  = int((r.get("relevance_score", 0)) * 100)
        sem  = int((r.get("semantic_similarity", 0)) * 100)
        pot  = int((r.get("potential_score", 0)) * 100)

        strengths = r.get("strengths") or []
        gaps = r.get("gaps") or []
        tech = r.get("technical_skills") or []
        rationale = r.get("llm_rationale") or "—"

        # Header
        elements.append(Paragraph(f"<b>#{idx} {name}</b>", styles["Heading2"]))
        elements.append(Spacer(1, 6))

        # Scores table
        score_data = [
            ["Composite", "Relevance", "Semantic", "Potential"],
            [f"{comp}%", f"{rel}%", f"{sem}%", f"{pot}%"]
        ]

        table = Table(score_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("GRID",(0,0),(-1,-1),1,colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 10))

        # Strengths
        elements.append(Paragraph("<b>Strengths</b>", styles["Heading3"]))
        if strengths:
            for s in strengths:
                elements.append(Paragraph(f"• {s}", styles["Normal"]))
        else:
            elements.append(Paragraph("—", styles["Normal"]))

        elements.append(Spacer(1, 8))

        # Gaps
        elements.append(Paragraph("<b>Gaps</b>", styles["Heading3"]))
        if gaps:
            for g in gaps:
                elements.append(Paragraph(f"• {g}", styles["Normal"]))
        else:
            elements.append(Paragraph("—", styles["Normal"]))

        elements.append(Spacer(1, 8))

        # Skills
        elements.append(Paragraph("<b>Technical Skills</b>", styles["Heading3"]))
        elements.append(Paragraph(", ".join(tech[:20]) if tech else "—", styles["Normal"]))

        elements.append(Spacer(1, 8))

        # Rationale
        elements.append(Paragraph("<b>AI Rationale</b>", styles["Heading3"]))
        elements.append(Paragraph(rationale, styles["Normal"]))

        elements.append(Spacer(1, 20))

        if idx < len(results):
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()



API_BASE = os.getenv("API_URL", "http://api:8000")
API      = f"{API_BASE}/api/v1"

FB_BLUE   = "#1877F2"
FB_GREEN  = "#42B72A"
FB_ORANGE = "#F5A623"
FB_RED    = "#FA3E3E"
FB_GREY   = "#BCC0C4"
FB_PURPLE = "#6B2FA0"
PLOT_BG   = "#FFFFFF"

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',-apple-system,sans-serif;font-size:14px;}
.stApp{background:#F0F2F5!important;}
.block-container{padding:0 1.5rem 3rem!important;max-width:1400px;}
header,[data-testid="stHeader"]{background:#FFFFFF!important;border-bottom:1px solid #CED0D4!important;}
section[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #CED0D4!important;}
h1,h2,h3,h4{color:#050505!important;}
label{color:#65676B!important;font-size:0.78rem!important;}
.ts-nav{background:linear-gradient(135deg,#0F2D6B 0%,#1877F2 100%);padding:0 1.5rem;height:60px;display:flex;align-items:center;justify-content:space-between;margin:-0.1rem -1.5rem 1.8rem -1.5rem;box-shadow:0 2px 12px rgba(24,119,242,0.25);}
.ts-nav-logo{font-size:1.4rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.5px;}
.ts-nav-badge{font-size:0.65rem;font-weight:700;background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:20px;letter-spacing:0.06em;text-transform:uppercase;margin-left:10px;}
.ts-nav-title{font-size:0.9rem;font-weight:600;color:rgba(255,255,255,0.9);}
.ts-nav-role{font-size:0.78rem;color:rgba(255,255,255,0.55);}
.metric-card{background:#FFFFFF;border-radius:10px;border:1px solid #CED0D4;padding:1rem 1.2rem;box-shadow:0 1px 4px rgba(0,0,0,0.05);position:relative;overflow:hidden;}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--accent,#1877F2);}
.metric-val{font-size:1.8rem;font-weight:800;color:#050505;line-height:1;}
.metric-lbl{font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#8A9BB0;margin-top:4px;}
.metric-sub{font-size:0.7rem;color:#BCC0C4;margin-top:2px;}
.filter-panel{background:#FFFFFF;border-radius:10px;border:1px solid #CED0D4;padding:1.2rem 1.5rem;margin-bottom:1.4rem;box-shadow:0 1px 4px rgba(0,0,0,0.05);}
.filter-title{font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#65676B;margin-bottom:1rem;}
.result-meta{display:flex;align-items:center;justify-content:space-between;background:#FFFFFF;border-radius:8px;border:1px solid #CED0D4;padding:10px 16px;margin-bottom:1rem;font-size:0.8rem;color:#65676B;}
.fb-card{background:#FFFFFF;border-radius:8px;border:1px solid #CED0D4;padding:1.2rem 1.4rem;margin-bottom:12px;box-shadow:0 1px 2px rgba(0,0,0,0.06);}
.fb-card-lg{background:#FFFFFF;border-radius:8px;border:1px solid #CED0D4;padding:1.5rem;margin-bottom:16px;box-shadow:0 1px 2px rgba(0,0,0,0.06);}
.sec-label{font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#65676B;margin-bottom:10px;}
.divider{height:1px;background:#E4E6EB;margin:1.2rem 0;}
.cand-header{display:flex;align-items:center;gap:14px;padding-bottom:14px;border-bottom:1px solid #E4E6EB;margin-bottom:14px;}
.cand-avatar{width:52px;height:52px;border-radius:50%;background:#1877F2;display:flex;align-items:center;justify-content:center;font-size:1.1rem;font-weight:700;color:#FFFFFF;flex-shrink:0;}
.cand-name{font-size:1.3rem;font-weight:700;color:#050505;line-height:1.2;}
.cand-email{font-size:0.82rem;color:#65676B;margin-top:2px;}
.badge{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:20px;font-size:0.78rem;font-weight:600;}
.badge-green{background:#E7F3E8;color:#1A6B1E;}.badge-blue{background:#E7F0FF;color:#1877F2;}
.badge-orange{background:#FFF3E0;color:#E65100;}.badge-red{background:#FFEBEE;color:#C62828;}
.badge-grey{background:#F0F2F5;color:#65676B;}.badge-dot{width:7px;height:7px;border-radius:50%;}
.fit-strong{background:#E6F9EE;color:#1A7A3A;border:1px solid #B5E8C9;padding:4px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;display:inline-block;}
.fit-moderate{background:#FFF4E5;color:#B35900;border:1px solid #FFCC80;padding:4px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;display:inline-block;}
.fit-weak{background:#FFECEC;color:#C62828;border:1px solid #FFAAA0;padding:4px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;display:inline-block;}
.sbar-row{margin:10px 0;}
.sbar-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;}
.sbar-name{font-size:0.8rem;font-weight:600;color:#050505;}
.sbar-weight{font-size:0.7rem;color:#BCC0C4;}
.sbar-val{font-size:0.85rem;font-weight:700;}
.sbar-track{height:8px;background:#F0F2F5;border-radius:4px;overflow:hidden;}
.sbar-fill{height:100%;border-radius:4px;}
.fill-blue{background:linear-gradient(90deg,#1877F2,#42A5F5);}
.fill-green{background:linear-gradient(90deg,#42B72A,#66BB6A);}
.fill-orange{background:linear-gradient(90deg,#F5A623,#FFB74D);}
.fill-red{background:linear-gradient(90deg,#FA3E3E,#EF5350);}
.sg-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.sg-box{border-radius:8px;padding:1rem;}
.sg-box-s{background:#E7F3E8;border:1px solid #B5DFBB;}
.sg-box-g{background:#FFF3E0;border:1px solid #FFCC80;}
.sg-box-label{font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;}
.sg-label-s{color:#1A6B1E;}.sg-label-g{color:#E65100;}
.sg-item{display:flex;gap:8px;align-items:flex-start;padding:5px 0;font-size:0.8rem;line-height:1.5;border-bottom:1px solid rgba(0,0,0,0.05);}
.sg-item:last-child{border-bottom:none;}
.sg-text-s{color:#1B5E20;}.sg-text-g{color:#BF360C;}
.chip-wrap{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;}
.chip{padding:4px 12px;border-radius:20px;font-size:0.75rem;font-weight:600;}
.chip-tech{background:#E7F0FF;color:#1877F2;border:1px solid #BBD3FB;}
.chip-domain{background:#F3E8FF;color:#6B2FA0;border:1px solid #DDB8FA;}
.insight-item{background:#F0F2F5;border-left:3px solid #1877F2;border-radius:0 6px 6px 0;padding:10px 14px;margin-bottom:8px;font-size:0.82rem;color:#050505;line-height:1.7;}
.rationale-box{background:#F0F2F5;border-radius:8px;border:1px solid #CED0D4;padding:1.2rem 1.4rem;font-size:0.85rem;color:#050505;line-height:1.85;font-style:italic;}
.rationale-label{font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#1877F2;margin-bottom:8px;}
.signal-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#CED0D4;border-radius:8px;overflow:hidden;margin-top:8px;}
.signal-cell{background:#FFFFFF;padding:14px 16px;}
.signal-val{font-size:1.5rem;font-weight:700;color:#050505;line-height:1;}
.signal-lbl{font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:#65676B;margin-top:3px;}
.signal-sub{font-size:0.72rem;color:#BCC0C4;margin-top:2px;}
.conf-row{display:flex;align-items:center;gap:10px;margin-top:10px;}
.conf-label{font-size:0.72rem;font-weight:600;color:#65676B;width:120px;flex-shrink:0;}
.conf-track{flex:1;height:6px;background:#F0F2F5;border-radius:3px;overflow:hidden;}
.conf-fill{height:100%;background:#1877F2;border-radius:3px;}
.conf-pct{font-size:0.75rem;font-weight:700;color:#1877F2;width:32px;text-align:right;}
.dl-strip{display:flex;gap:10px;margin:12px 0 0 0;flex-wrap:wrap;}
.stButton>button{background:#1877F2!important;color:#FFFFFF!important;border:none!important;border-radius:7px!important;font-weight:700!important;font-size:0.8rem!important;padding:8px 16px!important;}
.stButton>button:hover{background:#166FE5!important;}
.stSelectbox>div>div{background:#FFFFFF!important;border-color:#CED0D4!important;border-radius:7px!important;color:#050505!important;}
.stTextInput>div>div{background:#FFFFFF!important;border-color:#CED0D4!important;border-radius:7px!important;}
.stTextInput input{color:#050505!important;}
.stMultiSelect>div{background:#FFFFFF!important;border-color:#CED0D4!important;border-radius:7px!important;}
div[data-testid="stExpander"]{background:#FFFFFF!important;border:1px solid #CED0D4!important;border-radius:8px!important;margin-bottom:8px!important;}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def parse_list(val):
    if isinstance(val, list): return val
    if not val: return []
    try:
        r = json.loads(val); return r if isinstance(r, list) else [str(r)]
    except: return [str(val)] if val else []

def score_color(s):
    return FB_GREEN if s >= 0.65 else (FB_ORANGE if s >= 0.45 else FB_RED)

def fill_cls(s):
    return "fill-green" if s >= 0.65 else ("fill-orange" if s >= 0.45 else "fill-red")

def fit_label(s):
    if s >= 0.65: return ("Strong Fit", "strong")
    if s >= 0.45: return ("Moderate Fit", "moderate")
    return ("Weak Fit", "weak")

def badge_html(decision):
    d = (decision or "unknown").lower()
    label = (decision or "unknown").replace("_", " ").title()
    if "shortlisted" in d or "approved" in d: cls, dot = "badge-green",  "#42B72A"
    elif "rejected" in d:                      cls, dot = "badge-red",    "#FA3E3E"
    elif "hold" in d:                          cls, dot = "badge-grey",   "#BCC0C4"
    elif "forward" in d:                       cls, dot = "badge-blue",   "#1877F2"
    else:                                      cls, dot = "badge-orange", "#F5A623"
    return f'<span class="badge {cls}"><span class="badge-dot" style="background:{dot};"></span>{label}</span>'

def initials(name):
    parts = (name or "?").split()
    return "".join(p[0] for p in parts[:2]).upper()

def safe_float(val, default=0.0):
    try: return float(str(val).split()[0])
    except: return default

def get_parsed(r):
    p = r.get("parsed_data") or {}
    if isinstance(p, str):
        try: p = json.loads(p)
        except: p = {}
    return p

def subscore_html(name, value, weight):
    pct = int(value * 100)
    col = score_color(value); fc = fill_cls(value)
    return f"""<div class="sbar-row">
      <div class="sbar-header">
        <span class="sbar-name">{name} <span class="sbar-weight">{weight}</span></span>
        <span class="sbar-val" style="color:{col};">{pct}%</span>
      </div>
      <div class="sbar-track"><div class="sbar-fill {fc}" style="width:{pct}%;"></div></div>
    </div>"""

TECH_KW = {"python","sql","spark","cloud","azure","aws","gcp","kafka","airflow","api",
            "ml","ai","etl","pipeline","databricks","power bi","tableau","data",
            "engineering","model","docker","scala","java","react","node","typescript"}

# ── Chart helpers ─────────────────────────────────────────────────────────────
def gauge_chart(value, key_suffix=""):
    pct = value * 100; color = score_color(value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=pct,
        number={"suffix": "%", "font": {"size": 38, "color": "#050505"}},
        title={"text": "Composite Score", "font": {"size": 12, "color": "#65676B"}},
        gauge={"axis": {"range": [0, 100], "tickvals": [0,25,50,65,75,100],
                        "tickfont": {"size": 9, "color": "#BCC0C4"}},
               "bar": {"color": color, "thickness": 0.3},
               "bgcolor": "#F0F2F5", "bordercolor": "#E4E6EB",
               "steps": [{"range": [0,45],  "color": "#FFECEC"},
                         {"range": [45,65], "color": "#FFF4E5"},
                         {"range": [65,100],"color": "#E6F9EE"}],
               "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": pct}},
    ))
    fig.update_layout(height=220, margin=dict(t=30,b=10,l=20,r=20),
                      paper_bgcolor=PLOT_BG, font={"family": "Inter"})
    return fig

def radar_chart(rel, sem, pot, key_suffix=""):
    cats = ["Relevance<br>Score", "Semantic<br>Similarity", "Potential<br>Score"]
    vals = [rel*100, sem*100, pot*100]
    fig  = go.Figure(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]],
        fill="toself", fillcolor="rgba(24,119,242,0.12)",
        line=dict(color=FB_BLUE, width=2), marker=dict(color=FB_BLUE, size=6),
        hovertemplate="%{theta}: %{r:.0f}%<extra></extra>"
    ))
    fig.update_layout(
        polar=dict(bgcolor="#F0F2F5",
            radialaxis=dict(visible=True, range=[0,100], tickvals=[0,25,50,75,100],
                            tickfont=dict(size=9, color="#BCC0C4"), gridcolor="#E4E6EB"),
            angularaxis=dict(tickfont=dict(size=11, color="#050505"), gridcolor="#E4E6EB")),
        showlegend=False, height=260, margin=dict(t=20,b=20,l=50,r=50),
        paper_bgcolor=PLOT_BG, font={"family": "Inter"}
    )
    return fig

def waterfall_chart(rel, sem, pot, composite, key_suffix=""):
    r = rel*0.40*100; s = sem*0.35*100; p = pot*0.25*100
    color = score_color(composite)
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=["relative","relative","relative","total"],
        x=["Relevance<br>×40%","Semantic<br>×35%","Potential<br>×25%","Composite<br>Score"],
        y=[r, s, p, 0],
        text=[f"{r:.1f}",f"{s:.1f}",f"{p:.1f}",f"{composite*100:.1f}"],
        textposition="outside", textfont={"size": 11, "color": "#050505"},
        increasing={"marker": {"color": FB_BLUE}},
        totals={"marker": {"color": color}},
        connector={"line": {"color": "#E4E6EB", "width": 1}},
        hovertemplate="%{x}: %{y:.1f} pts<extra></extra>"
    ))
    fig.update_layout(height=280, margin=dict(t=30,b=10,l=10,r=10),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#050505")),
        yaxis=dict(range=[0,110], gridcolor="#F0F2F5",
                   tickfont=dict(size=10, color="#65676B"), title="Score Points"),
        showlegend=False, font={"family": "Inter"})
    return fig

def pool_bar_chart(results):
    if len(results) < 2: return None
    names  = [(r.get("full_name") or f"#{i+1}")[:20] for i,r in enumerate(results)]
    scores = [r.get("composite_score",0)*100 for r in results]
    colors = [score_color(s/100) for s in scores]
    fig = go.Figure(go.Bar(
        x=names, y=scores, marker_color=colors,
        text=[f"{s:.0f}%" for s in scores], textposition="outside",
        textfont=dict(size=10, color="#050505"),
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>", showlegend=False
    ))
    fig.add_hline(y=65, line_dash="dot", line_color=FB_GREEN,
                  annotation_text="Shortlist ≥65%",
                  annotation_font_size=10, annotation_font_color=FB_GREEN)
    fig.add_hline(y=45, line_dash="dot", line_color=FB_ORANGE,
                  annotation_text="Review ≥45%",
                  annotation_font_size=10, annotation_font_color=FB_ORANGE)
    fig.update_layout(height=300, margin=dict(t=30,b=10,l=10,r=10),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        xaxis=dict(tickfont=dict(size=10, color="#050505"), showgrid=False),
        yaxis=dict(range=[0,115], gridcolor="#F0F2F5",
                   tickfont=dict(size=10, color="#65676B"), title="Score (%)"),
        bargap=0.3, font={"family": "Inter"})
    return fig

def score_distribution_chart(results):
    """Histogram of composite scores across the pool."""
    scores = [r.get("composite_score",0)*100 for r in results]
    fig = go.Figure(go.Histogram(
        x=scores, nbinsx=20,
        marker_color=FB_BLUE, marker_opacity=0.75,
        hovertemplate="Score band %{x:.0f}%: %{y} candidates<extra></extra>"
    ))
    fig.add_vline(x=65, line_dash="dot", line_color=FB_GREEN,
                  annotation_text="65% threshold", annotation_font_size=10)
    fig.add_vline(x=45, line_dash="dot", line_color=FB_ORANGE,
                  annotation_text="45% threshold", annotation_font_size=10)
    fig.update_layout(height=250, margin=dict(t=30,b=20,l=30,r=10),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        xaxis=dict(title="AI Score (%)", gridcolor="#F0F2F5",
                   tickfont=dict(size=10, color="#65676B")),
        yaxis=dict(title="Candidates", gridcolor="#F0F2F5",
                   tickfont=dict(size=10, color="#65676B")),
        showlegend=False, font={"family": "Inter"})
    return fig

def experience_histogram(results):
    """Distribution of years of experience."""
    exps = []
    for r in results:
        parsed = get_parsed(r)
        v = r.get("years_of_experience") or parsed.get("total_years_exp")
        try: exps.append(float(str(v).split()[0]))
        except: pass
    if not exps: return None
    fig = go.Figure(go.Histogram(
        x=exps, nbinsx=12,
        marker_color=FB_PURPLE, marker_opacity=0.75,
        hovertemplate="%{x:.0f} yrs: %{y} candidates<extra></extra>"
    ))
    fig.update_layout(height=220, margin=dict(t=30,b=20,l=30,r=10),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        xaxis=dict(title="Years of Experience", gridcolor="#F0F2F5",
                   tickfont=dict(size=10)),
        yaxis=dict(title="Candidates", gridcolor="#F0F2F5",
                   tickfont=dict(size=10)),
        showlegend=False, font={"family": "Inter"})
    return fig

def dept_bar_chart(results):
    """Candidate count by inferred suitable department."""
    from collections import Counter

    def _dept(r):
        parsed = get_parsed(r)
        domain = parse_list(parsed.get("domain_expertise"))
        tech   = parse_list(r.get("technical_skills") or parsed.get("technical_skills"))
        text   = " ".join([str(x) for x in domain] + tech + [r.get("current_designation") or ""]).lower()
        if any(k in text for k in ["finance","accounting","treasury","audit"]): return "Finance"
        if any(k in text for k in ["data","analytics","bi","tableau","power bi","databricks","sql","python","ml","ai"]): return "Data & Analytics"
        if any(k in text for k in ["hr","human resource","talent","recruit"]): return "HR"
        if any(k in text for k in ["marketing","brand","digital","seo"]): return "Marketing"
        if any(k in text for k in ["sales","revenue","business development","crm"]): return "Sales"
        if any(k in text for k in ["engineering","software","developer","devops","cloud"]): return "Engineering"
        if any(k in text for k in ["operations","supply chain","logistics"]): return "Operations"
        if any(k in text for k in ["legal","compliance","regulatory","risk"]): return "Legal"
        if any(k in text for k in ["project","program","pmo","agile"]): return "PMO"
        return "General"

    counts = Counter(_dept(r) for r in results)
    labels = list(counts.keys()); values = list(counts.values())
    colors = [FB_BLUE, FB_GREEN, FB_ORANGE, FB_PURPLE, FB_RED,
              "#0F2D6B", "#17A589", "#E67E22", "#8E44AD", "#2ECC71"]
    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation="h",
        marker_color=colors[:len(labels)], marker_opacity=0.8,
        text=values, textposition="outside",
        hovertemplate="%{y}: %{x} candidates<extra></extra>", showlegend=False
    ))
    fig.update_layout(height=max(180, len(labels)*35+40), margin=dict(t=10,b=10,l=10,r=30),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        xaxis=dict(visible=True, gridcolor="#F0F2F5", tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=11)), bargap=0.3, font={"family": "Inter"})
    return fig

def fit_donut(results):
    from collections import Counter
    labels_map = {
        "auto_shortlisted": ("Auto Shortlisted", FB_GREEN),
        "hr_approved":      ("HR Approved",      "#17A589"),
        "needs_review":     ("Needs Review",      FB_ORANGE),
        "hr_hold":          ("HR Hold",           FB_GREY),
        "auto_rejected":    ("Auto Rejected",     FB_RED),
        "hr_rejected":      ("HR Rejected",       "#C62828"),
        "forwarded":        ("Forwarded",          FB_BLUE),
    }
    counts = Counter(r.get("decision","needs_review") for r in results)
    labels = []; values = []; colors = []
    for k, v in counts.items():
        lbl, col = labels_map.get(k, (k.replace("_"," ").title(), FB_GREY))
        labels.append(lbl); values.append(v); colors.append(col)
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color="white", width=2)),
        textinfo="label+percent", textfont=dict(size=10),
        hovertemplate="%{label}: %{value}<extra></extra>"
    ))
    fig.update_layout(height=260, margin=dict(t=20,b=20,l=20,r=20),
        paper_bgcolor=PLOT_BG, showlegend=False, font={"family": "Inter"},
        annotations=[dict(text=f"<b>{sum(values)}</b><br>Total",
                          x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#050505")])
    return fig

def skills_hbar(items, color=FB_BLUE):
    if not items: return None
    labels = [s[:48]+"…" if len(s)>48 else s for s in items[:10]]
    fig = go.Figure(go.Bar(
        x=list(range(len(labels),0,-1)), y=labels, orientation="h",
        marker_color=color, marker_opacity=0.78,
        hovertemplate="%{y}<extra></extra>", showlegend=False,
        text=labels, textposition="inside", insidetextanchor="start",
        textfont=dict(color="white", size=11)
    ))
    fig.update_layout(height=max(160, len(labels)*32+40), margin=dict(t=10,b=10,l=10,r=10),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        bargap=0.3, font={"family": "Inter"})
    return fig

def score_spider_pool(results, top_n=5):
    """Multi-candidate radar overlay — top N only."""
    top = sorted(results, key=lambda x: x.get("composite_score",0), reverse=True)[:top_n]
    cats = ["Relevance", "Semantic", "Potential"]; cats_c = cats + [cats[0]]
    colors = [FB_BLUE, FB_GREEN, FB_ORANGE, FB_PURPLE, FB_RED]
    fig = go.Figure()
    for i, r in enumerate(top):
        name = (r.get("full_name") or f"#{i+1}")[:18]
        vals = [r.get("relevance_score",0)*100, r.get("semantic_similarity",0)*100,
                r.get("potential_score",0)*100]
        fig.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats_c,
            fill="toself", fillcolor=f"rgba({int(colors[i][1:3],16)},{int(colors[i][3:5],16)},{int(colors[i][5:7],16)},0.08)",
            line=dict(color=colors[i], width=2), name=name,
            hovertemplate=f"{name} — %{{theta}}: %{{r:.0f}}%<extra></extra>"
        ))
    fig.update_layout(
        polar=dict(bgcolor="#F0F2F5",
            radialaxis=dict(visible=True, range=[0,100],
                            tickfont=dict(size=9, color="#BCC0C4"), gridcolor="#E4E6EB"),
            angularaxis=dict(tickfont=dict(size=12, color="#050505"), gridcolor="#E4E6EB")),
        showlegend=True, height=300, margin=dict(t=30,b=10,l=40,r=40),
        paper_bgcolor=PLOT_BG, font={"family": "Inter"},
        legend=dict(font=dict(size=10))
    )
    return fig


# ── Per-candidate Excel export ────────────────────────────────────────────────
def build_candidate_excel(r, role_name=""):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Candidate Profile"
    NAVY="0F2D6B"; BLUE="1877F2"; LIGHT="EBF3FF"
    BORDER_C="E2E6EA"; GRAY="8A9BB0"
    thin = Side(border_style="thin", color=BORDER_C)
    bdr  = Border(left=thin,right=thin,top=thin,bottom=thin)

    parsed  = get_parsed(r)
    edu     = parsed.get("education") or []
    exp_lst = parsed.get("experience") or []
    strengths  = parse_list(r.get("strengths") or [])
    gaps       = parse_list(r.get("gaps") or [])
    tech_skills= parse_list(r.get("technical_skills") or parsed.get("technical_skills") or [])
    transferable = parse_list(r.get("transferable_skills") or [])
    comp = r.get("composite_score",0); rel=r.get("relevance_score",0)
    sem  = r.get("semantic_similarity",0); pot=r.get("potential_score",0)
    fit_text, _ = fit_label(comp)
    name = r.get("full_name") or r.get("original_filename") or "Unknown"

    # Title
    ws.merge_cells("A1:D1")
    c = ws["A1"]; c.value = f"TalentScan — Candidate Profile: {name}"
    c.font = Font(name="Calibri",bold=True,size=14,color="FFFFFF")
    c.fill = PatternFill("solid",fgColor=NAVY)
    c.alignment = Alignment(horizontal="left",vertical="center",indent=1)
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:D2")
    c = ws["A2"]; c.value = f"Role: {role_name}   |   Screened: {(r.get('screened_at') or '')[:10]}   |   {fit_text}"
    c.font = Font(name="Calibri",size=10,color="FFFFFF"); c.fill = PatternFill("solid",fgColor=BLUE)
    c.alignment = Alignment(horizontal="left",vertical="center",indent=1)
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 6

    def hdr(row, text):
        ws.merge_cells(f"A{row}:D{row}")
        c = ws[f"A{row}"]; c.value = text
        c.font = Font(name="Calibri",bold=True,size=9,color=GRAY)
        c.fill = PatternFill("solid",fgColor="F7F8FC")
        c.alignment = Alignment(horizontal="left",vertical="center",indent=1)
        ws.row_dimensions[row].height = 18

    def row2(row, label, val):
        a = ws.cell(row=row,column=1,value=label)
        a.font = Font(name="Calibri",bold=True,size=10,color="050505"); a.border=bdr
        a.fill = PatternFill("solid",fgColor="F7F8FC")
        a.alignment = Alignment(vertical="top",indent=1)
        b = ws.cell(row=row,column=2,value=str(val) if val is not None else "")
        b.font = Font(name="Calibri",size=10); b.border=bdr
        b.alignment = Alignment(vertical="top",wrap_text=True)
        ws.merge_cells(f"B{row}:D{row}")
        ws.row_dimensions[row].height = 18

    ROW = 4
    hdr(ROW, "PERSONAL INFORMATION"); ROW+=1
    row2(ROW, "Full Name",  name);                                            ROW+=1
    row2(ROW, "Email",      r.get("email") or "");                            ROW+=1
    row2(ROW, "Phone",      r.get("phone") or parsed.get("phone") or "");     ROW+=1
    row2(ROW, "Location",   r.get("location") or "");                         ROW+=1
    row2(ROW, "Gender",     r.get("gender") or "");                           ROW+=1
    row2(ROW, "Nationality",r.get("nationality") or "");                      ROW+=1

    hdr(ROW, "EDUCATION"); ROW+=1
    if edu:
        for e in edu[:3]:
            row2(ROW, e.get("degree",""),
                 f"{e.get('field','')} | {e.get('institution','')} | {e.get('graduation_year','')}"); ROW+=1
    else:
        row2(ROW, "—", ""); ROW+=1

    hdr(ROW, "EXPERIENCE"); ROW+=1
    row2(ROW, "Total Years", r.get("years_of_experience") or parsed.get("total_years_exp") or ""); ROW+=1
    if exp_lst:
        for e in exp_lst[:4]:
            row2(ROW, e.get("role",""), f"{e.get('company','')} | {e.get('start_date','')} – {e.get('end_date','')}"); ROW+=1

    hdr(ROW, "AI SCORES"); ROW+=1
    for lbl, val in [("Composite Score", f"{int(comp*100)}%"),
                     ("Relevance Score", f"{int(rel*100)}%"),
                     ("Semantic Score",  f"{int(sem*100)}%"),
                     ("Potential Score", f"{int(pot*100)}%"),
                     ("Fit Status",      fit_text)]:
        row2(ROW, lbl, val); ROW+=1

    hdr(ROW, "STRENGTHS & GAPS"); ROW+=1
    row2(ROW, "Strengths", " | ".join(strengths[:8]) if strengths else ""); ROW+=1
    row2(ROW, "Gaps",      " | ".join(gaps[:8])      if gaps else "");      ROW+=1

    hdr(ROW, "TECHNICAL SKILLS"); ROW+=1
    row2(ROW, "Skills", ", ".join(tech_skills[:20]) if tech_skills else ""); ROW+=1

    hdr(ROW, "AI RATIONALE"); ROW+=1
    rat = r.get("llm_rationale") or ""
    ws.merge_cells(f"A{ROW}:D{ROW+3}")
    c = ws[f"A{ROW}"]; c.value = rat[:1500]; c.border=bdr
    c.font = Font(name="Calibri",size=10,italic=True); c.alignment=Alignment(wrap_text=True,vertical="top"); ROW+=4

    # Column widths
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 20

    buf = io.BytesIO(); wb.save(buf); buf.seek(0); return buf.getvalue()


# ── Per-candidate PDF using reportlab (fallback to HTML-based) ────────────────
def build_candidate_pdf(r, role_name=""):
    """Generates an HTML-based PDF summary. Falls back to plain HTML if reportlab absent."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_LEFT, TA_CENTER

        parsed  = get_parsed(r)
        edu     = parsed.get("education") or []
        exp_lst = parsed.get("experience") or []
        strengths  = parse_list(r.get("strengths") or [])
        gaps       = parse_list(r.get("gaps") or [])
        tech       = parse_list(r.get("technical_skills") or parsed.get("technical_skills") or [])
        comp = r.get("composite_score",0); rel=r.get("relevance_score",0)
        sem  = r.get("semantic_similarity",0); pot=r.get("potential_score",0)
        fit_text, _ = fit_label(comp)
        name = r.get("full_name") or r.get("original_filename") or "Unknown"

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                 rightMargin=2*cm, leftMargin=2*cm,
                                 topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        NAVY_COLOR = colors.HexColor("#0F2D6B")
        BLUE_COLOR = colors.HexColor("#1877F2")
        GREEN_COLOR= colors.HexColor("#42B72A")
        ORANGE_COLOR=colors.HexColor("#F5A623")
        RED_COLOR  = colors.HexColor("#FA3E3E")

        title_style = ParagraphStyle("TitleStyle", parent=styles["Title"],
            fontName="Helvetica-Bold", fontSize=18, textColor=colors.white,
            backColor=NAVY_COLOR, spaceAfter=2, leading=24)
        sub_style = ParagraphStyle("SubStyle", parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, textColor=colors.white,
            backColor=BLUE_COLOR, leading=16)
        section_style = ParagraphStyle("SectionStyle", parent=styles["Heading2"],
            fontName="Helvetica-Bold", fontSize=11, textColor=NAVY_COLOR,
            spaceAfter=4, spaceBefore=12, borderPadding=(4,4,4,4))
        body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, leading=15, textColor=colors.HexColor("#050505"))
        italic_style = ParagraphStyle("ItalicStyle", parent=styles["Normal"],
            fontName="Helvetica-Oblique", fontSize=9.5, leading=15,
            textColor=colors.HexColor("#444"))

        score_color_rl = GREEN_COLOR if comp>=0.65 else (ORANGE_COLOR if comp>=0.45 else RED_COLOR)

        story = []
        story.append(Paragraph(f"TalentScan AI — Candidate Profile", title_style))
        story.append(Paragraph(
            f"Role: {role_name}   |   Screened: {(r.get('screened_at') or '')[:10]}   |   Fit: {fit_text}",
            sub_style))
        story.append(Spacer(1, 0.4*cm))

        story.append(Paragraph("Personal Information", section_style))
        info_data = [
            ["Full Name", name],
            ["Email",     r.get("email") or "—"],
            ["Phone",     r.get("phone") or parsed.get("phone") or "—"],
            ["Location",  r.get("location") or "—"],
            ["Gender",    r.get("gender") or "—"],
            ["Nationality", r.get("nationality") or "—"],
        ]
        t = Table(info_data, colWidths=[5*cm, 11*cm])
        t.setStyle(TableStyle([
            ("FONTNAME",  (0,0),(-1,-1), "Helvetica"),
            ("FONTNAME",  (0,0),(0,-1),  "Helvetica-Bold"),
            ("FONTSIZE",  (0,0),(-1,-1), 9.5),
            ("BACKGROUND",(0,0),(0,-1),  colors.HexColor("#F7F8FC")),
            ("TEXTCOLOR", (0,0),(-1,-1), colors.HexColor("#050505")),
            ("GRID",      (0,0),(-1,-1), 0.5, colors.HexColor("#E2E6EA")),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white, colors.HexColor("#FAFBFC")]),
            ("TOPPADDING",(0,0),(-1,-1), 5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        story.append(t); story.append(Spacer(1, 0.3*cm))

        story.append(Paragraph("AI Score Summary", section_style))
        score_data = [
            ["Composite", f"{int(comp*100)}%", "Relevance", f"{int(rel*100)}%"],
            ["Semantic",  f"{int(sem*100)}%",  "Potential", f"{int(pot*100)}%"],
            ["Fit Status", fit_text, "Decision", (r.get("decision") or "").replace("_"," ").title()],
        ]
        t2 = Table(score_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        t2.setStyle(TableStyle([
            ("FONTNAME",  (0,0),(-1,-1), "Helvetica"),
            ("FONTNAME",  (0,0),(0,-1),  "Helvetica-Bold"),
            ("FONTNAME",  (2,0),(2,-1),  "Helvetica-Bold"),
            ("FONTSIZE",  (0,0),(-1,-1), 10),
            ("TEXTCOLOR", (1,0),(1,-1),  score_color_rl),
            ("TEXTCOLOR", (3,0),(3,-1),  score_color_rl),
            ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#EBF3FF")),
            ("GRID",      (0,0),(-1,-1), 0.5, colors.HexColor("#E2E6EA")),
            ("ALIGN",     (0,0),(-1,-1), "CENTER"),
            ("TOPPADDING",(0,0),(-1,-1), 7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ]))
        story.append(t2); story.append(Spacer(1, 0.3*cm))

        if edu:
            story.append(Paragraph("Education", section_style))
            for e in edu[:3]:
                story.append(Paragraph(
                    f"<b>{e.get('degree','')}</b> in {e.get('field','')} — "
                    f"{e.get('institution','')} ({e.get('graduation_year','')})", body_style))

        if exp_lst:
            story.append(Paragraph("Experience", section_style))
            for e in exp_lst[:4]:
                story.append(Paragraph(
                    f"<b>{e.get('role','')}</b> at {e.get('company','')} "
                    f"({e.get('start_date','')} – {e.get('end_date','')})", body_style))

        if strengths:
            story.append(Paragraph("Strengths", section_style))
            for s in strengths[:8]:
                story.append(Paragraph(f"• {s}", body_style))

        if gaps:
            story.append(Paragraph("Gaps", section_style))
            for g in gaps[:8]:
                story.append(Paragraph(f"• {g}", body_style))

        if tech:
            story.append(Paragraph("Technical Skills", section_style))
            story.append(Paragraph(", ".join(tech[:20]), body_style))

        rat = r.get("llm_rationale") or ""
        if rat:
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph("AI Rationale", section_style))
            story.append(Paragraph(rat[:1200], italic_style))

        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(
            f"Generated by TalentScan AI  ·  {datetime.now().strftime('%d %b %Y, %H:%M')}  ·  For HR use only",
            ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8,
                           textColor=colors.HexColor("#BCC0C4"), alignment=TA_CENTER)))

        doc.build(story)
        buf.seek(0)
        return buf.getvalue(), "pdf"

    except ImportError:
        # reportlab not installed — return an HTML file instead
        parsed  = get_parsed(r)
        edu     = parsed.get("education") or []
        exp_lst = parsed.get("experience") or []
        strengths = parse_list(r.get("strengths") or [])
        gaps      = parse_list(r.get("gaps") or [])
        tech      = parse_list(r.get("technical_skills") or parsed.get("technical_skills") or [])
        comp = r.get("composite_score",0); rel=r.get("relevance_score",0)
        sem  = r.get("semantic_similarity",0); pot=r.get("potential_score",0)
        fit_text, _ = fit_label(comp)
        name = r.get("full_name") or r.get("original_filename") or "Unknown"
        score_col = "#42B72A" if comp>=0.65 else ("#F5A623" if comp>=0.45 else "#FA3E3E")
        edu_html = "".join(f"<li><b>{e.get('degree','')}</b> in {e.get('field','')} — {e.get('institution','')} ({e.get('graduation_year','')})</li>" for e in edu[:3]) or "<li>—</li>"
        exp_html = "".join(f"<li><b>{e.get('role','')}</b> at {e.get('company','')} ({e.get('start_date','')} – {e.get('end_date','')})</li>" for e in exp_lst[:4]) or "<li>—</li>"
        str_html = "".join(f"<li>{s}</li>" for s in strengths[:8]) or "<li>—</li>"
        gap_html = "".join(f"<li>{g}</li>" for g in gaps[:8]) or "<li>—</li>"
        html_out = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{font-family:Arial,sans-serif;font-size:13px;color:#050505;max-width:900px;margin:0 auto;padding:20px;}}
.header{{background:#0F2D6B;color:white;padding:18px 22px;border-radius:8px 8px 0 0;}}
.subheader{{background:#1877F2;color:white;padding:8px 22px;border-radius:0 0 8px 8px;font-size:11px;margin-bottom:20px;}}
.section{{font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#8A9BB0;margin:18px 0 6px;}}
table.info{{width:100%;border-collapse:collapse;}}
table.info td{{padding:6px 10px;border:1px solid #E2E6EA;font-size:12px;}}
table.info td:first-child{{font-weight:700;background:#F7F8FC;width:140px;}}
.scores{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:10px 0;}}
.score-box{{background:#EBF3FF;border-radius:6px;padding:10px;text-align:center;}}
.score-val{{font-size:22px;font-weight:800;color:{score_col};}}
.score-lbl{{font-size:9px;text-transform:uppercase;color:#8A9BB0;margin-top:2px;}}
li{{margin:3px 0;}}
.footer{{margin-top:30px;font-size:10px;color:#BCC0C4;text-align:center;}}
</style></head><body>
<div class="header"><h2 style="margin:0;font-size:18px;">TalentScan AI — Candidate Profile</h2><p style="margin:4px 0 0;font-size:12px;">{name}</p></div>
<div class="subheader">Role: {role_name} &nbsp;|&nbsp; Screened: {(r.get('screened_at') or '')[:10]} &nbsp;|&nbsp; Fit: {fit_text}</div>
<div class="section">Personal Information</div>
<table class="info">
  <tr><td>Email</td><td>{r.get('email') or '—'}</td></tr>
  <tr><td>Phone</td><td>{r.get('phone') or parsed.get('phone') or '—'}</td></tr>
  <tr><td>Location</td><td>{r.get('location') or '—'}</td></tr>
  <tr><td>Gender</td><td>{r.get('gender') or '—'}</td></tr>
  <tr><td>Nationality</td><td>{r.get('nationality') or '—'}</td></tr>
</table>
<div class="section">AI Scores</div>
<div class="scores">
  <div class="score-box"><div class="score-val">{int(comp*100)}%</div><div class="score-lbl">Composite</div></div>
  <div class="score-box"><div class="score-val">{int(rel*100)}%</div><div class="score-lbl">Relevance</div></div>
  <div class="score-box"><div class="score-val">{int(sem*100)}%</div><div class="score-lbl">Semantic</div></div>
  <div class="score-box"><div class="score-val">{int(pot*100)}%</div><div class="score-lbl">Potential</div></div>
</div>
<div class="section">Education</div><ul>{edu_html}</ul>
<div class="section">Experience</div><ul>{exp_html}</ul>
<div class="section">Strengths</div><ul>{str_html}</ul>
<div class="section">Gaps</div><ul>{gap_html}</ul>
<div class="section">Technical Skills</div><p>{', '.join(tech[:20]) if tech else '—'}</p>
<div class="section">AI Rationale</div>
<p style="font-style:italic;background:#F0F2F5;padding:12px;border-radius:6px;">{r.get('llm_rationale') or '—'}</p>
<div class="footer">Generated by TalentScan AI &nbsp;·&nbsp; {datetime.now().strftime('%d %b %Y, %H:%M')} &nbsp;·&nbsp; For HR use only</div>
</body></html>"""
        return html_out.encode("utf-8"), "html"


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.2rem;">
      <div style="font-size:1.4rem;font-weight:900;color:#1877F2;letter-spacing:-0.5px;">TalentScan</div>
      <div style="font-size:0.68rem;color:#8A9BB0;margin-top:2px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">AI Screening Intelligence</div>
    </div>
    <div style="height:1px;background:#E4E6EB;margin-bottom:1rem;"></div>
    <div style="font-size:0.68rem;font-weight:700;color:#8A9BB0;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Navigation</div>
    """, unsafe_allow_html=True)
    st.page_link("app.py",                        label="🏠  Dashboard")
    st.page_link("pages/01_Post_a_Job.py",         label="📋  Post a Job")
    st.page_link("pages/02_Upload_CVs.py",         label="📤  Upload CVs")
    st.page_link("pages/03_High_Level_Review.py",  label="📊  High-Level Review")
    st.page_link("pages/04_Detailed_Insights.py",  label="🔬  Detailed Insights")
    st.page_link("pages/05_Candidate_History.py",  label="📁  Candidate History")
    st.markdown('<div style="height:1px;background:#E4E6EB;margin:1rem 0;"></div>', unsafe_allow_html=True)

    try:
        jobs_resp = requests.get(f"{API}/jobs/", timeout=5)
        jobs = jobs_resp.json() if jobs_resp.status_code == 200 else []
        job_options = {j["title"]: j["id"] for j in jobs}
    except Exception:
        job_options = {}
    if not job_options:
        st.warning("No active roles found."); st.stop()

    st.markdown('<div class="sec-label">Active Role</div>', unsafe_allow_html=True)
    selected_label  = st.selectbox("Role", list(job_options.keys()), label_visibility="collapsed")
    selected_job_id = job_options[selected_label]

    st.markdown('<div style="height:1px;background:#E4E6EB;margin:1rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Decision Filter</div>', unsafe_allow_html=True)
    filter_decision = st.multiselect("Decision",
        ["auto_shortlisted","auto_rejected","needs_review",
         "hr_approved","hr_hold","hr_rejected","forwarded"],
        default=["auto_shortlisted","needs_review","hr_approved","hr_hold"],
        label_visibility="collapsed")

    st.markdown('<div style="height:1px;background:#E4E6EB;margin:1rem 0;"></div>', unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("↻ Refresh", use_container_width=True): st.rerun()
    with col_r2:
        auto = st.checkbox("Auto 30s")
    if auto:
        time.sleep(30); st.rerun()

    st.markdown("""
    <div style="margin-top:1.5rem;background:#F0F2F5;border-radius:8px;padding:10px 12px;">
      <div class="sec-label">Scoring Weights</div>
      <div style="font-size:0.78rem;color:#050505;line-height:2.0;">
        Relevance &nbsp;·&nbsp; 40%<br>
        Semantic &nbsp;·&nbsp; 35%<br>
        Potential &nbsp;·&nbsp; 25%
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Fetch ─────────────────────────────────────────────────────────────────────
try:
    resp = requests.get(f"{API}/screenings/results/{selected_job_id}",
                        params={"min_score": 0, "limit": 500}, timeout=15)
    if resp.status_code != 200:
        st.error(f"API error {resp.status_code}"); st.stop()
    all_results = resp.json()
    if not isinstance(all_results, list): all_results = []
except Exception as e:
    st.error(f"Cannot reach API: {e}"); st.stop()

results_by_decision = [r for r in all_results if isinstance(r, dict)
                       and (not filter_decision or r.get("decision") in filter_decision)]


# ── Topnav ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="ts-nav">
  <div style="display:flex;align-items:center;">
    <div class="ts-nav-logo">TalentScan</div>
    <span class="ts-nav-badge">Analyst View</span>
  </div>
  <div class="ts-nav-title">Detailed Insights Dashboard</div>
  <div class="ts-nav-role">{selected_label}</div>
</div>
""", unsafe_allow_html=True)


# ── Pool metrics ───────────────────────────────────────────────────────────────
try:
    pipe   = requests.get(f"{API}/jobs/{selected_job_id}/pipeline", timeout=5).json()
    total_ = pipe.get("total_screened", 0)
    pend_  = pipe.get("pending_review", 0)
    short_ = pipe.get("shortlisted", 0)
    avg_   = pipe.get("avg_score") or 0
except Exception:
    total_ = len(all_results)
    pend_  = sum(1 for r in all_results if r.get("decision") == "needs_review")
    short_ = sum(1 for r in all_results if "shortlisted" in (r.get("decision") or ""))
    avg_   = (sum(r.get("composite_score",0) for r in all_results)/len(all_results)) if all_results else 0

strong_cnt = sum(1 for r in all_results if r.get("composite_score",0) >= 0.65)

c1,c2,c3,c4,c5 = st.columns(5)
for col, val, lbl, sub, acc in [
    (c1, total_,      "Total Screened", "All candidates",      "#1877F2"),
    (c2, pend_,       "Pending Review", "Awaiting HR",         "#F5A623"),
    (c3, short_,      "Shortlisted",    "Auto + HR approved",  "#42B72A"),
    (c4, strong_cnt,  "Strong Fit",     "Score ≥ 65%",         "#6B2FA0"),
    (c5, f"{avg_:.0%}" if avg_ else "—", "Avg Score", "Pool average", "#0F2D6B"),
]:
    with col:
        st.markdown(f"""<div class="metric-card" style="--accent:{acc};">
          <div class="metric-val">{val}</div>
          <div class="metric-lbl">{lbl}</div>
          <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)


# ── No-JD mode banner ────────────────────────────────────────────────────────
_no_jd_results = [r for r in all_results
                  if (r.get("score_breakdown") or {}).get("no_jd_mode") or
                  (r.get("ai_summary") or "").startswith("[NO JD]")]
if _no_jd_results:
    best_clusters = {}
    for r in _no_jd_results:
        sb = r.get("score_breakdown") or {}
        bc = sb.get("best_cluster","")
        if bc: best_clusters[bc] = best_clusters.get(bc, 0) + 1
    top_clusters_str = ", ".join(f"{k} ({v})" for k,v in sorted(best_clusters.items(), key=lambda x:-x[1])[:4])
    _nojd_msg = (
        f'<div style="background:#FFF8E6;border:1px solid #FFD975;border-radius:8px;padding:14px 18px;'
        f'margin-bottom:1.2rem;font-size:0.82rem;color:#7A5700;">'
        f'<strong>⚠️ No-JD Generic Screening — {len(_no_jd_results)} candidate(s)</strong><br>'
        f"These CVs were screened without a Job Description using the organisation's department taxonomy. "
        f'Scores are capped at 72% and represent general department fit, not role-specific suitability. '
        f'Top department clusters: <strong>{top_clusters_str or "see individual cards"}</strong>.'
        f'<br><em>Add a JD to this role for full role-specific screening.</em></div>'
    )
    st.markdown(_nojd_msg, unsafe_allow_html=True)

# ── Pool analytics section ─────────────────────────────────────────────────────
if len(all_results) >= 2:
    st.markdown('<div class="fb-card-lg">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">📊  Pool Analytics</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Score Distribution", "Fit Breakdown + Rankings", "Experience & Dept", "Multi-Candidate Radar"])

    with tab1:
        col_dist1, col_dist2 = st.columns(2, gap="medium")
        with col_dist1:
            st.markdown('<div class="sec-label">AI Score Distribution</div>', unsafe_allow_html=True)
            fig = score_distribution_chart(all_results)
            st.plotly_chart(fig, use_container_width=True, key="score_dist", config={"displayModeBar": False})
        with col_dist2:
            st.markdown('<div class="sec-label">Candidate Rankings (AI Score)</div>', unsafe_allow_html=True)
            fig = pool_bar_chart(all_results[:20])  # cap at 20 for readability
            if fig:
                st.plotly_chart(fig, use_container_width=True, key="pool_bar", config={"displayModeBar": False})

    with tab2:
        col_pie1, col_pie2 = st.columns(2, gap="medium")
        with col_pie1:
            st.markdown('<div class="sec-label">Decision Breakdown</div>', unsafe_allow_html=True)
            fig = fit_donut(all_results)
            st.plotly_chart(fig, use_container_width=True, key="fit_donut", config={"displayModeBar": False})
        with col_pie2:
            st.markdown('<div class="sec-label">Score Tier Summary</div>', unsafe_allow_html=True)
            strong = sum(1 for r in all_results if r.get("composite_score",0)>=0.65)
            mod    = sum(1 for r in all_results if 0.45<=r.get("composite_score",0)<0.65)
            weak   = sum(1 for r in all_results if r.get("composite_score",0)<0.45)
            fig2 = go.Figure(go.Pie(
                labels=["Strong Fit (≥65%)", "Moderate Fit (45–65%)", "Weak Fit (<45%)"],
                values=[strong, mod, weak], hole=0.5,
                marker=dict(colors=[FB_GREEN, FB_ORANGE, FB_RED], line=dict(color="white", width=2)),
                textinfo="label+percent+value", textfont=dict(size=11),
                hovertemplate="%{label}: %{value}<extra></extra>"
            ))
            fig2.update_layout(height=260, margin=dict(t=20,b=20,l=20,r=20),
                paper_bgcolor=PLOT_BG, showlegend=False, font={"family": "Inter"})
            st.plotly_chart(fig2, use_container_width=True, key="tier_pie", config={"displayModeBar": False})

    with tab3:
        col_e1, col_e2 = st.columns(2, gap="medium")
        with col_e1:
            st.markdown('<div class="sec-label">Experience Distribution</div>', unsafe_allow_html=True)
            fig = experience_histogram(all_results)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key="exp_hist", config={"displayModeBar": False})
            else:
                st.caption("No experience data available.")
        with col_e2:
            st.markdown('<div class="sec-label">Inferred Department Fit</div>', unsafe_allow_html=True)
            fig = dept_bar_chart(all_results)
            st.plotly_chart(fig, use_container_width=True, key="dept_bar", config={"displayModeBar": False})

    with tab4:
        st.markdown('<div class="sec-label">Top-5 Candidate Score Profile (Radar Overlay)</div>', unsafe_allow_html=True)
        fig = score_spider_pool(all_results, top_n=min(5, len(all_results)))
        st.plotly_chart(fig, use_container_width=True, key="pool_radar", config={"displayModeBar": False})
        st.caption("Shows Relevance, Semantic, and Potential sub-scores for the top-5 candidates by composite score.")

    st.markdown('</div>', unsafe_allow_html=True)


# ── Smart Filter Panel ─────────────────────────────────────────────────────────
st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
st.markdown('<div class="filter-title">🔍  Smart Filters</div>', unsafe_allow_html=True)

def unique_vals(field):
    vals = set()
    for r in all_results:
        v = r.get(field)
        if v and str(v).strip() not in ("—","","None"): vals.add(str(v).strip())
    return sorted(vals)

fcol1, fcol2, fcol3 = st.columns([3, 2, 2])
with fcol1: name_search = st.text_input("Candidate Name", placeholder="Type to filter by name…")
with fcol2: score_min, score_max = st.slider("Score Range (%)", 0, 100, (0, 100), step=5)
with fcol3: top5_only = st.toggle("🏆 Top 5 Only", value=False)

fcol4, fcol5, fcol6, fcol7 = st.columns(4)
loc_opts = ["All"] + list(dict.fromkeys(unique_vals("location") + unique_vals("city")))
nat_opts = ["All"] + unique_vals("nationality")
gen_opts = ["All"] + unique_vals("gender")
with fcol4: sel_location    = st.selectbox("Location",    loc_opts)
with fcol5: sel_nationality = st.selectbox("Nationality", nat_opts)
with fcol6: sel_gender      = st.selectbox("Gender",      gen_opts)
with fcol7: exp_range = st.slider("Years Exp", 0, 30, (0, 30), step=1)

fcol8, fcol9, fcol10, fcol11 = st.columns(4)
emp_opts = ["All"] + list(dict.fromkeys(unique_vals("current_employer") + unique_vals("current_company")))
des_opts = ["All"] + list(dict.fromkeys(unique_vals("current_designation") + unique_vals("current_role") + unique_vals("job_title")))
with fcol8:  sel_company     = st.selectbox("Company",     emp_opts)
with fcol9:  sel_designation = st.selectbox("Designation", des_opts)
with fcol10: sel_fit = st.selectbox("Fit Category", ["All","Strong Fit","Moderate Fit","Weak Fit"])
with fcol11: sort_by = st.selectbox("Sort By", ["Highest Score","Lowest Score","Most Experience","Recently Added"])

st.markdown('</div>', unsafe_allow_html=True)


# ── Apply filters ──────────────────────────────────────────────────────────────
def get_exp_years(r):
    v = r.get("years_of_experience") or get_parsed(r).get("total_years_exp")
    return safe_float(v)

def matches_fit(r, sel):
    if sel == "All": return True
    s = r.get("composite_score",0)
    if sel == "Strong Fit":   return s >= 0.65
    if sel == "Moderate Fit": return 0.45 <= s < 0.65
    if sel == "Weak Fit":     return s < 0.45
    return True

filtered = []
for r in results_by_decision:
    comp      = r.get("composite_score",0)
    score_pct = int(comp*100)
    name_v    = (r.get("full_name") or r.get("original_filename") or "").lower()
    loc_v     = str(r.get("location") or r.get("city") or "").lower()
    nat_v     = str(r.get("nationality") or "").lower()
    gen_v     = str(r.get("gender") or "").lower()
    emp_v     = str(r.get("current_employer") or r.get("current_company") or "").lower()
    des_v     = str(r.get("current_designation") or r.get("current_role") or r.get("job_title") or "").lower()
    exp_v     = get_exp_years(r)
    if name_search and name_search.lower() not in name_v:                         continue
    if not (score_min <= score_pct <= score_max):                                 continue
    if sel_location    != "All" and sel_location.lower()    not in loc_v:         continue
    if sel_nationality != "All" and sel_nationality.lower() not in nat_v:         continue
    if sel_gender      != "All" and sel_gender.lower()      not in gen_v:         continue
    if sel_company     != "All" and sel_company.lower()     not in emp_v:         continue
    if sel_designation != "All" and sel_designation.lower() not in des_v:         continue
    if not (exp_range[0] <= exp_v <= exp_range[1]):                               continue
    if not matches_fit(r, sel_fit):                                               continue
    filtered.append(r)

if sort_by == "Highest Score":    filtered.sort(key=lambda x: x.get("composite_score",0), reverse=True)
elif sort_by == "Lowest Score":   filtered.sort(key=lambda x: x.get("composite_score",0))
elif sort_by == "Most Experience":filtered.sort(key=lambda x: get_exp_years(x), reverse=True)
elif sort_by == "Recently Added": filtered.sort(key=lambda x: x.get("screened_at") or "", reverse=True)

results = filtered[:5] if top5_only else filtered

active_filters = sum([
    1 if name_search else 0, 1 if (score_min,score_max)!=(0,100) else 0,
    1 if sel_location!="All" else 0, 1 if sel_nationality!="All" else 0,
    1 if sel_gender!="All" else 0, 1 if (exp_range[0],exp_range[1])!=(0,30) else 0,
    1 if sel_company!="All" else 0, 1 if sel_designation!="All" else 0,
    1 if sel_fit!="All" else 0, 1 if top5_only else 0,
])

st.markdown(f"""<div class="result-meta">
  <span>Showing <strong>{len(results)}</strong> candidate{"s" if len(results)!=1 else ""}
    {f"(filtered from {len(results_by_decision)})" if active_filters else ""}
    &nbsp;·&nbsp; Sorted by <strong>{sort_by}</strong>
  </span>
  <span style="font-size:0.75rem;color:#8A9BB0;">
    {"🔵 "+str(active_filters)+" filter(s)" if active_filters else "No filters applied"}
  </span>
</div>""", unsafe_allow_html=True)

if not results:
    st.markdown("""
    <div style="text-align:center;padding:3rem;background:#FFFFFF;border-radius:10px;border:1px solid #CED0D4;">
      <div style="font-size:2rem;">🔍</div>
      <div style="font-weight:700;font-size:1rem;margin:8px 0 4px;">No candidates match the current filters</div>
      <div style="font-size:0.82rem;color:#65676B;">Adjust filters above to broaden the search.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

st.markdown('<div style="height:1px;background:#CED0D4;margin:0.5rem 0 1.5rem;"></div>', unsafe_allow_html=True)


# ── Render candidate cards ─────────────────────────────────────────────────────
for rank, r in enumerate(results, 1):
    name      = r.get("full_name") or r.get("original_filename") or "Unknown"
    email     = r.get("email") or ""
    fname     = r.get("original_filename") or ""
    decision  = r.get("decision") or "needs_review"
    ts        = (r.get("screened_at") or "")[:16].replace("T", " ")
    comp      = r.get("composite_score", 0)
    sem       = r.get("semantic_similarity", 0)
    rel       = r.get("relevance_score", 0)
    pot       = r.get("potential_score", 0)
    anoms     = r.get("anomaly_count", 0) or 0
    returning = r.get("is_returning", False)
    sid       = r.get("screening_id", "") or str(rank)
    rationale = r.get("llm_rationale") or ""
    conf      = r.get("parse_confidence") or 0.8

    strengths    = parse_list(r.get("strengths"))
    gaps         = parse_list(r.get("gaps"))
    transferable = parse_list(r.get("transferable_skills"))
    insights     = parse_list(r.get("value_add_insights"))
    parsed       = get_parsed(r)
    tech_skills  = parse_list(r.get("technical_skills") or parsed.get("technical_skills"))
    soft_skills  = parse_list(r.get("soft_skills") or parsed.get("soft_skills"))

    ini          = initials(name)
    comp_color   = score_color(comp)
    fit_text, fit_cls = fit_label(comp)
    key_id       = f"{sid}_{rank}"

    ret_badge   = '<span class="badge badge-orange">↩ Returning</span>' if returning else ""
    anom_badge  = f'<span class="badge badge-red">⚑ {anoms} Flag{"s" if anoms!=1 else ""}</span>' if anoms else ""
    fit_badge   = f'<span class="fit-{fit_cls}">{fit_text}</span>'

    st.markdown(f"""
    <div class="fb-card-lg">
      <div class="cand-header">
        <div class="cand-avatar">{ini}</div>
        <div style="flex:1;min-width:0;">
          <div class="cand-name">#{rank} &nbsp;{name}</div>
          <div class="cand-email">{email}</div>
          <div style="font-size:0.75rem;color:#BCC0C4;">{fname}</div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;flex-shrink:0;">
          {badge_html(decision)}
          {fit_badge}
          {ret_badge}
          {anom_badge}
          <div style="font-size:0.72rem;color:#BCC0C4;">{ts}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Per-candidate downloads ──────────────────────────────────────────────
    _safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name)[:30]
    _ts_now    = datetime.now().strftime("%Y%m%d_%H%M")

    dl_col1, dl_col2, dl_col3 = st.columns([2, 2, 6])
    with dl_col1:
        excel_bytes = build_candidate_excel(r, role_name=selected_label)
        st.download_button(
            label="⬇️ Excel Profile",
            data=excel_bytes,
            file_name=f"Profile_{_safe_name}_{_ts_now}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"xl_{key_id}",
            use_container_width=True,
        )
    with dl_col2:
        pdf_bytes, ext = build_candidate_pdf(r, role_name=selected_label)
        mime_type = "application/pdf" if ext == "pdf" else "text/html"
        file_ext  = ext
        st.download_button(
            label=f"⬇️ {'PDF' if ext=='pdf' else 'HTML'} Report",
            data=pdf_bytes,
            file_name=f"Profile_{_safe_name}_{_ts_now}.{file_ext}",
            mime=mime_type,
            key=f"pdf_{key_id}",
            use_container_width=True,
        )
    with dl_col3:
        st.markdown(
            f'<div style="font-size:0.7rem;color:#8A9BB0;padding-top:10px;">'
            f'Individual profile downloads for <strong style="color:#050505;">{name}</strong>'
            f'{"  ·  PDF requires reportlab (pip install reportlab)" if ext=="html" else ""}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Score Intelligence ───────────────────────────────────────────────────
    with st.expander(f"📊  Score Intelligence — {name}", expanded=(rank == 1)):
        gc1, gc2, gc3 = st.columns(3, gap="medium")
        with gc1:
            st.markdown('<div class="sec-label">Composite Gauge</div>', unsafe_allow_html=True)
            st.plotly_chart(gauge_chart(comp), use_container_width=True,
                            key=f"gauge_{key_id}", config={"displayModeBar": False})
        with gc2:
            st.markdown('<div class="sec-label">Score Profile Radar</div>', unsafe_allow_html=True)
            st.plotly_chart(radar_chart(rel, sem, pot), use_container_width=True,
                            key=f"radar_{key_id}", config={"displayModeBar": False})
        with gc3:
            st.markdown('<div class="sec-label">Score Contribution</div>', unsafe_allow_html=True)
            st.plotly_chart(waterfall_chart(rel, sem, pot, comp), use_container_width=True,
                            key=f"wfall_{key_id}", config={"displayModeBar": False})

        st.markdown(f"""
        <div class="fb-card">
          <div class="sec-label">Score Breakdown with Weights</div>
          {subscore_html("Relevance Score", rel, "· 40% — LLM JD–CV alignment")}
          {subscore_html("Semantic Similarity", sem, "· 35% — vector embedding cosine")}
          {subscore_html("Potential Score", pot, "· 25% — career trajectory signals")}
          <div style="margin-top:10px;font-size:0.72rem;color:#BCC0C4;background:#F0F2F5;border-radius:6px;padding:8px 10px;font-family:monospace;">
            ({int(rel*100)} × 0.40) + ({int(sem*100)} × 0.35) + ({int(pot*100)} × 0.25)
            &nbsp;=&nbsp; <b style="color:#1877F2;font-size:0.9rem;">{int(comp*100)}</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Strength & Gap Analysis ──────────────────────────────────────────────
    with st.expander(f"✅  Strength & Gap Analysis — {name}"):
        s_rows = "".join(f'<div class="sg-item"><span style="color:#42B72A;font-size:0.6rem;margin-top:3px;">▲</span><span class="sg-text-s">{s}</span></div>' for s in strengths) \
                 or "<div style='font-size:0.8rem;color:#BCC0C4;padding:4px 0;'>None identified</div>"
        g_rows = "".join(f'<div class="sg-item"><span style="color:#F5A623;font-size:0.6rem;margin-top:3px;">▼</span><span class="sg-text-g">{g}</span></div>' for g in gaps) \
                 or "<div style='font-size:0.8rem;color:#BCC0C4;padding:4px 0;'>None identified</div>"
        st.markdown(f"""
        <div class="sg-grid">
          <div class="sg-box sg-box-s"><div class="sg-box-label sg-label-s">✓ Strengths ({len(strengths)})</div>{s_rows}</div>
          <div class="sg-box sg-box-g"><div class="sg-box-label sg-label-g">⚠ Gaps ({len(gaps)})</div>{g_rows}</div>
        </div>
        """, unsafe_allow_html=True)
        if strengths:
            st.markdown("<div style='margin-top:14px;'><div class='sec-label'>Strength Signal Depth</div></div>", unsafe_allow_html=True)
            fig = skills_hbar(strengths, FB_BLUE)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key=f"str_bar_{key_id}", config={"displayModeBar": False})
        if gaps:
            st.markdown("<div style='margin-top:8px;'><div class='sec-label'>Gap Signal Depth</div></div>", unsafe_allow_html=True)
            fig = skills_hbar(gaps, FB_RED)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key=f"gap_bar_{key_id}", config={"displayModeBar": False})

    # ── Skills Breakdown ─────────────────────────────────────────────────────
    if tech_skills or soft_skills:
        with st.expander(f"🛠  Skills Breakdown — {name}"):
            sk1, sk2 = st.columns(2, gap="medium")
            with sk1:
                st.markdown('<div class="sec-label">Technical Skills</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip chip-tech">{s}</span>' for s in tech_skills[:20]) \
                        or "<span style='font-size:0.8rem;color:#BCC0C4;'>None extracted</span>"
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
                if len(tech_skills) > 3:
                    fig = skills_hbar(tech_skills[:10], FB_BLUE)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, key=f"tech_bar_{key_id}", config={"displayModeBar": False})
            with sk2:
                st.markdown('<div class="sec-label">Soft Skills</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip chip-domain">{s}</span>' for s in soft_skills[:15]) \
                        or "<span style='font-size:0.8rem;color:#BCC0C4;'>None extracted</span>"
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)

    # ── Transferable Skills ──────────────────────────────────────────────────
    if transferable:
        with st.expander(f"🔄  Transferable Skills — {name}"):
            tech_t   = [s for s in transferable if any(kw in s.lower() for kw in TECH_KW)]
            domain_t = [s for s in transferable if s not in tech_t]
            tc1, tc2 = st.columns(2, gap="medium")
            with tc1:
                st.markdown('<div class="sec-label">Technical</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip chip-tech">{s}</span>' for s in tech_t) \
                        or "<span style='font-size:0.8rem;color:#BCC0C4;'>None</span>"
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
            with tc2:
                st.markdown('<div class="sec-label">Domain</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="chip chip-domain">{s}</span>' for s in domain_t) \
                        or "<span style='font-size:0.8rem;color:#BCC0C4;'>None</span>"
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)

    # ── Strategic Insights ───────────────────────────────────────────────────
    if insights:
        with st.expander(f"💡  Strategic Insights — {name}"):
            for idx, insight in enumerate(insights, 1):
                st.markdown(f"""
                <div class="insight-item">
                  <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#1877F2;margin-bottom:3px;">Insight {idx:02d}</div>
                  {insight}
                </div>""", unsafe_allow_html=True)

    # ── AI Rationale ──────────────────────────────────────────────────────────
    if rationale:
        with st.expander(f"🧠  AI Rationale — {name}"):
            st.markdown(f"""
            <div class="rationale-box">
              <div class="rationale-label">🔵 AI Decision Rationale</div>
              {rationale}
              <div style="margin-top:10px;font-size:0.7rem;color:#BCC0C4;font-style:normal;">
                Generated by LLM pipeline · Not human-authored · For HR augmentation only
              </div>
            </div>""", unsafe_allow_html=True)

    # ── No-JD Dept Fit (only when no_jd_mode=True) ─────────────────────────────
    _sb = r.get("score_breakdown") or {}
    _is_no_jd = bool(_sb.get("no_jd_mode")) or (r.get("ai_summary") or "").startswith("[NO JD]")
    if _is_no_jd:
        _suggested = _sb.get("suggested_departments") or []
        _best_cluster = _sb.get("best_cluster") or ""
        _top_clusters = _sb.get("top_clusters") or []
        _seniority = _sb.get("seniority_band") or ""
        with st.expander(f"🏢  Department Fit Analysis — {name} (No-JD Mode)", expanded=True):
            st.markdown(f"""
            <div style="background:#FFF8E6;border:1px solid #FFD975;border-radius:8px;padding:12px 16px;
                margin-bottom:1rem;font-size:0.8rem;color:#7A5700;">
              ⚠️ <strong>No-JD Mode:</strong> This assessment is based on department taxonomy matching only
              (no Job Description was available). Score is capped at 72%. Results are indicative.
              Seniority: <strong>{_seniority}</strong>
            </div>""", unsafe_allow_html=True)

            if _best_cluster:
                st.markdown(f'<div class="sec-label">Best-Fit Cluster</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.1rem;font-weight:800;color:#1877F2;">{_best_cluster}</div>', unsafe_allow_html=True)

            if _top_clusters:
                st.markdown('<div class="sec-label" style="margin-top:12px;">All Cluster Scores</div>', unsafe_allow_html=True)
                import plotly.graph_objects as _go
                _clust_names = [c["cluster"][:35] for c in _top_clusters]
                _clust_scores = [c["score"]*100 for c in _top_clusters]
                _colors = [FB_BLUE if i==0 else FB_GREY for i in range(len(_clust_names))]
                _fig = _go.Figure(_go.Bar(x=_clust_scores, y=_clust_names, orientation="h",
                    marker_color=_colors, text=[f"{s:.0f}%" for s in _clust_scores],
                    textposition="outside", showlegend=False))
                _fig.update_layout(height=max(180, len(_clust_names)*36+40),
                    margin=dict(t=10,b=10,l=10,r=40),
                    paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
                    xaxis=dict(range=[0,100], ticksuffix="%", gridcolor="#F0F2F5"),
                    yaxis=dict(tickfont=dict(size=11)), font={"family":"Inter"})
                st.plotly_chart(_fig, use_container_width=True, key=f"nojd_bar_{key_id}", config={"displayModeBar":False})

            if _suggested:
                st.markdown('<div class="sec-label" style="margin-top:12px;">Suggested Departments</div>', unsafe_allow_html=True)
                for item in _suggested[:8]:
                    _score_c = "#42B72A" if item["score"]>=0.6 else ("#F5A623" if item["score"]>=0.35 else "#BCC0C4")
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:7px 12px;background:#F7F8FC;border-radius:6px;margin-bottom:4px;
                        border-left:3px solid {_score_c};">
                      <span style="font-size:0.82rem;font-weight:600;">{item["department"]}</span>
                      <span style="font-size:0.75rem;color:{_score_c};font-weight:700;">{int(item["score"]*100)}% fit</span>
                    </div>""", unsafe_allow_html=True)

    # ── System Signals ────────────────────────────────────────────────────────
    with st.expander(f"📡  System Signals — {name}"):
        conf_pct = int((conf or 0.8) * 100)
        st.markdown(f"""
        <div class="signal-strip">
          <div class="signal-cell">
            <div class="signal-val" style="color:{comp_color};">{int(comp*100)}%</div>
            <div class="signal-lbl">Composite</div><div class="signal-sub">Weighted score</div>
          </div>
          <div class="signal-cell">
            <div class="signal-val" style="color:{'#FA3E3E' if anoms else '#42B72A'};">{anoms}</div>
            <div class="signal-lbl">Anomaly Flags</div>
            <div class="signal-sub">{'Review required' if anoms else 'Clean'}</div>
          </div>
          <div class="signal-cell">
            <div class="signal-val" style="color:{'#1877F2' if returning else '#BCC0C4'};">{'Yes' if returning else 'No'}</div>
            <div class="signal-lbl">Returning</div>
            <div class="signal-sub">{'Prior application' if returning else 'First application'}</div>
          </div>
          <div class="signal-cell">
            <div class="signal-val" style="color:#1877F2;">{conf_pct}%</div>
            <div class="signal-lbl">Parse Confidence</div><div class="signal-sub">CV extraction quality</div>
          </div>
        </div>
        <div class="conf-row">
          <div class="conf-label">Parse Confidence</div>
          <div class="conf-track"><div class="conf-fill" style="width:{conf_pct}%;"></div></div>
          <div class="conf-pct">{conf_pct}%</div>
        </div>""", unsafe_allow_html=True)

    # ── HR Decision ───────────────────────────────────────────────────────────
    with st.expander(f"✍️  HR Decision — {name}"):
        decision_map = {"✅ Approve":"hr_approved","📤 Forward":"forwarded",
                        "⏸ Hold":"hr_hold","❌ Reject":"hr_rejected"}
        da, db, dc = st.columns([2,2,1], gap="medium")
        with da:
            choice = st.selectbox("Decision", list(decision_map.keys()), key=f"dec_{key_id}")
        with db:
            hr_name = st.text_input("HR Officer Name", placeholder="Your full name", key=f"hrn_{key_id}")
        with dc:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Save", key=f"save_{key_id}", use_container_width=True):
                if not hr_name.strip():
                    st.error("Name required.")
                else:
                    try:
                        patch = requests.patch(
                            f"{API}/screenings/{sid}/decision",
                            data={"decision": decision_map[choice], "decision_by": hr_name.strip()},
                            timeout=10,
                        )
                        if patch.status_code == 200:
                            st.success("✅ Decision saved.")
                            time.sleep(1); st.rerun()
                        else:
                            err = patch.json() if patch.headers.get("content-type","").startswith("application/json") else {}
                            st.error(err.get("detail", f"Error {patch.status_code}"))
                    except Exception as ex:
                        st.error(str(ex))

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)


def build_all_candidates_report(results, role_name=""):
    """
    Generates ONE combined HTML report for ALL candidates
    (can be converted to PDF via reportlab or returned as HTML)
    """

    from datetime import datetime

    def safe(v):
        return v if v not in (None, "", []) else "—"

    cards_html = ""

    for i, r in enumerate(results, 1):
        name = r.get("full_name") or r.get("original_filename") or "Unknown"
        comp = int((r.get("composite_score", 0)) * 100)
        rel = int((r.get("relevance_score", 0)) * 100)
        sem = int((r.get("semantic_similarity", 0)) * 100)
        pot = int((r.get("potential_score", 0)) * 100)

        strengths = ", ".join(r.get("strengths") or [])
        gaps = ", ".join(r.get("gaps") or [])
        skills = ", ".join((r.get("technical_skills") or [])[:15])

        cards_html += f"""
        <div style="border:1px solid #ddd;border-radius:10px;padding:15px;margin-bottom:15px;">
            <h3 style="margin:0;">#{i} {name}</h3>
            <p><b>Composite:</b> {comp}% | <b>Rel:</b> {rel}% | <b>Sem:</b> {sem}% | <b>Pot:</b> {pot}%</p>
            
            <p><b>Strengths:</b> {safe(strengths)}</p>
            <p><b>Gaps:</b> {safe(gaps)}</p>
            <p><b>Skills:</b> {safe(skills)}</p>
        </div>
        """

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding:20px; }}
            h1 {{ color:#1877F2; }}
        </style>
    </head>
    <body>
        <h1>TalentScan AI - Full Screening Report</h1>
        <p><b>Role:</b> {role_name}</p>
        <p><b>Generated:</b> {datetime.now().strftime('%d %b %Y %H:%M')}</p>
        <hr>
        {cards_html}
    </body>
    </html>
    """

    return html.encode("utf-8")
    st.markdown('<div style="height:1px;background:#E4E6EB;margin:1rem 0;"></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Reports</div>', unsafe_allow_html=True)

if st.button("📄 Download Full Candidate Report", use_container_width=True):

    # use FILTERED results (not raw API)
    report_data = build_all_candidates_report(results, selected_label)

    st.download_button(
        label="⬇️ Download Combined Report (HTML)",
        data=report_data,
        file_name=f"TalentScan_Full_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
        mime="text/html",
        use_container_width=True
    )
