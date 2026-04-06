"""
Operational Risk Scenario Analysis Framework — MDB Context
Portfolio Prototype by Yayan Puji Riyanto
PhD Candidate, Business Law and Taxation — Monash University

This tool demonstrates a scenario analysis approach for operational risk
in a multilateral development bank (MDB) context, aligned with Basel II/III
operational risk categories and MDB-specific risk drivers.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─── Page Config ───
st.set_page_config(
    page_title="OR Scenario Analysis — MDB Framework",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Constants ───
BASEL_CATEGORIES = {
    "Internal Fraud": {
        "icon": "🔴",
        "description": "Losses due to acts intended to defraud, misappropriate property, or circumvent regulations or policy by internal parties",
        "color": "#dc2626",
    },
    "External Fraud": {
        "icon": "🟠",
        "description": "Losses due to acts intended to defraud, misappropriate property, or circumvent the law by external parties",
        "color": "#ea580c",
    },
    "Employment Practices": {
        "icon": "🟡",
        "description": "Losses from acts inconsistent with employment, health, or safety laws/agreements",
        "color": "#ca8a04",
    },
    "Clients, Products & Business Practices": {
        "icon": "🔵",
        "description": "Losses from unintentional or negligent failure to meet professional obligations to clients",
        "color": "#2563eb",
    },
    "Damage to Physical Assets": {
        "icon": "🟤",
        "description": "Losses from damage to physical assets from natural disaster or other events",
        "color": "#92400e",
    },
    "Business Disruption & System Failures": {
        "icon": "🟣",
        "description": "Losses from disruption of business or system failures",
        "color": "#7c3aed",
    },
    "Execution, Delivery & Process Management": {
        "icon": "⚪",
        "description": "Losses from failed transaction processing or process management",
        "color": "#6b7280",
    },
}

MDB_SCENARIOS = [
    {
        "name": "Major Vendor Failure in Project Country",
        "category": "Execution, Delivery & Process Management",
        "description": "A critical third-party vendor delivering infrastructure services in a borrowing country becomes insolvent, causing project delays and cost overruns.",
        "likelihood": 3,
        "impact_financial": 4,
        "impact_reputational": 3,
        "impact_operational": 5,
        "existing_controls": [
            "Vendor due diligence at onboarding",
            "Periodic financial health monitoring",
            "Contractual termination clauses",
        ],
        "control_effectiveness": 2,
    },
    {
        "name": "Cyber Incident on Core Banking System",
        "category": "Business Disruption & System Failures",
        "description": "Ransomware attack encrypts critical financial systems, disrupting loan disbursement and reporting for 5+ business days.",
        "likelihood": 2,
        "impact_financial": 5,
        "impact_reputational": 5,
        "impact_operational": 5,
        "existing_controls": [
            "SOC monitoring 24/7",
            "Endpoint detection & response",
            "Offline backup systems",
            "Incident response plan",
        ],
        "control_effectiveness": 3,
    },
    {
        "name": "Regulatory Change in Member Country",
        "category": "Clients, Products & Business Practices",
        "description": "A member country introduces unexpected capital controls or changes foreign investment regulations, affecting active project disbursements.",
        "likelihood": 4,
        "impact_financial": 3,
        "impact_reputational": 2,
        "impact_operational": 4,
        "existing_controls": [
            "Country risk monitoring",
            "Legal & regulatory watch service",
            "Loan covenant flexibility clauses",
        ],
        "control_effectiveness": 2,
    },
    {
        "name": "Staff Misconduct in Procurement",
        "category": "Internal Fraud",
        "description": "An employee manipulates procurement processes to favour a vendor in exchange for personal benefit, leading to financial loss and compliance breach.",
        "likelihood": 2,
        "impact_financial": 3,
        "impact_reputational": 5,
        "impact_operational": 3,
        "existing_controls": [
            "Segregation of duties",
            "Whistleblower hotline",
            "Periodic internal audit",
            "Mandatory conflict of interest declarations",
        ],
        "control_effectiveness": 3,
    },
    {
        "name": "Natural Disaster Affecting Project Site",
        "category": "Damage to Physical Assets",
        "description": "Earthquake or flooding damages an infrastructure project under construction in a borrowing country, requiring significant remediation.",
        "likelihood": 3,
        "impact_financial": 5,
        "impact_reputational": 2,
        "impact_operational": 4,
        "existing_controls": [
            "Environmental & social impact assessments",
            "Insurance requirements in loan covenants",
            "Force majeure clauses",
        ],
        "control_effectiveness": 2,
    },
    {
        "name": "Data Privacy Breach — Employee Records",
        "category": "Employment Practices",
        "description": "Unauthorized access to HR systems exposes personal data of employees across multiple office locations.",
        "likelihood": 2,
        "impact_financial": 2,
        "impact_reputational": 4,
        "impact_operational": 3,
        "existing_controls": [
            "Access control & role-based permissions",
            "Data encryption at rest and in transit",
            "Privacy impact assessments",
        ],
        "control_effectiveness": 3,
    },
    {
        "name": "Third-Party Fraud in Disbursement Channel",
        "category": "External Fraud",
        "description": "External actors exploit weaknesses in a correspondent banking channel to redirect project loan disbursements.",
        "likelihood": 2,
        "impact_financial": 4,
        "impact_reputational": 4,
        "impact_operational": 3,
        "existing_controls": [
            "Multi-factor authentication for payments",
            "Dual-approval for large transactions",
            "Correspondent bank due diligence",
        ],
        "control_effectiveness": 3,
    },
]

LIKELIHOOD_LABELS = {1: "Rare", 2: "Unlikely", 3: "Possible", 4: "Likely", 5: "Almost Certain"}
IMPACT_LABELS = {1: "Negligible", 2: "Minor", 3: "Moderate", 4: "Major", 5: "Severe"}
CONTROL_LABELS = {1: "Ineffective", 2: "Partially Effective", 3: "Effective", 4: "Highly Effective"}


def calc_inherent_risk(likelihood, impact_fin, impact_rep, impact_ops):
    max_impact = max(impact_fin, impact_rep, impact_ops)
    return likelihood * max_impact


def calc_residual_risk(inherent, control_eff):
    reduction = {1: 0.0, 2: 0.25, 3: 0.50, 4: 0.75}
    return max(1, inherent * (1 - reduction.get(control_eff, 0)))


def risk_rating(score):
    if score >= 16:
        return "Critical", "#dc2626"
    elif score >= 10:
        return "High", "#ea580c"
    elif score >= 5:
        return "Medium", "#f59e0b"
    else:
        return "Low", "#22c55e"


# ─── Sidebar ───
with st.sidebar:
    st.markdown("## 🏦 OR Scenario Analysis")
    st.markdown("**MDB Operational Risk Framework**")
    st.divider()

    mode = st.radio(
        "Mode",
        ["📊 Pre-built MDB Scenarios", "✏️ Custom Scenario Builder"],
        index=0,
    )

    st.divider()
    st.markdown(
        """
    **Framework Basis:**
    - Basel II/III OR Categories
    - 5×5 Likelihood × Impact Matrix
    - Control Effectiveness Adjustment
    - Residual Risk Scoring
    
    ---
    *Portfolio by Yayan Puji Riyanto*  
    *PhD Candidate — Monash University*
    """
    )

# ─── Header ───
st.markdown(
    """
# Operational Risk Scenario Analysis Framework
### Prototype for Multilateral Development Bank (MDB) Context

This tool provides a structured approach to **identify, assess, and prioritise operational risk scenarios** 
relevant to an MDB's operations. It applies a Basel II/III risk taxonomy adapted for the unique risk landscape 
of international development finance — including project execution risk, multi-jurisdictional regulatory risk, 
and third-party/vendor risk.
"""
)

st.divider()

# ═══════════════════════════════════════════════════════
# MODE 1: Pre-built Scenarios
# ═══════════════════════════════════════════════════════
if mode == "📊 Pre-built MDB Scenarios":

    # ── Risk Register Table ──
    st.markdown("## Risk Register Overview")

    rows = []
    for s in MDB_SCENARIOS:
        inherent = calc_inherent_risk(
            s["likelihood"],
            s["impact_financial"],
            s["impact_reputational"],
            s["impact_operational"],
        )
        residual = calc_residual_risk(inherent, s["control_effectiveness"])
        rating, color = risk_rating(residual)
        cat_info = BASEL_CATEGORIES[s["category"]]
        rows.append(
            {
                "Scenario": s["name"],
                "Category": f'{cat_info["icon"]} {s["category"]}',
                "Likelihood": f'{s["likelihood"]} — {LIKELIHOOD_LABELS[s["likelihood"]]}',
                "Max Impact": max(
                    s["impact_financial"],
                    s["impact_reputational"],
                    s["impact_operational"],
                ),
                "Inherent Risk": inherent,
                "Controls": s["control_effectiveness"],
                "Residual Risk": round(residual, 1),
                "Rating": rating,
            }
        )

    df_register = pd.DataFrame(rows)

    # Color-coded display
    def color_rating(val):
        colors = {
            "Critical": "background-color: #fecaca; color: #991b1b; font-weight: bold",
            "High": "background-color: #fed7aa; color: #9a3412; font-weight: bold",
            "Medium": "background-color: #fef3c7; color: #92400e; font-weight: bold",
            "Low": "background-color: #d1fae5; color: #065f46; font-weight: bold",
        }
        return colors.get(val, "")

    styled = df_register.style.applymap(color_rating, subset=["Rating"])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=320)

    # ── Risk Heatmap ──
    st.markdown("## Risk Heatmap — Likelihood × Impact")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_heat = go.Figure()

        # Background grid
        for li in range(1, 6):
            for im in range(1, 6):
                score = li * im
                _, bg_color = risk_rating(score)
                fig_heat.add_shape(
                    type="rect",
                    x0=im - 0.5, x1=im + 0.5,
                    y0=li - 0.5, y1=li + 0.5,
                    fillcolor=bg_color,
                    opacity=0.15,
                    line=dict(color="white", width=2),
                    layer="below",
                )

        # Plot scenarios
        for s in MDB_SCENARIOS:
            max_imp = max(
                s["impact_financial"],
                s["impact_reputational"],
                s["impact_operational"],
            )
            residual = calc_residual_risk(
                calc_inherent_risk(
                    s["likelihood"],
                    s["impact_financial"],
                    s["impact_reputational"],
                    s["impact_operational"],
                ),
                s["control_effectiveness"],
            )
            _, color = risk_rating(residual)
            cat_info = BASEL_CATEGORIES[s["category"]]

            # Add jitter to avoid overlap
            jitter_x = np.random.uniform(-0.2, 0.2)
            jitter_y = np.random.uniform(-0.2, 0.2)

            fig_heat.add_trace(
                go.Scatter(
                    x=[max_imp + jitter_x],
                    y=[s["likelihood"] + jitter_y],
                    mode="markers+text",
                    marker=dict(size=18, color=cat_info["color"], line=dict(width=2, color="white")),
                    text=[s["name"][:25]],
                    textposition="top center",
                    textfont=dict(size=9),
                    hovertemplate=(
                        f"<b>{s['name']}</b><br>"
                        f"Category: {s['category']}<br>"
                        f"Likelihood: {LIKELIHOOD_LABELS[s['likelihood']]}<br>"
                        f"Max Impact: {IMPACT_LABELS[max_imp]}<br>"
                        f"Residual Risk: {residual:.0f}<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

        fig_heat.update_layout(
            xaxis=dict(
                title="Impact",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=list(IMPACT_LABELS.values()),
                range=[0.5, 5.5],
            ),
            yaxis=dict(
                title="Likelihood",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=list(LIKELIHOOD_LABELS.values()),
                range=[0.5, 5.5],
            ),
            height=450,
            margin=dict(t=30),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.markdown("### Risk Distribution")
        rating_counts = df_register["Rating"].value_counts()
        fig_pie = px.pie(
            values=rating_counts.values,
            names=rating_counts.index,
            color=rating_counts.index,
            color_discrete_map={
                "Critical": "#dc2626",
                "High": "#ea580c",
                "Medium": "#f59e0b",
                "Low": "#22c55e",
            },
            hole=0.4,
        )
        fig_pie.update_layout(height=250, margin=dict(t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("### By Basel Category")
        cat_counts = pd.DataFrame(rows)["Category"].value_counts()
        for cat, count in cat_counts.items():
            st.markdown(f"**{cat}**: {count} scenario(s)")

    # ── Scenario Deep Dives ──
    st.divider()
    st.markdown("## Scenario Deep Dive")

    selected = st.selectbox(
        "Select scenario for detailed analysis",
        [s["name"] for s in MDB_SCENARIOS],
    )

    scenario = next(s for s in MDB_SCENARIOS if s["name"] == selected)
    inherent = calc_inherent_risk(
        scenario["likelihood"],
        scenario["impact_financial"],
        scenario["impact_reputational"],
        scenario["impact_operational"],
    )
    residual = calc_residual_risk(inherent, scenario["control_effectiveness"])
    rating, rating_color = risk_rating(residual)
    cat_info = BASEL_CATEGORIES[scenario["category"]]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Inherent Risk Score", f"{inherent}")
    c2.metric("Control Effectiveness", CONTROL_LABELS[scenario["control_effectiveness"]])
    c3.metric("Residual Risk Score", f"{residual:.0f}")
    c4.markdown(
        f"<div style='background-color:{rating_color}; color:white; "
        f"padding:14px; border-radius:8px; text-align:center; font-size:20px; font-weight:bold;'>"
        f"{rating}</div>",
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**{cat_info['icon']} Category:** {scenario['category']}")
        st.markdown(f"**Description:** {scenario['description']}")
        st.markdown("**Existing Controls:**")
        for ctrl in scenario["existing_controls"]:
            st.markdown(f"- {ctrl}")

    with col_b:
        # Impact radar
        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=[
                    scenario["impact_financial"],
                    scenario["impact_reputational"],
                    scenario["impact_operational"],
                    scenario["impact_financial"],
                ],
                theta=["Financial", "Reputational", "Operational", "Financial"],
                fill="toself",
                fillcolor=f"rgba({int(rating_color[1:3],16)},{int(rating_color[3:5],16)},{int(rating_color[5:7],16)},0.3)",
                line=dict(color=rating_color, width=2),
                name="Impact Profile",
            )
        )
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickvals=[1, 2, 3, 4, 5])),
            height=300,
            margin=dict(t=30, b=30),
            title="Impact Profile",
        )
        st.plotly_chart(fig_radar, use_container_width=True)


# ═══════════════════════════════════════════════════════
# MODE 2: Custom Scenario Builder
# ═══════════════════════════════════════════════════════
else:
    st.markdown("## Custom Scenario Builder")
    st.markdown(
        "Define your own operational risk scenario and assess it using the framework."
    )

    with st.form("custom_scenario"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Scenario Name", placeholder="e.g., IT system outage during year-end close")
            category = st.selectbox("Basel II Category", list(BASEL_CATEGORIES.keys()))
            description = st.text_area(
                "Scenario Description",
                placeholder="Describe the risk event, its triggers, and potential consequences...",
                height=120,
            )

        with col2:
            likelihood = st.select_slider(
                "Likelihood",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} — {LIKELIHOOD_LABELS[x]}",
                value=3,
            )
            impact_fin = st.select_slider(
                "Financial Impact",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} — {IMPACT_LABELS[x]}",
                value=3,
            )
            impact_rep = st.select_slider(
                "Reputational Impact",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} — {IMPACT_LABELS[x]}",
                value=3,
            )
            impact_ops = st.select_slider(
                "Operational Impact",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} — {IMPACT_LABELS[x]}",
                value=3,
            )
            control_eff = st.select_slider(
                "Control Effectiveness",
                options=[1, 2, 3, 4],
                format_func=lambda x: f"{x} — {CONTROL_LABELS[x]}",
                value=2,
            )

        controls_text = st.text_area(
            "Existing Controls (one per line)",
            placeholder="Segregation of duties\nPeriodic audit\nAutomated monitoring",
            height=100,
        )

        submitted = st.form_submit_button("🔍 Assess Scenario", use_container_width=True)

    if submitted and name:
        inherent = calc_inherent_risk(likelihood, impact_fin, impact_rep, impact_ops)
        residual = calc_residual_risk(inherent, control_eff)
        rating, rating_color = risk_rating(residual)

        st.divider()
        st.markdown(f"## Assessment: {name}")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Inherent Risk", f"{inherent} / 25")
        m2.metric("Control Reduction", f"{(1 - residual / inherent) * 100:.0f}%")
        m3.metric("Residual Risk", f"{residual:.0f} / 25")
        m4.markdown(
            f"<div style='background-color:{rating_color}; color:white; "
            f"padding:14px; border-radius:8px; text-align:center; font-size:20px; font-weight:bold;'>"
            f"{rating}</div>",
            unsafe_allow_html=True,
        )

        ca, cb = st.columns(2)
        with ca:
            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=[impact_fin, impact_rep, impact_ops, impact_fin],
                    theta=["Financial", "Reputational", "Operational", "Financial"],
                    fill="toself",
                    fillcolor=f"rgba({int(rating_color[1:3],16)},{int(rating_color[3:5],16)},{int(rating_color[5:7],16)},0.3)",
                    line=dict(color=rating_color, width=2),
                )
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                height=300,
                margin=dict(t=30, b=30),
                title="Impact Profile",
                showlegend=False,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with cb:
            # Waterfall: inherent → controls → residual
            fig_wf = go.Figure(
                go.Waterfall(
                    x=["Inherent Risk", "Control Mitigation", "Residual Risk"],
                    y=[inherent, -(inherent - residual), 0],
                    measure=["absolute", "relative", "total"],
                    connector=dict(line=dict(color="gray", width=1)),
                    decreasing=dict(marker=dict(color="#22c55e")),
                    increasing=dict(marker=dict(color="#dc2626")),
                    totals=dict(marker=dict(color=rating_color)),
                    text=[f"{inherent}", f"-{inherent - residual:.0f}", f"{residual:.0f}"],
                    textposition="outside",
                )
            )
            fig_wf.update_layout(
                height=300,
                margin=dict(t=30, b=30),
                title="Risk Waterfall",
                yaxis_title="Risk Score",
            )
            st.plotly_chart(fig_wf, use_container_width=True)

        # Recommendations
        st.markdown("### 📋 Recommended Actions")
        if residual >= 16:
            st.error(
                "**CRITICAL:** Immediate escalation to senior management required. "
                "Consider additional controls, risk transfer (insurance), or activity cessation."
            )
        elif residual >= 10:
            st.warning(
                "**HIGH:** Active management required. Strengthen existing controls, "
                "implement additional mitigants, and increase monitoring frequency."
            )
        elif residual >= 5:
            st.info(
                "**MEDIUM:** Monitor through regular RCSA cycle. "
                "Review control effectiveness periodically and maintain risk awareness."
            )
        else:
            st.success(
                "**LOW:** Acceptable risk level. Continue routine monitoring. "
                "Document in risk register for completeness."
            )

# ─── Footer ───
st.divider()
st.markdown(
    """
<div style='text-align: center; color: #9ca3af; font-size: 13px;'>
    Operational Risk Scenario Analysis Framework — MDB Context<br>
    Portfolio Prototype by <b>Yayan Puji Riyanto</b><br>
    PhD Candidate, Business Law & Taxation — Monash University<br>
    MS Business Analytics — University of Colorado Boulder<br><br>
    <em>Built as part of portfolio for AIIB Operational Risk Intern position (Ref. 25238)</em>
</div>
""",
    unsafe_allow_html=True,
)
