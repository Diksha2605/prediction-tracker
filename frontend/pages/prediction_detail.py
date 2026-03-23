import streamlit as st
import plotly.graph_objects as go
from frontend.utils.api_client import get_prediction, update_confidence, resolve_prediction, delete_prediction
from frontend.utils.state import go_to

def show():
    pid = st.session_state.get("selected_id")
    if not pid: go_to("dashboard"); return
    p = get_prediction(pid)
    if not p: go_to("dashboard"); return

    if st.button("← Back"): go_to("dashboard")
    st.title(p["title"])
    if p["notes"]: st.caption(p["notes"])
    st.divider()

    c1,c2,c3 = st.columns(3)
    c1.metric("Current confidence", f"{p['current_confidence']}%")
    c2.metric("Change since start",
              f"{'+' if p['confidence_delta']>=0 else ''}{p['confidence_delta']}%")
    c3.metric("Status", p["status"].upper())

    logs = p.get("confidence_logs", [])
    if logs:
        st.subheader("Confidence decay chart")
        dates  = [l["logged_at"][:10] for l in logs]
        values = [l["confidence"]     for l in logs]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=values,
            mode="lines+markers",
            line=dict(color="#378ADD", width=2),
            marker=dict(size=7), fill="tozeroy",
            fillcolor="rgba(55,138,221,0.08)",
            hovertemplate="%{x}: %{y}%<extra></extra>"))
        fig.update_layout(yaxis=dict(range=[0,105], ticksuffix="%"),
            height=280, margin=dict(l=0,r=0,t=20,b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Update log")
        for l in reversed(logs):
            st.markdown(f"**{l['confidence']}%** — {l['logged_at'][:10]}" +
                        (f" · {l['note']}" if l.get("note") else ""))

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if p["status"] == "open":
            st.subheader("Update confidence")
            with st.form("upd"):
                nc = st.slider("New confidence", 1, 100, p["current_confidence"])
                nt = st.text_input("What changed?")
                if st.form_submit_button("Update", use_container_width=True):
                    update_confidence(pid, nc, nt); st.rerun()

    with col2:
        if p["status"] == "open":
            st.subheader("Resolve")
            if st.button("Mark correct", use_container_width=True, type="primary"):
                resolve_prediction(pid, "correct"); st.rerun()
            if st.button("Mark wrong", use_container_width=True):
                resolve_prediction(pid, "wrong"); st.rerun()
        if st.button("Delete", use_container_width=True):
            delete_prediction(pid); go_to("dashboard")