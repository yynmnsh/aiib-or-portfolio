"""
Risk & Control Self-Assessment (RCSA) Dashboard
Digital Tax Services — 4-Channel API Platform
Portfolio by Yayan Puji Riyanto
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
from datetime import datetime

st.set_page_config(page_title="RCSA Dashboard — Digital Tax Services", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .block-container { padding-top: 3.5rem; max-width: 1200px; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0a1628 0%, #14294d 100%); }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] strong { color: #f1f5f9 !important; }
    .mc { background: linear-gradient(135deg,#f8fafc,#e2e8f0); border-radius:12px; padding:18px; text-align:center; border:1px solid #e2e8f0; box-shadow:0 1px 3px rgba(0,0,0,.06); }
    .mc h3 { font-size:12px; color:#64748b; margin:0 0 5px; text-transform:uppercase; letter-spacing:.5px; }
    .mc .v { font-size:26px; font-weight:700; color:#1e293b; margin:0; }
    .mc .s { font-size:11px; color:#94a3b8; margin-top:3px; }
    .sh { background:linear-gradient(90deg,#0f172a,#1e3a5f); color:white; padding:12px 20px; border-radius:8px; font-size:17px; font-weight:600; margin:22px 0 14px; }
    .ib { background:#f8fafc; border-left:4px solid #3b82f6; padding:14px 18px; border-radius:0 8px 8px 0; margin:10px 0; font-size:14px; color:#334155; line-height:1.6; }
    .fc { background:white; border:1px solid #e2e8f0; border-radius:12px; padding:22px; height:100%; box-shadow:0 1px 3px rgba(0,0,0,.04); }
    .fc h4 { color:#1e293b; margin-top:0; } .fc p { color:#475569; font-size:14px; line-height:1.6; }
    .ch-card { background:white; border:1px solid #e2e8f0; border-radius:12px; padding:18px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,.04); }
    .ch-icon { font-size:32px; margin-bottom:6px; }
    .ch-name { font-size:15px; font-weight:600; color:#1e293b; }
    .ch-sub { font-size:12px; color:#64748b; margin-top:2px; }
    .ctrl-p { background:#f0fdf4; border-left:3px solid #22c55e; padding:7px 12px; border-radius:0 6px 6px 0; margin:3px 0; font-size:13px; color:#166534; }
    .ctrl-d { background:#fefce8; border-left:3px solid #eab308; padding:7px 12px; border-radius:0 6px 6px 0; margin:3px 0; font-size:13px; color:#854d0e; }
    .ctrl-c { background:#fef2f2; border-left:3px solid #ef4444; padding:7px 12px; border-radius:0 6px 6px 0; margin:3px 0; font-size:13px; color:#991b1b; }
    .gap-tag { display:inline-block; background:#fef2f2; color:#991b1b; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:500; margin:2px; border:1px solid #fecaca; }
    .action-item { background:#eff6ff; border-left:3px solid #3b82f6; padding:8px 14px; border-radius:0 6px 6px 0; margin:4px 0; font-size:13px; color:#1e40af; }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;} .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

CHANNELS = {
    "e-Registration": {"icon": "📝", "desc": "Taxpayer registration & NPWP issuance via API", "color": "#2563eb", "api_endpoints": 4, "daily_volume": "~12,000 req/day"},
    "e-Billing": {"icon": "💳", "desc": "Tax payment code generation & billing via API", "color": "#059669", "api_endpoints": 6, "daily_volume": "~45,000 req/day"},
    "e-Filing": {"icon": "📄", "desc": "Tax return submission & processing via API", "color": "#d97706", "api_endpoints": 8, "daily_volume": "~85,000 req/day"},
    "e-Invoice": {"icon": "🧾", "desc": "Electronic tax invoice creation & validation via API", "color": "#7c3aed", "api_endpoints": 5, "daily_volume": "~120,000 req/day"},
}

L_LABELS = {1:"Rare",2:"Unlikely",3:"Possible",4:"Likely",5:"Almost Certain"}
I_LABELS = {1:"Negligible",2:"Minor",3:"Moderate",4:"Major",5:"Severe"}
EFF_LABELS = {1:"Ineffective",2:"Weak",3:"Adequate",4:"Strong",5:"Robust"}
L_DESC = {1:"< 5% probability",2:"5-20% probability",3:"20-50% probability",4:"50-80% probability",5:"> 80% probability"}
I_DESC = {1:"< IDR 1B loss; minimal disruption",2:"IDR 1-10B; short-term disruption",3:"IDR 10-50B; operational delays",4:"IDR 50-200B; significant disruption",5:"> IDR 200B; critical system failure"}
EFF_DESC = {1:"Control does not exist or fundamentally flawed",2:"Exists but significant gaps",3:"Designed appropriately, minor gaps",4:"Well-designed, consistently operated",5:"Best-in-class, automated, continuously monitored"}

INIT_RCSA = [
    {"id":"R-001","channel":"e-Registration","process":"Identity Verification","risk_event":"Fraudulent taxpayer registration using stolen identity documents",
     "risk_category":"External Fraud","likelihood":3,"impact":4,
     "controls":[("Preventive","NIK validation against Dukcapil (national ID database)"),("Preventive","Biometric verification for high-risk registrations"),("Detective","Post-registration audit sampling (5% of new registrations)")],
     "ctrl_effectiveness":3,"gaps":["No real-time biometric check for API channel","Dukcapil API latency causes timeout — fallback to manual check"],"status":"Open",
     "actions":[("Implement real-time biometric verification for API registrations","Q3 2022","IT / Registration"),("Increase post-registration audit sampling to 10%","Q2 2022","Internal Audit")]},
    {"id":"R-002","channel":"e-Registration","process":"NPWP Issuance","risk_event":"Duplicate NPWP issuance due to race condition in concurrent API requests",
     "risk_category":"Process Failure","likelihood":2,"impact":3,
     "controls":[("Preventive","Database unique constraint on NIK-NPWP mapping"),("Detective","Daily batch reconciliation of new NPWPs against master registry")],
     "ctrl_effectiveness":4,"gaps":["Race condition window of ~200ms during peak load"],"status":"Mitigated",
     "actions":[("Implement distributed lock mechanism for NPWP generation","Q2 2022","IT")]},
    {"id":"R-003","channel":"e-Registration","process":"API Authentication","risk_event":"Unauthorized access to registration API by non-certified tax service providers",
     "risk_category":"Unauthorized Access","likelihood":2,"impact":4,
     "controls":[("Preventive","OAuth 2.0 token-based authentication"),("Preventive","IP whitelisting for certified providers"),("Detective","API access logging and anomaly detection")],
     "ctrl_effectiveness":4,"gaps":["Token refresh interval too long (24h) — stolen token exposure window"],"status":"Mitigated",
     "actions":[("Reduce OAuth token TTL from 24h to 1h","Q1 2022","IT Security")]},
    {"id":"B-001","channel":"e-Billing","process":"Payment Code Generation","risk_event":"Incorrect tax payment codes (Kode Billing) due to MAP/KJS mapping error",
     "risk_category":"Process Failure","likelihood":3,"impact":4,
     "controls":[("Preventive","Lookup table validation against 400+ MAP/KJS codes"),("Detective","Real-time validation against taxpayer profile"),("Corrective","Billing code cancellation and reissuance workflow")],
     "ctrl_effectiveness":3,"gaps":["MAP/KJS lookup table update lag (manual, quarterly)","No automated cross-check between billing code and SPT data"],"status":"Open",
     "actions":[("Automate MAP/KJS reference table synchronization","Q2 2022","IT"),("Implement SPT-billing cross-validation","Q3 2022","Business Process")]},
    {"id":"B-002","channel":"e-Billing","process":"Payment Reconciliation","risk_event":"Failed reconciliation between e-Billing and MPN (State Revenue Module) causing unmatched payments",
     "risk_category":"Process Failure","likelihood":3,"impact":5,
     "controls":[("Detective","T+1 automated reconciliation between e-Billing and MPN"),("Detective","Weekly exception report reviewed by Reconciliation Unit"),("Corrective","Manual matching procedure for unreconciled items")],
     "ctrl_effectiveness":2,"gaps":["Reconciliation runs T+1 not real-time — 24h exposure","Manual matching backlog averaging 15 business days","No automated escalation for items >IDR 1B"],"status":"Open",
     "actions":[("Implement real-time or T+0 reconciliation with MPN","Q4 2022","IT / Treasury"),("Automate escalation for items >IDR 1B within 3 days","Q2 2022","Reconciliation"),("Clear backlog and set 5-day SLA","Q2 2022","Operations")]},
    {"id":"B-003","channel":"e-Billing","process":"Payment Channel Integration","risk_event":"Payment channel partner (bank) outage causing billing code rejection at point of payment",
     "risk_category":"System Failure","likelihood":4,"impact":3,
     "controls":[("Preventive","Multi-bank payment channel redundancy (3 state-owned banks)"),("Detective","Real-time uptime monitoring for all channels"),("Corrective","Fallback to alternative channel within 15 minutes")],
     "ctrl_effectiveness":4,"gaps":["Taxpayer not auto-redirected to alternative channel"],"status":"Mitigated",
     "actions":[("Implement automatic failover routing","Q3 2022","IT / Banking Partners")]},
    {"id":"F-001","channel":"e-Filing","process":"Tax Return Submission","risk_event":"Data loss or corruption during peak filing season (March) due to API overload",
     "risk_category":"System Failure","likelihood":4,"impact":5,
     "controls":[("Preventive","Horizontal auto-scaling infrastructure"),("Preventive","Rate limiting per API consumer (1000 req/min)"),("Detective","Real-time throughput and error rate monitoring"),("Corrective","Queue-based retry mechanism for failed submissions")],
     "ctrl_effectiveness":3,"gaps":["Auto-scaling lag 3-5 min during sudden spikes","Queue retry does not guarantee FIFO ordering","No dedicated capacity for large enterprise filers"],"status":"Open",
     "actions":[("Implement predictive auto-scaling from historical patterns","Q1 2022","IT Infra"),("Add priority queue tier for enterprise filers","Q2 2022","IT / Policy")]},
    {"id":"F-002","channel":"e-Filing","process":"Data Validation","risk_event":"Acceptance of tax returns with material calculation errors due to insufficient server-side validation",
     "risk_category":"Process Failure","likelihood":3,"impact":4,
     "controls":[("Preventive","72 server-side validation rules for SPT calculations"),("Preventive","Cross-reference against prior year filing data"),("Detective","Post-submission statistical anomaly detection (quarterly)")],
     "ctrl_effectiveness":3,"gaps":["Validation rules not updated for 2022 HPP amendments","No real-time validation feedback to API consumers","Anomaly detection quarterly, not continuous"],"status":"Open",
     "actions":[("Update rules for HPP Tax Harmonization Law","Q1 2022","Tax Policy / IT"),("Implement synchronous validation in API response","Q2 2022","IT"),("Move anomaly detection to monthly","Q2 2022","Compliance")]},
    {"id":"F-003","channel":"e-Filing","process":"Digital Signature","risk_event":"Digital certificate compromise enabling fraudulent tax return submission",
     "risk_category":"External Fraud","likelihood":2,"impact":5,
     "controls":[("Preventive","PKI-based digital certificate from certified CA"),("Preventive","Certificate pinning in API"),("Detective","CRL check at submission time")],
     "ctrl_effectiveness":4,"gaps":["CRL not OCSP-based — revocation propagation delay up to 24h"],"status":"Mitigated",
     "actions":[("Migrate from CRL to OCSP for real-time status","Q3 2022","IT Security")]},
    {"id":"I-001","channel":"e-Invoice","process":"Invoice Number Generation","risk_event":"NSFP (tax invoice serial number) exhaustion preventing new invoice issuance",
     "risk_category":"Process Failure","likelihood":3,"impact":4,
     "controls":[("Preventive","Automated NSFP allocation in blocks of 1000"),("Detective","Utilization monitoring with 80% threshold alert"),("Corrective","Emergency allocation procedure (24h turnaround)")],
     "ctrl_effectiveness":3,"gaps":["80% alert gives insufficient lead time for high-volume issuers","Emergency allocation requires manual approval — no auto-replenishment"],"status":"Open",
     "actions":[("Lower alert to 60% + predictive exhaustion modeling","Q2 2022","IT"),("Auto-replenishment for pre-approved taxpayers","Q3 2022","Policy / IT")]},
    {"id":"I-002","channel":"e-Invoice","process":"Invoice Validation","risk_event":"Acceptance of invoices with mismatched NPWP enabling fictitious tax invoices (faktur pajak fiktif)",
     "risk_category":"External Fraud","likelihood":3,"impact":5,
     "controls":[("Preventive","Real-time NPWP validation for buyer and seller"),("Preventive","PKP status verification at invoice creation"),("Detective","ML-based anomaly detection for invoice patterns"),("Detective","Purchase-sales invoice cross-matching (quarterly)")],
     "ctrl_effectiveness":3,"gaps":["ML false positive rate at 12%","Cross-matching quarterly — 3-month exposure","No velocity check for unusual volume spikes"],"status":"Open",
     "actions":[("Retrain ML to reduce false positives to <5%","Q2 2022","Data Analytics"),("Move cross-matching to monthly","Q2 2022","Compliance"),("Implement real-time velocity checks (>50 invoices/hr)","Q3 2022","IT / Compliance")]},
    {"id":"I-003","channel":"e-Invoice","process":"API Rate Management","risk_event":"DoS on e-Invoice API during VAT reporting deadline causing widespread business disruption",
     "risk_category":"System Failure","likelihood":3,"impact":5,
     "controls":[("Preventive","API rate limiting (500 req/min per consumer)"),("Preventive","CDN and DDoS protection layer"),("Detective","Real-time traffic anomaly detection"),("Corrective","Emergency capacity burst (2x) activation")],
     "ctrl_effectiveness":3,"gaps":["500 req/min insufficient for large ERP integrators","No priority lane for critical sectors (FMCG, manufacturing)"],"status":"Open",
     "actions":[("Tiered rate limits by taxpayer classification","Q2 2022","IT / Policy"),("Priority API lane for critical sectors","Q3 2022","IT / Policy")]},
]

def calc_inh(l,i): return l*i
def calc_res(inh,ce):
    r={1:0.0,2:.15,3:.35,4:.55,5:.75}
    return max(1,round(inh*(1-r.get(ce,0)),1))
def rr(s):
    if s>=16: return "Critical","#dc2626"
    if s>=10: return "High","#ea580c"
    if s>=5: return "Medium","#eab308"
    return "Low","#22c55e"
def mc_render(l,v,s=""):
    st.markdown(f'<div class="mc"><h3>{l}</h3><p class="v">{v}</p><p class="s">{s}</p></div>',unsafe_allow_html=True)

# --- SESSION STATE ---
if "RCSA" not in st.session_state:
    st.session_state.RCSA = [dict(r) for r in INIT_RCSA]
if "rcsa_audit" not in st.session_state:
    st.session_state.rcsa_audit = []

# Precompute
for r in st.session_state.RCSA:
    r["_inh"]=calc_inh(r["likelihood"],r["impact"])
    r["_res"]=calc_res(r["_inh"],r["ctrl_effectiveness"])
    r["_rat"],r["_col"]=rr(r["_res"])
    r["_gap_count"]=len(r["gaps"])

DATA = st.session_state.RCSA
total=len(DATA)
open_count=sum(1 for r in DATA if r["status"]=="Open")
all_res=[r["_res"] for r in DATA]
all_rats=[r["_rat"] for r in DATA]
crit_high=sum(1 for r in DATA if r["_rat"] in ("Critical","High"))
avg_res=np.mean(all_res)
total_gaps=sum(r["_gap_count"] for r in DATA)
total_actions=sum(len(r["actions"]) for r in DATA)

# SIDEBAR
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:10px 0 18px;'>
        <div style='font-size:36px;margin-bottom:4px;'>🛡️</div>
        <div style='font-size:17px;font-weight:700;color:#f1f5f9!important;'>RCSA Dashboard</div>
        <div style='font-size:12px;color:#94a3b8!important;margin-top:4px;'>Digital Tax Services — 4-Channel API</div>
    </div>""",unsafe_allow_html=True)
    st.divider()
    ch_filter=st.multiselect("Filter by Channel",list(CHANNELS.keys()),default=list(CHANNELS.keys()))
    status_filter=st.multiselect("Filter by Status",["Open","Mitigated"],default=["Open","Mitigated"])
    rating_filter=st.multiselect("Filter by Rating",["Critical","High","Medium","Low"],default=["Critical","High","Medium","Low"])
    filtered=[r for r in DATA if r["channel"] in ch_filter and r["status"] in status_filter and r["_rat"] in rating_filter]
    st.divider()
    st.markdown(f"""<div style='padding:6px 0;font-size:12px;'>
        <div style='color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Register Summary</div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Showing</span><span style='font-weight:600;color:#f1f5f9!important;'>{len(filtered)} / {total}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>🔴 Critical+High</span><span style='font-weight:600;color:#fca5a5!important;'>{sum(1 for r in filtered if r["_rat"] in ("Critical","High"))}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Open Items</span><span style='font-weight:600;color:#fdba74!important;'>{sum(1 for r in filtered if r["status"]=="Open")}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Control Gaps</span><span style='font-weight:600;color:#fde047!important;'>{sum(r["_gap_count"] for r in filtered)}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Action Items</span><span style='font-weight:600;color:#93c5fd!important;'>{sum(len(r["actions"]) for r in filtered)}</span></div>
    </div>""",unsafe_allow_html=True)
    st.divider()

    # CSV Export
    exp_rows=[]
    for r in DATA:
        exp_rows.append({"ID":r["id"],"Channel":r["channel"],"Process":r["process"],"Risk Event":r["risk_event"],"Category":r["risk_category"],
            "L":r["likelihood"],"I":r["impact"],"Inherent":r["_inh"],"Ctrl Eff":r["ctrl_effectiveness"],"Residual":r["_res"],"Rating":r["_rat"],
            "Gaps":r["_gap_count"],"Status":r["status"]})
    csv_data=pd.DataFrame(exp_rows).to_csv(index=False).encode("utf-8")
    st.download_button("💾 Export Register to CSV",data=csv_data,file_name="rcsa_register.csv",mime="text/csv",use_container_width=True)

    st.divider()
    st.markdown("""<div style='font-size:11px;color:#64748b;line-height:1.6;'>
        <strong style='color:#94a3b8!important;'>Context</strong><br>
        RCSA conducted on Indonesia's 4-channel API digital tax services pilot at DGT (2019-2022). Identified critical control gaps adopted in the agency's digital reform roadmap.<br><br>
        <strong style='color:#94a3b8!important;'>Portfolio by</strong><br>Yayan Puji Riyanto<br>IT Governance & Regulatory Analyst<br>DGT, Ministry of Finance (2019-2022)
    </div>""",unsafe_allow_html=True)

# TABS
tab1,tab2,tab3,tab4,tab5,tab6=st.tabs(["📊 Dashboard","📋 Risk Register","🔍 Risk Detail","📈 Stress Test","✏️ Custom Risk","📝 Audit Trail"])

# ═══ TAB 1: DASHBOARD ═══
with tab1:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Risk & Control Self-Assessment</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Digital Tax Services — 4-Channel API Platform · DGT, Indonesia</p>',unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1: mc_render("Total Risks",total,"In register")
    with c2: mc_render("Open Items",f"{open_count}",f"{open_count/total:.0%} of total")
    with c3: mc_render("Avg Residual",f"{avg_res:.1f}","/25")
    with c4: mc_render("Critical+High",f"{crit_high}","Requiring action")
    with c5: mc_render("Control Gaps",f"{total_gaps}","Identified")
    with c6: mc_render("Action Items",f"{total_actions}","In pipeline")

    st.markdown('<div class="sh">📡 Channel Overview</div>',unsafe_allow_html=True)
    cc1,cc2,cc3,cc4=st.columns(4)
    for col,ch_name in zip([cc1,cc2,cc3,cc4],CHANNELS.keys()):
        ch=CHANNELS[ch_name]; ch_risks=[r for r in DATA if r["channel"]==ch_name]
        ch_open=sum(1 for r in ch_risks if r["status"]=="Open")
        ch_avg=np.mean([r["_res"] for r in ch_risks]) if ch_risks else 0
        _,ch_col=rr(ch_avg)
        with col:
            st.markdown(f"""<div class="ch-card"><div class="ch-icon">{ch["icon"]}</div><div class="ch-name">{ch_name}</div><div class="ch-sub">{ch["desc"]}</div>
                <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e2e8f0;font-size:12px;color:#64748b;">
                <div style="display:flex;justify-content:space-between;"><span>Risks</span><span style="font-weight:600;color:#1e293b;">{len(ch_risks)}</span></div>
                <div style="display:flex;justify-content:space-between;"><span>Open</span><span style="font-weight:600;color:#dc2626;">{ch_open}</span></div>
                <div style="display:flex;justify-content:space-between;"><span>Avg Residual</span><span style="font-weight:600;color:{ch_col};">{ch_avg:.1f}</span></div>
                <div style="display:flex;justify-content:space-between;"><span>Volume</span><span style="font-weight:500;">{ch["daily_volume"]}</span></div>
                </div></div>""",unsafe_allow_html=True)

    st.markdown('<div class="sh">📈 Risk Landscape</div>',unsafe_allow_html=True)
    vc1,vc2,vc3=st.columns([2,2,2])
    with vc1:
        ch_names=list(CHANNELS.keys()); ch_colors=[CHANNELS[c]["color"] for c in ch_names]
        ch_res_vals=[np.mean([r["_res"] for r in DATA if r["channel"]==c]) for c in ch_names]
        fig_ch=go.Figure(go.Bar(x=ch_names,y=ch_res_vals,marker_color=ch_colors,text=[f"{v:.1f}" for v in ch_res_vals],textposition="outside"))
        fig_ch.add_hline(y=10,line_dash="dash",line_color="#ea580c",opacity=.5,annotation_text="High threshold",annotation_position="top right")
        fig_ch.update_layout(title="Avg Residual Risk by Channel",title_font_size=14,height=300,margin=dict(t=40,b=30,l=30,r=20),yaxis=dict(range=[0,max(ch_res_vals)*1.3],title="Score"),plot_bgcolor="white",yaxis_gridcolor="#f1f5f9")
        st.plotly_chart(fig_ch,use_container_width=True)
    with vc2:
        ro=["Critical","High","Medium","Low"];rcm={"Critical":"#dc2626","High":"#ea580c","Medium":"#eab308","Low":"#22c55e"}
        rv=[all_rats.count(x) for x in ro]
        fig_p=go.Figure(go.Pie(values=rv,labels=ro,marker_colors=[rcm[x] for x in ro],hole=.5,textinfo="label+value",textposition="outside",textfont=dict(size=11)))
        fig_p.update_layout(title="Risk Rating Distribution",title_font_size=14,height=300,margin=dict(t=40,b=20,l=20,r=20),showlegend=False)
        st.plotly_chart(fig_p,use_container_width=True)
    with vc3:
        eff_vals=[r["ctrl_effectiveness"] for r in DATA]; eff_counts=[eff_vals.count(i) for i in range(1,6)]
        eff_colors=["#dc2626","#ea580c","#eab308","#22c55e","#059669"]
        fig_e=go.Figure(go.Bar(x=[EFF_LABELS[i] for i in range(1,6)],y=eff_counts,marker_color=eff_colors,text=eff_counts,textposition="outside"))
        fig_e.update_layout(title="Control Effectiveness",title_font_size=14,height=300,margin=dict(t=40,b=30,l=30,r=20),plot_bgcolor="white",yaxis_gridcolor="#f1f5f9",yaxis_title="Count")
        st.plotly_chart(fig_e,use_container_width=True)

    st.markdown('<div class="sh">🗺️ Risk Heatmap — Likelihood × Impact</div>',unsafe_allow_html=True)
    fig_h=go.Figure()
    for li in range(1,6):
        for im in range(1,6):
            _,bg=rr(li*im)
            fig_h.add_shape(type="rect",x0=im-.5,x1=im+.5,y0=li-.5,y1=li+.5,fillcolor=bg,opacity=.12,line=dict(color="white",width=2),layer="below")
            fig_h.add_annotation(x=im,y=li,text=str(li*im),showarrow=False,font=dict(size=10,color="rgba(0,0,0,.12)"))
    np.random.seed(99)
    for r in filtered:
        ch=CHANNELS[r["channel"]]; jx,jy=np.random.uniform(-.2,.2),np.random.uniform(-.2,.2)
        fig_h.add_trace(go.Scatter(x=[r["impact"]+jx],y=[r["likelihood"]+jy],mode="markers+text",showlegend=False,
            marker=dict(size=20,color=ch["color"],line=dict(width=2,color="white"),opacity=.9),
            text=[r["id"]],textposition="middle center",textfont=dict(size=7,color="white"),
            hovertemplate=f"<b>{r['id']}: {r['risk_event'][:50]}...</b><br>Channel: {r['channel']}<br>L={r['likelihood']}, I={r['impact']}<br>Inherent: {r['_inh']} → Residual: {r['_res']}<br>Rating: {r['_rat']}<extra></extra>"))
    for ch_name,ch_info in CHANNELS.items():
        fig_h.add_trace(go.Scatter(x=[None],y=[None],mode="markers",name=ch_name,marker=dict(size=10,color=ch_info["color"])))
    fig_h.update_layout(xaxis=dict(title="<b>Impact</b>",tickvals=[1,2,3,4,5],ticktext=list(I_LABELS.values()),range=[.3,5.7]),
        yaxis=dict(title="<b>Likelihood</b>",tickvals=[1,2,3,4,5],ticktext=list(L_LABELS.values()),range=[.3,5.7]),
        height=420,margin=dict(t=20,b=40,l=40,r=20),plot_bgcolor="white",font=dict(size=11),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=.5))
    st.plotly_chart(fig_h,use_container_width=True)

# ═══ TAB 2: EDITABLE REGISTER ═══
with tab2:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">RCSA Register</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Editable risk register — modify Likelihood, Impact, or Control Effectiveness inline</p>',unsafe_allow_html=True)

    reg_rows=[]
    for r in filtered:
        reg_rows.append({"ID":r["id"],"Channel":f'{CHANNELS[r["channel"]]["icon"]} {r["channel"]}',
            "Risk Event":r["risk_event"][:55]+("..." if len(r["risk_event"])>55 else ""),
            "Category":r["risk_category"],
            "L_Label":f'{r["likelihood"]} - {L_LABELS[r["likelihood"]]}',
            "I_Label":f'{r["impact"]} - {I_LABELS[r["impact"]]}',
            "Inherent":r["_inh"],
            "Ctrl_Label":f'{r["ctrl_effectiveness"]} - {EFF_LABELS[r["ctrl_effectiveness"]]}',
            "Residual":r["_res"],"Rating":r["_rat"],"Gaps":r["_gap_count"],"Status":r["status"]})

    df_r=pd.DataFrame(reg_rows)

    def sr2(v):
        m={"Critical":"background-color:#fef2f2;color:#991b1b;font-weight:600","High":"background-color:#fff7ed;color:#9a3412;font-weight:600",
           "Medium":"background-color:#fefce8;color:#854d0e;font-weight:600","Low":"background-color:#f0fdf4;color:#166534;font-weight:600"}
        return m.get(v,"")
    def ss(v):
        return "background-color:#fef2f2;color:#991b1b;font-weight:600" if v=="Open" else "background-color:#f0fdf4;color:#166534;font-weight:600"

    if not df_r.empty:
        edited_df = st.data_editor(
            df_r,
            use_container_width=True,hide_index=True,height=500,
            column_config={
                "ID": st.column_config.TextColumn("ID",disabled=True),
                "Channel": st.column_config.TextColumn("Channel",disabled=True),
                "Risk Event": st.column_config.TextColumn("Risk Event",disabled=True),
                "Category": st.column_config.TextColumn("Category",disabled=True),
                "L_Label": st.column_config.SelectboxColumn("Likelihood",options=[f"{k} - {v}" for k,v in L_LABELS.items()],required=True),
                "I_Label": st.column_config.SelectboxColumn("Impact",options=[f"{k} - {v}" for k,v in I_LABELS.items()],required=True),
                "Inherent": st.column_config.NumberColumn("Inherent",disabled=True),
                "Ctrl_Label": st.column_config.SelectboxColumn("Ctrl Eff",options=[f"{k} - {v}" for k,v in EFF_LABELS.items()],required=True),
                "Residual": st.column_config.NumberColumn("Residual",disabled=True),
                "Rating": st.column_config.TextColumn("Rating",disabled=True),
                "Gaps": st.column_config.NumberColumn("Gaps",disabled=True),
                "Status": st.column_config.SelectboxColumn("Status",options=["Open","Mitigated"],required=True),
            })

        # Detect changes
        changes_made=False
        for i in range(len(df_r)):
            old=df_r.iloc[i]; new=edited_df.iloc[i]
            if old["L_Label"]!=new["L_Label"] or old["I_Label"]!=new["I_Label"] or old["Ctrl_Label"]!=new["Ctrl_Label"] or old["Status"]!=new["Status"]:
                changes_made=True
                new_l=int(new["L_Label"].split(" - ")[0]); new_i=int(new["I_Label"].split(" - ")[0]); new_ce=int(new["Ctrl_Label"].split(" - ")[0])
                # Find matching risk in session state
                rid=old["ID"]
                for r in st.session_state.RCSA:
                    if r["id"]==rid:
                        st.session_state.rcsa_audit.append({
                            "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ID":rid,
                            "Risk":r["risk_event"][:50],
                            "Old":f"L:{r['likelihood']}, I:{r['impact']}, CE:{r['ctrl_effectiveness']}, {r['status']}",
                            "New":f"L:{new_l}, I:{new_i}, CE:{new_ce}, {new['Status']}"})
                        r["likelihood"]=new_l; r["impact"]=new_i; r["ctrl_effectiveness"]=new_ce; r["status"]=new["Status"]
                        break
        if changes_made: st.rerun()
    else:
        st.info("No risks match the current filter selection.")

    # Gap summary
    st.markdown('<div class="sh">⚠️ Open Control Gaps Summary</div>',unsafe_allow_html=True)
    open_risks=[r for r in filtered if r["status"]=="Open"]
    for r in sorted(open_risks,key=lambda x:x["_res"],reverse=True):
        _,gcol=rr(r["_res"])
        gap_tags="".join(f'<span class="gap-tag">{g}</span>' for g in r["gaps"])
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:6px 0;border-left:4px solid {gcol};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div><span style="font-weight:600;color:#1e293b;">{r["id"]}</span> · <span style="color:#64748b;">{r["channel"]}</span> · <span style="font-size:13px;color:#475569;">{r["risk_event"][:70]}</span></div>
                <div style="background:{gcol};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">{r["_rat"]} ({r["_res"]:.0f})</div>
            </div><div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;">{gap_tags}</div>
        </div>""",unsafe_allow_html=True)

# ═══ TAB 3: RISK DETAIL ═══
with tab3:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Risk Detail View</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Detailed assessment for individual risk items</p>',unsafe_allow_html=True)
    if not filtered:
        st.info("No risks match filter."); st.stop()
    sel_r=st.selectbox("Select Risk",[f"{r['id']} — [{r['channel']}] {r['risk_event'][:55]}" for r in filtered],label_visibility="collapsed")
    ri=next(r for r in filtered if sel_r.startswith(r["id"]))
    rat_label,rat_col=rr(ri["_res"]); red_pct=(1-ri["_res"]/ri["_inh"])*100

    m1,m2,m3,m4,m5=st.columns(5)
    with m1: mc_render("Inherent",f"{ri['_inh']}","L×I")
    with m2: mc_render("Ctrl Effectiveness",EFF_LABELS[ri["ctrl_effectiveness"]],f"{ri['ctrl_effectiveness']}/5")
    with m3: mc_render("Reduction",f"{red_pct:.0f}%","")
    with m4: mc_render("Residual",f"{ri['_res']:.0f}","After controls")
    with m5: st.markdown(f'<div class="mc" style="background:{rat_col};border:none;"><h3 style="color:rgba(255,255,255,.8);">Rating</h3><p class="v" style="color:white;">{rat_label}</p><p class="s" style="color:rgba(255,255,255,.7);">{ri["status"]}</p></div>',unsafe_allow_html=True)

    st.markdown("",unsafe_allow_html=True)
    dl,dr=st.columns([3,2])
    with dl:
        ch=CHANNELS[ri["channel"]]
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;"><span style="font-size:24px;">{ch["icon"]}</span><div><div style="font-size:16px;font-weight:600;color:#1e293b;">{ri["id"]} — {ri["risk_event"]}</div>
            <div style="font-size:12px;color:#64748b;">{ri["channel"]} · {ri["process"]} · {ri["risk_category"]}</div></div></div>
            <div style="margin-top:12px;padding-top:12px;border-top:1px solid #e2e8f0;"><div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">Scoring</div>
            <div style="font-size:13px;color:#475569;margin-top:4px;">Likelihood: <strong>{ri["likelihood"]}</strong> ({L_LABELS[ri["likelihood"]]}) · Impact: <strong>{ri["impact"]}</strong> ({I_LABELS[ri["impact"]]})</div></div>
        </div>""",unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#1e293b;margin:12px 0 6px;">Existing Controls</div>',unsafe_allow_html=True)
        for ct,cd in ri["controls"]:
            cls_map={"Preventive":"ctrl-p","Detective":"ctrl-d","Corrective":"ctrl-c"}; icon_map={"Preventive":"🟢","Detective":"🟡","Corrective":"🔴"}
            st.markdown(f'<div class="{cls_map.get(ct,"ctrl-d")}">{icon_map.get(ct,"")} <strong>{ct}:</strong> {cd}</div>',unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#991b1b;margin:16px 0 6px;">⚠️ Control Gaps ({ri["_gap_count"]})</div>',unsafe_allow_html=True)
        for g in ri["gaps"]: st.markdown(f'<span class="gap-tag">✗ {g}</span>',unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#1e40af;margin:16px 0 6px;">📋 Actions ({len(ri["actions"])})</div>',unsafe_allow_html=True)
        for desc,target,owner in ri["actions"]:
            st.markdown(f'<div class="action-item">→ {desc}<br><span style="font-size:11px;color:#6b7280;">Target: {target} · Owner: {owner}</span></div>',unsafe_allow_html=True)
    with dr:
        fig_w=go.Figure(go.Waterfall(x=["Inherent","Controls","Residual"],y=[ri["_inh"],-(ri["_inh"]-ri["_res"]),0],
            measure=["absolute","relative","total"],connector=dict(line=dict(color="#cbd5e1",dash="dot")),
            decreasing=dict(marker=dict(color="#22c55e")),totals=dict(marker=dict(color=rat_col)),
            text=[str(ri["_inh"]),f"-{ri['_inh']-ri['_res']:.0f}",f"{ri['_res']:.0f}"],textposition="outside",textfont=dict(size=13)))
        fig_w.update_layout(height=250,margin=dict(t=30,b=30),title="Risk Waterfall",plot_bgcolor="white",yaxis_gridcolor="#f1f5f9")
        st.plotly_chart(fig_w,use_container_width=True)
        ctrl_types=[ct for ct,_ in ri["controls"]]; ct_counts={"Preventive":ctrl_types.count("Preventive"),"Detective":ctrl_types.count("Detective"),"Corrective":ctrl_types.count("Corrective")}
        fig_ct=go.Figure(go.Bar(x=list(ct_counts.keys()),y=list(ct_counts.values()),marker_color=["#22c55e","#eab308","#ef4444"],text=list(ct_counts.values()),textposition="outside"))
        fig_ct.update_layout(height=200,margin=dict(t=30,b=30),title="Control Types",plot_bgcolor="white",yaxis_gridcolor="#f1f5f9")
        st.plotly_chart(fig_ct,use_container_width=True)

    if ri["_res"]>=16: st.error("**CRITICAL** — Immediate escalation. Additional controls or process suspension required.")
    elif ri["_res"]>=10: st.warning("**HIGH** — Active remediation required. Prioritize action items.")
    elif ri["_res"]>=5: st.info("**MEDIUM** — Monitor through regular RCSA cycle.")
    else: st.success("**LOW** — Acceptable. Maintain in register.")

# ═══ TAB 4: STRESS TEST ═══
with tab4:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Simulation & Stress Testing</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Macro stress scenarios and Monte Carlo loss simulation for digital tax services platform</p>',unsafe_allow_html=True)

    st.markdown('<div class="sh">📈 Platform Stress Testing</div>',unsafe_allow_html=True)
    st.markdown("Simulate the effect of a severe macro event (e.g., system-wide outage during peak filing, coordinated cyberattack) that escalates Likelihood and/or Impact across all channels.")

    cs1,cs2=st.columns([1,2])
    with cs1:
        stress_l=st.slider("Macro Likelihood Shift",0,2,0,help="Increases likelihood of all events")
        stress_i=st.slider("Macro Impact Shift",0,2,0,help="Increases severity of all events")
        stressed_res=[]
        for r in DATA:
            sl=min(5,r["likelihood"]+stress_l); si=min(5,r["impact"]+stress_i)
            stressed_res.append(calc_res(calc_inh(sl,si),r["ctrl_effectiveness"]))
        st_avg=np.mean(stressed_res); st_crit=sum(1 for r in stressed_res if r>=16)
        st.metric("Stressed Avg Residual",f"{st_avg:.1f}",f"{st_avg-avg_res:+.1f} shift")
        st.metric("Critical under Stress",st_crit,f"{st_crit-sum(1 for r in all_rats if r=='Critical'):+d} new",delta_color="inverse")
    with cs2:
        fig_st=go.Figure()
        fig_st.add_trace(go.Box(y=all_res,name="Base Portfolio",marker_color="#3b82f6"))
        fig_st.add_trace(go.Box(y=stressed_res,name="Stressed Portfolio",marker_color="#ef4444"))
        fig_st.update_layout(title="Residual Risk Distribution Shift",height=300,margin=dict(t=30,b=20,l=40,r=20),plot_bgcolor="white",yaxis=dict(title="Residual Risk (0-25)",range=[0,26]))
        st.plotly_chart(fig_st,use_container_width=True)

    st.markdown('<div class="sh">🧠 Monte Carlo Loss Simulation (10,000 iterations)</div>',unsafe_allow_html=True)
    st.markdown("Maps Likelihood (1-5) to probabilities and Impact (1-5) to IDR losses to estimate 95% Operational VaR for the digital tax platform.")
    if st.button("▶️ Run Monte Carlo Simulation",type="primary"):
        with st.spinner("Running 10,000 iterations..."):
            prob_map={1:.025,2:.125,3:.35,4:.65,5:.90}
            impact_map_idr={1:0.5,2:5,3:25,4:100,5:300}  # Billion IDR
            n_iter=10000; total_losses=np.zeros(n_iter); np.random.seed(42)
            for r in DATA:
                sl=min(5,r["likelihood"]+stress_l); si=min(5,r["impact"]+stress_i)
                p=prob_map.get(sl,0); mean_loss=impact_map_idr.get(si,0)
                occ=np.random.binomial(1,p,n_iter)
                sev=np.random.lognormal(mean=np.log(mean_loss)-.125,sigma=.5,size=n_iter)
                red_map={1:0,2:.15,3:.35,4:.55,5:.75}
                total_losses+=occ*sev*(1-red_map.get(r["ctrl_effectiveness"],0))
            var95=np.percentile(total_losses,95); med=np.median(total_losses)
            fig_mc=px.histogram(total_losses,nbins=100,title="Simulated Annual Loss Distribution (IDR Billion)")
            fig_mc.update_traces(marker_color="#3b82f6")
            fig_mc.add_vline(x=var95,line_dash="dash",line_color="red",annotation_text=f" 95% VaR: IDR {var95:.1f}B",annotation_position="top right")
            fig_mc.add_vline(x=med,line_dash="dot",line_color="blue",annotation_text=f" Median: IDR {med:.1f}B",annotation_position="top right")
            fig_mc.update_layout(showlegend=False,plot_bgcolor="white",height=400,xaxis_title="Total Estimated Loss (IDR Billion)",yaxis_title="Frequency")
            mc1,mc2=st.columns([1,3])
            with mc1:
                st.metric("Median Expected Loss",f"IDR {med:.1f}B")
                st.metric("95% OpRisk VaR",f"IDR {var95:.1f}B",help="95% of simulated years, losses will not exceed this.")
                st.caption("Controls mitigate final loss distributions.")
            with mc2: st.plotly_chart(fig_mc,use_container_width=True)

# ═══ TAB 5: CUSTOM RISK ═══
with tab5:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Add Custom Risk</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Define a new risk item manually or auto-generate a draft</p>',unsafe_allow_html=True)

    if "rcsa_draft" not in st.session_state: st.session_state.rcsa_draft=None

    cb1,cb2=st.columns([1,4])
    with cb1:
        if st.button("🤖 Auto-Generate Draft"):
            ideas=[
                {"ch":"e-Filing","pr":"Bulk Upload","re":"Mass fraudulent SPT submission via compromised bulk upload API endpoint","rc":"External Fraud","l":2,"i":5,"ce":3,
                 "ctrls":"Rate limiting on bulk endpoints\nDigital signature verification per SPT\nPost-upload anomaly scan"},
                {"ch":"e-Invoice","pr":"Cross-border Invoice","re":"VAT fraud via fictitious cross-border invoices exploiting ASEAN trade agreement provisions","rc":"External Fraud","l":3,"i":4,"ce":2,
                 "ctrls":"Country-of-origin validation\nCustoms data cross-check\nManual review for cross-border invoices >IDR 500M"},
                {"ch":"e-Billing","pr":"Refund Processing","re":"Unauthorized tax refund issuance through manipulation of overpayment billing codes","rc":"Internal Fraud","l":2,"i":5,"ce":3,
                 "ctrls":"Dual approval for refund billing codes\nSegregation of duties\nQuarterly refund audit sampling"},
            ]
            st.session_state.rcsa_draft=random.choice(ideas)

    if st.session_state.rcsa_draft:
        st.success(f"Draft populated: **{st.session_state.rcsa_draft['re'][:60]}**")

    with st.form("custom_rcsa"):
        draft=st.session_state.rcsa_draft or {"ch":"e-Registration","pr":"","re":"","rc":"Process Failure","l":3,"i":3,"ce":3,"ctrls":""}
        f1,f2=st.columns([3,2])
        with f1:
            c_ch=st.selectbox("Channel",list(CHANNELS.keys()),index=list(CHANNELS.keys()).index(draft["ch"]))
            c_pr=st.text_input("Process",value=draft["pr"],placeholder="e.g., Identity Verification")
            c_re=st.text_input("Risk Event",value=draft["re"],placeholder="Describe the risk event")
            c_rc=st.selectbox("Risk Category",["Process Failure","External Fraud","Internal Fraud","System Failure","Unauthorized Access"],
                index=["Process Failure","External Fraud","Internal Fraud","System Failure","Unauthorized Access"].index(draft["rc"]) if draft["rc"] in ["Process Failure","External Fraud","Internal Fraud","System Failure","Unauthorized Access"] else 0)
            c_ctrls=st.text_area("Controls (one per line)",value=draft["ctrls"],height=80)
            c_gaps=st.text_area("Identified Gaps (one per line)",height=60)
        with f2:
            st.markdown("##### Scoring")
            c_l=st.select_slider("Likelihood",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {L_LABELS[x]}",value=draft["l"])
            st.caption(L_DESC[c_l])
            c_i=st.select_slider("Impact",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {I_LABELS[x]}",value=draft["i"])
            st.caption(I_DESC[c_i])
            c_ce=st.select_slider("Control Effectiveness",options=[1,2,3,4,5],format_func=lambda x:f"{x} — {EFF_LABELS[x]}",value=draft["ce"])
            st.caption(EFF_DESC[c_ce])
            c_status=st.radio("Status",["Open","Mitigated"],horizontal=True)
        sub=st.form_submit_button("➕ Add to Register",use_container_width=True,type="primary")

    if sub and c_re:
        new_id=f"X-{len(st.session_state.RCSA)+1:03d}"
        ctrl_list=[("Preventive" if i==0 else "Detective",c.strip()) for i,c in enumerate(c_ctrls.strip().split("\n")) if c.strip()]
        gap_list=[g.strip() for g in c_gaps.strip().split("\n") if g.strip()]
        new_risk={"id":new_id,"channel":c_ch,"process":c_pr,"risk_event":c_re,"risk_category":c_rc,
            "likelihood":c_l,"impact":c_i,"controls":ctrl_list,"ctrl_effectiveness":c_ce,
            "gaps":gap_list,"status":c_status,"actions":[]}
        st.session_state.RCSA.append(new_risk)
        st.session_state.rcsa_audit.append({"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ID":new_id,"Risk":c_re[:50],"Old":"—","New":f"CREATED L:{c_l}, I:{c_i}, CE:{c_ce}"})
        st.session_state.rcsa_draft=None
        st.success(f"✅ **{new_id}** added to register.")
        st.rerun()

# ═══ TAB 6: AUDIT TRAIL ═══
with tab6:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Audit Trail</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Track all modifications to the RCSA register</p>',unsafe_allow_html=True)
    if st.session_state.rcsa_audit:
        df_audit=pd.DataFrame(st.session_state.rcsa_audit)
        st.dataframe(df_audit.sort_values(by="Timestamp",ascending=False),use_container_width=True,hide_index=True)
        csv_audit=df_audit.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Audit Trail",data=csv_audit,file_name="rcsa_audit_trail.csv",mime="text/csv")
    else:
        st.info("No changes recorded yet. Modify Likelihood, Impact, Control Effectiveness, or Status values in the Risk Register tab to generate audit entries.")

# FOOTER
st.divider()
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">RCSA Dashboard — Digital Tax Services 4-Channel API<br>Portfolio by <strong>Yayan Puji Riyanto</strong> · IT Governance & Regulatory Analyst, DGT (2019-2022)<br>PhD Candidate, Business Law & Taxation — Monash University<br><em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em></div>',unsafe_allow_html=True)
