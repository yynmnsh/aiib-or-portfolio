"""
MDB Peer Benchmarking: Operational Risk Frameworks
AIIB vs World Bank vs ADB vs EBRD vs IFC
Portfolio by Yayan Puji Riyanto
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MDB OR Benchmarking — AIIB COR",page_icon="🏦",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
    .block-container{padding-top:3.5rem;max-width:1200px;}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#0c1e3c,#162d50);}
    [data-testid="stSidebar"] *{color:#cbd5e1!important;}
    [data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] strong{color:#f1f5f9!important;}
    .mc{background:linear-gradient(135deg,#f8fafc,#e2e8f0);border-radius:12px;padding:18px;text-align:center;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.06);}
    .mc h3{font-size:12px;color:#64748b;margin:0 0 5px;text-transform:uppercase;letter-spacing:.5px;}.mc .v{font-size:22px;font-weight:700;color:#1e293b;margin:0;}.mc .s{font-size:11px;color:#94a3b8;margin-top:3px;}
    .sh{background:linear-gradient(90deg,#0f172a,#1e3a5f);color:white;padding:12px 20px;border-radius:8px;font-size:17px;font-weight:600;margin:22px 0 14px;}
    .ib{background:#f8fafc;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 8px 8px 0;margin:10px 0;font-size:14px;color:#334155;line-height:1.6;}
    .fc{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:22px;height:100%;box-shadow:0 1px 3px rgba(0,0,0,.04);}
    .fc h4{color:#1e293b;margin-top:0;}.fc p{color:#475569;font-size:14px;line-height:1.6;}
    .mdb-card{background:white;border-radius:12px;padding:20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.04);text-align:center;}
    .gap-card{background:#fffbeb;border:1px solid #fef08a;border-radius:10px;padding:16px;margin:8px 0;}
    .opp-card{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:16px;margin:8px 0;}
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}.stDeployButton{display:none;}
</style>
""",unsafe_allow_html=True)

MDBS={
    "AIIB":{"full":"Asian Infrastructure Investment Bank","hq":"Beijing","est":2016,"members":111,"capital":"USD 100B","rating":"AAA","color":"#2563eb","icon":"🏛️","focus":"Infrastructure for Tomorrow — green, tech-enabled, regional connectivity"},
    "World Bank":{"full":"International Bank for Reconstruction and Development (IBRD)","hq":"Washington DC","est":1944,"members":189,"capital":"USD 318B","rating":"AAA","color":"#059669","icon":"🌍","focus":"Ending extreme poverty, boosting shared prosperity"},
    "ADB":{"full":"Asian Development Bank","hq":"Manila","est":1966,"members":68,"capital":"USD 175B","rating":"AAA","color":"#d97706","icon":"🌏","focus":"Prosperous, inclusive, resilient, and sustainable Asia-Pacific"},
    "EBRD":{"full":"European Bank for Reconstruction and Development","hq":"London","est":1991,"members":73,"capital":"EUR 30B","rating":"AAA","color":"#7c3aed","icon":"🏗️","focus":"Transition to open market-oriented economies"},
    "IFC":{"full":"International Finance Corporation","hq":"Washington DC","est":1956,"members":186,"capital":"USD 25B","rating":"AAA","color":"#dc2626","icon":"🏢","focus":"Private sector development in emerging markets"},
}

# Benchmarking dimensions with detailed comparison
DIMENSIONS = {
    "Governance & Structure":{
        "desc":"How OR function is positioned within the organization",
        "metrics":["OR function placement","Reporting line","Board committee oversight","CRO role","OR team size (approx.)"],
        "data":{
            "AIIB":["COR within Risk Management Dept (2nd line)","Head of COR → CRO → Risk Committee","Audit & Risk Committee","Dedicated CRO","~10-15 (growing institution)"],
            "World Bank":["Operational Risk within Risk Vice Presidency","VP Risk → Managing Director → Board","Audit Committee + Risk Committee","VP-level Risk officer","~50-80"],
            "ADB":["Risk Management within Office of Risk Management","Director Risk Mgmt → VP Finance","Audit Committee","Director-level","~30-40"],
            "EBRD":["Operational Risk within Risk Management","Head OR → CRO → Board Risk Committee","Audit Committee","Dedicated CRO","~20-30"],
            "IFC":["Within Risk & Finance Vice Presidency","Director Risk → VP Risk & Finance","Audit Committee","VP-level","~25-35"],
        }
    },
    "Risk Identification & Assessment":{
        "desc":"Methods and tools for identifying and assessing operational risks",
        "metrics":["RCSA","Scenario Analysis","Loss Event Database","KRIs","Risk Taxonomy"],
        "data":{
            "AIIB":["Developing (annual cycle)","Developing framework","Established (limited history since 2016)","Defined at Board/President/CRO levels","Basel II/III aligned"],
            "World Bank":["Mature (annual + event-driven)","Advanced (quantitative)","Extensive (20+ years)","Comprehensive with automated monitoring","Custom MDB taxonomy"],
            "ADB":["Established (annual cycle)","Established framework","Established (15+ years)","Defined with quarterly review","Basel II/III adapted"],
            "EBRD":["Mature (semi-annual)","Advanced (incl. stress testing)","Extensive (30+ years)","Advanced with real-time dashboards","Basel II/III + EBRD-specific"],
            "IFC":["Mature (annual + continuous)","Advanced (scenario-based capital)","Extensive (25+ years)","Comprehensive","Basel II/III + IFC-specific"],
        }
    },
    "Compliance & AML/CFT":{
        "desc":"Compliance risk management and financial integrity controls",
        "metrics":["AML/CFT framework","Sanctions screening","FATF alignment","Tax transparency","Integrity due diligence"],
        "data":{
            "AIIB":["Aligned with FATF Recommendations + UNSC Resolutions","Automated (OFAC, UN, EU lists)","Full alignment","OECD Global Forum Observer (2023)","On project counterparties"],
            "World Bank":["Comprehensive (longest established among MDBs)","Multi-list automated + enhanced DD","Full alignment","Full OECD membership","Extensive — all counterparties + staff"],
            "ADB":["Aligned with FATF","Automated screening","Full alignment","OECD engagement","On counterparties"],
            "EBRD":["Aligned with EU regulations + FATF","Automated + manual enhanced screening","Full alignment + EU AML Directive","Full OECD membership","Comprehensive"],
            "IFC":["Aligned with World Bank Group framework","Automated + ongoing monitoring","Full alignment","OECD engagement","Extensive — private sector focus"],
        }
    },
    "Incident Management":{
        "desc":"How OR events are captured, recorded, and managed",
        "metrics":["Incident capture process","Root cause analysis","Escalation framework","Reporting cadence","Lessons learned process"],
        "data":{
            "AIIB":["Established — COR-managed","Conducted for High/Critical events","Defined (CRO → Risk Committee → ARC)","Quarterly to Risk Committee","Developing"],
            "World Bank":["Mature — centralized system","Mandatory for all events","Multi-tier (VP → MD → Board)","Monthly + quarterly + annual","Mature — integrated into RCSA"],
            "ADB":["Established — centralized","Conducted for material events","Defined escalation matrix","Quarterly","Established"],
            "EBRD":["Mature — integrated GRC platform","Mandatory + 5-Why methodology","Automated threshold-based","Monthly + quarterly","Mature — shared across BUs"],
            "IFC":["Mature — shared with WBG systems","Mandatory for all events","Aligned with WBG framework","Monthly + quarterly","Mature — cross-IFC learning"],
        }
    },
    "Technology & Reporting":{
        "desc":"Technology platforms and reporting capabilities for OR management",
        "metrics":["GRC/OR platform","Automation level","Dashboard/visualization","Data analytics capability","AI/ML usage in OR"],
        "data":{
            "AIIB":["Developing (newer systems)","Moderate — sanctions screening automated","Basic dashboards","Python/SQL capabilities in team","Exploring"],
            "World Bank":["Enterprise GRC platform (ServiceNow/Archer)","High — automated workflows","Advanced BI dashboards","Dedicated analytics team","Predictive risk models"],
            "ADB":["Enterprise GRC platform","Moderate-High","Established BI reporting","Analytics team","Exploring"],
            "EBRD":["Integrated GRC platform","High — automated KRI monitoring","Real-time dashboards","Advanced analytics","ML for fraud detection"],
            "IFC":["Shared WBG GRC + IFC-specific tools","High","Advanced","Strong analytics capability","ML for portfolio risk"],
        }
    },
    "Business Continuity & Crisis":{
        "desc":"Operational resilience and crisis management capabilities",
        "metrics":["BCP/DR framework","Crisis management plan","Pandemic preparedness","Cyber resilience","DR testing frequency"],
        "data":{
            "AIIB":["Established","Developing","Tested during COVID-19 (rapid remote transition)","SOC + EDR + incident response","Annual"],
            "World Bank":["Mature (multi-site)","Comprehensive (incl. field offices)","Mature (extensive experience)","Advanced (dedicated CISO)","Semi-annual"],
            "ADB":["Established (multi-site)","Established","Tested during COVID-19","Established","Annual"],
            "EBRD":["Mature","Comprehensive","Mature","Advanced","Quarterly"],
            "IFC":["Mature (aligned with WBG)","Comprehensive","Mature","Advanced (shared with WBG)","Semi-annual"],
        }
    },
}

MATURITY_SCORES = {
    "AIIB":       {"Governance":3,"Risk Assessment":2.5,"Compliance":3.5,"Incident Mgmt":2.5,"Technology":2,"BCP/Crisis":3},
    "World Bank": {"Governance":5,"Risk Assessment":5,"Compliance":5,"Incident Mgmt":5,"Technology":5,"BCP/Crisis":5},
    "ADB":        {"Governance":4,"Risk Assessment":3.5,"Compliance":4,"Incident Mgmt":3.5,"Technology":3.5,"BCP/Crisis":3.5},
    "EBRD":       {"Governance":4.5,"Risk Assessment":4.5,"Compliance":4.5,"Incident Mgmt":4.5,"Technology":4.5,"BCP/Crisis":4.5},
    "IFC":        {"Governance":4.5,"Risk Assessment":4.5,"Compliance":4.5,"Incident Mgmt":4.5,"Technology":4,"BCP/Crisis":4},
}

GAPS_AND_OPPS = [
    {"area":"Risk Assessment Maturity","gap":"AIIB's RCSA and scenario analysis frameworks are still developing compared to peers with 20+ years of operational history. Limited internal loss data constrains quantitative risk modeling.",
     "opportunity":"Leapfrog legacy approaches by implementing modern, data-driven RCSA from the start. Adopt best practices from World Bank/EBRD without legacy system constraints. Build scenario library using peer MDB loss data.",
     "priority":"High","effort":"Medium"},
    {"area":"GRC Technology Platform","gap":"AIIB uses newer but less integrated systems compared to peers with enterprise GRC platforms (e.g., World Bank's ServiceNow/Archer). Limited automation in KRI monitoring and incident workflow.",
     "opportunity":"Implement a modern, cloud-native GRC platform from scratch — avoiding the technical debt of peers. Integrate AI/ML capabilities natively rather than retrofitting. Start with automated KRI dashboards and incident workflows.",
     "priority":"High","effort":"High"},
    {"area":"Incident Management & Lessons Learned","gap":"Limited internal loss history (operational since 2016). Lessons learned process is still developing. Incident data volume insufficient for statistical analysis.",
     "opportunity":"Establish a robust incident taxonomy early. Participate in MDB loss data sharing consortia. Leverage peer MDB incident libraries (anonymized) to build scenario analysis capability.",
     "priority":"Medium","effort":"Low"},
    {"area":"Sanctions Screening Depth","gap":"Current screening focuses on primary counterparties. Sub-contractor screening below threshold is not mandatory (as highlighted in INC-2025-005 scenario).",
     "opportunity":"Extend screening to all tiers of supply chain. Implement continuous monitoring (vs point-in-time screening). Benchmark against EBRD's comprehensive approach which covers full supply chain.",
     "priority":"High","effort":"Medium"},
    {"area":"AI/ML in Operational Risk","gap":"AIIB is still exploring AI/ML for OR management while peers (World Bank, EBRD) have deployed predictive models and ML-based fraud detection.",
     "opportunity":"As a younger institution, AIIB can adopt latest-generation AI tools without legacy integration challenges. Consider NLP for incident classification, ML for anomaly detection in disbursement patterns, and predictive analytics for KRI forecasting.",
     "priority":"Medium","effort":"High"},
    {"area":"Operational Resilience","gap":"BCP/DR framework is established but less mature than peers with decades of crisis management experience across multiple field offices.",
     "opportunity":"Build resilience framework natively incorporating post-COVID lessons. Focus on cyber resilience given increasing digital operations. Benchmark against EBRD's quarterly DR testing cadence.",
     "priority":"Medium","effort":"Medium"},
]

def mc_render(l,v,s=""):
    st.markdown(f'<div class="mc"><h3>{l}</h3><p class="v">{v}</p><p class="s">{s}</p></div>',unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:10px 0 18px;'>
        <div style='font-size:36px;margin-bottom:4px;'>🏦</div>
        <div style='font-size:17px;font-weight:700;color:#f1f5f9!important;'>MDB Peer Benchmarking</div>
        <div style='font-size:12px;color:#94a3b8!important;margin-top:4px;'>Operational Risk Frameworks</div>
    </div>""",unsafe_allow_html=True)
    st.divider()
    selected_mdbs=st.multiselect("Compare MDBs",list(MDBS.keys()),default=list(MDBS.keys()))
    st.divider()
    st.markdown("""<div style='font-size:11px;color:#64748b;line-height:1.6;'>
        <strong style='color:#94a3b8!important;'>Purpose</strong><br>
        Benchmarking AIIB's OR framework against peer MDBs to identify enhancement opportunities — directly supporting COR's mandate for framework improvement.<br><br>
        <strong style='color:#94a3b8!important;'>Sources</strong><br>
        Annual reports, public policy documents, risk management frameworks, and job postings from each MDB.<br><br>
        <strong style='color:#94a3b8!important;'>Portfolio by</strong><br>Yayan Puji Riyanto<br>PhD Candidate — Monash University
    </div>""",unsafe_allow_html=True)

# TABS
tab1,tab2,tab3,tab4=st.tabs(["📊 Maturity Overview","📋 Detailed Comparison","🎯 Gap Analysis & Opportunities","📖 MDB Profiles"])

with tab1:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">OR Framework Maturity Benchmarking</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Comparing AIIB against peer MDBs across 6 framework dimensions</p>',unsafe_allow_html=True)

    # Radar chart
    dims=list(list(MATURITY_SCORES.values())[0].keys())
    fig_radar=go.Figure()
    for mdb in selected_mdbs:
        scores=MATURITY_SCORES[mdb]
        vals=[scores[d] for d in dims]+[scores[dims[0]]]
        fig_radar.add_trace(go.Scatterpolar(r=vals,theta=dims+[dims[0]],fill="toself",name=mdb,
            line=dict(color=MDBS[mdb]["color"],width=2.5),fillcolor=f'rgba({int(MDBS[mdb]["color"][1:3],16)},{int(MDBS[mdb]["color"][3:5],16)},{int(MDBS[mdb]["color"][5:7],16)},.1)'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],tickvals=[1,2,3,4,5],
        ticktext=["1-Initial","2-Developing","3-Established","4-Advanced","5-Mature"],tickfont=dict(size=9),gridcolor="#e2e8f0"),
        angularaxis=dict(tickfont=dict(size=12,color="#334155"))),
        height=480,margin=dict(t=30,b=30,l=80,r=80),legend=dict(orientation="h",y=-0.05,x=.5,xanchor="center"),
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_radar,use_container_width=True)

    # Bar comparison
    st.markdown('<div class="sh">📊 Dimension-by-Dimension Comparison</div>',unsafe_allow_html=True)
    fig_bar=go.Figure()
    for mdb in selected_mdbs:
        scores=MATURITY_SCORES[mdb]
        fig_bar.add_trace(go.Bar(name=mdb,x=dims,y=[scores[d] for d in dims],marker_color=MDBS[mdb]["color"],text=[scores[d] for d in dims],textposition="outside"))
    fig_bar.update_layout(barmode="group",height=350,margin=dict(t=20,b=30),plot_bgcolor="white",
        yaxis=dict(range=[0,5.8],title="Maturity Level",gridcolor="#f1f5f9"),
        legend=dict(orientation="h",y=1.08,x=.5,xanchor="center"))
    fig_bar.add_hline(y=3,line_dash="dash",line_color="#94a3b8",opacity=.4,annotation_text="Established baseline",annotation_position="top right")
    st.plotly_chart(fig_bar,use_container_width=True)

    # AIIB summary
    aiib_scores=MATURITY_SCORES["AIIB"]
    aiib_avg=np.mean(list(aiib_scores.values()))
    peer_avg=np.mean([np.mean(list(MATURITY_SCORES[m].values())) for m in MDBS if m!="AIIB"])
    gap=peer_avg-aiib_avg

    st.markdown('<div class="sh">📈 AIIB Position Summary</div>',unsafe_allow_html=True)
    s1,s2,s3,s4=st.columns(4)
    with s1: mc_render("AIIB Avg Maturity",f"{aiib_avg:.1f}","/5.0")
    with s2: mc_render("Peer Avg",f"{peer_avg:.1f}","/5.0")
    with s3: mc_render("Gap to Peers",f"{gap:.1f}","Points below avg")
    with s4: mc_render("Strongest Area",max(aiib_scores,key=aiib_scores.get),f"{max(aiib_scores.values())}/5")

    st.markdown(f"""<div class="ib">
        <strong>Key Insight:</strong> AIIB's OR framework is at an <strong>Established (Level 3)</strong> maturity overall, which is appropriate
        for an institution operational since 2016. The gap to peers is primarily driven by institutional age — World Bank has 80+ years of
        operational history. AIIB's strongest area is <strong>Compliance/AML-CFT</strong> (3.5/5), reflecting early investment in FATF alignment.
        The largest gaps are in <strong>Technology & Reporting</strong> and <strong>Risk Assessment</strong>, where peers have
        enterprise GRC platforms and decades of loss data.
    </div>""",unsafe_allow_html=True)

with tab2:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Detailed Framework Comparison</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Side-by-side comparison across 6 dimensions and 30 metrics</p>',unsafe_allow_html=True)

    for dim_name,dim_data in DIMENSIONS.items():
        st.markdown(f'<div class="sh">{dim_name}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="ib">{dim_data["desc"]}</div>',unsafe_allow_html=True)

        comp_rows=[]
        for i,metric in enumerate(dim_data["metrics"]):
            row={"Metric":metric}
            for mdb in selected_mdbs:
                row[mdb]=dim_data["data"][mdb][i]
            comp_rows.append(row)

        df_comp=pd.DataFrame(comp_rows)
        st.dataframe(df_comp,use_container_width=True,hide_index=True,height=35+len(comp_rows)*35)

with tab3:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Gap Analysis & Enhancement Opportunities</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Identified gaps between AIIB and peer best practices, with actionable recommendations</p>',unsafe_allow_html=True)

    st.markdown(f"""<div class="ib">
        This analysis identifies <strong>{len(GAPS_AND_OPPS)} key areas</strong> where AIIB's OR framework could be enhanced
        based on peer benchmarking. Each gap is paired with a specific opportunity and prioritized by impact and effort.
        These recommendations directly support the COR intern responsibility: <em>"Support OR framework enhancements through
        research and benchmarking of peer practice."</em>
    </div>""",unsafe_allow_html=True)

    # Priority matrix
    st.markdown('<div class="sh">🎯 Priority Matrix</div>',unsafe_allow_html=True)
    fig_pm=go.Figure()
    effort_map={"Low":1,"Medium":2,"High":3}
    prio_map={"Low":1,"Medium":2,"High":3}
    for g in GAPS_AND_OPPS:
        x=effort_map[g["effort"]]; y=prio_map[g["priority"]]
        fig_pm.add_trace(go.Scatter(x=[x+np.random.uniform(-.15,.15)],y=[y+np.random.uniform(-.15,.15)],
            mode="markers+text",showlegend=False,
            marker=dict(size=24,color="#2563eb" if g["priority"]=="High" else "#eab308" if g["priority"]=="Medium" else "#22c55e",
                       line=dict(width=2,color="white")),
            text=[g["area"][:20]],textposition="top center",textfont=dict(size=9),
            hovertemplate=f"<b>{g['area']}</b><br>Priority: {g['priority']}<br>Effort: {g['effort']}<extra></extra>"))
    # Quadrant labels
    fig_pm.add_annotation(x=1,y=3,text="⭐ Quick Wins",showarrow=False,font=dict(size=11,color="#16a34a"),bgcolor="#f0fdf4",borderpad=4)
    fig_pm.add_annotation(x=3,y=3,text="🎯 Strategic",showarrow=False,font=dict(size=11,color="#1e40af"),bgcolor="#eff6ff",borderpad=4)
    fig_pm.add_annotation(x=1,y=1,text="📋 Fill-ins",showarrow=False,font=dict(size=11,color="#64748b"),bgcolor="#f8fafc",borderpad=4)
    fig_pm.add_annotation(x=3,y=1,text="⏸️ Deprioritize",showarrow=False,font=dict(size=11,color="#94a3b8"),bgcolor="#f8fafc",borderpad=4)
    fig_pm.update_layout(xaxis=dict(title="Implementation Effort →",tickvals=[1,2,3],ticktext=["Low","Medium","High"],range=[.3,3.7]),
        yaxis=dict(title="Business Priority →",tickvals=[1,2,3],ticktext=["Low","Medium","High"],range=[.3,3.7]),
        height=380,margin=dict(t=20,b=40),plot_bgcolor="white")
    st.plotly_chart(fig_pm,use_container_width=True)

    # Detailed gaps
    st.markdown('<div class="sh">📋 Detailed Gap Analysis</div>',unsafe_allow_html=True)
    for g in sorted(GAPS_AND_OPPS,key=lambda x:prio_map[x["priority"]],reverse=True):
        prio_col={"High":"#dc2626","Medium":"#eab308","Low":"#22c55e"}[g["priority"]]
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin:10px 0;border-left:4px solid {prio_col};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <div style="font-size:16px;font-weight:600;color:#1e293b;">{g["area"]}</div>
                <div style="display:flex;gap:6px;">
                    <span style="background:{prio_col};color:white;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600;">Priority: {g["priority"]}</span>
                    <span style="background:#f1f5f9;color:#475569;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600;">Effort: {g["effort"]}</span>
                </div>
            </div>
            <div class="gap-card"><div style="font-size:12px;font-weight:600;color:#92400e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">⚠️ Gap Identified</div>
                <div style="font-size:13px;color:#78350f;">{g["gap"]}</div></div>
            <div class="opp-card"><div style="font-size:12px;font-weight:600;color:#166534;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">💡 Enhancement Opportunity</div>
                <div style="font-size:13px;color:#14532d;">{g["opportunity"]}</div></div>
        </div>""",unsafe_allow_html=True)

with tab4:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">MDB Profiles</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Institutional overview of benchmarked MDBs</p>',unsafe_allow_html=True)

    cols=st.columns(len(selected_mdbs)) if len(selected_mdbs)<=5 else st.columns(3)
    for i,mdb in enumerate(selected_mdbs):
        m=MDBS[mdb]
        col_idx=i%len(cols)
        with cols[col_idx]:
            avg_mat=np.mean(list(MATURITY_SCORES[mdb].values()))
            st.markdown(f"""<div class="mdb-card" style="border-top:4px solid {m['color']};">
                <div style="font-size:32px;margin-bottom:6px;">{m['icon']}</div>
                <div style="font-size:18px;font-weight:700;color:#1e293b;">{mdb}</div>
                <div style="font-size:11px;color:#64748b;margin:4px 0 12px;">{m['full']}</div>
                <div style="font-size:12px;color:#475569;text-align:left;line-height:1.8;">
                    <div style="display:flex;justify-content:space-between;"><span>HQ</span><strong>{m['hq']}</strong></div>
                    <div style="display:flex;justify-content:space-between;"><span>Established</span><strong>{m['est']}</strong></div>
                    <div style="display:flex;justify-content:space-between;"><span>Members</span><strong>{m['members']}</strong></div>
                    <div style="display:flex;justify-content:space-between;"><span>Capital</span><strong>{m['capital']}</strong></div>
                    <div style="display:flex;justify-content:space-between;"><span>Rating</span><strong>{m['rating']}</strong></div>
                    <div style="display:flex;justify-content:space-between;"><span>OR Maturity</span><strong style="color:{m['color']};">{avg_mat:.1f}/5</strong></div>
                </div>
                <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e2e8f0;font-size:11px;color:#64748b;text-align:left;font-style:italic;">{m['focus']}</div>
            </div>""",unsafe_allow_html=True)

    st.markdown('<div class="sh">📎 Sources & References</div>',unsafe_allow_html=True)
    st.markdown("""<div class="ib">
        <strong>AIIB:</strong> Risk Management Framework (Dec 2025); COR Overview (aiib.org); Annual Reports 2022-2024; COR job postings<br>
        <strong>World Bank:</strong> Risk Management Annual Report; IBRD Financial Statements; Operational Risk Policy (internal, inferred from public documents)<br>
        <strong>ADB:</strong> Risk Management Policy; Annual Report 2023; Enterprise Risk Management Framework<br>
        <strong>EBRD:</strong> Risk Management Report; Annual Report 2023; Operational Risk Framework (public summary)<br>
        <strong>IFC:</strong> Annual Report 2023; Risk & Finance VP structure; WBG shared risk infrastructure documentation<br><br>
        <strong>Note:</strong> Maturity scores are the author's assessment based on publicly available information. Actual internal maturity may differ.
        This analysis is intended as a portfolio demonstration piece, not as an official assessment.
    </div>""",unsafe_allow_html=True)

st.divider()
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">MDB Peer Benchmarking — OR Frameworks<br>Portfolio by <strong>Yayan Puji Riyanto</strong> · PhD, Business Law & Taxation — Monash University · MS Business Analytics — CU Boulder<br><em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em></div>',unsafe_allow_html=True)
