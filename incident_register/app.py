"""
Operational Risk Incident Register & Reporting Dashboard
MDB Context — AIIB COR Function
Portfolio by Yayan Puji Riyanto
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="OR Incident Register — AIIB COR", page_icon="📑", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .block-container { padding-top: 3.5rem; max-width: 1200px; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0c1e3c 0%, #162d50 100%); }
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
    .inc-card { background:white; border:1px solid #e2e8f0; border-radius:12px; padding:18px; margin:8px 0; box-shadow:0 1px 3px rgba(0,0,0,.04); }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;} .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

SEVERITY = {1:"Low",2:"Medium",3:"High",4:"Critical"}
SEV_COLOR = {1:"#22c55e",2:"#eab308",3:"#ea580c",4:"#dc2626"}
STATUS_LIST = ["New","Under Investigation","Root Cause Identified","Remediation In Progress","Closed","Lessons Learned Captured"]
STATUS_COLOR = {"New":"#dc2626","Under Investigation":"#ea580c","Root Cause Identified":"#eab308","Remediation In Progress":"#3b82f6","Closed":"#22c55e","Lessons Learned Captured":"#059669"}
BASEL_CATS = ["Internal Fraud","External Fraud","Employment Practices","Clients, Products & Business Practices","Damage to Physical Assets","Business Disruption & System Failures","Execution, Delivery & Process Management"]
DEPARTMENTS = ["Treasury","Investment Operations","Corporate Services","IT","Legal","HR","Finance & Accounting","Risk Management"]
ROOT_CAUSES = ["Process Gap","Human Error","System Failure","External Event","Policy Gap","Training Deficiency","Vendor/Third-Party Failure","Design Flaw"]

def mc_render(l,v,s=""):
    st.markdown(f'<div class="mc"><h3>{l}</h3><p class="v">{v}</p><p class="s">{s}</p></div>',unsafe_allow_html=True)

# Sample incidents — realistic MDB context
INIT_INCIDENTS = [
    {"id":"INC-2025-001","date":"2025-01-14","reported_by":"Treasury Operations","department":"Treasury",
     "title":"Bond coupon payment delayed by 4 hours due to SWIFT message formatting error",
     "description":"A Sustainable Development Bond coupon payment of USD 12.3M was delayed by 4 hours due to an incorrect BIC code in the SWIFT MT202 message. The error was caught by the correspondent bank and returned for correction. Payment was reprocessed successfully within the same business day.",
     "category":"Execution, Delivery & Process Management","severity":2,
     "financial_impact":0,"currency":"USD","near_miss":False,
     "root_cause":"Human Error","root_cause_detail":"Manual entry of BIC code instead of using pre-populated template. Staff member was processing 3 concurrent payments.",
     "controls_failed":["Four-eyes check on SWIFT messages — checker did not verify BIC field"],
     "remediation":["Implement auto-population of BIC codes from beneficiary master data","Add specific BIC validation rule in SWIFT message pre-check","Refresh training on payment processing procedures"],
     "lessons":"Concurrent processing of multiple high-value payments increases error probability. Consider sequential processing or dedicated payment windows.",
     "status":"Remediation In Progress","closed_date":None,"days_open":None},
    {"id":"INC-2025-002","date":"2025-02-03","reported_by":"IT Security","department":"IT",
     "title":"Phishing email compromised staff credentials — no data exfiltration confirmed",
     "description":"A sophisticated spear-phishing email targeting 5 Investment Operations staff resulted in 1 credential compromise. The attacker gained access to the staff member's email for approximately 2 hours before SOC detected unusual login patterns from an IP in Eastern Europe. Account was locked, password reset enforced, and forensic analysis confirmed no sensitive data was accessed or exfiltrated.",
     "category":"External Fraud","severity":3,
     "financial_impact":0,"currency":"USD","near_miss":True,
     "root_cause":"External Event","root_cause_detail":"Highly targeted phishing using scraped LinkedIn data to impersonate a co-financing partner. Email passed SPF/DKIM checks via compromised sender domain.",
     "controls_failed":["Phishing awareness — staff clicked link despite training","Email filtering — message bypassed URL scanning due to zero-day domain"],
     "remediation":["Deploy advanced URL sandboxing for all inbound links","Conduct targeted phishing simulation for Investment Operations","Implement hardware security keys for high-privilege accounts","Report compromised domain to relevant CERT"],
     "lessons":"Spear-phishing using co-financing partner impersonation is a credible attack vector for MDBs. Staff with access to member country data require enhanced protection.",
     "status":"Closed","closed_date":"2025-03-01","days_open":26},
    {"id":"INC-2025-003","date":"2025-02-18","reported_by":"Investment Operations","department":"Investment Operations",
     "title":"Sovereign loan disbursement of USD 25M sent to incorrect beneficiary account",
     "description":"A USD 25M tranche of a sovereign-backed infrastructure loan was disbursed to an incorrect beneficiary account at the Central Bank of the borrowing country. The error was caused by outdated account details in the disbursement instruction. The funds were recovered within 5 business days through the Central Bank's internal transfer, but the project implementation was delayed by 2 weeks.",
     "category":"Execution, Delivery & Process Management","severity":3,
     "financial_impact":25000,"currency":"USD","near_miss":False,
     "root_cause":"Process Gap","root_cause_detail":"Disbursement instruction template contained account details from a previous loan to the same country. No mandatory re-confirmation of account details was required before disbursement.",
     "controls_failed":["Beneficiary account validation — no re-confirmation step for repeat borrowers","Disbursement template management — outdated templates not archived"],
     "remediation":["Mandate beneficiary account re-confirmation for every disbursement regardless of borrower history","Implement template version control with automatic expiry after 6 months","Add automated account number validation against Central Bank directory"],
     "lessons":"Repeat borrower familiarity creates complacency risk. Controls must be equally rigorous for first-time and repeat disbursements.",
     "status":"Lessons Learned Captured","closed_date":"2025-04-01","days_open":42},
    {"id":"INC-2025-004","date":"2025-03-05","reported_by":"HR","department":"HR",
     "title":"Unauthorized access to staff compensation data via shared drive misconfiguration",
     "description":"Compensation data for 120 Beijing-based staff (including salary bands and bonus amounts) was inadvertently made accessible to all staff via a misconfigured shared drive folder. The exposure lasted approximately 3 weeks before being reported by a staff member. No evidence of external access or data download beyond normal HR team access.",
     "category":"Employment Practices","severity":2,
     "financial_impact":0,"currency":"USD","near_miss":False,
     "root_cause":"System Failure","root_cause_detail":"IT team migrated HR shared drive to new server without replicating folder-level access permissions. Default permissions were set to 'all staff read access'.",
     "controls_failed":["Access control replication during migration — permissions not verified post-migration","Data classification enforcement — sensitive HR data not flagged for restricted access"],
     "remediation":["Implement mandatory access permission verification checklist for all data migrations","Deploy automated data classification scanning for PII/compensation data","Conduct access review of all shared drives within 30 days"],
     "lessons":"System migrations are high-risk events for access control failures. All migrations involving sensitive data require explicit access permission verification as a go-live gate.",
     "status":"Remediation In Progress","closed_date":None,"days_open":None},
    {"id":"INC-2025-005","date":"2025-03-22","reported_by":"Compliance","department":"Risk Management",
     "title":"Sanctions screening gap: sub-contractor on OFAC SDN list not detected during project appraisal",
     "description":"During a post-approval review, COR identified that a sub-contractor engaged on an AIIB co-financed transport project had been added to the OFAC SDN list 6 months prior to project approval. The sub-contractor was not screened because the screening was only performed on the primary contractor. The sub-contractor's involvement was limited to non-critical earthwork services (USD 2.1M contract value). The sub-contract was terminated and replaced.",
     "category":"Clients, Products & Business Practices","severity":3,
     "financial_impact":2100,"currency":"USD","near_miss":False,
     "root_cause":"Process Gap","root_cause_detail":"Sanctions screening policy required screening of primary counterparties only. Sub-contractors below USD 5M threshold were excluded from mandatory screening scope.",
     "controls_failed":["Sanctions screening scope — sub-contractors below threshold excluded","Ongoing monitoring — no periodic re-screening of project counterparties post-approval"],
     "remediation":["Expand sanctions screening to all sub-contractors regardless of contract value","Implement quarterly re-screening of all active project counterparties","Update AML/CFT policy to align with expanded screening scope","Notify co-financing partner (World Bank) of gap and remediation"],
     "lessons":"In co-financed projects with complex supply chains, screening scope must extend to all tiers of the contractor hierarchy. Threshold-based exclusions create unacceptable compliance risk.",
     "status":"Under Investigation","closed_date":None,"days_open":None},
    {"id":"INC-2025-006","date":"2025-04-02","reported_by":"Finance & Accounting","department":"Finance & Accounting",
     "title":"Duplicate vendor payment of USD 340K due to invoice number format mismatch",
     "description":"A vendor invoice for IT consulting services (USD 340K) was paid twice because the same invoice was submitted in two different formats (PDF and e-invoice) with slightly different invoice number formats (INV-2025-0891 vs INV/2025/0891). The duplicate payment detection system treated them as distinct invoices. The duplicate was identified during month-end reconciliation and recovery was initiated.",
     "category":"Execution, Delivery & Process Management","severity":2,
     "financial_impact":340,"currency":"USD","near_miss":False,
     "root_cause":"Design Flaw","root_cause_detail":"Duplicate detection logic uses exact string matching on invoice numbers. Different formatting (hyphens vs slashes) bypasses the check.",
     "controls_failed":["Duplicate invoice detection — exact match logic too rigid","Vendor payment review — checker approved without cross-referencing recent payments to same vendor"],
     "remediation":["Implement fuzzy matching for invoice number duplicate detection (normalize separators)","Add vendor-amount-date combination as secondary duplicate check","Recovery of USD 340K from vendor (in progress)"],
     "lessons":"Duplicate detection controls must account for format variations. Combining multiple matching criteria (vendor + amount + date range) provides more robust protection than single-field matching.",
     "status":"Remediation In Progress","closed_date":None,"days_open":None},
    {"id":"INC-2024-007","date":"2024-11-15","reported_by":"Investment Operations","department":"Investment Operations",
     "title":"ESF complaint: inadequate resettlement compensation in road project — PPM referral",
     "description":"The Project-affected People's Mechanism (PPM) received a complaint from 45 households affected by an AIIB-financed road improvement project. Complainants alleged that resettlement compensation was below market rate and that the grievance redress mechanism at the project level was unresponsive. PPM initiated a compliance review. Investigation found that the borrower's compensation methodology deviated from AIIB ESF requirements.",
     "category":"Clients, Products & Business Practices","severity":3,
     "financial_impact":0,"currency":"USD","near_miss":False,
     "root_cause":"Vendor/Third-Party Failure","root_cause_detail":"Borrower's implementing agency used outdated land valuation methodology not compliant with ESF Standard 2 (Involuntary Resettlement). AIIB supervision mission in Q2 2024 noted the issue but did not escalate.",
     "controls_failed":["ESF supervision — issue noted but not escalated per protocol","Grievance redress mechanism — project-level GRM was non-functional for 4 months"],
     "remediation":["Require borrower to engage independent land valuator and provide top-up compensation","Strengthen ESF supervision escalation protocols — any Standard 2 deviation requires immediate CRO notification","Provide technical assistance to borrower on GRM operationalization"],
     "lessons":"ESF supervision findings must trigger immediate escalation when related to involuntary resettlement (Standard 2). Delayed escalation compounds reputational risk and community impact.",
     "status":"Closed","closed_date":"2025-02-28","days_open":105},
    {"id":"INC-2024-008","date":"2024-10-08","reported_by":"IT","department":"IT",
     "title":"Core banking system unplanned downtime — 6 hours during Asian business hours",
     "description":"The core banking system experienced an unplanned outage lasting 6 hours (02:00-08:00 UTC, covering full Asian business hours) due to a database cluster failover that did not complete successfully. During the outage, loan disbursements, treasury transactions, and portfolio reporting were unavailable. 3 time-sensitive disbursements were delayed to the next business day.",
     "category":"Business Disruption & System Failures","severity":3,
     "financial_impact":0,"currency":"USD","near_miss":False,
     "root_cause":"System Failure","root_cause_detail":"Database cluster failover mechanism had an untested edge case where simultaneous write operations from 2 application servers caused a split-brain condition. The issue was not detected in the last DR test because the test did not simulate concurrent writes.",
     "controls_failed":["DR testing — test scenario did not cover concurrent write failover","System monitoring — alerting threshold for failover completion was 30 minutes, too long"],
     "remediation":["Update DR test scenarios to include concurrent write failover simulation","Reduce failover completion alert threshold from 30 to 5 minutes","Implement automated rollback to primary if failover does not complete within 10 minutes","Establish manual payment processing procedure for critical disbursements during outages"],
     "lessons":"DR test scenarios must be continuously updated to reflect real-world usage patterns. As system load increases, edge cases in failover mechanisms become more likely to manifest.",
     "status":"Lessons Learned Captured","closed_date":"2025-01-15","days_open":99},
]

if "incidents" not in st.session_state:
    st.session_state.incidents = [dict(inc) for inc in INIT_INCIDENTS]
if "inc_audit" not in st.session_state:
    st.session_state.inc_audit = []

INC = st.session_state.incidents

# Compute days_open for open incidents
today = datetime.now()
for inc in INC:
    d = datetime.strptime(inc["date"], "%Y-%m-%d")
    if inc["closed_date"]:
        inc["days_open"] = (datetime.strptime(inc["closed_date"], "%Y-%m-%d") - d).days
    else:
        inc["days_open"] = (today - d).days

total = len(INC)
open_inc = [i for i in INC if i["status"] not in ("Closed","Lessons Learned Captured")]
closed_inc = [i for i in INC if i["status"] in ("Closed","Lessons Learned Captured")]
near_misses = sum(1 for i in INC if i.get("near_miss"))
total_fin = sum(i["financial_impact"] for i in INC)
avg_days = np.mean([i["days_open"] for i in closed_inc]) if closed_inc else 0

# SIDEBAR
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:10px 0 18px;'>
        <div style='font-size:36px;margin-bottom:4px;'>📑</div>
        <div style='font-size:17px;font-weight:700;color:#f1f5f9!important;'>Incident Register</div>
        <div style='font-size:12px;color:#94a3b8!important;margin-top:4px;'>Operational Risk — AIIB COR</div>
    </div>""",unsafe_allow_html=True)
    st.divider()

    f_status = st.multiselect("Status", STATUS_LIST, default=STATUS_LIST)
    f_sev = st.multiselect("Severity", [1,2,3,4], default=[1,2,3,4], format_func=lambda x: f"{x} — {SEVERITY[x]}")
    f_cat = st.multiselect("Category", BASEL_CATS, default=BASEL_CATS)
    filtered = [i for i in INC if i["status"] in f_status and i["severity"] in f_sev and i["category"] in f_cat]

    st.divider()
    st.markdown(f"""<div style='padding:6px 0;font-size:12px;'>
        <div style='color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Summary</div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Total</span><span style='font-weight:600;color:#f1f5f9!important;'>{total}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Open</span><span style='font-weight:600;color:#fca5a5!important;'>{len(open_inc)}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Closed</span><span style='font-weight:600;color:#86efac!important;'>{len(closed_inc)}</span></div>
        <div style='display:flex;justify-content:space-between;margin:5px 0;'><span>Near Misses</span><span style='font-weight:600;color:#fde047!important;'>{near_misses}</span></div>
    </div>""",unsafe_allow_html=True)
    st.divider()

    exp = [{"ID":i["id"],"Date":i["date"],"Title":i["title"],"Category":i["category"],"Severity":SEVERITY[i["severity"]],
            "Status":i["status"],"Financial Impact":i["financial_impact"],"Root Cause":i["root_cause"],"Days Open":i["days_open"]} for i in INC]
    st.download_button("💾 Export to CSV", data=pd.DataFrame(exp).to_csv(index=False).encode("utf-8"),
                       file_name="incident_register.csv", mime="text/csv", use_container_width=True)
    st.divider()
    st.markdown("""<div style='font-size:11px;color:#64748b;line-height:1.6;'>
        <strong style='color:#94a3b8!important;'>Context</strong><br>
        Prototype incident register for AIIB COR — capturing, categorizing, and reporting operational risk events with root cause analysis and lessons learned.<br><br>
        <strong style='color:#94a3b8!important;'>Portfolio by</strong><br>Yayan Puji Riyanto<br>PhD Candidate — Monash University
    </div>""",unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard & Reporting","📋 Incident Register","🔍 Incident Detail","➕ Log New Incident"])

# ═══ TAB 1: DASHBOARD ═══
with tab1:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Incident Reporting Dashboard</h1><p style="font-size:15px;color:#64748b;margin-top:0;">AIIB Compliance & Operational Risk — Incident Monitoring & Trend Analysis</p>',unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: mc_render("Total Incidents", total, "All time")
    with c2: mc_render("Open", len(open_inc), f"{len(open_inc)/total:.0%} of total" if total else "")
    with c3: mc_render("Near Misses", near_misses, "No actual loss")
    with c4: mc_render("Avg Resolution", f"{avg_days:.0f}d", "Closed incidents")
    with c5: mc_render("High+Critical", sum(1 for i in INC if i["severity"]>=3), "Requiring escalation")
    with c6: mc_render("Financial Impact", f"${total_fin/1000:.0f}K" if total_fin<1e6 else f"${total_fin/1e6:.1f}M", "Total reported")

    st.markdown('<div class="sh">📈 Trend Analysis</div>',unsafe_allow_html=True)
    t1,t2 = st.columns([3,2])
    with t1:
        # Monthly trend
        inc_dates = [datetime.strptime(i["date"],"%Y-%m-%d") for i in INC]
        months = sorted(set(d.strftime("%Y-%m") for d in inc_dates))
        month_counts = [sum(1 for d in inc_dates if d.strftime("%Y-%m")==m) for m in months]
        month_sev3 = [sum(1 for i in INC if datetime.strptime(i["date"],"%Y-%m-%d").strftime("%Y-%m")==m and i["severity"]>=3) for m in months]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(x=months, y=month_counts, name="All Incidents", marker_color="#3b82f6", text=month_counts, textposition="outside"))
        fig_trend.add_trace(go.Bar(x=months, y=month_sev3, name="High/Critical", marker_color="#dc2626", text=month_sev3, textposition="outside"))
        fig_trend.update_layout(title="Monthly Incident Volume", title_font_size=14, height=300, margin=dict(t=40,b=30),
                                plot_bgcolor="white", barmode="overlay", yaxis_gridcolor="#f1f5f9", legend=dict(orientation="h",y=1.15))
        st.plotly_chart(fig_trend, use_container_width=True)

    with t2:
        # Status breakdown
        status_counts = {s: sum(1 for i in INC if i["status"]==s) for s in STATUS_LIST if sum(1 for i in INC if i["status"]==s)>0}
        fig_status = go.Figure(go.Pie(values=list(status_counts.values()), labels=list(status_counts.keys()),
            marker_colors=[STATUS_COLOR[s] for s in status_counts.keys()], hole=.5, textinfo="label+value", textposition="outside", textfont=dict(size=10)))
        fig_status.update_layout(title="Status Breakdown", title_font_size=14, height=300, margin=dict(t=40,b=10), showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)

    st.markdown('<div class="sh">📊 Analysis</div>',unsafe_allow_html=True)
    a1,a2,a3 = st.columns(3)
    with a1:
        cat_counts = {}
        for i in INC: cat_counts[i["category"]] = cat_counts.get(i["category"],0)+1
        fig_bc = go.Figure(go.Bar(y=list(cat_counts.keys()), x=list(cat_counts.values()), orientation="h",
            marker_color="#3b82f6", text=list(cat_counts.values()), textposition="auto"))
        fig_bc.update_layout(title="By Basel Category", title_font_size=14, height=280, margin=dict(t=40,b=10,l=10,r=10),
            plot_bgcolor="white", xaxis=dict(showgrid=False,showticklabels=False), yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig_bc, use_container_width=True)

    with a2:
        rc_counts = {}
        for i in INC: rc_counts[i["root_cause"]] = rc_counts.get(i["root_cause"],0)+1
        rc_sorted = dict(sorted(rc_counts.items(), key=lambda x:x[1], reverse=True))
        fig_rc = go.Figure(go.Bar(y=list(rc_sorted.keys()), x=list(rc_sorted.values()), orientation="h",
            marker_color="#7c3aed", text=list(rc_sorted.values()), textposition="auto"))
        fig_rc.update_layout(title="By Root Cause", title_font_size=14, height=280, margin=dict(t=40,b=10,l=10,r=10),
            plot_bgcolor="white", xaxis=dict(showgrid=False,showticklabels=False), yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig_rc, use_container_width=True)

    with a3:
        dept_counts = {}
        for i in INC: dept_counts[i["department"]] = dept_counts.get(i["department"],0)+1
        dept_sorted = dict(sorted(dept_counts.items(), key=lambda x:x[1], reverse=True))
        fig_dept = go.Figure(go.Bar(y=list(dept_sorted.keys()), x=list(dept_sorted.values()), orientation="h",
            marker_color="#059669", text=list(dept_sorted.values()), textposition="auto"))
        fig_dept.update_layout(title="By Department", title_font_size=14, height=280, margin=dict(t=40,b=10,l=10,r=10),
            plot_bgcolor="white", xaxis=dict(showgrid=False,showticklabels=False), yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig_dept, use_container_width=True)

    # Aging analysis
    st.markdown('<div class="sh">⏱️ Open Incident Aging</div>',unsafe_allow_html=True)
    if open_inc:
        aging_data = []
        for i in sorted(open_inc, key=lambda x:x["days_open"], reverse=True):
            color = "#dc2626" if i["days_open"]>60 else "#ea580c" if i["days_open"]>30 else "#eab308" if i["days_open"]>14 else "#22c55e"
            aging_data.append({"ID":i["id"],"days":i["days_open"],"title":i["title"][:50],"color":color,"sev":i["severity"]})
        fig_aging = go.Figure(go.Bar(
            y=[a["ID"] for a in aging_data], x=[a["days"] for a in aging_data], orientation="h",
            marker_color=[a["color"] for a in aging_data],
            text=[f'{a["days"]}d — {a["title"]}' for a in aging_data], textposition="auto", textfont=dict(size=10)))
        fig_aging.add_vline(x=30, line_dash="dash", line_color="#ea580c", opacity=.5, annotation_text="30d SLA")
        fig_aging.add_vline(x=60, line_dash="dash", line_color="#dc2626", opacity=.5, annotation_text="60d escalation")
        fig_aging.update_layout(height=40+len(aging_data)*45, margin=dict(t=10,b=20,l=10,r=10), plot_bgcolor="white",
            xaxis=dict(title="Days Open"), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_aging, use_container_width=True)
    else:
        st.success("No open incidents.")

# ═══ TAB 2: REGISTER ═══
with tab2:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Incident Register</h1><p style="font-size:15px;color:#64748b;margin-top:0;">All recorded operational risk incidents</p>',unsafe_allow_html=True)

    reg_rows = []
    for i in filtered:
        reg_rows.append({"ID":i["id"],"Date":i["date"],"Title":i["title"][:55]+("..." if len(i["title"])>55 else ""),
            "Category":i["category"],"Severity":f'{i["severity"]} — {SEVERITY[i["severity"]]}',
            "Department":i["department"],"Root Cause":i["root_cause"],
            "Status":i["status"],"Days":i["days_open"],
            "Financial":f'${i["financial_impact"]:,}' if i["financial_impact"]>0 else "—"})
    df_inc = pd.DataFrame(reg_rows)

    def sev_style(v):
        if "Critical" in str(v): return "background-color:#fef2f2;color:#991b1b;font-weight:600"
        if "High" in str(v): return "background-color:#fff7ed;color:#9a3412;font-weight:600"
        if "Medium" in str(v): return "background-color:#fefce8;color:#854d0e"
        return "background-color:#f0fdf4;color:#166534"
    def stat_style(v):
        if v in ("New","Under Investigation"): return "background-color:#fef2f2;color:#991b1b;font-weight:600"
        if v in ("Root Cause Identified","Remediation In Progress"): return "background-color:#eff6ff;color:#1e40af;font-weight:600"
        return "background-color:#f0fdf4;color:#166534;font-weight:600"

    if not df_inc.empty:
        st.dataframe(df_inc.style.map(sev_style,subset=["Severity"]).map(stat_style,subset=["Status"]),
                     use_container_width=True, hide_index=True, height=450)
    else:
        st.info("No incidents match filter.")

# ═══ TAB 3: DETAIL ═══
with tab3:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Incident Detail</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Full incident report with root cause analysis and remediation</p>',unsafe_allow_html=True)

    if not filtered:
        st.info("No incidents match filter."); st.stop()
    sel = st.selectbox("Select Incident", [f"{i['id']} — {i['title'][:60]}" for i in filtered], label_visibility="collapsed")
    inc = next(i for i in filtered if sel.startswith(i["id"]))

    sev_col = SEV_COLOR[inc["severity"]]
    m1,m2,m3,m4,m5 = st.columns(5)
    with m1: mc_render("Date", inc["date"], "Reported")
    with m2: mc_render("Severity", SEVERITY[inc["severity"]], f"Level {inc['severity']}/4")
    with m3: mc_render("Days Open", f"{inc['days_open']}", "Closed" if inc["closed_date"] else "Active")
    with m4: mc_render("Financial", f'${inc["financial_impact"]:,}' if inc["financial_impact"]>0 else "Nil", inc["currency"])
    with m5: st.markdown(f'<div class="mc" style="background:{STATUS_COLOR.get(inc["status"],"#64748b")};border:none;"><h3 style="color:rgba(255,255,255,.8);">Status</h3><p class="v" style="color:white;font-size:16px;">{inc["status"]}</p></div>',unsafe_allow_html=True)

    st.markdown("",unsafe_allow_html=True)
    dl,dr = st.columns([3,2])
    with dl:
        nm_tag = '<span style="background:#fefce8;color:#854d0e;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;margin-left:8px;">NEAR MISS</span>' if inc.get("near_miss") else ""
        st.markdown(f"""<div class="inc-card">
            <div style="font-size:16px;font-weight:600;color:#1e293b;margin-bottom:6px;">{inc["id"]} — {inc["title"]}{nm_tag}</div>
            <div style="font-size:12px;color:#64748b;margin-bottom:12px;">{inc["category"]} · {inc["department"]} · Reported by: {inc["reported_by"]}</div>
            <div style="font-size:13px;color:#475569;line-height:1.6;">{inc["description"]}</div>
        </div>""",unsafe_allow_html=True)

        # Root Cause
        st.markdown(f"""<div class="inc-card" style="border-left:4px solid #7c3aed;">
            <div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">Root Cause Analysis</div>
            <div style="margin-top:6px;"><span style="background:#f5f3ff;color:#6d28d9;padding:3px 10px;border-radius:10px;font-size:12px;font-weight:600;">{inc["root_cause"]}</span></div>
            <div style="font-size:13px;color:#475569;margin-top:8px;line-height:1.5;">{inc["root_cause_detail"]}</div>
        </div>""",unsafe_allow_html=True)

        # Controls that failed
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#991b1b;margin:14px 0 6px;">❌ Controls That Failed ({len(inc["controls_failed"])})</div>',unsafe_allow_html=True)
        for cf in inc["controls_failed"]:
            st.markdown(f'<div style="background:#fef2f2;border-left:3px solid #dc2626;padding:7px 12px;border-radius:0 6px 6px 0;margin:3px 0;font-size:13px;color:#991b1b;">✗ {cf}</div>',unsafe_allow_html=True)

        # Remediation
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#1e40af;margin:14px 0 6px;">🔧 Remediation Actions ({len(inc["remediation"])})</div>',unsafe_allow_html=True)
        for rm in inc["remediation"]:
            st.markdown(f'<div style="background:#eff6ff;border-left:3px solid #3b82f6;padding:7px 12px;border-radius:0 6px 6px 0;margin:3px 0;font-size:13px;color:#1e40af;">→ {rm}</div>',unsafe_allow_html=True)

    with dr:
        # Lessons learned
        if inc["lessons"]:
            st.markdown(f"""<div class="inc-card" style="border-left:4px solid #059669; background:#f0fdf4;">
                <div style="font-size:12px;font-weight:600;color:#064e3b;text-transform:uppercase;letter-spacing:.5px;">💡 Lessons Learned</div>
                <div style="font-size:13px;color:#166534;margin-top:8px;line-height:1.6;">{inc["lessons"]}</div>
            </div>""",unsafe_allow_html=True)

        # Timeline
        st.markdown(f"""<div class="inc-card">
            <div style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">📅 Timeline</div>
            <div style="margin-top:10px;font-size:13px;color:#475569;">
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#94a3b8;">Reported:</span><strong>{inc["date"]}</strong></div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#94a3b8;">Status:</span><strong>{inc["status"]}</strong></div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#94a3b8;">Days Open:</span><strong>{inc["days_open"]}</strong></div>
                {"<div style='display:flex;gap:8px;margin:6px 0;'><span style='color:#94a3b8;'>Closed:</span><strong>"+inc["closed_date"]+"</strong></div>" if inc["closed_date"] else ""}
            </div>
        </div>""",unsafe_allow_html=True)

        # Status update
        st.markdown("##### Update Status")
        new_status = st.selectbox("New Status", STATUS_LIST, index=STATUS_LIST.index(inc["status"]), key="status_update")
        if st.button("Update", use_container_width=True, type="primary"):
            if new_status != inc["status"]:
                old_s = inc["status"]
                inc["status"] = new_status
                if new_status in ("Closed","Lessons Learned Captured") and not inc["closed_date"]:
                    inc["closed_date"] = today.strftime("%Y-%m-%d")
                st.session_state.inc_audit.append({"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ID":inc["id"],"Change":f"Status: {old_s} → {new_status}"})
                st.rerun()

# ═══ TAB 4: LOG NEW ═══
with tab4:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#0f172a;margin-bottom:4px;">Log New Incident</h1><p style="font-size:15px;color:#64748b;margin-top:0;">Capture and record a new operational risk event</p>',unsafe_allow_html=True)

    with st.form("new_incident"):
        f1,f2 = st.columns([3,2])
        with f1:
            n_title = st.text_input("Incident Title", placeholder="Brief description of the event")
            n_desc = st.text_area("Full Description", placeholder="What happened, when, how it was discovered, immediate impact...", height=120)
            n_cat = st.selectbox("Basel Category", BASEL_CATS)
            n_dept = st.selectbox("Department", DEPARTMENTS)
            n_reported = st.text_input("Reported By", placeholder="Name or team")
            n_ctrls = st.text_area("Controls That Failed (one per line)", height=60)
            n_remed = st.text_area("Remediation Actions (one per line)", height=60)
        with f2:
            n_date = st.date_input("Incident Date", value=today)
            n_sev = st.select_slider("Severity", options=[1,2,3,4], format_func=lambda x: f"{x} — {SEVERITY[x]}", value=2)
            n_fin = st.number_input("Financial Impact (USD)", min_value=0, value=0, step=1000)
            n_nm = st.checkbox("Near Miss (no actual loss)")
            n_rc = st.selectbox("Root Cause Category", ROOT_CAUSES)
            n_rc_detail = st.text_area("Root Cause Detail", height=60)
            n_lessons = st.text_area("Lessons Learned (if known)", height=60)

        sub = st.form_submit_button("📋 Log Incident", use_container_width=True, type="primary")

    if sub and n_title:
        new_id = f"INC-{n_date.year}-{len(st.session_state.incidents)+1:03d}"
        new_inc = {
            "id":new_id, "date":n_date.strftime("%Y-%m-%d"), "reported_by":n_reported or "Unknown", "department":n_dept,
            "title":n_title, "description":n_desc, "category":n_cat, "severity":n_sev,
            "financial_impact":n_fin, "currency":"USD", "near_miss":n_nm,
            "root_cause":n_rc, "root_cause_detail":n_rc_detail,
            "controls_failed":[c.strip() for c in n_ctrls.split("\n") if c.strip()],
            "remediation":[r.strip() for r in n_remed.split("\n") if r.strip()],
            "lessons":n_lessons, "status":"New", "closed_date":None, "days_open":0
        }
        st.session_state.incidents.append(new_inc)
        st.session_state.inc_audit.append({"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ID":new_id,"Change":"CREATED"})
        st.success(f"✅ **{new_id}** logged successfully.")
        st.rerun()

st.divider()
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">OR Incident Register — AIIB COR Context<br>Portfolio by <strong>Yayan Puji Riyanto</strong> · PhD, Business Law & Taxation — Monash University · MS Business Analytics — CU Boulder<br><em>Prepared for AIIB Operational Risk Intern (Ref. 25238)</em></div>',unsafe_allow_html=True)
