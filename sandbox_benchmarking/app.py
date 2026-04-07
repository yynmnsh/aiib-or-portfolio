"""
Regulatory Sandbox Framework: International Benchmarking & Design
Taxation Regulatory Sandbox — DGT, Ministry of Finance, Indonesia
Portfolio by Yayan Puji Riyanto
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Regulatory Sandbox Benchmarking",page_icon="🧪",layout="wide",initial_sidebar_state="collapsed")
st.markdown("""
<style>
    .block-container{padding-top:2rem;max-width:1100px;}
    .hero{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:white;padding:40px;border-radius:16px;margin-bottom:28px;}
    .hero h1{font-size:30px;font-weight:800;margin:0 0 8px;}.hero p{font-size:15px;color:#94a3b8;margin:0;line-height:1.5;}
    .hero .tag{display:inline-block;background:rgba(255,255,255,.12);padding:4px 12px;border-radius:16px;font-size:12px;color:#cbd5e1;margin:2px;}
    .sh{background:linear-gradient(90deg,#0f172a,#1e3a5f);color:white;padding:12px 20px;border-radius:8px;font-size:17px;font-weight:600;margin:24px 0 14px;}
    .mc{background:linear-gradient(135deg,#f8fafc,#e2e8f0);border-radius:12px;padding:18px;text-align:center;border:1px solid #e2e8f0;}
    .mc h3{font-size:11px;color:#64748b;margin:0 0 4px;text-transform:uppercase;letter-spacing:.5px;}.mc .v{font-size:24px;font-weight:700;color:#1e293b;margin:0;}.mc .s{font-size:11px;color:#94a3b8;margin-top:3px;}
    .ib{background:#f8fafc;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 8px 8px 0;margin:10px 0;font-size:14px;color:#334155;line-height:1.6;}
    .fc{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:22px;height:100%;box-shadow:0 1px 3px rgba(0,0,0,.04);}
    .fc h4{color:#1e293b;margin-top:0;}.fc p{color:#475569;font-size:14px;line-height:1.6;}
    .jur-card{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,.04);height:100%;}
    .adopted{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:14px 18px;margin:6px 0;font-size:13px;color:#166534;}
    .adapted{background:#fefce8;border:1px solid #fef08a;border-radius:10px;padding:14px 18px;margin:6px 0;font-size:13px;color:#854d0e;}
    .aiib-card{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #bfdbfe;border-radius:12px;padding:20px;margin:8px 0;}
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}.stDeployButton{display:none;}
</style>
""",unsafe_allow_html=True)

JURISDICTIONS = {
    "UK (FCA)":{
        "flag":"🇬🇧","color":"#2563eb","year":2016,"regulator":"Financial Conduct Authority",
        "scope":"Fintech firms offering innovative financial products/services",
        "duration":"6 months (extendable to 12)","cohort_size":"~30 firms/cohort",
        "entry":"Application-based; must demonstrate genuine innovation, consumer benefit, and need for sandbox",
        "consumer_protection":"Mandatory: informed consent, compensation scheme, fair treatment obligation",
        "exit":"Transition to full authorisation, restricted authorisation, or exit market",
        "data_reporting":"Monthly progress reports; incident reporting within 1 business day",
        "key_feature":"Pioneer model — most replicated globally. Consumer protection ring-fenced from day one.",
        "maturity":5,
    },
    "Singapore (MAS)":{
        "flag":"🇸🇬","color":"#059669","year":2016,"regulator":"Monetary Authority of Singapore",
        "scope":"Financial institutions and fintech for innovative financial services",
        "duration":"6–12 months (case-by-case)","cohort_size":"Individual applications",
        "entry":"Must demonstrate technological innovation and benefit to Singapore's financial ecosystem",
        "consumer_protection":"Risk-proportionate: based on nature and scale of proposed service",
        "exit":"Graduation to full licence or discontinuation with transition plan",
        "data_reporting":"Periodic reports per sandbox agreement; real-time incident escalation",
        "key_feature":"Sandbox Express (2019): pre-defined parameters for specific activities — faster approval.",
        "maturity":5,
    },
    "Australia (ASIC)":{
        "flag":"🇦🇺","color":"#d97706","year":2017,"regulator":"Australian Securities and Investments Commission",
        "scope":"Fintech businesses testing financial services and credit activities",
        "duration":"12 months (extendable to 24)","cohort_size":"Individual + Enhanced Regulatory Sandbox (ERS)",
        "entry":"ASIC individual exemption or ERS notification (streamlined path)",
        "consumer_protection":"Maximum 100 retail clients; $10K max exposure per client; mandatory PI insurance",
        "exit":"Apply for AFSL (Australian Financial Services Licence) or cease activity",
        "data_reporting":"6-monthly reports to ASIC; client complaint register; PI insurance maintenance",
        "key_feature":"Enhanced Regulatory Sandbox (2020): legislative sandbox with automatic 24-month testing period — no ASIC approval needed for qualifying activities.",
        "maturity":4,
    },
    "India (RBI/IFSCA)":{
        "flag":"🇮🇳","color":"#dc2626","year":2019,"regulator":"Reserve Bank of India + IFSCA",
        "scope":"Banks, fintech, and NBFCs for innovative products in payments, lending, insurance",
        "duration":"6 months (extendable)","cohort_size":"Thematic cohorts (e.g., MSME lending, cross-border payments)",
        "entry":"Thematic application rounds; demonstrated innovation in cohort theme",
        "consumer_protection":"Boundary conditions per cohort theme; customer data protection mandatory",
        "exit":"Regulatory integration if successful; exit plan for unsuccessful participants",
        "data_reporting":"Monthly dashboards per cohort requirements; customer feedback collection",
        "key_feature":"Thematic cohort approach — focused innovation in specific regulatory pain points.",
        "maturity":3,
    },
    "Indonesia (OJK)":{
        "flag":"🇮🇩","color":"#7c3aed","year":2018,"regulator":"Otoritas Jasa Keuangan (Financial Services Authority)",
        "scope":"Fintech firms in payments, lending, insurance technology, and digital banking",
        "duration":"12 months (extendable to 24)","cohort_size":"Individual registration",
        "entry":"Registration-based; must be Indonesian legal entity with operational office",
        "consumer_protection":"Client data protection; mandatory complaint handling mechanism; limited testing scope",
        "exit":"Apply for full OJK licence within 12 months; or orderly wind-down",
        "data_reporting":"Monthly reports to OJK; annual audit; incident reporting within 24 hours",
        "key_feature":"First Indonesian financial sandbox. Separate from the taxation sandbox designed by Yayan at DGT.",
        "maturity":3,
    },
}

DESIGN_ELEMENTS = {
    "Governance Structure":{
        "desc":"How the sandbox is governed within the regulatory institution",
        "metrics":["Oversight body","Decision authority","Review mechanism","Stakeholder involvement"],
        "indonesia_design":["DGT Sandbox Committee (cross-directorate)","Director General approval for entry/exit","Quarterly review by Committee + annual report to Minister","Industry consultation via tax profession associations"],
        "benchmark_source":["UK FCA governance model (dedicated sandbox unit)","Singapore MAS (integrated within innovation office)","Australia ASIC (legislative sandbox — automated governance)","UK/Singapore (industry roundtables)"],
        "adopted_or_adapted":["Adopted from UK","Adapted from Singapore","Not adopted (Indonesia's legal system requires ministerial decree)","Adopted from UK/Singapore"],
    },
    "Participant Eligibility":{
        "desc":"Who can enter the sandbox and under what conditions",
        "metrics":["Eligible entities","Innovation requirement","Fit & proper test","Scope limitations"],
        "indonesia_design":["Certified tax application service providers (ASP) + fintech firms with tax-adjacent services","Must demonstrate genuine innovation in tax compliance, payment, or reporting","Company registration, tax compliance history, financial capacity assessment","Testing limited to specific tax process (e.g., e-Filing API, e-Invoice API) — not full tax administration"],
        "benchmark_source":["UK FCA (authorised + unauthorised firms)","All jurisdictions require genuine innovation","UK/Singapore fit & proper standards","Australia ASIC (client + exposure caps)"],
        "adopted_or_adapted":["Adapted — limited to tax-relevant entities","Adopted standard across benchmarks","Adapted with tax-specific compliance history check","Adopted from Australia with tax-process scoping"],
    },
    "Risk Controls & Consumer Protection":{
        "desc":"How risks are managed during the testing period",
        "metrics":["Taxpayer protection","Data protection","Incident handling","Financial safeguards"],
        "indonesia_design":["Taxpayer informed consent + right to opt-out at any time + DGT fallback for failed transactions","Compliant with Indonesian Data Protection Law (UU PDP); data localisation requirement","24-hour incident reporting to DGT; mandatory root cause analysis; participant may be suspended","Escrow deposit or bank guarantee proportional to testing scope value"],
        "benchmark_source":["UK FCA mandatory consumer protection","Singapore/Australia data protection requirements","UK/Singapore incident reporting standards","Australia ASIC (PI insurance + client caps)"],
        "adopted_or_adapted":["Adopted from UK with DGT fallback added","Adapted for Indonesian legal context (UU PDP)","Adopted from UK/Singapore; added suspension power","Adapted from Australia — escrow instead of insurance (Indonesian market context)"],
    },
    "Testing Parameters":{
        "desc":"The boundaries and duration of sandbox testing",
        "metrics":["Duration","Scale limits","Geographic scope","Performance metrics"],
        "indonesia_design":["12 months initial, extendable to 18 months with Committee approval","Max 10,000 taxpayers or IDR 50B transaction value (whichever reached first)","National scope but with regional pilot option (single Kanwil first)","Defined KPIs per entrant: system uptime >99.5%, error rate <0.1%, taxpayer satisfaction >80%"],
        "benchmark_source":["UK (6-12m), Singapore (6-12m), Australia (12-24m)","Australia ASIC (100 clients / $10K per client)","UK/Singapore (national)","India RBI (thematic cohort KPIs)"],
        "adopted_or_adapted":["Adopted 12-month standard","Adapted for Indonesian tax system scale","Adapted — added regional pilot option (Indonesia's geographic diversity)","Adopted from India with tax-specific KPIs"],
    },
    "Exit & Graduation":{
        "desc":"What happens when the testing period ends",
        "metrics":["Graduation path","Failure protocol","Regulatory integration","Knowledge sharing"],
        "indonesia_design":["Successful participants receive full DGT certification as tax application service provider","Orderly wind-down: 30-day transition period; DGT assumes service continuity for affected taxpayers","Sandbox learnings integrated into DGT regulatory framework for third-party tax service providers","Anonymised results shared with tax policy division for regulatory improvement"],
        "benchmark_source":["UK (full authorisation), Singapore (full licence)","UK/Australia (transition plans)","Singapore (regulatory integration is explicit goal)","UK FCA (published sandbox reports)"],
        "adopted_or_adapted":["Adapted for DGT certification framework","Adopted from UK with DGT continuity obligation","Adopted from Singapore — regulatory learning as explicit outcome","Adopted from UK — transparency model"],
    },
}

def mc_render(l,v,s=""):
    st.markdown(f'<div class="mc"><h3>{l}</h3><p class="v">{v}</p><p class="s">{s}</p></div>',unsafe_allow_html=True)

# ═══ HERO ═══
st.markdown("""<div class="hero">
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px;">
        <span style="font-size:40px;">🧪</span>
        <div>
            <h1>Regulatory Sandbox: International Benchmarking & Framework Design</h1>
            <p>Benchmarking global sandbox practices to design Indonesia's first taxation regulatory sandbox</p>
        </div>
    </div>
    <div style="margin-top:12px;">
        <span class="tag">🏛️ Directorate General of Taxes (DGT)</span>
        <span class="tag">📋 Ministry of Finance, Indonesia</span>
        <span class="tag">📅 2020 – 2022</span>
        <span class="tag">👤 Yayan Puji Riyanto — IT Governance & Regulatory Analyst</span>
        <span class="tag">✅ Adopted as official Ministry policy</span>
    </div>
</div>""",unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
with c1: mc_render("Jurisdictions Benchmarked","5","UK, Singapore, Australia, India, Indonesia (OJK)")
with c2: mc_render("Framework Elements","5","Governance, eligibility, controls, testing, exit")
with c3: mc_render("Design Metrics","20","Across all framework elements")
with c4: mc_render("Outcome","Adopted","As official Ministry of Finance policy")

# TABS
tab1,tab2,tab3,tab4=st.tabs(["🌍 Jurisdiction Comparison","📐 Framework Design","🔍 Design Decisions","🏛️ AIIB Relevance"])

with tab1:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">International Sandbox Benchmarking</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Comparing regulatory sandbox approaches across 5 jurisdictions</p>',unsafe_allow_html=True)

    # Maturity radar
    st.markdown('<div class="sh">📊 Sandbox Maturity Comparison</div>',unsafe_allow_html=True)

    dims_j=["Governance","Consumer Protection","Innovation Scope","Scalability","Regulatory Integration"]
    maturity_data={
        "UK (FCA)":[5,5,5,4,5],"Singapore (MAS)":[5,4,5,5,5],
        "Australia (ASIC)":[4,5,4,4,4],"India (RBI/IFSCA)":[3,3,3,3,3],
        "Indonesia (OJK)":[3,3,3,3,2],
        "Indonesia Tax (DGT)\n— Yayan's Design":[4,4,3,3,4],
    }
    colors_j=["#2563eb","#059669","#d97706","#dc2626","#7c3aed","#0891b2"]

    fig_r=go.Figure()
    for (name,vals),col in zip(maturity_data.items(),colors_j):
        fig_r.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=dims_j+[dims_j[0]],fill="toself",name=name,
            line=dict(color=col,width=2.5 if "DGT" in name else 1.5),
            fillcolor=f"rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},.08)"))
    fig_r.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],tickvals=[1,2,3,4,5],tickfont=dict(size=8))),
        height=440,margin=dict(t=20,b=30,l=80,r=80),legend=dict(orientation="h",y=-0.08,x=.5,xanchor="center",font=dict(size=10)))
    st.plotly_chart(fig_r,use_container_width=True)

    # Jurisdiction cards
    st.markdown('<div class="sh">🌍 Jurisdiction Profiles</div>',unsafe_allow_html=True)
    cols=st.columns(3)
    for i,(jur_name,jur) in enumerate(JURISDICTIONS.items()):
        with cols[i%3]:
            st.markdown(f"""<div class="jur-card" style="border-top:4px solid {jur['color']};">
                <div style="font-size:28px;text-align:center;">{jur['flag']}</div>
                <div style="text-align:center;font-size:16px;font-weight:700;color:#1e293b;">{jur_name}</div>
                <div style="text-align:center;font-size:11px;color:#64748b;margin-bottom:10px;">{jur['regulator']} · Since {jur['year']}</div>
                <div style="font-size:12px;color:#475569;line-height:1.7;">
                    <div style="display:flex;justify-content:space-between;border-bottom:1px solid #f1f5f9;padding:3px 0;"><span>Scope</span><span style="font-weight:500;text-align:right;max-width:60%;">{jur['scope'][:50]}</span></div>
                    <div style="display:flex;justify-content:space-between;border-bottom:1px solid #f1f5f9;padding:3px 0;"><span>Duration</span><span style="font-weight:500;">{jur['duration']}</span></div>
                    <div style="display:flex;justify-content:space-between;border-bottom:1px solid #f1f5f9;padding:3px 0;"><span>Cohort</span><span style="font-weight:500;">{jur['cohort_size']}</span></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>Maturity</span><span style="font-weight:600;color:{jur['color']};">{'★'*jur['maturity']}{'☆'*(5-jur['maturity'])}</span></div>
                </div>
                <div style="margin-top:8px;padding-top:8px;border-top:1px solid #e2e8f0;font-size:11px;color:#64748b;font-style:italic;">💡 {jur['key_feature']}</div>
            </div>""",unsafe_allow_html=True)

    # Comparison table
    st.markdown('<div class="sh">📋 Side-by-Side Comparison</div>',unsafe_allow_html=True)
    comp_metrics=["Entry Criteria","Consumer/Taxpayer Protection","Duration","Data & Reporting","Exit Mechanism"]
    comp_keys=["entry","consumer_protection","duration","data_reporting","exit"]
    comp_rows=[]
    for metric,key in zip(comp_metrics,comp_keys):
        row={"Metric":metric}
        for jn,jd in JURISDICTIONS.items():
            row[f"{jd['flag']} {jn}"]=jd[key]
        comp_rows.append(row)
    st.dataframe(pd.DataFrame(comp_rows),use_container_width=True,hide_index=True,height=250)

with tab2:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Indonesia Taxation Sandbox — Framework Design</h1><p style="font-size:15px;color:#64748b;margin-top:0;">How benchmarking informed the design of each framework element</p>',unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        The taxation regulatory sandbox was designed to enable <strong>controlled testing of fintech innovations</strong>
        in Indonesia's tax administration — including new API-based tax filing services, blockchain-based invoice verification,
        and AI-powered tax compliance tools. The framework was authored by Yayan Puji Riyanto at DGT's Directorate of ICT
        and <strong>formally adopted as official Ministry of Finance policy</strong>.
    </div>""",unsafe_allow_html=True)

    for elem_name,elem in DESIGN_ELEMENTS.items():
        st.markdown(f'<div class="sh">{elem_name}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="ib">{elem["desc"]}</div>',unsafe_allow_html=True)

        for i,metric in enumerate(elem["metrics"]):
            col_design,col_source,col_decision=st.columns([3,2,2])
            with col_design:
                st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:4px 0;">
                    <div style="font-size:12px;font-weight:600;color:#1e40af;text-transform:uppercase;letter-spacing:.3px;">🇮🇩 Indonesia Tax Sandbox Design — {metric}</div>
                    <div style="font-size:13px;color:#334155;margin-top:4px;">{elem['indonesia_design'][i]}</div>
                </div>""",unsafe_allow_html=True)
            with col_source:
                st.markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:4px 0;">
                    <div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.3px;">📚 Benchmark Source</div>
                    <div style="font-size:13px;color:#475569;margin-top:4px;">{elem['benchmark_source'][i]}</div>
                </div>""",unsafe_allow_html=True)
            with col_decision:
                is_adopted="Adopted" in elem["adopted_or_adapted"][i] and "Adapted" not in elem["adopted_or_adapted"][i]
                cls="adopted" if is_adopted else "adapted"
                icon="✅" if is_adopted else "🔄"
                st.markdown(f'<div class="{cls}">{icon} {elem["adopted_or_adapted"][i]}</div>',unsafe_allow_html=True)

with tab3:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Design Decision Analysis</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Why certain practices were adopted, adapted, or not adopted</p>',unsafe_allow_html=True)

    # Decision breakdown
    all_decisions=[]
    for elem in DESIGN_ELEMENTS.values():
        all_decisions.extend(elem["adopted_or_adapted"])
    adopted=sum(1 for d in all_decisions if "Adopted" in d and "Adapted" not in d and "Not" not in d)
    adapted=sum(1 for d in all_decisions if "Adapted" in d)
    not_adopted=sum(1 for d in all_decisions if "Not adopted" in d)

    d1,d2=st.columns([1,2])
    with d1:
        fig_dec=go.Figure(go.Pie(values=[adopted,adapted,not_adopted],labels=["Adopted","Adapted","Not Adopted"],
            marker_colors=["#22c55e","#eab308","#dc2626"],hole=.5,textinfo="label+value",textposition="outside"))
        fig_dec.update_layout(height=280,margin=dict(t=20,b=20),showlegend=False,title="Design Decisions",title_font_size=14)
        st.plotly_chart(fig_dec,use_container_width=True)
    with d2:
        st.markdown("""<div class="ib">
            <strong>Design Philosophy:</strong> The framework prioritized <strong>adaptation over direct adoption</strong> — recognizing
            that Indonesia's legal system (civil law, ministerial decree-based regulation), tax administration scale (270M+ population,
            516 offices), and market context (emerging fintech ecosystem) required tailoring of international best practices.<br><br>
            <strong>Key adaptations:</strong><br>
            • Escrow deposits instead of PI insurance (underdeveloped insurance market for fintech in Indonesia)<br>
            • Regional pilot option added (Indonesia's geographic diversity requires phased geographic rollout)<br>
            • Tax compliance history as entry criterion (unique to taxation sandbox — not in financial sandboxes)<br>
            • DGT service continuity obligation for failed participants (taxpayers cannot be left without tax filing capability)
        </div>""",unsafe_allow_html=True)

    # Benchmark influence map
    st.markdown('<div class="sh">🌐 Benchmark Influence Map</div>',unsafe_allow_html=True)
    influence={
        "UK (FCA)":["Governance structure","Consumer protection model","Exit/graduation framework","Knowledge sharing protocol"],
        "Singapore (MAS)":["Innovation office integration","Regulatory integration as explicit goal","Sandbox Express concept (streamlined path)"],
        "Australia (ASIC)":["Scale limits (client + exposure caps)","Legislative sandbox concept (automated governance)","Duration standards"],
        "India (RBI/IFSCA)":["Thematic cohort approach (adapted for tax processes)","KPI-driven performance metrics"],
        "Indonesia (OJK)":["Domestic regulatory precedent","Indonesian legal framework alignment","Data localisation requirements"],
    }
    for jur,influences in influence.items():
        flag=JURISDICTIONS[jur]["flag"];color=JURISDICTIONS[jur]["color"]
        items_html="".join(f'<span style="display:inline-block;background:#f1f5f9;padding:3px 10px;border-radius:10px;font-size:12px;color:#475569;margin:2px;">{inf}</span>' for inf in influences)
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:6px 0;border-left:4px solid {color};">
            <div style="font-size:14px;font-weight:600;color:#1e293b;">{flag} {jur}</div>
            <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:4px;">{items_html}</div>
        </div>""",unsafe_allow_html=True)

with tab4:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Relevance to AIIB</h1><p style="font-size:15px;color:#64748b;margin-top:0;">How this experience maps to the Operational Risk Intern responsibilities</p>',unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        This project directly demonstrates the <strong>first responsibility</strong> in the AIIB OR Intern JD:
        <em>"Support Operational Risk framework enhancements activities through research and the benchmarking of peer practice."</em>
        The methodology — research peer practices, analyse applicability, design adapted framework, implement — is identical
        to what the OR Intern would do for AIIB's OR framework.
    </div>""",unsafe_allow_html=True)

    r1,r2,r3=st.columns(3)
    with r1:
        st.markdown("""<div class="aiib-card">
            <div style="font-size:24px;margin-bottom:6px;">🔍</div>
            <h4 style="color:#1e40af;margin-top:0;">Peer Practice Research</h4>
            <p style="font-size:13px;color:#334155;line-height:1.5;">Researched 5 international jurisdictions, analysed 20+ design metrics,
            and synthesized findings into actionable framework recommendations. At AIIB, this maps to benchmarking
            World Bank, ADB, EBRD, and IFC operational risk practices to identify enhancement opportunities.</p>
        </div>""",unsafe_allow_html=True)
    with r2:
        st.markdown("""<div class="aiib-card">
            <div style="font-size:24px;margin-bottom:6px;">📐</div>
            <h4 style="color:#1e40af;margin-top:0;">Framework Design</h4>
            <p style="font-size:13px;color:#334155;line-height:1.5;">Designed a governance framework that balances innovation with internal control
            and compliance safeguards. The framework was formally adopted as Ministry policy. At AIIB, this maps to
            supporting OR framework enhancements — scenario analysis, RCSA, incident management.</p>
        </div>""",unsafe_allow_html=True)
    with r3:
        st.markdown("""<div class="aiib-card">
            <div style="font-size:24px;margin-bottom:6px;">🧪</div>
            <h4 style="color:#1e40af;margin-top:0;">Scenario Analysis Thinking</h4>
            <p style="font-size:13px;color:#334155;line-height:1.5;">A regulatory sandbox is essentially a <strong>controlled risk environment with defined risk parameters</strong> —
            the same mindset behind OR scenario analysis. Designing what-if testing boundaries, escalation triggers,
            and exit criteria is directly transferable to scenario analysis framework development at AIIB.</p>
        </div>""",unsafe_allow_html=True)

    st.markdown('<div class="sh">💡 Transferable Skills</div>',unsafe_allow_html=True)
    skills=[
        ("International Benchmarking Methodology","Systematic comparison of peer practices across jurisdictions using structured frameworks — directly applicable to MDB OR framework benchmarking."),
        ("Regulatory Framework Authorship","Drafted ministerial-level regulatory text with precise legal language — transferable to drafting OR policies, procedures, and reporting templates at AIIB."),
        ("Risk-Based Thinking","Designed risk controls proportional to testing scope (participant eligibility, scale limits, exit protocols) — the foundation of OR risk assessment."),
        ("Policy-to-Implementation Bridge","Translated high-level policy objectives into operational procedures, KPIs, and governance structures — exactly what COR does when implementing OR frameworks."),
    ]
    for title,desc in skills:
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:6px 0;border-left:4px solid #2563eb;">
            <div style="font-size:14px;font-weight:600;color:#1e293b;">{title}</div>
            <div style="font-size:13px;color:#475569;margin-top:4px;">{desc}</div>
        </div>""",unsafe_allow_html=True)

st.divider()
st.markdown("""<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">
    Regulatory Sandbox Benchmarking & Framework Design<br>
    Portfolio by <strong>Yayan Puji Riyanto</strong> · IT Governance & Regulatory Analyst, DGT (2019-2022)<br>
    PhD Candidate, Business Law & Taxation — Monash University<br>
    <em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em>
</div>""",unsafe_allow_html=True)
