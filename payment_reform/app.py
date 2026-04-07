"""
Case Study: Cross-Institutional Payment System Reform
DG Tax ↔ DG Treasury — Ministry of Finance, Indonesia
Portfolio by Yayan Puji Riyanto
"""
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Payment Reform Case Study",page_icon="🤝",layout="wide",initial_sidebar_state="collapsed")
st.markdown("""
<style>
    .block-container{padding-top:2rem;max-width:1100px;}
    .hero{background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);color:white;padding:40px;border-radius:16px;margin-bottom:28px;}
    .hero h1{font-size:32px;font-weight:800;margin:0 0 8px;}.hero p{font-size:16px;color:#94a3b8;margin:0;line-height:1.5;}
    .hero .tag{display:inline-block;background:rgba(255,255,255,.12);padding:4px 12px;border-radius:16px;font-size:12px;color:#cbd5e1;margin:2px;}
    .sh{background:linear-gradient(90deg,#0f172a,#1e3a5f);color:white;padding:12px 20px;border-radius:8px;font-size:17px;font-weight:600;margin:24px 0 14px;}
    .mc{background:linear-gradient(135deg,#f8fafc,#e2e8f0);border-radius:12px;padding:18px;text-align:center;border:1px solid #e2e8f0;}
    .mc h3{font-size:11px;color:#64748b;margin:0 0 4px;text-transform:uppercase;letter-spacing:.5px;}.mc .v{font-size:26px;font-weight:700;color:#1e293b;margin:0;}.mc .s{font-size:11px;color:#94a3b8;margin-top:3px;}
    .stake-card{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.04);height:100%;}
    .stake-card h4{margin-top:0;color:#1e293b;}.stake-card p{color:#475569;font-size:13px;line-height:1.5;}
    .tl-item{display:flex;gap:16px;margin:12px 0;}.tl-dot{min-width:14px;height:14px;border-radius:50%;margin-top:4px;}
    .tl-content{flex:1;}.tl-date{font-size:12px;color:#64748b;font-weight:600;}.tl-text{font-size:13px;color:#334155;line-height:1.5;}
    .outcome-card{background:white;border-radius:12px;padding:20px;border:1px solid #e2e8f0;text-align:center;}
    .outcome-num{font-size:36px;font-weight:800;margin:8px 0 4px;}.outcome-label{font-size:13px;color:#64748b;}
    .ib{background:#f8fafc;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 8px 8px 0;margin:10px 0;font-size:14px;color:#334155;line-height:1.6;}
    .challenge{background:#fef2f2;border-left:4px solid #dc2626;padding:12px 16px;border-radius:0 8px 8px 0;margin:6px 0;font-size:13px;color:#991b1b;}
    .solution{background:#f0fdf4;border-left:4px solid #22c55e;padding:12px 16px;border-radius:0 8px 8px 0;margin:6px 0;font-size:13px;color:#166534;}
    .aiib-card{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #bfdbfe;border-radius:12px;padding:20px;margin:8px 0;}
    .fc{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:22px;height:100%;box-shadow:0 1px 3px rgba(0,0,0,.04);}
    .fc h4{color:#1e293b;margin-top:0;}.fc p{color:#475569;font-size:14px;line-height:1.6;}
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}.stDeployButton{display:none;}
</style>
""",unsafe_allow_html=True)

# ═══ HERO ═══
st.markdown("""
<div class="hero">
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px;">
        <span style="font-size:40px;">🤝</span>
        <div>
            <h1>Cross-Institutional Payment System Reform</h1>
            <p>Negotiating the transition from manual to electronic tax payments across 516 offices in Indonesia</p>
        </div>
    </div>
    <div style="margin-top:12px;">
        <span class="tag">🏛️ DG Tax ↔ DG Treasury</span>
        <span class="tag">📋 Ministry of Finance, Indonesia</span>
        <span class="tag">📅 2016 – 2018</span>
        <span class="tag">👤 Yayan Puji Riyanto — Policy & Business Process Analyst</span>
    </div>
</div>
""",unsafe_allow_html=True)

# ═══ OUTCOME METRICS ═══
c1,c2,c3,c4,c5 = st.columns(5)
with c1: st.markdown('<div class="outcome-card"><div style="font-size:24px;">🏢</div><div class="outcome-num" style="color:#2563eb;">516</div><div class="outcome-label">Tax offices nationwide</div></div>',unsafe_allow_html=True)
with c2: st.markdown('<div class="outcome-card"><div style="font-size:24px;">💳</div><div class="outcome-num" style="color:#059669;">7</div><div class="outcome-label">Electronic payment methods</div></div>',unsafe_allow_html=True)
with c3: st.markdown('<div class="outcome-card"><div style="font-size:24px;">🏦</div><div class="outcome-num" style="color:#d97706;">3</div><div class="outcome-label">State-owned bank partners</div></div>',unsafe_allow_html=True)
with c4: st.markdown('<div class="outcome-card"><div style="font-size:24px;">📍</div><div class="outcome-num" style="color:#7c3aed;">31</div><div class="outcome-label">Regional offices coordinated</div></div>',unsafe_allow_html=True)
with c5: st.markdown('<div class="outcome-card"><div style="font-size:24px;">✅</div><div class="outcome-num" style="color:#dc2626;">0</div><div class="outcome-label">Manual payment channels remaining</div></div>',unsafe_allow_html=True)

# ═══ CONTEXT ═══
st.markdown('<div class="sh">📋 Context & Challenge</div>',unsafe_allow_html=True)
st.markdown("""<div class="ib">
    Indonesia's tax payment infrastructure relied on <strong>manual, cash-based payment processing</strong> at tax offices nationwide.
    Taxpayers would physically bring cash or checks to tax offices, where staff manually processed payments and reconciled
    against tax assessments. This system created significant <strong>operational risks</strong>: cash-handling vulnerabilities,
    reconciliation errors, fraud exposure, and lack of auditable transaction trails.<br><br>
    The Directorate General of Taxes (DGT) and the Directorate General of Treasury (DGTr) — both under the Ministry of Finance
    but with <strong>competing institutional mandates and different operational priorities</strong> — needed to agree on a
    unified transition to electronic payments. As <strong>Policy & Business Process Analyst</strong>, I led the negotiation
    between these two institutions.
</div>""",unsafe_allow_html=True)

# ═══ STAKEHOLDER MAP ═══
st.markdown('<div class="sh">🗺️ Stakeholder Landscape</div>',unsafe_allow_html=True)

fig_stake = go.Figure()

# Nodes
nodes = [
    ("DG Tax (DJP)", 0.2, 0.7, 50, "#2563eb", "Policy owner\nTax collection mandate\n516 tax offices"),
    ("DG Treasury (DJPb)", 0.8, 0.7, 50, "#059669", "Payment infrastructure owner\nState revenue management\nMPN system operator"),
    ("State-Owned Banks", 0.5, 0.3, 40, "#d97706", "Payment channel providers\nBRI, BNI, Mandiri\nEDC terminal deployment"),
    ("Taxpayers", 0.5, 0.95, 35, "#7c3aed", "270M+ citizens\nBusinesses & individuals\nEnd users of payment system"),
    ("Regional Offices", 0.15, 0.3, 35, "#ea580c", "31 Kanwil\n516 KPP offices\nImplementation responsibility"),
    ("Ministry of Finance\n(Coordinating)", 0.85, 0.3, 35, "#475569", "Policy oversight\nBudget allocation\nInter-DG coordination"),
    ("Yayan (Negotiator)", 0.5, 0.6, 30, "#dc2626", "Policy & Business Process Analyst\nDirectorate of BPT\nLed negotiation & coordination"),
]

for name, x, y, size, color, hover in nodes:
    fig_stake.add_trace(go.Scatter(
        x=[x], y=[y], mode="markers+text", showlegend=False,
        marker=dict(size=size, color=color, line=dict(width=2, color="white"), opacity=0.9),
        text=[name], textposition="bottom center" if y > 0.5 else "top center",
        textfont=dict(size=10, color="#1e293b"),
        hovertemplate=f"<b>{name}</b><br>{hover}<extra></extra>"
    ))

# Connection lines
connections = [
    (0.2,0.7,0.5,0.6,"#2563eb","Mandate alignment"),
    (0.8,0.7,0.5,0.6,"#059669","Infrastructure agreement"),
    (0.5,0.6,0.5,0.3,"#d97706","Bank partner coordination"),
    (0.5,0.6,0.15,0.3,"#ea580c","Rollout coordination"),
    (0.5,0.95,0.5,0.6,"#7c3aed","User needs"),
    (0.85,0.3,0.5,0.6,"#475569","Policy oversight"),
]
for x0,y0,x1,y1,color,label in connections:
    fig_stake.add_trace(go.Scatter(x=[x0,x1],y=[y0,y1],mode="lines",showlegend=False,
        line=dict(color=color,width=1.5,dash="dot"),opacity=0.4))

fig_stake.update_layout(
    height=420,margin=dict(t=10,b=10,l=10,r=10),plot_bgcolor="white",
    xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.05,1.05]),
    yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[0.15,1.05]),
)
st.plotly_chart(fig_stake,use_container_width=True)

# Competing interests
st.markdown('<div class="sh">⚔️ Competing Institutional Interests</div>',unsafe_allow_html=True)
ci1,ci2=st.columns(2)
with ci1:
    st.markdown("""<div class="stake-card" style="border-top:4px solid #2563eb;">
        <h4 style="color:#2563eb;">🔵 DG Tax (DJP) Position</h4>
        <p><strong>Mandate:</strong> Maximize tax collection efficiency and taxpayer compliance</p>
        <p><strong>Concerns:</strong></p>
        <ul style="font-size:13px;color:#475569;">
            <li>Losing direct control over payment collection points</li>
            <li>Dependency on Treasury's MPN system for revenue data</li>
            <li>Risk of service disruption during transition affecting tax revenue</li>
            <li>Need to maintain <strong>real-time visibility</strong> of incoming payments for taxpayer accounting</li>
            <li>Preferred <strong>gradual transition</strong> with fallback to manual processing</li>
        </ul>
    </div>""",unsafe_allow_html=True)
with ci2:
    st.markdown("""<div class="stake-card" style="border-top:4px solid #059669;">
        <h4 style="color:#059669;">🟢 DG Treasury (DJPb) Position</h4>
        <p><strong>Mandate:</strong> Manage state revenue flow and payment infrastructure integrity</p>
        <p><strong>Concerns:</strong></p>
        <ul style="font-size:13px;color:#475569;">
            <li>Maintaining MPN (State Revenue Module) system stability with increased transaction volume</li>
            <li>Standardizing payment codes across all revenue types, not just tax</li>
            <li>Budget constraints for upgrading payment infrastructure at 516 offices</li>
            <li>Preferred <strong>immediate full cutover</strong> to reduce dual-system maintenance cost</li>
            <li>Insisted on <strong>Treasury payment codes</strong> (MAP) format, which DGT resisted</li>
        </ul>
    </div>""",unsafe_allow_html=True)

# ═══ NEGOTIATION APPROACH ═══
st.markdown('<div class="sh">🎯 Negotiation Approach & Resolution</div>',unsafe_allow_html=True)

st.markdown("""<div class="ib">
    The core conflict was <strong>speed vs control</strong>: Treasury wanted immediate full cutover to eliminate manual payment
    infrastructure costs; Tax wanted gradual transition to protect revenue collection continuity. Additionally, both institutions
    had incompatible views on payment code formats, reconciliation data ownership, and exception handling procedures.
</div>""",unsafe_allow_html=True)

# Challenges and Solutions
issues = [
    ("Transition speed: immediate vs gradual",
     "Proposed phased rollout by region (6 waves across 31 regional offices over 18 months) — gave DGT control over pace while giving DGTr a firm end date"),
    ("Payment code format dispute (DGT vs MPN format)",
     "Designed hybrid MAP/KJS mapping system: DGT maintains its own tax-type codes (KJS) while system auto-translates to Treasury MAP codes at transaction time — both systems preserved"),
    ("Reconciliation data ownership",
     "Established shared reconciliation protocol: real-time data feed from MPN to DGT's taxpayer accounting system — DGT gets visibility, DGTr maintains system-of-record authority"),
    ("Exception handling for failed electronic payments",
     "Created escalation matrix with defined SLAs: bank-side failures route to bank helpdesk; MPN-side failures route to DGTr; tax-code failures route to DGT — clear accountability per failure type"),
    ("Budget for EDC terminals at 516 offices",
     "Negotiated cost-sharing: banks provide EDC hardware (zero cost to government) in exchange for exclusive payment channel contracts per region — aligned bank commercial interest with government policy"),
    ("Staff resistance to change at field offices",
     "Designed training program with regional champion model: 2 trained champions per office who train peers — reduced central training burden while building local ownership"),
    ("Risk of revenue loss during transition",
     "Built parallel-run protocol: 30-day period per office where both manual and electronic channels operate simultaneously — no hard cutover until electronic channel handles 95%+ of volume"),
]

for challenge, solution in issues:
    st.markdown(f'<div class="challenge">⚠️ <strong>Challenge:</strong> {challenge}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="solution">✅ <strong>Resolution:</strong> {solution}</div>',unsafe_allow_html=True)
    st.markdown("",unsafe_allow_html=True)

# ═══ TIMELINE ═══
st.markdown('<div class="sh">📅 Implementation Timeline</div>',unsafe_allow_html=True)

timeline = [
    ("#dc2626","Q1 2016","Stakeholder Analysis & Mandate Mapping","Mapped competing interests of DGT, DGTr, banks, and 31 regional offices. Identified 7 critical negotiation points."),
    ("#ea580c","Q2 2016","Bilateral Negotiation Sessions","Led 12 bilateral sessions between DGT and DGTr technical teams. Resolved payment code format dispute through hybrid MAP/KJS mapping."),
    ("#d97706","Q3 2016","Framework Agreement Signed","Both DGs signed framework agreement covering: 7 payment methods, phased rollout plan, reconciliation protocol, and exception handling matrix."),
    ("#eab308","Q4 2016","Bank Partner Onboarding","Negotiated EDC deployment agreements with BRI, BNI, and Mandiri. Secured zero-cost hardware provision in exchange for regional exclusivity."),
    ("#22c55e","Q1-Q2 2017","Wave 1-3 Rollout (Java)","Deployed across 180 offices in Java (highest volume region). Achieved 97% electronic payment adoption within 60 days per office."),
    ("#059669","Q3-Q4 2017","Wave 4-5 Rollout (Sumatra, Kalimantan, Sulawesi)","Extended to 220 additional offices. Encountered and resolved connectivity challenges in remote locations via mobile payment fallback."),
    ("#2563eb","Q1-Q2 2018","Wave 6 Rollout (Eastern Indonesia) + Full Completion","Final 116 offices onboarded. Manual payment channels officially decommissioned. Full auditable electronic trail established nationwide."),
]

for color,date,title,desc in timeline:
    st.markdown(f"""<div class="tl-item">
        <div class="tl-dot" style="background:{color};"></div>
        <div class="tl-content">
            <div class="tl-date">{date} — {title}</div>
            <div class="tl-text">{desc}</div>
        </div>
    </div>""",unsafe_allow_html=True)

# ═══ OUTCOMES ═══
st.markdown('<div class="sh">📊 Outcomes & Impact</div>',unsafe_allow_html=True)

o1,o2=st.columns(2)
with o1:
    outcomes = [
        ("Eliminated manual cash-handling risk", "Removed cash-handling control vulnerabilities across all 516 offices — the #1 source of operational risk incidents in tax offices."),
        ("7 standardized payment methods", "ATM transfer, internet banking, mobile banking, EDC (debit), over-the-counter bank, e-wallet, and virtual account — covering 99%+ of taxpayer preferences."),
        ("Fully auditable transaction trail", "Every payment now generates an electronic record linked to the taxpayer's NPWP, tax type (KJS), and MPN transaction ID — enabling end-to-end reconciliation."),
        ("30% reduction in reconciliation exceptions", "Automated MPN integration reduced manual reconciliation workload by an estimated 30% within the first year of full deployment."),
    ]
    for title,desc in outcomes:
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:6px 0;border-left:4px solid #22c55e;">
            <div style="font-size:14px;font-weight:600;color:#166534;">{title}</div>
            <div style="font-size:13px;color:#475569;margin-top:4px;">{desc}</div>
        </div>""",unsafe_allow_html=True)

with o2:
    # Before/after comparison
    fig_ba = go.Figure()
    categories = ['Cash Handling Risk','Reconciliation Time','Audit Trail Coverage','Payment Speed','Fraud Exposure']
    before = [5, 4.5, 1.5, 1, 4.5]
    after = [0.5, 1.5, 5, 4.5, 0.5]
    fig_ba.add_trace(go.Scatterpolar(r=before+[before[0]], theta=categories+[categories[0]], fill='toself',
        name='Before (Manual)', fillcolor='rgba(220,38,38,.15)', line=dict(color='#dc2626',width=2)))
    fig_ba.add_trace(go.Scatterpolar(r=after+[after[0]], theta=categories+[categories[0]], fill='toself',
        name='After (Electronic)', fillcolor='rgba(34,197,94,.15)', line=dict(color='#22c55e',width=2)))
    fig_ba.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],tickfont=dict(size=8))),
        height=350,margin=dict(t=30,b=30),title="Before vs After: Risk Profile",title_font_size=14,
        legend=dict(orientation="h",y=-0.05,x=.5,xanchor="center"))
    st.plotly_chart(fig_ba,use_container_width=True)

# ═══ AIIB RELEVANCE ═══
st.markdown('<div class="sh">🏛️ Relevance to AIIB Operational Risk Intern Role</div>',unsafe_allow_html=True)

r1,r2,r3=st.columns(3)
with r1:
    st.markdown("""<div class="aiib-card">
        <div style="font-size:24px;margin-bottom:6px;">🤝</div>
        <h4 style="color:#1e40af;margin-top:0;">Multi-Stakeholder Coordination</h4>
        <p style="font-size:13px;color:#334155;line-height:1.5;">Coordinated 6 stakeholder groups with competing mandates — directly comparable to AIIB's multi-country, multi-institutional environment where COR must coordinate with Investment Operations, Treasury, Legal, IT, and member country counterparties.</p>
    </div>""",unsafe_allow_html=True)
with r2:
    st.markdown("""<div class="aiib-card">
        <div style="font-size:24px;margin-bottom:6px;">🛡️</div>
        <h4 style="color:#1e40af;margin-top:0;">Operational Risk Elimination</h4>
        <p style="font-size:13px;color:#334155;line-height:1.5;">Identified and eliminated the #1 operational risk source (manual cash handling) across 516 offices. Designed mitigation controls for transition risks. This is exactly what COR does: identify, assess, manage, and monitor operational risk.</p>
    </div>""",unsafe_allow_html=True)
with r3:
    st.markdown("""<div class="aiib-card">
        <div style="font-size:24px;margin-bottom:6px;">📋</div>
        <h4 style="color:#1e40af;margin-top:0;">Process Documentation & Governance</h4>
        <p style="font-size:13px;color:#334155;line-height:1.5;">Drafted framework agreement, reconciliation protocols, escalation matrices, and exception handling procedures — the same documentation skills needed for AIIB's OR framework enhancement, incident recording, and reporting activities.</p>
    </div>""",unsafe_allow_html=True)

# ═══ SKILLS ═══
st.markdown('<div class="sh">💡 Skills Demonstrated</div>',unsafe_allow_html=True)
sk1,sk2=st.columns(2)
with sk1:
    st.markdown("""<div class="fc">
        <h4>Negotiation & Conflict Resolution</h4>
        <p>Resolved 7 critical negotiation points between institutions with fundamentally competing mandates.
        Used interest-based negotiation (not positional): identified underlying interests behind each position
        and designed solutions that addressed both parties' core needs.</p>
    </div>""",unsafe_allow_html=True)
with sk2:
    st.markdown("""<div class="fc">
        <h4>Large-Scale Change Management</h4>
        <p>Designed and coordinated rollout across 516 offices, 31 regional offices, 3 bank partners, and
        thousands of field staff. Used phased approach with parallel-run protocol to manage transition risk —
        directly applicable to OR framework implementation in a growing MDB.</p>
    </div>""",unsafe_allow_html=True)

# FOOTER
st.divider()
st.markdown("""<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">
    Case Study: Cross-Institutional Payment System Reform<br>
    Portfolio by <strong>Yayan Puji Riyanto</strong> · Policy & Business Process Analyst, DGT (2015-2018)<br>
    PhD Candidate, Business Law & Taxation — Monash University<br>
    <em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em>
</div>""",unsafe_allow_html=True)
