import streamlit as st
from frontend.utils.api_client import get_calibration, get_bias_report

def show():
    st.title("Calibration & Bias Report")
    st.caption("How well-calibrated is your judgment?")
    st.divider()

    cal  = get_calibration()
    data = cal.get("data", {})
    if not data:
        st.info("Resolve some predictions first to see your calibration score.")
        return
    
    st.subheader("Calibration score")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Brier score",     data.get("brier_score", "—"))
    c2.metric("Skill score",     data.get("brier_skill_score", "—"))
    c3.metric("Avg confidence",  f"{data.get('avg_confidence','—')}%")
    c4.metric("Actual accuracy", f"{data.get('actual_accuracy','—')}%")

    gap = data.get("overconfidence_gap", 0)
    if   gap >  0.05: st.warning(f"Overconfident by {round(gap*100,1)}%")
    elif gap < -0.05: st.info(f"Underconfident by {round(abs(gap)*100,1)}%")
    else: st.success("Your confidence is well calibrated!")

    st.divider()
    st.subheader("Bias report")
    bias = get_bias_report().get("data", {})
    if not bias: st.info("Not enough data yet."); return

    b1,b2,b3 = st.columns(3)
    oc = bias.get("overconfidence", {})
    an = bias.get("anchoring", {})
    he = bias.get("hedging", {})
    with b1:
        st.markdown("**Overconfidence**")
        st.error(oc.get("message","")) if oc.get("detected") else st.success("Not detected")
    with b2:
        st.markdown("**Anchoring**")
        st.warning(an.get("message","")) if an.get("detected") else st.success("Not detected")
    with b3:
        st.markdown("**Hedging**")
        st.warning(he.get("message","")) if he.get("detected") else st.success("Not detected")