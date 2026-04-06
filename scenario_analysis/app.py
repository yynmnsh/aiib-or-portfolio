"""
Operational Risk Scenario Analysis Framework — AIIB Context
Portfolio Prototype by Yayan Puji Riyanto
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

st.set_page_config(page_title="OR Scenario Analysis — AIIB COR", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .block-container {padding-top: 3.5rem; max-width: 1200px;}
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0c1e3c 0%, #162d50 100%); }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] strong { color: #f1f5f9 !important; }
    .metric-card { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .metric-card h3 { font-size: 13px; color: #64748b; margin: 0 0 6px 0; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-card .value { font-size: 28px; font-weight: 700; color: #1e293b; margin: 0; }
    .metric-card .sub { font-size: 12px; color: #94a3b8; margin-top: 4px; }
    .section-header { background: linear-gradient(90deg, #0f172a 0%, #1e3a5f 100%); color: white; padding: 12px 20px; border-radius: 8px; font-size: 18px; font-weight: 600; margin: 24px 0 16px 0; }
    .info-box { background: #f8fafc; border-left: 4px solid #3b82f6; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 12px 0; font-size: 14px; color: #334155; line-height: 1.6; }
    .scenario-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    .scenario-title { font-size: 16px; font-weight: 600; color: #1e293b; margin-bottom: 6px; }
    .scenario-cat { font-size: 12px; color: #64748b; margin-bottom: 8px; }
    .scenario-desc { font-size: 13px; color: #475569; line-height: 1.5; }
    .control-item { background: #f1f5f9; padding: 8px 14px; border-radius: 6px; margin: 4px 0; font-size: 13px; color: #334155; border-left: 3px solid #3b82f6; }
    .fw-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    .fw-card h4 { color: #1e293b; margin-top: 0; }
    .fw-card p { color: #475569; font-size: 14px; line-height: 1.6; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

LIKELIHOOD_LABELS = {1: "Rare", 2: "Unlikely", 3: "Possible", 4: "Likely", 5: "Almost Certain"}
LIKELIHOOD_DESC = {1: "< 5% probability; may occur only in exceptional circumstances", 2: "5-20% probability; could occur but not expected", 3: "20-50% probability; might occur at some time", 4: "50-80% probability; will probably occur", 5: "> 80% probability; expected to occur in most circumstances"}
IMPACT_LABELS = {1: "Negligible", 2: "Minor", 3: "Moderate", 4: "Major", 5: "Severe"}
IMPACT_DESC = {1: "< USD 1M loss; no reputational impact; minimal disruption", 2: "USD 1-5M loss; limited media attention; short-term disruption", 3: "USD 5-25M loss; regional media coverage; operational delays", 4: "USD 25-100M loss; international media; significant disruption", 5: "> USD 100M loss; sustained negative coverage; critical failure"}
CONTROL_LABELS = {1: "Ineffective", 2: "Needs Improvement", 3: "Adequate", 4: "Strong", 5: "Robust"}
CONTROL_DESC = {1: "Control does not exist or is fundamentally flawed", 2: "Control exists but has significant gaps", 3: "Control designed appropriately, operates with minor gaps", 4: "Control well-designed, consistently operated and tested", 5: "Best-in-class, automated where possible, continuously monitored"}

BASEL_CATEGORIES = {
    "Internal Fraud": {"icon": "🔴", "color": "#dc2626", "description": "Losses due to acts intended to defraud, misappropriate property, or circumvent regulations by internal parties."},
    "External Fraud": {"icon": "🟠", "color": "#ea580c", "description": "Losses due to acts intended to defraud, misappropriate property, or circumvent the law by third parties."},
    "Employment Practices & Workplace Safety": {"icon": "🟡", "color": "#eab308", "description": "Losses from acts inconsistent with employment, health or safety laws or agreements."},
    "Clients, Products & Business Practices": {"icon": "🔵", "color": "#2563eb", "description": "Losses from unintentional or negligent failure to meet professional obligations to clients."},
    "Damage to Physical Assets": {"icon": "🟤", "color": "#92400e", "description": "Losses from loss or damage to physical assets from natural disaster or other events."},
    "Business Disruption & System Failures": {"icon": "🟣", "color": "#7c3aed", "description": "Losses from disruption of business or system failures."},
    "Execution, Delivery & Process Management": {"icon": "⚪", "color": "#475569", "description": "Losses from failed transaction processing or process management."},
}

# --- INITIALIZE SESSION STATE ---
if "MDB_SCENARIOS" not in st.session_state:
    st.session_state.MDB_SCENARIOS = [
        {"id": "SCN-001", "name": "Sanctions Screening Failure on Co-financed Project", "category": "Clients, Products & Business Practices",
         "description": "A contractor on an AIIB co-financed infrastructure project (with World Bank or ADB) is found on a sanctioned entity list. Screening failure during due diligence exposes AIIB to compliance risk under AML/CFT obligations aligned with FATF recommendations and UNSC resolutions.",
         "trigger": "Inadequate screening of sub-contractors in complex multi-jurisdictional supply chains",
         "affected_areas": ["Project disbursement", "Co-financing partner relationship", "AAA credit rating", "Member country relationship"],
         "likelihood": 2, "impact_financial": 3, "impact_reputational": 5, "impact_operational": 3,
         "existing_controls": ["Automated sanctions screening (OFAC, UN, EU lists)", "Enhanced due diligence for high-risk jurisdictions", "AML/CFT policy aligned with FATF Recommendations", "Integrity due diligence on project counterparties"],
         "control_effectiveness": 3, "kri": "Number of late/missed screenings per quarter", "owner": "COR"},
        {"id": "SCN-002", "name": "Core Treasury System Outage During Bond Settlement", "category": "Business Disruption & System Failures",
         "description": "AIIB's treasury system experiences critical failure during settlement of a Sustainable Development Bond issuance. The outage disrupts payment processing and delays settlement, potentially triggering cross-default provisions and affecting AIIB's AAA rating.",
         "trigger": "System upgrade failure or cyberattack coinciding with bond settlement window",
         "affected_areas": ["Treasury operations", "Bond settlement", "Investor confidence", "Credit rating"],
         "likelihood": 2, "impact_financial": 5, "impact_reputational": 4, "impact_operational": 5,
         "existing_controls": ["Business continuity plan with defined RPO/RTO", "Redundant system architecture", "24/7 SOC monitoring", "Manual fallback procedures for critical payments", "Regular disaster recovery testing"],
         "control_effectiveness": 4, "kri": "System availability % (target: 99.9%); DR test completion rate", "owner": "Treasury / IT"},
        {"id": "SCN-003", "name": "ESF Non-Compliance in Sovereign-Backed Project", "category": "Clients, Products & Business Practices",
         "description": "An infrastructure project violates AIIB's Environmental and Social Framework (ESF) — involuntary resettlement without compensation or undisclosed environmental damage. A formal complaint is filed to AIIB's Project-affected People's Mechanism (PPM).",
         "trigger": "Weak borrower capacity for ESF implementation; inadequate supervision during construction",
         "affected_areas": ["Project implementation", "PPM complaint process", "Civil society reputation", "Paris Agreement alignment"],
         "likelihood": 3, "impact_financial": 3, "impact_reputational": 5, "impact_operational": 4,
         "existing_controls": ["Environmental & Social Impact Assessment at appraisal", "ESF compliance conditions in loan agreements", "Periodic implementation support missions", "Grievance redress mechanism at project level", "PPM as independent accountability mechanism"],
         "control_effectiveness": 3, "kri": "ESF compliance issues per project; PPM complaints received", "owner": "Operations / ESG"},
        {"id": "SCN-004", "name": "Procurement Fraud by Internal Staff", "category": "Internal Fraud",
         "description": "A staff member manipulates procurement for IT consulting, directing contracts to a vendor with undisclosed personal connections. The fraud bypasses segregation of duties and is discovered through internal audit.",
         "trigger": "Collusion between staff and vendor; override of procurement thresholds",
         "affected_areas": ["Financial loss", "Institutional integrity", "Staff trust", "Internal audit findings"],
         "likelihood": 2, "impact_financial": 2, "impact_reputational": 4, "impact_operational": 3,
         "existing_controls": ["Segregation of duties in procurement", "Mandatory annual conflict of interest declarations", "Procurement review committee for contracts above threshold", "Whistleblower / ethics hotline", "Internal audit coverage of procurement"],
         "control_effectiveness": 4, "kri": "Procurement policy exceptions per quarter; whistleblower reports", "owner": "Internal Audit / COR"},
        {"id": "SCN-005", "name": "Regulatory Change Blocking Sovereign Loan Disbursement", "category": "Execution, Delivery & Process Management",
         "description": "A borrowing member country introduces unexpected capital controls or FX restrictions preventing AIIB from disbursing an approved sovereign loan tranche. Delays affect project implementation and pipeline management.",
         "trigger": "Political instability or economic crisis leading to emergency FX controls in member country",
         "affected_areas": ["Loan disbursement", "Project timeline", "Borrower relationship", "Portfolio management"],
         "likelihood": 3, "impact_financial": 4, "impact_reputational": 2, "impact_operational": 4,
         "existing_controls": ["Country risk monitoring and sovereign rating review", "Legal & regulatory watch via external counsel", "Flexible disbursement mechanisms in loan agreements", "Escalation to Risk Committee for country limit breaches"],
         "control_effectiveness": 3, "kri": "Country risk rating changes; disbursement delay days", "owner": "Risk Mgmt / Inv. Ops"},
        {"id": "SCN-006", "name": "Earthquake Damages Active Infrastructure Project", "category": "Damage to Physical Assets",
         "description": "A major earthquake (7+) in Central/South Asia severely damages an AIIB-financed road/bridge project during construction. Requires significant remediation, cost overruns, and project restructuring.",
         "trigger": "Seismic event in earthquake-prone project region (e.g., Turkiye, Indonesia, Philippines, Pakistan)",
         "affected_areas": ["Project physical assets", "Contractor safety", "Budget overruns", "Community impact"],
         "likelihood": 2, "impact_financial": 5, "impact_reputational": 2, "impact_operational": 4,
         "existing_controls": ["Seismic risk assessment in project appraisal", "Insurance requirements in loan covenants", "Force majeure clauses", "Emergency response procedures", "Climate & disaster resilience standards in design"],
         "control_effectiveness": 3, "kri": "Natural catastrophe events in active project countries", "owner": "Investment Operations"},
        {"id": "SCN-007", "name": "Data Breach Exposing Member Country Financial Data", "category": "Business Disruption & System Failures",
         "description": "A phishing attack on AIIB staff exposes sensitive member country data — undisbursed loan details, sovereign credit assessments, and draft country strategy documents. Breach affects AIIB's trusted relationship with member governments.",
         "trigger": "Sophisticated spear-phishing targeting staff with access to member country data",
         "affected_areas": ["Member country trust", "Data confidentiality", "Institutional reputation", "IT security posture"],
         "likelihood": 3, "impact_financial": 2, "impact_reputational": 5, "impact_operational": 3,
         "existing_controls": ["Multi-factor authentication for all systems", "Data classification and access controls", "Regular phishing simulation and security awareness", "Endpoint detection and response (EDR)", "Incident response plan with communication protocols"],
         "control_effectiveness": 3, "kri": "Phishing test failure rate; security incident count", "owner": "IT / COR"},
        {"id": "SCN-008", "name": "Staff Discrimination Grievance", "category": "Employment Practices & Workplace Safety",
         "description": "Multiple staff from the same regional office file grievances alleging systematic discrimination in evaluations and promotions. Given AIIB's 111-member diversity commitment, the claim risks internal morale impact and external media attention.",
         "trigger": "Perceived bias in promotion cycle; lack of diversity metrics transparency",
         "affected_areas": ["Staff morale", "Talent retention", "Institutional values", "External reputation"],
         "likelihood": 3, "impact_financial": 1, "impact_reputational": 4, "impact_operational": 3,
         "existing_controls": ["Code of Conduct and ethics policies", "Independent grievance mechanism", "Diversity & inclusion initiatives", "Regular staff engagement surveys"],
         "control_effectiveness": 3, "kri": "Staff grievance count; diversity metrics by grade", "owner": "HR / Ethics"},
        {"id": "SCN-009", "name": "Mis-booking of USD 50M Loan Disbursement", "category": "Execution, Delivery & Process Management",
         "description": "A USD 50M sovereign loan disbursement is mistakenly processed to the wrong beneficiary account due to manual data entry error. Detected 3 days later during reconciliation.",
         "trigger": "Manual entry error during concurrent processing of multiple large disbursements",
         "affected_areas": ["Funds recovery", "Borrower relationship", "Operational efficiency", "Audit findings"],
         "likelihood": 2, "impact_financial": 3, "impact_reputational": 3, "impact_operational": 4,
         "existing_controls": ["Four-eyes principle (maker-checker) for disbursements", "Automated validation of beneficiary details", "Daily reconciliation of disbursement accounts", "Pre-populated disbursement instruction templates"],
         "control_effectiveness": 4, "kri": "Payment processing error rate; reconciliation exceptions", "owner": "Controller / Treasury"},
    ]

if "audit_trail" not in st.session_state:
    st.session_state.audit_trail = []

if "ai_draft" not in st.session_state:
    st.session_state.ai_draft = None

def calc_inherent_risk(l, fi, re, op): return l * max(fi, re, op)
def calc_residual_risk(inh, ce):
    red = {1: 0.0, 2: 0.15, 3: 0.35, 4: 0.55, 5: 0.75}
    return max(1, round(inh * (1 - red.get(ce, 0)), 1))
def risk_rating(s):
    if s >= 16: return "Critical", "#dc2626", "risk-critical"
    if s >= 10: return "High", "#ea580c", "risk-high"
    if s >= 5:  return "Medium", "#eab308", "risk-medium"
    return "Low", "#22c55e", "risk-low"
def render_metric(label, value, sub=""):
    st.markdown(f'<div class="metric-card"><h3>{label}</h3><p class="value">{value}</p><p class="sub">{sub}</p></div>', unsafe_allow_html=True)

# Precompute for Dashboard
all_rows, all_residuals, all_ratings = [], [], []
for s in st.session_state.MDB_SCENARIOS:
    inh = calc_inherent_risk(s["likelihood"], s["impact_financial"], s["impact_reputational"], s["impact_operational"])
    res = calc_residual_risk(inh, s["control_effectiveness"])
    rat, col, css = risk_rating(res)
    all_residuals.append(res); all_ratings.append(rat)
    
    l_label = f"{s['likelihood']} - {LIKELIHOOD_LABELS[s['likelihood']]}"
    i_val = max(s["impact_financial"], s["impact_reputational"], s["impact_operational"])
    i_label = f"{i_val} - {IMPACT_LABELS[i_val]}"
    c_label = f"{s['control_effectiveness']} - {CONTROL_LABELS[s['control_effectiveness']]}"
    
    all_rows.append({
        "ID": s["id"], 
        "Scenario": s["name"],
        "Category": f'{BASEL_CATEGORIES[s["category"]]["icon"]} {s["category"]}',
        "L_Label": l_label, 
        "I_Label": i_label,
        "Inherent": inh, 
        "Ctrl_Label": c_label, 
        "Residual": res, 
        "Rating": rat, 
        "_col": col
    })

crit_count = all_ratings.count("Critical"); high_count = all_ratings.count("High")

# SIDEBAR
with st.sidebar:
    st.markdown(f"""<div style='text-align:center;padding:10px 0 20px 0;'>
        <div style='font-size:36px;margin-bottom:4px;'>🏛️</div>
        <div style='font-size:18px;font-weight:700;color:#f1f5f9!important;'>OR Scenario Analysis</div>
        <div style='font-size:12px;color:#94a3b8!important;margin-top:4px;'>Compliance & Operational Risk</div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"""<div style='padding:8px 0;'>
        <div style='font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Dashboard Summary</div>
        <div style='display:flex;justify-content:space-between;margin:6px 0;'><span>Total Scenarios</span><span style='font-weight:600;color:#f1f5f9!important;'>{len(st.session_state.MDB_SCENARIOS)}</span></div>
        <div style='display:flex;justify-content:space-between;margin:6px 0;'><span>🔴 Critical</span><span style='font-weight:600;color:#fca5a5!important;'>{crit_count}</span></div>
        <div style='display:flex;justify-content:space-between;margin:6px 0;'><span>🟠 High</span><span style='font-weight:600;color:#fdba74!important;'>{high_count}</span></div>
        <div style='display:flex;justify-content:space-between;margin:6px 0;'><span>🟡 Medium</span><span style='font-weight:600;color:#fde047!important;'>{all_ratings.count("Medium")}</span></div>
        <div style='display:flex;justify-content:space-between;margin:6px 0;'><span>🟢 Low</span><span style='font-weight:600;color:#86efac!important;'>{all_ratings.count("Low")}</span></div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    
    df_export = pd.DataFrame(all_rows).drop(columns=["_col"])
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Export Register to CSV", data=csv_data, file_name="risk_register.csv", mime="text/csv", use_container_width=True)
    
    st.divider()
    st.markdown("""<div style='font-size:11px;color:#64748b;line-height:1.6;'>
        <strong style='color:#94a3b8!important;'>Context</strong><br>
        Prototype OR scenario analysis framework for AIIB's COR function — 2nd line of defense within Risk Management Dept.<br><br>
        <strong style='color:#94a3b8!important;'>Portfolio by</strong><br>Yayan Puji Riyanto<br>PhD Candidate — Monash University<br>MS Business Analytics — CU Boulder
    </div>""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Scenario Dashboard", "🔍 Deep Dive", "✏️ Custom Assessment", "📈 Simulation & Stress Test", "📖 Framework", "📝 Audit Trail"])

with tab1:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Operational Risk Scenario Analysis</h1><p style="font-size:15px;color:#64748b;margin-top:0;">AIIB Compliance & Operational Risk — Scenario Register & Risk Heatmap</p>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: render_metric("Total Scenarios", len(st.session_state.MDB_SCENARIOS), "Active in register")
    with c2: render_metric("Avg Residual Risk", f"{np.mean(all_residuals):.1f}" if all_residuals else "0", "Out of 25")
    
    highest_res = max(all_residuals) if all_residuals else 0
    highest_name = all_rows[[r["Residual"] for r in all_rows].index(highest_res)]["Scenario"][:30] if all_residuals else ""
    with c3: render_metric("Highest Residual", f"{highest_res:.0f}", highest_name)
    with c4: render_metric("Critical + High", f"{crit_count+high_count}", f"Out of {len(st.session_state.MDB_SCENARIOS)} scenarios")

    st.markdown('<div class="section-header">📋 Risk Register</div>', unsafe_allow_html=True)
    df_reg = pd.DataFrame(all_rows)[["ID","Scenario","Category","L_Label","I_Label","Inherent","Ctrl_Label","Residual","Rating"]]
    
    def sr(v):
        m={"Critical":"background-color:#fef2f2;color:#991b1b;font-weight:600","High":"background-color:#fff7ed;color:#9a3412;font-weight:600","Medium":"background-color:#fefce8;color:#854d0e;font-weight:600","Low":"background-color:#f0fdf4;color:#166534;font-weight:600"}
        return m.get(v,"")
    def sres(v):
        if v>=16: return "background-color:#fef2f2;color:#991b1b;font-weight:600"
        if v>=10: return "background-color:#fff7ed;color:#9a3412;font-weight:600"
        if v>=5: return "background-color:#fefce8;color:#854d0e"
        return "background-color:#f0fdf4;color:#166534"

    edited_df = st.data_editor(
        df_reg.style.map(sr,subset=["Rating"]).map(sres,subset=["Residual"]), 
        use_container_width=True, hide_index=True, height=380,
        column_config={
            "ID": st.column_config.TextColumn("ID", disabled=True),
            "Scenario": st.column_config.TextColumn("Scenario"),
            "Category": st.column_config.TextColumn("Category", disabled=True),
            "L_Label": st.column_config.SelectboxColumn("Likelihood", options=[f"{k} - {v}" for k,v in LIKELIHOOD_LABELS.items()], required=True),
            "I_Label": st.column_config.SelectboxColumn("Max Impact", options=[f"{k} - {v}" for k,v in IMPACT_LABELS.items()], required=True),
            "Ctrl_Label": st.column_config.SelectboxColumn("Controls", options=[f"{k} - {v}" for k,v in CONTROL_LABELS.items()], required=True),
            "Inherent": st.column_config.NumberColumn("Inherent", disabled=True),
            "Residual": st.column_config.NumberColumn("Residual", disabled=True),
            "Rating": st.column_config.TextColumn("Rating", disabled=True)
        }
    )

    changes_made = False
    for i in range(len(df_reg)):
        old_row = df_reg.iloc[i]
        new_row = edited_df.iloc[i]
        
        if (old_row['L_Label'] != new_row['L_Label'] or 
            old_row['I_Label'] != new_row['I_Label'] or 
            old_row['Ctrl_Label'] != new_row['Ctrl_Label'] or
            old_row['Scenario'] != new_row['Scenario']):
            
            changes_made = True
            new_l = int(new_row['L_Label'].split(" - ")[0])
            new_i = int(new_row['I_Label'].split(" - ")[0])
            new_ctrl = int(new_row['Ctrl_Label'].split(" - ")[0])
            
            st.session_state.MDB_SCENARIOS[i]['name'] = new_row['Scenario']
            st.session_state.MDB_SCENARIOS[i]['likelihood'] = new_l
            st.session_state.MDB_SCENARIOS[i]['impact_financial'] = new_i
            st.session_state.MDB_SCENARIOS[i]['impact_reputational'] = new_i
            st.session_state.MDB_SCENARIOS[i]['impact_operational'] = new_i
            st.session_state.MDB_SCENARIOS[i]['control_effectiveness'] = new_ctrl
            
            st.session_state.audit_trail.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ID": old_row['ID'],
                "Scenario Changed": old_row['Scenario'],
                "Old State": f"L:{old_row['L_Label'][0]}, I:{old_row['I_Label'][0]}, Ctrl:{old_row['Ctrl_Label'][0]}",
                "New State": f"L:{new_l}, I:{new_i}, Ctrl:{new_ctrl}"
            })

    if changes_made:
        st.rerun()

    st.markdown('<div class="section-header">🗺️ Risk Heatmap — Likelihood × Impact</div>', unsafe_allow_html=True)
    ch, cd = st.columns([5,3])
    with ch:
        fig=go.Figure()
        for li in range(1,6):
            for im in range(1,6):
                _,bg,_=risk_rating(li*im)
                fig.add_shape(type="rect",x0=im-.5,x1=im+.5,y0=li-.5,y1=li+.5,fillcolor=bg,opacity=.12,line=dict(color="white",width=2),layer="below")
                fig.add_annotation(x=im,y=li,text=str(li*im),showarrow=False,font=dict(size=10,color="rgba(0,0,0,0.15)"))
        np.random.seed(42)
        for s in st.session_state.MDB_SCENARIOS:
            mi=max(s["impact_financial"],s["impact_reputational"],s["impact_operational"])
            cat=BASEL_CATEGORIES[s["category"]]
            jx,jy=np.random.uniform(-.25,.25),np.random.uniform(-.25,.25)
            inh=calc_inherent_risk(s["likelihood"],s["impact_financial"],s["impact_reputational"],s["impact_operational"])
            res=calc_residual_risk(inh,s["control_effectiveness"])
            fig.add_trace(go.Scatter(x=[mi+jx],y=[s["likelihood"]+jy],mode="markers+text",showlegend=False,
                marker=dict(size=22,color=cat["color"],line=dict(width=2.5,color="white"),opacity=.9),
                text=[s["id"].replace("SCN-","")],textposition="middle center",textfont=dict(size=8,color="white"),
                hovertemplate=f"<b>{s['id']}: {s['name']}</b><br>Category: {s['category']}<br>Likelihood: {LIKELIHOOD_LABELS[s['likelihood']]}<br>Max Impact: {IMPACT_LABELS[mi]}<br>Inherent: {inh} → Residual: {res}<extra></extra>"))
        fig.update_layout(xaxis=dict(title="<b>Impact</b>",tickvals=[1,2,3,4,5],ticktext=list(IMPACT_LABELS.values()),range=[.3,5.7]),
            yaxis=dict(title="<b>Likelihood</b>",tickvals=[1,2,3,4,5],ticktext=list(LIKELIHOOD_LABELS.values()),range=[.3,5.7]),
            height=420,margin=dict(t=20,b=40,l=40,r=20),plot_bgcolor="white",font=dict(size=11))
        st.plotly_chart(fig,use_container_width=True)
    with cd:
        cat_data={}
        for s in st.session_state.MDB_SCENARIOS: cat_data[s["category"]]=cat_data.get(s["category"],0)+1
        fig_c=go.Figure(go.Bar(y=list(cat_data.keys()),x=list(cat_data.values()),orientation="h",
            marker_color=[BASEL_CATEGORIES[c]["color"] for c in cat_data.keys()],text=list(cat_data.values()),textposition="auto"))
        fig_c.update_layout(title="Scenarios by Category",title_font_size=14,height=200,margin=dict(t=35,b=10,l=10,r=10),
            xaxis=dict(showgrid=False,showticklabels=False),yaxis=dict(tickfont=dict(size=10)),plot_bgcolor="white")
        st.plotly_chart(fig_c,use_container_width=True)
        
        ro=["Critical","High","Medium","Low"];rc={"Critical":"#dc2626","High":"#ea580c","Medium":"#eab308","Low":"#22c55e"}
        rv=[all_ratings.count(r) for r in ro if all_ratings.count(r)>0];rn=[r for r in ro if all_ratings.count(r)>0]
        fig_d=go.Figure(go.Pie(values=rv,labels=rn,marker_colors=[rc[r] for r in rn],hole=.55,textinfo="label+value",textposition="outside",textfont=dict(size=11)))
        fig_d.update_layout(title="Residual Risk Distribution",title_font_size=14,height=200,margin=dict(t=35,b=10,l=10,r=10),showlegend=False)
        st.plotly_chart(fig_d,use_container_width=True)

with tab2:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Scenario Deep Dive</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Select a scenario for full assessment, controls, and impact analysis</p>', unsafe_allow_html=True)
    sel=st.selectbox("Select Scenario",[f"{s['id']} — {s['name']}" for s in st.session_state.MDB_SCENARIOS],label_visibility="collapsed")
    s=next(sc for sc in st.session_state.MDB_SCENARIOS if sel.startswith(sc["id"]))
    inh=calc_inherent_risk(s["likelihood"],s["impact_financial"],s["impact_reputational"],s["impact_operational"])
    res=calc_residual_risk(inh,s["control_effectiveness"]);rat,rcol,rcss=risk_rating(res);cat=BASEL_CATEGORIES[s["category"]]
    red_pct=(1-res/inh)*100
    m1,m2,m3,m4,m5=st.columns(5)
    with m1: render_metric("Inherent Risk",f"{inh}","Before controls")
    with m2: render_metric("Control Eff.",CONTROL_LABELS[s["control_effectiveness"]],f"Score: {s['control_effectiveness']}/5")
    with m3: render_metric("Reduction",f"{red_pct:.0f}%","By controls")
    with m4: render_metric("Residual Risk",f"{res:.0f}","After controls")
    with m5: st.markdown(f'<div class="metric-card" style="background:{rcol};border:none;"><h3 style="color:rgba(255,255,255,.8);">Rating</h3><p class="value" style="color:white;">{rat}</p><p class="sub" style="color:rgba(255,255,255,.7);">{s["id"]}</p></div>',unsafe_allow_html=True)
    st.markdown("",unsafe_allow_html=True)
    dl,dr=st.columns([3,2])
    with dl:
        tags=''.join(f'<span style="background:#f1f5f9;padding:4px 10px;border-radius:12px;font-size:12px;color:#475569;">{a}</span>' for a in s["affected_areas"])
        st.markdown(f'''<div class="scenario-card">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;"><span style="font-size:24px;">{cat["icon"]}</span><div><div class="scenario-title">{s["name"]}</div><div class="scenario-cat">{s["category"]} · Owner: {s["owner"]}</div></div></div>
            <div class="scenario-desc">{s["description"]}</div>
            <div style="margin-top:12px;padding-top:12px;border-top:1px solid #e2e8f0;"><div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">Trigger</div><div style="font-size:13px;color:#475569;margin-top:4px;">{s["trigger"]}</div></div>
            <div style="margin-top:12px;padding-top:12px;border-top:1px solid #e2e8f0;"><div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">Key Risk Indicator</div><div style="font-size:13px;color:#475569;margin-top:4px;">📏 {s["kri"]}</div></div>
            <div style="margin-top:12px;padding-top:12px;border-top:1px solid #e2e8f0;"><div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">Affected Areas</div><div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:6px;">{tags}</div></div>
        </div>''',unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#1e293b;margin:16px 0 8px;">Existing Controls <span style="font-size:12px;font-weight:400;color:#64748b;margin-left:8px;">Effectiveness: {CONTROL_LABELS[s["control_effectiveness"]]} ({s["control_effectiveness"]}/5)</span></div>',unsafe_allow_html=True)
        for ctrl in s["existing_controls"]: st.markdown(f'<div class="control-item">✓ {ctrl}</div>',unsafe_allow_html=True)
    with dr:
        fig_r=go.Figure(go.Scatterpolar(r=[s["impact_financial"],s["impact_reputational"],s["impact_operational"],s["impact_financial"]],
            theta=["Financial","Reputational","Operational","Financial"],fill="toself",
            fillcolor=f"rgba({int(rcol[1:3],16)},{int(rcol[3:5],16)},{int(rcol[5:7],16)},.2)",line=dict(color=rcol,width=2.5)))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],tickvals=[1,2,3,4,5],tickfont=dict(size=9),gridcolor="#e2e8f0"),
            angularaxis=dict(tickfont=dict(size=12,color="#334155"))),height=280,margin=dict(t=40,b=30,l=50,r=50),title=dict(text="Impact Profile",font=dict(size=14)),showlegend=False,paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r,use_container_width=True)
        fig_w=go.Figure(go.Waterfall(x=["Inherent<br>Risk","Control<br>Mitigation","Residual<br>Risk"],y=[inh,-(inh-res),0],measure=["absolute","relative","total"],
            connector=dict(line=dict(color="#cbd5e1",width=1,dash="dot")),decreasing=dict(marker=dict(color="#22c55e",line=dict(color="#16a34a",width=1))),
            totals=dict(marker=dict(color=rcol,line=dict(color=rcol,width=1))),text=[f"{inh}",f"-{inh-res:.0f}",f"{res:.0f}"],textposition="outside",textfont=dict(size=13,color="#334155")))
        fig_w.update_layout(height=250,margin=dict(t=40,b=30,l=30,r=30),title=dict(text="Risk Waterfall",font=dict(size=14)),yaxis_title="Score",plot_bgcolor="white",yaxis=dict(gridcolor="#f1f5f9"))
        st.plotly_chart(fig_w,use_container_width=True)
    if res>=16: st.error("**CRITICAL** — Escalate to CRO and Risk Committee. Consider additional controls, risk transfer, or activity restriction.")
    elif res>=10: st.warning("**HIGH** — Strengthen controls, increase monitoring. Include in quarterly COR report to Risk Committee.")
    elif res>=5: st.info("**MEDIUM** — Monitor through regular RCSA cycle. Review control effectiveness annually.")
    else: st.success("**LOW** — Acceptable risk. Maintain in register, routine monitoring.")

with tab3:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Custom Scenario Assessment</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Define and assess a new operational risk scenario manually or generate via AI.</p>', unsafe_allow_html=True)
    
    # AI GENERATOR BUTTON
    c_btn1, c_btn2 = st.columns([1, 4])
    with c_btn1:
        if st.button("🤖 Auto-Generate AI Scenario"):
            ai_ideas = [
                {"n": "Geopolitical Sanctions on Key Tech Vendor", "c": "Business Disruption & System Failures", "d": "Sudden international sanctions prohibit the use of a core IT vendor's hardware/software, requiring an immediate rip-and-replace of core banking architecture.", "t": "Geopolitical conflict escalation in critical vendor's origin country", "ctrl": "Vendor diversification\nMulti-cloud strategy\nIT resilience planning", "l": 2, "i": 5, "ce": 3},
                {"n": "Generative AI Code Vulnerability Exploitation", "c": "External Fraud", "d": "Cyber attackers exploit hidden vulnerabilities in code generated by internal AI co-pilots, accessing sensitive treasury transaction data.", "t": "Deployment of unvetted AI-generated code to production", "ctrl": "Automated SAST/DAST pipeline\nAI security guidelines\nManual code reviews", "l": 3, "i": 4, "ce": 2},
                {"n": "ESG Greenwashing Allegation by International Media", "c": "Clients, Products & Business Practices", "d": "A major investigative report accuses AIIB of greenwashing a flagship renewable energy project, alleging hidden environmental destruction and human rights abuses.", "t": "Whistleblower leak or deep-dive NGO investigation", "ctrl": "Strict ESF enforcement\nIndependent ESG audits\nTransparent reporting mechanisms", "l": 2, "i": 4, "ce": 4}
            ]
            st.session_state.ai_draft = random.choice(ai_ideas)
            
    if st.session_state.ai_draft:
        st.success(f"Draft populated with an AI-generated scenario idea regarding: **{st.session_state.ai_draft['n']}**")
    
    with st.form("custom"):
        draft = st.session_state.ai_draft or {"n":"", "c":list(BASEL_CATEGORIES.keys())[0], "d":"", "t":"", "ctrl":"", "l":3, "i":3, "ce":3}
        f1,f2=st.columns([3,2])
        with f1:
            cn=st.text_input("Scenario Name", value=draft['n'], placeholder="e.g., IT vendor lock-in for core banking migration")
            cat_index = list(BASEL_CATEGORIES.keys()).index(draft['c']) if draft['c'] in BASEL_CATEGORIES else 0
            cc=st.selectbox("Basel II/III Category", list(BASEL_CATEGORIES.keys()), index=cat_index)
            cd=st.text_area("Description", value=draft['d'], placeholder="Describe the risk event, triggers, consequences...", height=100)
            ct=st.text_input("Trigger Event", value=draft['t'], placeholder="What causes this scenario?")
            cctrl=st.text_area("Existing Controls (one per line)", value=draft['ctrl'], height=80)
        with f2:
            st.markdown("##### Likelihood & Impact")
            cl=st.select_slider("Likelihood",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {LIKELIHOOD_LABELS[x]}",value=draft['l'])
            st.caption(LIKELIHOOD_DESC[cl])
            cif=st.select_slider("Financial Impact",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {IMPACT_LABELS[x]}",value=draft['i'])
            cir=st.select_slider("Reputational Impact",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {IMPACT_LABELS[x]}",value=draft['i'])
            cio=st.select_slider("Operational Impact",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {IMPACT_LABELS[x]}",value=draft['i'])
            st.markdown("##### Control Assessment")
            cce=st.select_slider("Control Effectiveness",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {CONTROL_LABELS[x]}",value=draft['ce'])
            st.caption(CONTROL_DESC[cce])
        sub=st.form_submit_button("🔍 Assess Scenario",use_container_width=True,type="primary")
        
    if sub and cn:
        ci=calc_inherent_risk(cl,cif,cir,cio);cr2=calc_residual_risk(ci,cce);crat,ccol,_=risk_rating(cr2);cred=(1-cr2/ci)*100
        st.divider();st.markdown(f"### Assessment: {cn}")
        r1,r2,r3,r4=st.columns(4)
        with r1: render_metric("Inherent",f"{ci}/25","")
        with r2: render_metric("Reduction",f"{cred:.0f}%","")
        with r3: render_metric("Residual",f"{cr2:.0f}/25","")
        with r4: st.markdown(f'<div class="metric-card" style="background:{ccol};border:none;"><h3 style="color:rgba(255,255,255,.8);">Rating</h3><p class="value" style="color:white;">{crat}</p></div>',unsafe_allow_html=True)
        cx1,cx2=st.columns(2)
        with cx1:
            fr=go.Figure(go.Scatterpolar(r=[cif,cir,cio,cif],theta=["Financial","Reputational","Operational","Financial"],fill="toself",
                fillcolor=f"rgba({int(ccol[1:3],16)},{int(ccol[3:5],16)},{int(ccol[5:7],16)},.2)",line=dict(color=ccol,width=2.5)))
            fr.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5])),height=280,margin=dict(t=30,b=30),showlegend=False,title="Impact Profile")
            st.plotly_chart(fr,use_container_width=True)
        with cx2:
            fw=go.Figure(go.Waterfall(x=["Inherent","Controls","Residual"],y=[ci,-(ci-cr2),0],measure=["absolute","relative","total"],
                connector=dict(line=dict(color="#cbd5e1",dash="dot")),decreasing=dict(marker=dict(color="#22c55e")),totals=dict(marker=dict(color=ccol)),
                text=[str(ci),f"-{ci-cr2:.0f}",f"{cr2:.0f}"],textposition="outside"))
            fw.update_layout(height=280,margin=dict(t=30,b=30),title="Risk Waterfall",plot_bgcolor="white")
            st.plotly_chart(fw,use_container_width=True)
            
        st.session_state.ai_draft = None # Reset draft after submission

with tab4:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Simulation & Stress Testing</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Macro vulnerability and Value at Risk (VaR) estimations based on portfolio scenario data</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📈 Scenario Portfolio Stress Testing</div>', unsafe_allow_html=True)
    st.markdown("Simulate the effect of a severe macro event (e.g., global pandemic, massive geopolitical shift) that simultaneously escalates Likelihood or Impact across all scenarios.")
    
    col_st1, col_st2 = st.columns([1, 2])
    with col_st1:
        stress_l = st.slider("Macro Likelihood Shift", 0, 2, 0, help="Increases the likelihood of all events occurring.")
        stress_i = st.slider("Macro Impact Shift", 0, 2, 0, help="Increases the financial/operational severity of all events.")
        
        # Calculate stressed residual average
        stressed_residuals = []
        for s in st.session_state.MDB_SCENARIOS:
            st_l = min(5, s["likelihood"] + stress_l)
            st_i_f = min(5, s["impact_financial"] + stress_i)
            st_i_r = min(5, s["impact_reputational"] + stress_i)
            st_i_o = min(5, s["impact_operational"] + stress_i)
            
            st_inh = calc_inherent_risk(st_l, st_i_f, st_i_r, st_i_o)
            st_res = calc_residual_risk(st_inh, s["control_effectiveness"])
            stressed_residuals.append(st_res)
            
        st_avg_res = np.mean(stressed_residuals)
        st_crit = sum([1 for r in stressed_residuals if r >= 16])
        st.metric("Stressed Average Residual Risk", f"{st_avg_res:.1f}", f"{(st_avg_res - np.mean(all_residuals)):.1f} shift")
        st.metric("Critical Scenarios under Stress", st_crit, f"{st_crit - crit_count} new criticals", delta_color="inverse")

    with col_st2:
        # Plotly comparison
        fig_stress = go.Figure()
        fig_stress.add_trace(go.Box(y=all_residuals, name="Base Portfolio", marker_color="#3b82f6"))
        fig_stress.add_trace(go.Box(y=stressed_residuals, name="Stressed Portfolio", marker_color="#ef4444"))
        fig_stress.update_layout(title="Residual Risk Distribution Shift", height=300, margin=dict(t=30, b=20, l=40, r=20), plot_bgcolor="white", yaxis=dict(title="Residual Risk Score (0-25)", range=[0, 26]))
        st.plotly_chart(fig_stress, use_container_width=True)

    st.markdown('<div class="section-header">🧠 Monte Carlo Loss Simulation (10,000 Iterations)</div>', unsafe_allow_html=True)
    st.markdown("Runs 10,000 probabilistic simulations mapping Likelihood (1-5) to actual probabilities and Impact (1-5) to monetary USD losses to estimate the 95% Operational Value at Risk (VaR).")
    
    if st.button("▶️ Run Monte Carlo Simulation", type="primary"):
        with st.spinner("Running 10,000 iterations..."):
            # Probabilities derived from LIKELIHOOD_DESC
            prob_map = {1: 0.025, 2: 0.125, 3: 0.35, 4: 0.65, 5: 0.90}
            # Mean loss derived from IMPACT_DESC (in Millions USD)
            impact_map = {1: 0.5, 2: 3.0, 3: 15.0, 4: 60.0, 5: 200.0}
            
            n_iterations = 10000
            total_losses = np.zeros(n_iterations)
            np.random.seed(42)
            
            for s in st.session_state.MDB_SCENARIOS:
                # Apply stress factors for the simulation
                sl = min(5, s["likelihood"] + stress_l)
                si = min(5, max(s["impact_financial"], s["impact_reputational"], s["impact_operational"]) + stress_i)
                
                p_occur = prob_map.get(sl, 0.0)
                mean_loss = impact_map.get(si, 0.0)
                
                # Simulate occurrences (Binomial)
                occurrences = np.random.binomial(1, p_occur, n_iterations)
                # Simulate severity (Lognormal approximation)
                sigma = 0.5 # Assumed volatility
                mu = np.log(mean_loss) - (sigma**2 / 2) 
                severity = np.random.lognormal(mean=mu, sigma=sigma, size=n_iterations)
                
                # Combine frequency and severity
                scenario_loss = occurrences * severity
                
                # Apply control effectiveness reduction
                reduction_map = {1: 0.0, 2: 0.15, 3: 0.35, 4: 0.55, 5: 0.75}
                ctrl_reduction = 1 - reduction_map.get(s["control_effectiveness"], 0)
                scenario_loss = scenario_loss * ctrl_reduction
                
                total_losses += scenario_loss
            
            var_95 = np.percentile(total_losses, 95)
            median_loss = np.median(total_losses)
            
            fig_mc = px.histogram(total_losses, nbins=100, title="Simulated Annual Loss Distribution (M USD)",
                                  labels={'value': 'Total Estimated Loss (Million USD)', 'count': 'Frequency'})
            fig_mc.add_vline(x=var_95, line_dash="dash", line_color="red", annotation_text=f" 95% VaR: ${var_95:.1f}M", annotation_position="top right")
            fig_mc.add_vline(x=median_loss, line_dash="dot", line_color="blue", annotation_text=f" Median: ${median_loss:.1f}M", annotation_position="top right")
            fig_mc.update_layout(showlegend=False, plot_bgcolor="white", height=400)
            
            mc1, mc2 = st.columns([1, 3])
            with mc1:
                st.metric("Median Expected Loss", f"${median_loss:.1f}M")
                st.metric("95% OpRisk VaR", f"${var_95:.1f}M", help="In 95% of simulated years, losses will not exceed this amount.")
                st.caption("Note: Controls mitigate final estimated loss distributions.")
            with mc2:
                st.plotly_chart(fig_mc, use_container_width=True)

with tab5:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Framework & Methodology</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Theoretical basis, AIIB context, and assessment methodology</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🏛️ AIIB Compliance & Operational Risk Context</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
        <strong>The Compliance & Operational Risk (COR)</strong> unit is a <strong>second line of defense</strong> function
        within AIIB's Risk Management Department. COR is responsible for governance, oversight, and credible challenge
        of compliance and operational risk exposures across the Bank. The Head of COR reports to the Chief Risk Officer (CRO)
        and has access to the Risk Committee and the Audit & Risk Committee of the Board of Directors.<br><br>
        COR's mandate covers: <strong>AML/CFT and CPF compliance</strong> (aligned with FATF Recommendations and UNSC Resolutions),
        <strong>operational risk framework management</strong> (identification, assessment, monitoring, and reporting),
        <strong>risk culture promotion</strong> through training, and <strong>crisis management coordination</strong>.
        In 2023, AIIB joined the OECD Global Forum on Tax Transparency as an Observer.<br><br>
        AIIB's Risk Management Framework uses <strong>Key Risk Indicators (KRIs)</strong> and <strong>Key Performance Indicators (KPIs)</strong>
        classified at three levels — Board, President, and CRO — in accordance with materiality. The Board evaluates Risk Appetite at least annually.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">🛡️ Three Lines of Defense Model</div>', unsafe_allow_html=True)
    l1,l2,l3=st.columns(3)
    with l1: st.markdown("""<div class="fw-card"><h4>1st Line — Business Units</h4><p>Investment Operations, Treasury, Corporate Services. Staff hold <strong>frontline responsibility</strong> for identifying, assessing, managing, and reporting risk exposures, having regard to AIIB's Risk Appetite and policies.</p></div>""",unsafe_allow_html=True)
    with l2: st.markdown("""<div class="fw-card" style="border-color:#3b82f6;border-width:2px;"><h4 style="color:#2563eb;">2nd Line — Risk Management (incl. COR) ← <em>This function</em></h4><p>Independently oversees risk-taking activities. <strong>COR</strong> manages compliance risk (AML/CFT, sanctions) and operational risk (scenario analysis, RCSA, incident management). Reports to CRO with access to Risk Committee.</p></div>""",unsafe_allow_html=True)
    with l3: st.markdown("""<div class="fw-card"><h4>3rd Line — Internal Audit</h4><p>Provides <strong>independent assurance</strong> to the Board on effectiveness of governance, risk management, and internal controls. Audit & Risk Committee reviews findings and oversees remediation.</p></div>""",unsafe_allow_html=True)

    st.markdown('<div class="section-header">📐 Scenario Analysis Methodology</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
        Scenario analysis is a <strong>forward-looking</strong> risk assessment technique identifying plausible but severe
        operational risk events. Unlike historical loss data analysis (backward-looking), scenario analysis anticipates risks
        that <strong>have not yet occurred</strong> but could materially impact the Bank. This is particularly important for
        AIIB as a relatively young institution (operational since 2016) with limited internal loss history.
    </div>""", unsafe_allow_html=True)

    p1,p2,p3,p4=st.columns(4)
    with p1: st.markdown('<div class="fw-card" style="text-align:center;"><div style="font-size:32px;margin-bottom:8px;">1️⃣</div><h4>Identify</h4><p>Identify plausible scenarios across Basel II/III categories, informed by AIIB operations, peer MDB experiences, and industry loss data.</p></div>',unsafe_allow_html=True)
    with p2: st.markdown('<div class="fw-card" style="text-align:center;"><div style="font-size:32px;margin-bottom:8px;">2️⃣</div><h4>Assess</h4><p>Score each scenario on <strong>Likelihood</strong> (1-5) and <strong>Impact</strong> across financial, reputational, and operational dimensions (1-5).</p></div>',unsafe_allow_html=True)
    with p3: st.markdown('<div class="fw-card" style="text-align:center;"><div style="font-size:32px;margin-bottom:8px;">3️⃣</div><h4>Control</h4><p>Evaluate existing controls for effectiveness (1-5). Calculate <strong>residual risk</strong> by applying control mitigation to inherent risk.</p></div>',unsafe_allow_html=True)
    with p4: st.markdown('<div class="fw-card" style="text-align:center;"><div style="font-size:32px;margin-bottom:8px;">4️⃣</div><h4>Act & Monitor</h4><p>Define <strong>KRIs</strong> for monitoring. Escalate Critical/High risks. Report to Risk Committee quarterly. Review annually.</p></div>',unsafe_allow_html=True)

    st.markdown("#### Scoring Reference Tables")
    r1,r2=st.columns(2)
    with r1:
        st.markdown("**Likelihood Scale**")
        st.dataframe(pd.DataFrame([{"Score":k,"Label":v,"Description":LIKELIHOOD_DESC[k]} for k,v in LIKELIHOOD_LABELS.items()]),use_container_width=True,hide_index=True,height=220)
    with r2:
        st.markdown("**Impact Scale**")
        st.dataframe(pd.DataFrame([{"Score":k,"Label":v,"Description":IMPACT_DESC[k]} for k,v in IMPACT_LABELS.items()]),use_container_width=True,hide_index=True,height=220)
    st.markdown("**Control Effectiveness Scale**")
    st.dataframe(pd.DataFrame([{"Score":k,"Label":v,"Description":CONTROL_DESC[k]} for k,v in CONTROL_LABELS.items()]),use_container_width=True,hide_index=True,height=230)

    st.markdown("#### Risk Rating Matrix (Likelihood × Max Impact)")
    md=[];
    for li in range(5,0,-1):
        row={"Likelihood":f"{li} — {LIKELIHOOD_LABELS[li]}"}
        for im in range(1,6):
            sc=li*im;ra,_,_=risk_rating(sc);row[f"{im} — {IMPACT_LABELS[im]}"]=f"{sc} ({ra})"
        md.append(row)
    dfm=pd.DataFrame(md);ic=[c for c in dfm.columns if c!="Likelihood"]
    def cm(v):
        if "Critical" in str(v): return "background-color:#fef2f2;color:#991b1b;font-weight:600"
        if "High" in str(v): return "background-color:#fff7ed;color:#9a3412;font-weight:600"
        if "Medium" in str(v): return "background-color:#fefce8;color:#854d0e"
        if "Low" in str(v): return "background-color:#f0fdf4;color:#166534"
        return ""
    st.dataframe(dfm.style.map(cm,subset=ic),use_container_width=True,hide_index=True)

    st.markdown('<div class="section-header">📚 Basel II/III Operational Risk Categories</div>', unsafe_allow_html=True)
    for cn,ci in BASEL_CATEGORIES.items():
        st.markdown(f'<div style="display:flex;align-items:flex-start;gap:12px;margin:8px 0;padding:12px 16px;background:white;border-radius:8px;border:1px solid #e2e8f0;"><span style="font-size:20px;">{ci["icon"]}</span><div><div style="font-size:14px;font-weight:600;color:#1e293b;">{cn}</div><div style="font-size:13px;color:#64748b;margin-top:2px;">{ci["description"]}</div></div></div>',unsafe_allow_html=True)

    st.markdown('<div class="section-header">📎 References & Sources</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
        <strong>AIIB Documents:</strong><br>
        • AIIB Risk Management Framework (December 2025 revision)<br>
        • AIIB Compliance & Operational Risk — Overview (aiib.org)<br>
        • AIIB Annual Reports 2022-2024<br>
        • AIIB Environmental and Social Framework<br>
        • AIIB Climate Action Plan 2024-2030<br><br>
        <strong>Industry Standards:</strong><br>
        • Basel Committee — Principles for the Sound Management of Operational Risk (BCBS 195)<br>
        • COSO Internal Control — Integrated Framework (2013)<br>
        • FATF Recommendations on AML/CFT/CPF<br>
        • ISO 31000:2018 — Risk Management<br><br>
        <strong>Peer MDB Frameworks:</strong><br>
        • World Bank Group — Operational Risk Management Framework<br>
        • ADB — Risk Management Policy<br>
        • EBRD — Operational Risk Framework
    </div>""", unsafe_allow_html=True)

with tab6:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Audit Trail</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Track data modifications in the Risk Register</p>', unsafe_allow_html=True)
    if st.session_state.audit_trail:
        df_audit = pd.DataFrame(st.session_state.audit_trail)
        st.dataframe(df_audit.sort_values(by="Timestamp", ascending=False), use_container_width=True, hide_index=True)
        
        csv_audit = df_audit.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Audit Trail (CSV)", data=csv_audit, file_name="audit_trail_log.csv", mime="text/csv")
    else:
        st.info("No data changes recorded yet. Try modifying the Likelihood, Impact, or Control values in the 'Scenario Dashboard' table to see the logs generated here.")

st.divider()
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">OR Scenario Analysis Framework — AIIB COR Context<br>Portfolio by <strong>Yayan Puji Riyanto</strong> · PhD, Business Law & Taxation — Monash University · MS Business Analytics — CU Boulder<br><em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em></div>', unsafe_allow_html=True)
