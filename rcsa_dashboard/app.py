"""
Risk & Control Self-Assessment (RCSA) Dashboard
Digital Tax Services — 4-Channel API Platform
Portfolio by Yayan Puji Riyanto

Based on actual RCSA experience at the Directorate General of Taxes,
Ministry of Finance — Republic of Indonesia (2019-2022).
Assessed operational risk and control gaps across e-Registration,
e-Billing, e-Filing, and e-Invoice API channels.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="RCSA Dashboard — Digital Tax Services", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 1200px; }
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

# ═══════════════════════════════════════════════════════
# DATA — RCSA Register
# ═══════════════════════════════════════════════════════
CHANNELS = {
    "e-Registration": {"icon": "📝", "desc": "Taxpayer registration & NPWP issuance via API", "color": "#2563eb", "api_endpoints": 4, "daily_volume": "~12,000 requests/day"},
    "e-Billing": {"icon": "💳", "desc": "Tax payment code generation & billing via API", "color": "#059669", "api_endpoints": 6, "daily_volume": "~45,000 requests/day"},
    "e-Filing": {"icon": "📄", "desc": "Tax return submission & processing via API", "color": "#d97706", "api_endpoints": 8, "daily_volume": "~85,000 requests/day (peak season: 500K+)"},
    "e-Invoice": {"icon": "🧾", "desc": "Electronic tax invoice creation & validation via API", "color": "#7c3aed", "api_endpoints": 5, "daily_volume": "~120,000 requests/day"},
}

L_LABELS = {1:"Rare",2:"Unlikely",3:"Possible",4:"Likely",5:"Almost Certain"}
I_LABELS = {1:"Negligible",2:"Minor",3:"Moderate",4:"Major",5:"Severe"}
EFF_LABELS = {1:"Ineffective",2:"Weak",3:"Adequate",4:"Strong",5:"Robust"}

RCSA_DATA = [
    # e-Registration
    {"id":"R-001","channel":"e-Registration","process":"Identity Verification","risk_event":"Fraudulent taxpayer registration using stolen identity documents",
     "risk_category":"External Fraud","likelihood":3,"impact":4,
     "controls":[("Preventive","NIK validation against Dukcapil (national ID database)"),("Preventive","Biometric verification for high-risk registrations"),("Detective","Post-registration audit sampling (5% of new registrations)")],
     "ctrl_effectiveness":3,"gaps":["No real-time biometric check for API channel","Dukcapil API latency causes timeout → fallback to manual check"],"status":"Open",
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

    # e-Billing
    {"id":"B-001","channel":"e-Billing","process":"Payment Code Generation","risk_event":"Generation of incorrect tax payment codes (Kode Billing) due to tax type mapping error",
     "risk_category":"Process Failure","likelihood":3,"impact":4,
     "controls":[("Preventive","Lookup table validation against 400+ tax payment codes (MAP/KJS)"),("Detective","Real-time validation against taxpayer profile for code eligibility"),("Corrective","Billing code cancellation and reissuance workflow")],
     "ctrl_effectiveness":3,"gaps":["MAP/KJS lookup table update lag (manual process, updated quarterly)","No automated cross-check between billing code and SPT data"],"status":"Open",
     "actions":[("Automate MAP/KJS reference table synchronization","Q2 2022","IT"),("Implement SPT-billing cross-validation at code generation","Q3 2022","Business Process")]},

    {"id":"B-002","channel":"e-Billing","process":"Payment Reconciliation","risk_event":"Failed reconciliation between billing system and MPN (State Revenue Module) causing unmatched payments",
     "risk_category":"Process Failure","likelihood":3,"impact":5,
     "controls":[("Detective","T+1 automated reconciliation between e-Billing and MPN"),("Detective","Weekly exception report reviewed by Reconciliation Unit"),("Corrective","Manual matching procedure for unreconciled items")],
     "ctrl_effectiveness":2,"gaps":["Reconciliation runs T+1 not real-time — 24h exposure window","Manual matching backlog averaging 15 business days","No automated escalation for high-value unmatched items (>IDR 1B)"],"status":"Open",
     "actions":[("Implement real-time or T+0 reconciliation with MPN","Q4 2022","IT / Treasury"),("Automate escalation for unmatched items >IDR 1B within 3 business days","Q2 2022","Reconciliation Unit"),("Clear manual matching backlog and set 5-day SLA","Q2 2022","Operations")]},

    {"id":"B-003","channel":"e-Billing","process":"Payment Channel Integration","risk_event":"Payment channel partner (bank) system outage causing billing code rejection at point of payment",
     "risk_category":"System Failure","likelihood":4,"impact":3,
     "controls":[("Preventive","Multi-bank payment channel redundancy (3 state-owned banks)"),("Detective","Real-time uptime monitoring dashboard for all payment channels"),("Corrective","Fallback to alternative payment channel within 15 minutes")],
     "ctrl_effectiveness":4,"gaps":["Taxpayer not automatically redirected to alternative channel — manual process"],"status":"Mitigated",
     "actions":[("Implement automatic failover routing to alternative payment channels","Q3 2022","IT / Banking Partners")]},

    # e-Filing
    {"id":"F-001","channel":"e-Filing","process":"Tax Return Submission","risk_event":"Data loss or corruption during peak filing season (March deadline) due to API overload",
     "risk_category":"System Failure","likelihood":4,"impact":5,
     "controls":[("Preventive","Horizontal auto-scaling infrastructure (cloud-based)"),("Preventive","Rate limiting per API consumer (1000 req/min)"),("Detective","Real-time throughput and error rate monitoring"),("Corrective","Queue-based retry mechanism for failed submissions")],
     "ctrl_effectiveness":3,"gaps":["Auto-scaling lag of 3-5 minutes during sudden traffic spikes","Queue retry mechanism does not guarantee FIFO ordering","No dedicated capacity reservation for large enterprise filers"],"status":"Open",
     "actions":[("Implement predictive auto-scaling based on historical filing patterns","Q1 2022","IT Infrastructure"),("Add priority queue tier for enterprise filers (>1000 employees)","Q2 2022","IT / Policy")]},

    {"id":"F-002","channel":"e-Filing","process":"Data Validation","risk_event":"Acceptance of tax returns with material calculation errors due to insufficient server-side validation",
     "risk_category":"Process Failure","likelihood":3,"impact":4,
     "controls":[("Preventive","72 server-side validation rules for SPT calculations"),("Preventive","Cross-reference check against prior year filing data"),("Detective","Post-submission statistical anomaly detection (quarterly)")],
     "ctrl_effectiveness":3,"gaps":["Validation rules not updated for 2022 tax law amendments","No real-time validation feedback to API consumers — only batch error codes","Statistical anomaly detection runs quarterly, not continuously"],"status":"Open",
     "actions":[("Update validation rules for 2022 HPP (Tax Harmonization Law) amendments","Q1 2022","Tax Policy / IT"),("Implement synchronous validation response in API","Q2 2022","IT"),("Move anomaly detection to monthly cadence","Q2 2022","Compliance")]},

    {"id":"F-003","channel":"e-Filing","process":"Digital Signature","risk_event":"Digital certificate compromise enabling submission of fraudulent tax returns",
     "risk_category":"External Fraud","likelihood":2,"impact":5,
     "controls":[("Preventive","PKI-based digital certificate issued by certified CA"),("Preventive","Certificate pinning in API communication"),("Detective","Certificate revocation list (CRL) check at submission time")],
     "ctrl_effectiveness":4,"gaps":["CRL check is not OCSP-based — revocation propagation delay up to 24h"],"status":"Mitigated",
     "actions":[("Migrate from CRL to OCSP for real-time certificate status checking","Q3 2022","IT Security")]},

    # e-Invoice
    {"id":"I-001","channel":"e-Invoice","process":"Invoice Number Generation","risk_event":"NSFP (tax invoice serial number) exhaustion causing inability to issue new invoices",
     "risk_category":"Process Failure","likelihood":3,"impact":4,
     "controls":[("Preventive","Automated NSFP allocation in blocks of 1000"),("Detective","NSFP utilization monitoring with 80% threshold alert"),("Corrective","Emergency NSFP allocation procedure (24h turnaround)")],
     "ctrl_effectiveness":3,"gaps":["Threshold alert at 80% gives insufficient lead time for high-volume issuers","Emergency allocation still requires manual approval — no auto-replenishment"],"status":"Open",
     "actions":[("Lower alert threshold to 60% and add predictive exhaustion modeling","Q2 2022","IT"),("Implement auto-replenishment for pre-approved taxpayers","Q3 2022","Policy / IT")]},

    {"id":"I-002","channel":"e-Invoice","process":"Invoice Validation","risk_event":"Acceptance of invoices with mismatched buyer-seller NPWP data enabling fictitious tax invoices (faktur pajak fiktif)",
     "risk_category":"External Fraud","likelihood":3,"impact":5,
     "controls":[("Preventive","Real-time NPWP validation against master file for both buyer and seller"),("Preventive","PKP (taxable entrepreneur) status verification at invoice creation"),("Detective","Machine learning-based anomaly detection for invoice patterns"),("Detective","Cross-matching of purchase and sales invoices across taxpayers (quarterly)")],
     "ctrl_effectiveness":3,"gaps":["ML model false positive rate at 12% — causes legitimate invoice rejections","Cross-matching runs quarterly — 3-month exposure window for fictitious invoices","No velocity check for unusual invoice volume spikes from single NPWP"],"status":"Open",
     "actions":[("Retrain ML model with updated training data to reduce false positives to <5%","Q2 2022","Data Analytics"),("Move cross-matching to monthly cadence","Q2 2022","Compliance"),("Implement real-time velocity checks (>50 invoices/hour triggers review)","Q3 2022","IT / Compliance")]},

    {"id":"I-003","channel":"e-Invoice","process":"API Rate Management","risk_event":"Denial of service on e-Invoice API during VAT reporting deadline causing widespread business disruption",
     "risk_category":"System Failure","likelihood":3,"impact":5,
     "controls":[("Preventive","API rate limiting (500 req/min per consumer)"),("Preventive","CDN and DDoS protection layer"),("Detective","Real-time traffic anomaly detection"),("Corrective","Emergency capacity burst (2x normal) activation procedure")],
     "ctrl_effectiveness":3,"gaps":["Rate limit of 500 req/min insufficient for large ERP integrators","No priority lane for critical business sectors (e.g., FMCG, manufacturing)"],"status":"Open",
     "actions":[("Implement tiered rate limits based on taxpayer classification","Q2 2022","IT / Policy"),("Create priority API lane for critical sector taxpayers","Q3 2022","IT / Policy")]},
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
def mc(l,v,s=""):
    st.markdown(f'<div class="mc"><h3>{l}</h3><p class="v">{v}</p><p class="s">{s}</p></div>',unsafe_allow_html=True)

# Precompute
for r in RCSA_DATA:
    r["_inh"]=calc_inh(r["likelihood"],r["impact"])
    r["_res"]=calc_res(r["_inh"],r["ctrl_effectiveness"])
    r["_rat"],r["_col"]=rr(r["_res"])
    r["_gap_count"]=len(r["gaps"])

total=len(RCSA_DATA)
open_count=sum(1 for r in RCSA_DATA if r["status"]=="Open")
crit_high=sum(1 for r in RCSA_DATA if r["_rat"] in ("Critical","High"))
avg_res=np.mean([r["_res"] for r in RCSA_DATA])
total_gaps=sum(r["_gap_count"] for r in RCSA_DATA)
total_actions=sum(len(r["actions"]) for r in RCSA_DATA)

# SIDEBAR
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:10px 0 18px;'>
        <div style='font-size:36px;margin-bottom:4px;'>🛡️</div>
        <div style='font-size:17px;font-weight:700;color:#f1f5f9!important;'>RCSA Dashboard</div>
        <div style='font-size:12px;color:#94a3b8!important;margin-top:4px;'>Digital Tax Services — 4-Channel API</div>
    </div>""",unsafe_allow_html=True)
    st.divider()

    # Channel filter
    ch_filter=st.multiselect("Filter by Channel",list(CHANNELS.keys()),default=list(CHANNELS.keys()))
    status_filter=st.multiselect("Filter by Status",["Open","Mitigated"],default=["Open","Mitigated"])
    rating_filter=st.multiselect("Filter by Rating",["Critical","High","Medium","Low"],default=["Critical","High","Medium","Low"])

    filtered=[r for r in RCSA_DATA if r["channel"] in ch_filter and r["status"] in status_filter and r["_rat"] in rating_filter]

    st.divider()
    st.markdown(f"""<div style='padding:6px 0;font-size:12px;'>
        <div style='color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Register Summary</div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Showing</span><span style='font-weight:600;color:#f1f5f9!important;'>{len(filtered)} / {total}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Open Items</span><span style='font-weight:600;color:#fca5a5!important;'>{sum(1 for r in filtered if r["status"]=="Open")}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Control Gaps</span><span style='font-weight:600;color:#fdba74!important;'>{sum(r["_gap_count"] for r in filtered)}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Action Items</span><span style='font-weight:600;color:#93c5fd!important;'>{sum(len(r["actions"]) for r in filtered)}</span></div>
    </div>""",unsafe_allow_html=True)
    st.divider()
    st.markdown("""<div style='font-size:11px;color:#64748b;line-height:1.6;'>
        <strong style='color:#94a3b8!important;'>Context</strong><br>
        RCSA conducted on Indonesia's 4-channel API digital tax services pilot at the Directorate General of Taxes (2019-2022). Identified critical control gaps and produced actionable recommendations adopted in the agency's digital reform roadmap.<br><br>
        <strong style='color:#94a3b8!important;'>Portfolio by</strong><br>Yayan Puji Riyanto<br>IT Governance & Regulatory Analyst<br>DGT, Ministry of Finance (2019-2022)
    </div>""",unsafe_allow_html=True)

# TABS
tab1,tab2,tab3,tab4=st.tabs(["📊 RCSA Dashboard","📋 Risk Register","🔍 Risk Detail","📖 Methodology"])

with tab1:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Risk & Control Self-Assessment</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Digital Tax Services — 4-Channel API Platform · Directorate General of Taxes, Indonesia</p>',unsafe_allow_html=True)

    # Top metrics
    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1: mc("Total Risks",total,"In register")
    with c2: mc("Open Items",f"{open_count}",f"{open_count/total:.0%} of total")
    with c3: mc("Avg Residual",f"{avg_res:.1f}","/25")
    with c4: mc("Critical+High",f"{crit_high}","Requiring action")
    with c5: mc("Control Gaps",f"{total_gaps}","Identified")
    with c6: mc("Action Items",f"{total_actions}","In pipeline")

    # Channel overview
    st.markdown('<div class="sh">📡 Channel Overview</div>',unsafe_allow_html=True)
    cc1,cc2,cc3,cc4=st.columns(4)
    for col,ch_name in zip([cc1,cc2,cc3,cc4],CHANNELS.keys()):
        ch=CHANNELS[ch_name]
        ch_risks=[r for r in RCSA_DATA if r["channel"]==ch_name]
        ch_open=sum(1 for r in ch_risks if r["status"]=="Open")
        ch_avg=np.mean([r["_res"] for r in ch_risks]) if ch_risks else 0
        _,ch_col=rr(ch_avg)
        with col:
            st.markdown(f"""<div class="ch-card">
                <div class="ch-icon">{ch["icon"]}</div>
                <div class="ch-name">{ch_name}</div>
                <div class="ch-sub">{ch["desc"]}</div>
                <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e2e8f0;font-size:12px;color:#64748b;">
                    <div style="display:flex;justify-content:space-between;"><span>Risks</span><span style="font-weight:600;color:#1e293b;">{len(ch_risks)}</span></div>
                    <div style="display:flex;justify-content:space-between;"><span>Open</span><span style="font-weight:600;color:#dc2626;">{ch_open}</span></div>
                    <div style="display:flex;justify-content:space-between;"><span>Avg Residual</span><span style="font-weight:600;color:{ch_col};">{ch_avg:.1f}</span></div>
                    <div style="display:flex;justify-content:space-between;"><span>Volume</span><span style="font-weight:500;">{ch["daily_volume"]}</span></div>
                </div>
            </div>""",unsafe_allow_html=True)

    # Charts
    st.markdown('<div class="sh">📈 Risk Landscape</div>',unsafe_allow_html=True)
    vc1,vc2,vc3=st.columns([2,2,2])

    with vc1:
        # Residual risk by channel
        ch_names=list(CHANNELS.keys())
        ch_colors=[CHANNELS[c]["color"] for c in ch_names]
        ch_res_vals=[np.mean([r["_res"] for r in RCSA_DATA if r["channel"]==c]) for c in ch_names]
        fig_ch=go.Figure(go.Bar(x=ch_names,y=ch_res_vals,marker_color=ch_colors,text=[f"{v:.1f}" for v in ch_res_vals],textposition="outside"))
        fig_ch.update_layout(title="Avg Residual Risk by Channel",title_font_size=14,height=300,margin=dict(t=40,b=30,l=30,r=20),
            yaxis=dict(range=[0,max(ch_res_vals)*1.3],title="Score"),plot_bgcolor="white",yaxis_gridcolor="#f1f5f9")
        # Add threshold line
        fig_ch.add_hline(y=10,line_dash="dash",line_color="#ea580c",opacity=.5,annotation_text="High threshold",annotation_position="top right")
        st.plotly_chart(fig_ch,use_container_width=True)

    with vc2:
        # Rating distribution
        rats=[r["_rat"] for r in RCSA_DATA]
        ro=["Critical","High","Medium","Low"];rcm={"Critical":"#dc2626","High":"#ea580c","Medium":"#eab308","Low":"#22c55e"}
        rv=[rats.count(x) for x in ro];rn=[x for x in ro]
        fig_p=go.Figure(go.Pie(values=rv,labels=rn,marker_colors=[rcm[x] for x in rn],hole=.5,textinfo="label+value",textposition="outside",textfont=dict(size=11)))
        fig_p.update_layout(title="Risk Rating Distribution",title_font_size=14,height=300,margin=dict(t=40,b=20,l=20,r=20),showlegend=False)
        st.plotly_chart(fig_p,use_container_width=True)

    with vc3:
        # Control effectiveness distribution
        eff_vals=[r["ctrl_effectiveness"] for r in RCSA_DATA]
        eff_counts=[eff_vals.count(i) for i in range(1,6)]
        eff_colors=["#dc2626","#ea580c","#eab308","#22c55e","#059669"]
        fig_e=go.Figure(go.Bar(x=[EFF_LABELS[i] for i in range(1,6)],y=eff_counts,marker_color=eff_colors,text=eff_counts,textposition="outside"))
        fig_e.update_layout(title="Control Effectiveness",title_font_size=14,height=300,margin=dict(t=40,b=30,l=30,r=20),
            plot_bgcolor="white",yaxis_gridcolor="#f1f5f9",yaxis_title="Count")
        st.plotly_chart(fig_e,use_container_width=True)

    # Heatmap
    st.markdown('<div class="sh">🗺️ Risk Heatmap — Likelihood × Impact</div>',unsafe_allow_html=True)
    fig_h=go.Figure()
    for li in range(1,6):
        for im in range(1,6):
            _,bg=rr(li*im)
            fig_h.add_shape(type="rect",x0=im-.5,x1=im+.5,y0=li-.5,y1=li+.5,fillcolor=bg,opacity=.12,line=dict(color="white",width=2),layer="below")
            fig_h.add_annotation(x=im,y=li,text=str(li*im),showarrow=False,font=dict(size=10,color="rgba(0,0,0,.12)"))
    np.random.seed(99)
    for r in filtered:
        ch=CHANNELS[r["channel"]]
        jx,jy=np.random.uniform(-.2,.2),np.random.uniform(-.2,.2)
        fig_h.add_trace(go.Scatter(x=[r["impact"]+jx],y=[r["likelihood"]+jy],mode="markers+text",showlegend=False,
            marker=dict(size=20,color=ch["color"],line=dict(width=2,color="white"),opacity=.9,symbol="circle"),
            text=[r["id"]],textposition="middle center",textfont=dict(size=7,color="white"),
            hovertemplate=f"<b>{r['id']}: {r['risk_event'][:50]}...</b><br>Channel: {r['channel']}<br>L={r['likelihood']}, I={r['impact']}<br>Inherent: {r['_inh']} → Residual: {r['_res']}<br>Rating: {r['_rat']}<extra></extra>"))
    fig_h.update_layout(xaxis=dict(title="<b>Impact</b>",tickvals=[1,2,3,4,5],ticktext=list(I_LABELS.values()),range=[.3,5.7]),
        yaxis=dict(title="<b>Likelihood</b>",tickvals=[1,2,3,4,5],ticktext=list(L_LABELS.values()),range=[.3,5.7]),
        height=420,margin=dict(t=20,b=40,l=40,r=20),plot_bgcolor="white",font=dict(size=11))
    # Legend for channels
    for ch_name,ch_info in CHANNELS.items():
        fig_h.add_trace(go.Scatter(x=[None],y=[None],mode="markers",name=ch_name,marker=dict(size=10,color=ch_info["color"])))
    fig_h.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=.5))
    st.plotly_chart(fig_h,use_container_width=True)

with tab2:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">RCSA Register</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Full risk register with control assessment and gap analysis</p>',unsafe_allow_html=True)

    reg_rows=[]
    for r in filtered:
        reg_rows.append({"ID":r["id"],"Channel":f'{CHANNELS[r["channel"]]["icon"]} {r["channel"]}',
            "Risk Event":r["risk_event"][:60]+("..." if len(r["risk_event"])>60 else ""),
            "Category":r["risk_category"],"L":r["likelihood"],"I":r["impact"],
            "Inherent":r["_inh"],"Ctrl Eff":r["ctrl_effectiveness"],"Residual":r["_res"],
            "Rating":r["_rat"],"Gaps":r["_gap_count"],"Status":r["status"]})

    df_r=pd.DataFrame(reg_rows)
    def sr2(v):
        m={"Critical":"background-color:#fef2f2;color:#991b1b;font-weight:600","High":"background-color:#fff7ed;color:#9a3412;font-weight:600",
           "Medium":"background-color:#fefce8;color:#854d0e;font-weight:600","Low":"background-color:#f0fdf4;color:#166534;font-weight:600"}
        return m.get(v,"")
    def ss(v):
        return "background-color:#fef2f2;color:#991b1b;font-weight:600" if v=="Open" else "background-color:#f0fdf4;color:#166534;font-weight:600"

    if not df_r.empty:
        st.dataframe(df_r.style.map(sr2,subset=["Rating"]).map(ss,subset=["Status"]),use_container_width=True,hide_index=True,height=500)
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
            </div>
            <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;">{gap_tags}</div>
        </div>""",unsafe_allow_html=True)

with tab3:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Risk Detail View</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Detailed assessment for individual risk items</p>',unsafe_allow_html=True)

    sel_r=st.selectbox("Select Risk",
        [f"{r['id']} — [{r['channel']}] {r['risk_event'][:60]}" for r in filtered] if filtered else ["No risks match filter"],
        label_visibility="collapsed")

    if filtered and sel_r!="No risks match filter":
        ri=next(r for r in filtered if sel_r.startswith(r["id"]))
        rat_label,rat_col=rr(ri["_res"])
        red_pct=(1-ri["_res"]/ri["_inh"])*100

        m1,m2,m3,m4,m5=st.columns(5)
        with m1: mc("Inherent",f"{ri['_inh']}","L×I")
        with m2: mc("Ctrl Effectiveness",EFF_LABELS[ri["ctrl_effectiveness"]],f"{ri['ctrl_effectiveness']}/5")
        with m3: mc("Reduction",f"{red_pct:.0f}%","")
        with m4: mc("Residual",f"{ri['_res']:.0f}","After controls")
        with m5: st.markdown(f'<div class="mc" style="background:{rat_col};border:none;"><h3 style="color:rgba(255,255,255,.8);">Rating</h3><p class="v" style="color:white;">{rat_label}</p><p class="s" style="color:rgba(255,255,255,.7);">{ri["status"]}</p></div>',unsafe_allow_html=True)

        st.markdown("",unsafe_allow_html=True)
        dl,dr=st.columns([3,2])
        with dl:
            ch=CHANNELS[ri["channel"]]
            st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:12px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <span style="font-size:24px;">{ch["icon"]}</span>
                    <div><div style="font-size:16px;font-weight:600;color:#1e293b;">{ri["id"]} — {ri["risk_event"]}</div>
                    <div style="font-size:12px;color:#64748b;">{ri["channel"]} · {ri["process"]} · {ri["risk_category"]}</div></div>
                </div>
                <div style="margin-top:12px;padding-top:12px;border-top:1px solid #e2e8f0;">
                    <div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">Scoring</div>
                    <div style="font-size:13px;color:#475569;margin-top:4px;">Likelihood: <strong>{ri["likelihood"]}</strong> ({L_LABELS[ri["likelihood"]]}) · Impact: <strong>{ri["impact"]}</strong> ({I_LABELS[ri["impact"]]})</div>
                </div>
            </div>""",unsafe_allow_html=True)

            # Controls
            st.markdown(f'<div style="font-size:14px;font-weight:600;color:#1e293b;margin:12px 0 6px;">Existing Controls</div>',unsafe_allow_html=True)
            for ct,cd in ri["controls"]:
                cls_map={"Preventive":"ctrl-p","Detective":"ctrl-d","Corrective":"ctrl-c"}
                icon_map={"Preventive":"🟢","Detective":"🟡","Corrective":"🔴"}
                st.markdown(f'<div class="{cls_map.get(ct,"ctrl-d")}">{icon_map.get(ct,"")} <strong>{ct}:</strong> {cd}</div>',unsafe_allow_html=True)

            # Gaps
            st.markdown(f'<div style="font-size:14px;font-weight:600;color:#991b1b;margin:16px 0 6px;">⚠️ Control Gaps Identified ({ri["_gap_count"]})</div>',unsafe_allow_html=True)
            for g in ri["gaps"]:
                st.markdown(f'<span class="gap-tag">✗ {g}</span>',unsafe_allow_html=True)

            # Actions
            st.markdown(f'<div style="font-size:14px;font-weight:600;color:#1e40af;margin:16px 0 6px;">📋 Recommended Actions ({len(ri["actions"])})</div>',unsafe_allow_html=True)
            for desc,target,owner in ri["actions"]:
                st.markdown(f'<div class="action-item">→ {desc}<br><span style="font-size:11px;color:#6b7280;">Target: {target} · Owner: {owner}</span></div>',unsafe_allow_html=True)

        with dr:
            # Waterfall
            fig_w=go.Figure(go.Waterfall(x=["Inherent","Controls","Residual"],y=[ri["_inh"],-(ri["_inh"]-ri["_res"]),0],
                measure=["absolute","relative","total"],
                connector=dict(line=dict(color="#cbd5e1",dash="dot")),
                decreasing=dict(marker=dict(color="#22c55e")),totals=dict(marker=dict(color=rat_col)),
                text=[str(ri["_inh"]),f"-{ri['_inh']-ri['_res']:.0f}",f"{ri['_res']:.0f}"],textposition="outside",textfont=dict(size=13)))
            fig_w.update_layout(height=250,margin=dict(t=30,b=30),title="Risk Waterfall",plot_bgcolor="white",yaxis_gridcolor="#f1f5f9")
            st.plotly_chart(fig_w,use_container_width=True)

            # Control type breakdown
            ctrl_types=[ct for ct,_ in ri["controls"]]
            ct_counts={"Preventive":ctrl_types.count("Preventive"),"Detective":ctrl_types.count("Detective"),"Corrective":ctrl_types.count("Corrective")}
            fig_ct=go.Figure(go.Bar(x=list(ct_counts.keys()),y=list(ct_counts.values()),
                marker_color=["#22c55e","#eab308","#ef4444"],text=list(ct_counts.values()),textposition="outside"))
            fig_ct.update_layout(height=200,margin=dict(t=30,b=30),title="Control Types",plot_bgcolor="white",yaxis_gridcolor="#f1f5f9")
            st.plotly_chart(fig_ct,use_container_width=True)

with tab4:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">RCSA Methodology</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Assessment framework and process documentation</p>',unsafe_allow_html=True)

    st.markdown('<div class="sh">🏛️ Project Context</div>',unsafe_allow_html=True)
    st.markdown("""<div class="ib">
        <strong>Directorate of ICT, Directorate General of Taxes (DGT)</strong> — Ministry of Finance, Republic of Indonesia<br><br>
        As IT Governance & Regulatory Analyst (2019-2022), I conducted a comprehensive <strong>Risk & Control Self-Assessment</strong>
        of Indonesia's 4-channel API digital tax services pilot. The pilot enabled certified third-party tax application
        service providers to access DGT's core services (registration, billing, filing, invoicing) via API — replacing
        legacy web-based portals.<br><br>
        The RCSA identified <strong>critical control gaps</strong> across all four channels, assessed residual risk after existing
        controls, and produced <strong>actionable recommendations</strong> that were adopted into the agency's digital reform roadmap
        and informed the regulatory framework for third-party tax service providers.
    </div>""",unsafe_allow_html=True)

    st.markdown('<div class="sh">📐 RCSA Process</div>',unsafe_allow_html=True)
    p1,p2,p3,p4,p5=st.columns(5)
    steps=[("1️⃣","Scope","Define channels, processes, and API endpoints in scope"),
           ("2️⃣","Identify","Map risk events per process using workshops with channel owners"),
           ("3️⃣","Assess","Score likelihood & impact; evaluate control design and effectiveness"),
           ("4️⃣","Gap Analysis","Identify gaps between required and actual control coverage"),
           ("5️⃣","Action Plan","Define remediation actions with owners, targets, and KRIs")]
    for col,s in zip([p1,p2,p3,p4,p5],steps):
        with col: st.markdown(f'<div class="fc" style="text-align:center;"><div style="font-size:28px;margin-bottom:6px;">{s[0]}</div><h4>{s[1]}</h4><p style="font-size:13px;">{s[2]}</p></div>',unsafe_allow_html=True)

    st.markdown('<div class="sh">🔧 Control Type Framework</div>',unsafe_allow_html=True)
    ct1,ct2,ct3=st.columns(3)
    with ct1: st.markdown('<div class="fc"><h4 style="color:#16a34a;">🟢 Preventive Controls</h4><p>Designed to <strong>prevent</strong> a risk event from occurring. Most effective control type. Examples: input validation, access controls, segregation of duties, automated checks.</p></div>',unsafe_allow_html=True)
    with ct2: st.markdown('<div class="fc"><h4 style="color:#ca8a04;">🟡 Detective Controls</h4><p>Designed to <strong>detect</strong> a risk event after it has occurred. Enables timely response. Examples: reconciliation, audit sampling, anomaly detection, monitoring dashboards.</p></div>',unsafe_allow_html=True)
    with ct3: st.markdown('<div class="fc"><h4 style="color:#dc2626;">🔴 Corrective Controls</h4><p>Designed to <strong>correct or remediate</strong> after a risk event is detected. Last line of defense. Examples: rollback procedures, incident response, manual workarounds.</p></div>',unsafe_allow_html=True)

    st.markdown('<div class="sh">📊 Key Findings Summary</div>',unsafe_allow_html=True)
    st.markdown(f"""<div class="ib">
        <strong>Assessment Scope:</strong> {total} risk items across 4 API channels ({sum(CHANNELS[c]["api_endpoints"] for c in CHANNELS)} API endpoints total)<br><br>
        <strong>Key Findings:</strong><br>
        • <strong>{open_count} of {total} risks remain open</strong> requiring remediation action<br>
        • <strong>{total_gaps} control gaps</strong> identified — most critical in e-Billing reconciliation and e-Invoice fraud detection<br>
        • <strong>e-Billing payment reconciliation (B-002)</strong> has the highest residual risk — T+1 reconciliation creates 24h exposure window for unmatched payments<br>
        • <strong>e-Invoice fictitious invoice detection (I-002)</strong> has significant gap — ML model false positive rate at 12% and quarterly cross-matching too infrequent<br>
        • <strong>e-Filing peak season capacity (F-001)</strong> requires predictive scaling — current 3-5 minute auto-scaling lag is insufficient for March deadline spike<br><br>
        <strong>Overall Assessment:</strong> The 4-channel API platform has a reasonable baseline of preventive controls, but detective and corrective controls need strengthening. The transition from web-based to API-based services has introduced new risk vectors — particularly around concurrent processing, real-time validation, and third-party provider management — that the existing control framework was not designed for.
    </div>""",unsafe_allow_html=True)

st.divider()
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">RCSA Dashboard — Digital Tax Services 4-Channel API<br>Portfolio by <strong>Yayan Puji Riyanto</strong> · IT Governance & Regulatory Analyst, DGT (2019-2022)<br>PhD Candidate, Business Law & Taxation — Monash University<br><em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em></div>',unsafe_allow_html=True)
