"""
PhD Research Brief: Tax Compliance in Crypto-Asset Environments
Executive Summary for Non-Academic Audience
Yayan Puji Riyanto — Monash University
"""
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="PhD Research Brief — Crypto Tax Compliance",page_icon="🎓",layout="wide",initial_sidebar_state="collapsed")
st.markdown("""
<style>
    .block-container{padding-top:2rem;max-width:1100px;}
    .hero{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:white;padding:40px;border-radius:16px;margin-bottom:28px;}
    .hero h1{font-size:28px;font-weight:800;margin:0 0 8px;}.hero p{font-size:15px;color:#94a3b8;margin:0;line-height:1.5;}
    .hero .tag{display:inline-block;background:rgba(255,255,255,.12);padding:4px 12px;border-radius:16px;font-size:12px;color:#cbd5e1;margin:2px;}
    .sh{background:linear-gradient(90deg,#0f172a,#1e3a5f);color:white;padding:12px 20px;border-radius:8px;font-size:17px;font-weight:600;margin:24px 0 14px;}
    .mc{background:linear-gradient(135deg,#f8fafc,#e2e8f0);border-radius:12px;padding:18px;text-align:center;border:1px solid #e2e8f0;}
    .mc h3{font-size:11px;color:#64748b;margin:0 0 4px;text-transform:uppercase;letter-spacing:.5px;}.mc .v{font-size:24px;font-weight:700;color:#1e293b;margin:0;}.mc .s{font-size:11px;color:#94a3b8;margin-top:3px;}
    .ib{background:#f8fafc;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 8px 8px 0;margin:10px 0;font-size:14px;color:#334155;line-height:1.6;}
    .fc{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:22px;height:100%;box-shadow:0 1px 3px rgba(0,0,0,.04);}
    .fc h4{color:#1e293b;margin-top:0;}.fc p{color:#475569;font-size:14px;line-height:1.6;}
    .finding{background:white;border:1px solid #e2e8f0;border-radius:10px;padding:16px 18px;margin:8px 0;border-left:4px solid #2563eb;}
    .pub-card{background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:6px 0;}
    .aiib-card{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #bfdbfe;border-radius:12px;padding:20px;margin:8px 0;}
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}.stDeployButton{display:none;}
</style>
""",unsafe_allow_html=True)

# ═══ HERO ═══
st.markdown("""<div class="hero">
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px;">
        <span style="font-size:40px;">🎓</span>
        <div>
            <h1>Exploring Tax Compliance Behaviour in Crypto-Asset Environments</h1>
            <p>PhD Dissertation — Executive Research Brief for Non-Academic Audience</p>
        </div>
    </div>
    <div style="margin-top:12px;">
        <span class="tag">🏫 Monash University — Faculty of Business & Economics</span>
        <span class="tag">📋 Business Law & Taxation</span>
        <span class="tag">📅 Sep 2022 – Present</span>
        <span class="tag">👤 Yayan Puji Riyanto</span>
        <span class="tag">🔬 Mixed Methods: Experiment + Survey + Interviews</span>
    </div>
</div>""",unsafe_allow_html=True)

c1,c2,c3,c4,c5=st.columns(5)
with c1: st.markdown('<div class="mc"><h3>Methods</h3><p class="v">3</p><p class="s">Experiment, Survey, Interview</p></div>',unsafe_allow_html=True)
with c2: st.markdown('<div class="mc"><h3>Stakeholder Groups</h3><p class="v">3</p><p class="s">Tax authority, Intermediary, Taxpayer</p></div>',unsafe_allow_html=True)
with c3: st.markdown('<div class="mc"><h3>Survey N</h3><p class="v">220</p><p class="s">Respondents</p></div>',unsafe_allow_html=True)
with c4: st.markdown('<div class="mc"><h3>Publications</h3><p class="v">4</p><p class="s">Journal articles (2024-2026)</p></div>',unsafe_allow_html=True)
with c5: st.markdown('<div class="mc"><h3>Country Focus</h3><p class="v">🇮🇩</p><p class="s">Indonesia</p></div>',unsafe_allow_html=True)

# TABS
tab1,tab2,tab3,tab4=st.tabs(["📋 Research Overview","🔬 Methodology & Findings","📚 Publications","🏛️ OR Relevance"])

with tab1:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Research Overview</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Why this research matters and what it contributes</p>',unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        <strong>The Problem:</strong> Crypto-assets represent a rapidly growing digital financial ecosystem that poses
        unprecedented challenges for tax compliance. Globally, tax authorities struggle to enforce compliance in an environment
        characterised by pseudonymity, cross-border transactions, decentralised platforms, and the absence of traditional
        financial intermediaries. Indonesia — the world's 4th most populous country with one of the fastest-growing
        crypto markets in Asia — introduced crypto-asset taxation in 2022 (PMK-68/2022), but compliance remains
        a significant challenge.<br><br>
        <strong>The Gap:</strong> Existing tax compliance research predominantly uses a <strong>dyadic model</strong>
        (tax authority ↔ taxpayer). However, in crypto-asset environments, <strong>intermediaries</strong> (exchanges,
        custodial wallets, DeFi protocols) play a critical role in enabling or hindering compliance — yet they are
        largely absent from compliance theory.<br><br>
        <strong>The Contribution:</strong> This dissertation extends the Slippery Slope Framework (SSF) of tax compliance
        to a <strong>triadic model</strong> incorporating tax authorities, intermediaries, and taxpayers — and introduces
        two new theoretical concepts: <strong>structural compliance</strong> and <strong>risk-primed compliance</strong>.
    </div>""",unsafe_allow_html=True)

    # Theoretical framework visual
    st.markdown('<div class="sh">📐 Theoretical Framework: Triadic Slippery Slope</div>',unsafe_allow_html=True)

    fig_fw=go.Figure()
    # Three nodes
    nodes=[("Tax Authority\n(DGT)",0.5,0.92,55,"#dc2626","Power of authority\nEnforcement capability\nRegulatory design"),
           ("Intermediary\n(Crypto Exchange)",0.12,0.25,50,"#2563eb","Structural compliance enabler\nWithholding agent\nData reporting"),
           ("Taxpayer\n(Crypto Investor)",0.88,0.25,50,"#059669","Voluntary compliance\nEnforced compliance\nRisk perception")]
    for name,x,y,size,color,hover in nodes:
        fig_fw.add_trace(go.Scatter(x=[x],y=[y],mode="markers+text",showlegend=False,
            marker=dict(size=size,color=color,line=dict(width=3,color="white")),
            text=[name],textposition="bottom center",textfont=dict(size=11,color="#1e293b",weight=700 if "NEW" in name else 400),
            hovertemplate=f"<b>{name.replace(chr(10),' ')}</b><br>{hover}<extra></extra>"))

    # Arrows (relationships)
    arrows=[
        (0.5,0.85,0.18,0.32,"#7c3aed","Power & Trust\n(Authority → Intermediary)","NEW: Triadic relationship"),
        (0.5,0.85,0.82,0.32,"#475569","Power & Trust\n(Authority → Taxpayer)","Traditional SSF"),
        (0.22,0.25,0.78,0.25,"#d97706","Structural Compliance\n(Intermediary → Taxpayer)","NEW: Third compliance modality"),
    ]
    for x0,y0,x1,y1,color,label,note in arrows:
        fig_fw.add_annotation(x=x1,y=y1,ax=x0,ay=y0,xref="x",yref="y",axref="x",ayref="y",
            showarrow=True,arrowhead=3,arrowsize=1.5,arrowwidth=2.5,arrowcolor=color,opacity=0.7)
        mx,my=(x0+x1)/2,(y0+y1)/2
        fig_fw.add_annotation(x=mx,y=my,text=f"<b>{label}</b>",showarrow=False,
            font=dict(size=9,color=color),bgcolor="rgba(255,255,255,0.85)",borderpad=3)

    # Labels for new contributions
    fig_fw.add_annotation(x=0.12,y=0.08,text="🆕 NEW in this research:\nIntermediary as 3rd node",
        showarrow=False,font=dict(size=10,color="#2563eb"),align="center",
        bgcolor="#eff6ff",bordercolor="#bfdbfe",borderwidth=1,borderpad=6)
    fig_fw.add_annotation(x=0.88,y=0.08,text="Traditional SSF:\nPower & Trust → Compliance",
        showarrow=False,font=dict(size=10,color="#059669"),align="center",
        bgcolor="#f0fdf4",bordercolor="#bbf7d0",borderwidth=1,borderpad=6)

    fig_fw.update_layout(height=450,margin=dict(t=10,b=10,l=10,r=10),plot_bgcolor="white",
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.05,1.05]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.05,1.05]))
    st.plotly_chart(fig_fw,use_container_width=True)

    # Key concepts
    st.markdown('<div class="sh">💡 Key Theoretical Contributions</div>',unsafe_allow_html=True)
    k1,k2,k3=st.columns(3)
    with k1:
        st.markdown("""<div class="fc" style="border-top:4px solid #7c3aed;">
            <h4 style="color:#7c3aed;">🔺 Triadic SSF Extension</h4>
            <p>Extends the Slippery Slope Framework from a <strong>dyadic</strong> (authority ↔ taxpayer) to a
            <strong>triadic</strong> model by adding the intermediary as a third node. This reflects the reality of
            crypto-asset ecosystems where exchanges and platforms mediate the compliance relationship.</p>
        </div>""",unsafe_allow_html=True)
    with k2:
        st.markdown("""<div class="fc" style="border-top:4px solid #2563eb;">
            <h4 style="color:#2563eb;">🏗️ Structural Compliance</h4>
            <p>A <strong>third compliance modality</strong> beyond voluntary and enforced compliance. Structural compliance
            occurs when the system architecture (e.g., automated tax withholding by exchanges) makes non-compliance
            technically difficult or impossible — compliance "by design" rather than by choice or coercion.</p>
        </div>""",unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="fc" style="border-top:4px solid #d97706;">
            <h4 style="color:#d97706;">⚡ Risk-Primed Compliance</h4>
            <p>Taxpayers' compliance decisions are <strong>primed by their perception of risk</strong> in the crypto
            environment — volatility, regulatory uncertainty, and platform trust all influence whether they comply
            with tax obligations. Risk perception acts as a moderator in the SSF model.</p>
        </div>""",unsafe_allow_html=True)

with tab2:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Methodology & Key Findings</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Mixed-methods research design and principal findings</p>',unsafe_allow_html=True)

    st.markdown('<div class="sh">🔬 Research Design: Three-Study Mixed Methods</div>',unsafe_allow_html=True)

    m1,m2,m3=st.columns(3)
    with m1:
        st.markdown("""<div class="fc" style="text-align:center;border-top:4px solid #dc2626;">
            <div style="font-size:32px;margin-bottom:6px;">🧪</div>
            <h4>Study 1: Experiment</h4>
            <p><strong>Method:</strong> Randomised controlled experiment with factorial design<br><br>
            <strong>Focus:</strong> Testing the causal effects of power (enforcement strength) and trust (institutional trust)
            on crypto-asset tax compliance behaviour<br><br>
            <strong>Participants:</strong> Indonesian taxpayers with crypto-asset holdings<br><br>
            <strong>Analysis:</strong> ANOVA, regression, moderation analysis</p>
        </div>""",unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="fc" style="text-align:center;border-top:4px solid #2563eb;">
            <div style="font-size:32px;margin-bottom:6px;">📊</div>
            <h4>Study 2: Survey (N=220)</h4>
            <p><strong>Method:</strong> Cross-sectional survey with Structural Equation Modeling (SEM/CFA)<br><br>
            <strong>Focus:</strong> Validating the triadic SSF model — measuring relationships between power, trust,
            structural compliance, and compliance behaviour across 3 stakeholder groups<br><br>
            <strong>Analysis:</strong> SEM, CFA, moderation, mediation analysis using semopy</p>
        </div>""",unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="fc" style="text-align:center;border-top:4px solid #059669;">
            <div style="font-size:32px;margin-bottom:6px;">🎙️</div>
            <h4>Study 3: Interviews</h4>
            <p><strong>Method:</strong> Semi-structured interviews with thematic analysis<br><br>
            <strong>Focus:</strong> Understanding lived experiences of compliance decisions in crypto-asset environments —
            tax authority officials, exchange operators, and individual crypto investors<br><br>
            <strong>Analysis:</strong> Thematic analysis, triangulation with quantitative findings</p>
        </div>""",unsafe_allow_html=True)

    st.markdown('<div class="sh">📊 Key Findings</div>',unsafe_allow_html=True)

    findings=[
        ("Institutional trust drives voluntary compliance in crypto","Higher trust in DGT correlates with greater willingness to voluntarily report crypto gains — but trust levels are currently low among crypto investors due to perceived regulatory uncertainty.","Survey (SEM)","#2563eb"),
        ("Enforcement power has diminishing returns in crypto","Unlike traditional tax settings, increasing enforcement power (audit probability, penalties) shows diminishing marginal effects on crypto compliance — partly because enforcement is technically difficult in decentralised environments.","Experiment","#dc2626"),
        ("Structural compliance via intermediaries is the strongest driver","When crypto exchanges automatically withhold tax (as mandated by PMK-68/2022), compliance rates are highest — regardless of taxpayer attitudes. System design matters more than individual motivation.","Survey + Interviews","#059669"),
        ("Risk perception moderates compliance behaviour","Taxpayers who perceive higher risk in the crypto environment (volatility, scams, platform insolvency) are more likely to comply — possibly because they seek regulatory protection as a form of risk mitigation.","Survey (moderation analysis)","#d97706"),
        ("Intermediary trust gap: exchanges vs DeFi","Compliance is significantly higher through centralised exchanges (which can withhold tax) than DeFi protocols (which cannot). This 'intermediary trust gap' is a key challenge for tax authorities globally.","Interviews","#7c3aed"),
    ]
    for title,desc,method,color in findings:
        st.markdown(f"""<div class="finding" style="border-left-color:{color};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:15px;font-weight:600;color:#1e293b;">{title}</div>
                <span style="background:#f1f5f9;padding:3px 10px;border-radius:10px;font-size:11px;color:#64748b;">{method}</span>
            </div>
            <div style="font-size:13px;color:#475569;margin-top:6px;line-height:1.5;">{desc}</div>
        </div>""",unsafe_allow_html=True)

    # Compliance model visual
    st.markdown('<div class="sh">📈 The Three Compliance Modalities</div>',unsafe_allow_html=True)
    fig_cm=go.Figure()
    modalities=["Voluntary\nCompliance","Enforced\nCompliance","Structural\nCompliance\n(NEW)"]
    drivers=["Trust in authority","Power of authority","System architecture"]
    effectiveness=[3.2,2.8,4.5]
    colors_cm=["#059669","#dc2626","#2563eb"]

    fig_cm.add_trace(go.Bar(x=modalities,y=effectiveness,marker_color=colors_cm,
        text=[f"{v}/5" for v in effectiveness],textposition="outside",textfont=dict(size=14,color="#1e293b")))
    for i,(mod,drv) in enumerate(zip(modalities,drivers)):
        fig_cm.add_annotation(x=i,y=0.3,text=f"Driver: {drv}",showarrow=False,font=dict(size=10,color="white"))
    fig_cm.update_layout(height=350,margin=dict(t=30,b=30),plot_bgcolor="white",
        yaxis=dict(title="Effectiveness in Crypto Context (1-5)",range=[0,5.5],gridcolor="#f1f5f9"),
        title="Compliance Modality Effectiveness in Crypto-Asset Environments",title_font_size=14)
    st.plotly_chart(fig_cm,use_container_width=True)

with tab3:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Publications</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Peer-reviewed journal articles from this research</p>',unsafe_allow_html=True)

    pubs=[
        {"title":"Indonesia's Challenges in Crypto-Asset Tax Regulation","venue":"Digital Transformation and Regulatory Laws in South and Southeast Asian Societies, Springer","year":"2026 (forthcoming April)","type":"Book Chapter","status":"In Press"},
        {"title":"The Role of Legal Theory in the Era of Digital Globalization","venue":"Jurnal Pembangunan Hukum Indonesia, Vol. 7(2)","year":"2025","type":"Journal Article","status":"Published"},
        {"title":"How Do (Tax) Researchers Perceive Crypto? A Systematic Literature Review","venue":"Journal of the Australasian Tax Teachers Association, Vol. 19","year":"2024","type":"Journal Article","status":"Published"},
        {"title":"Tax Compliance through Prefilled Forms in a Laboratory Experiment","venue":"Scientax, Vol. 5(2)","year":"2024","type":"Journal Article","status":"Published"},
    ]
    for pub in pubs:
        status_color="#059669" if pub["status"]=="Published" else "#d97706"
        st.markdown(f"""<div class="pub-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="flex:1;">
                    <div style="font-size:15px;font-weight:600;color:#1e293b;">{pub['title']}</div>
                    <div style="font-size:13px;color:#64748b;margin-top:4px;">{pub['venue']}</div>
                </div>
                <div style="text-align:right;min-width:100px;">
                    <span style="background:{status_color};color:white;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600;">{pub['status']}</span>
                    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">{pub['year']} · {pub['type']}</div>
                </div>
            </div>
        </div>""",unsafe_allow_html=True)

    # Related academic projects
    st.markdown('<div class="sh">🔬 Related Analytical Projects</div>',unsafe_allow_html=True)
    projects=[
        ("SEM/CFA Analysis — Slippery Slope Framework","Structural Equation Modeling and Confirmatory Factor Analysis of the triadic SSF model using semopy (Python). Validated construct reliability, discriminant validity, and path coefficients across 3 stakeholder groups.","Python (semopy, pandas, scipy)"),
        ("Slippery Slope Regression & Moderation Analysis","Multiple regression and moderation analysis testing the effects of power, trust, and risk perception on compliance behaviour. Includes interaction effects and robustness checks.","Python, Stata, SPSS"),
        ("Bitcoin Market Correlation with Indonesian Crypto Tax Revenue","Time-series correlation analysis examining the relationship between Bitcoin price movements, crypto trading volumes, and Indonesian crypto tax revenue (PMK-68/2022 collection data).","Python (pandas, statsmodels, matplotlib)"),
        ("Compliance Behaviour Survey Design (N=220)","Full survey design, piloting, distribution, and analysis across tax authority officials, crypto exchange operators, and individual crypto investors in Indonesia.","Qualtrics, SPSS, semopy"),
    ]
    for title,desc,tools in projects:
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:6px 0;border-left:4px solid #7c3aed;">
            <div style="font-size:14px;font-weight:600;color:#1e293b;">{title}</div>
            <div style="font-size:13px;color:#475569;margin-top:4px;">{desc}</div>
            <div style="font-size:11px;color:#94a3b8;margin-top:6px;">🛠️ Tools: {tools}</div>
        </div>""",unsafe_allow_html=True)

with tab4:
    st.markdown('<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Relevance to AIIB Operational Risk</h1><p style="font-size:15px;color:#64748b;margin-top:0;">How PhD research skills map to the OR Intern role</p>',unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        The JD states: <em>"PhD research on compliance in crypto-asset environments involves complex analysis of
        institutional trust, enforcement mechanisms, and risk perception in digital financial ecosystems.
        This requires a high level of critical thinking and attention to detail that the role demands."</em><br><br>
        Beyond the domain knowledge, the <strong>methodological skills</strong> developed through this research
        are directly transferable to operational risk analysis at AIIB.
    </div>""",unsafe_allow_html=True)

    r1,r2=st.columns(2)
    with r1:
        st.markdown('<div style="font-size:16px;font-weight:600;color:#1e293b;margin-bottom:10px;">🔬 Research → OR Skill Mapping</div>',unsafe_allow_html=True)
        mappings=[
            ("Experimental Design","Scenario Analysis","Designing controlled experiments to test causal hypotheses → designing plausible risk scenarios with defined parameters"),
            ("SEM/CFA Statistical Analysis","Risk Data Analytics","Advanced multivariate analysis of complex variable relationships → analysing operational risk patterns and KRI interdependencies"),
            ("Survey Design & Analysis","RCSA Data Collection","Designing instruments to capture compliance behaviour data from stakeholders → designing RCSA questionnaires for risk owners"),
            ("Thematic Interview Analysis","Root Cause Analysis","Extracting themes from qualitative data to explain compliance decisions → extracting root causes from incident investigations"),
            ("Compliance Behaviour Theory","OR Risk Culture","Understanding why people comply (or don't) with rules → understanding why staff follow (or bypass) operational controls"),
        ]
        for research,or_skill,desc in mappings:
            st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:6px 0;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="background:#f5f3ff;color:#6d28d9;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:600;">{research}</span>
                    <span style="color:#94a3b8;">→</span>
                    <span style="background:#eff6ff;color:#1e40af;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:600;">{or_skill}</span>
                </div>
                <div style="font-size:12px;color:#475569;margin-top:6px;">{desc}</div>
            </div>""",unsafe_allow_html=True)

    with r2:
        st.markdown('<div style="font-size:16px;font-weight:600;color:#1e293b;margin-bottom:10px;">🏛️ Domain Relevance to AIIB</div>',unsafe_allow_html=True)

        domains=[
            ("Digital Financial Ecosystems","PhD researches compliance in crypto/digital finance — AIIB increasingly finances digital infrastructure and fintech projects in member countries. Understanding risk in digital ecosystems is directly relevant."),
            ("Institutional Trust & Enforcement","The SSF's core dimensions (power & trust) are the same dimensions that drive OR risk culture at AIIB — how staff and counterparties respond to controls depends on enforcement credibility and institutional trust."),
            ("Regulatory Framework Analysis","PhD includes detailed analysis of Indonesia's crypto tax regulations (PMK-68/2022, PMK-50/2025) — demonstrates ability to analyse and interpret regulatory frameworks, a key COR skill."),
            ("Multi-Stakeholder Compliance","The triadic model (authority-intermediary-taxpayer) mirrors AIIB's multi-stakeholder reality: AIIB (authority), project implementers (intermediary), borrowing country governments (counterparty) — same compliance dynamics."),
        ]
        for title,desc in domains:
            st.markdown(f"""<div class="aiib-card">
                <div style="font-size:14px;font-weight:600;color:#1e40af;">{title}</div>
                <div style="font-size:13px;color:#334155;margin-top:4px;line-height:1.5;">{desc}</div>
            </div>""",unsafe_allow_html=True)

st.divider()
st.markdown("""<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">
    PhD Research Brief: Tax Compliance in Crypto-Asset Environments<br>
    <strong>Yayan Puji Riyanto</strong> · PhD Candidate, Business Law & Taxation — Monash University<br>
    MS Business Analytics — University of Colorado Boulder<br>
    <em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em>
</div>""",unsafe_allow_html=True)
