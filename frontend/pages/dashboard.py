import streamlit as st
from frontend.utils.api_client import get_predictions, create_prediction
from frontend.utils.state import go_to
from datetime import date

def show():
    st.title("My Predictions")
    predictions = get_predictions()
    total   = len(predictions)
    open_p  = [p for p in predictions if p["status"] == "open"]
    correct = [p for p in predictions if p["status"] == "correct"]
    wrong   = [p for p in predictions if p["status"] == "wrong"]
    accuracy = round(len(correct) / (len(correct)+len(wrong)) * 100) \
               if (correct or wrong) else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total",    total)
    c2.metric("Open",     len(open_p))
    c3.metric("Accuracy", f"{accuracy}%")
    c4.metric("Resolved", len(correct)+len(wrong))
    st.divider()
 
    col_left, col_right = st.columns([2, 1])

    with col_right:
        st.subheader("New prediction")
        with st.form("add_form", clear_on_submit=True):
            title      = st.text_input("Prediction *")
            notes      = st.text_area("Notes", height=80)
            deadline   = st.date_input("Deadline", value=None)
            confidence = st.slider("Confidence", 1, 100, 70)
            category   = st.text_input("Category (optional)")
            submitted  = st.form_submit_button("Save prediction", use_container_width=True)
        if submitted and title:
            data, code = create_prediction(title, notes, deadline, confidence, category)
            if code == 201: st.rerun()
            else: st.error("Could not save")

    with col_left:
        st.subheader("All predictions")
        fs = st.selectbox("Filter", ["All","open","correct","wrong"],
                           label_visibility="collapsed")
        filtered = predictions if fs == "All" else \
                   [p for p in predictions if p["status"] == fs]
        if not filtered: st.info("No predictions yet!")
        for p in filtered:
            conf  = p["current_confidence"]
            delta = p["confidence_delta"]
            icon  = "✅" if p["status"]=="correct" else "❌" if p["status"]=="wrong" else "🔵"
            ds    = f"({'+' if delta>=0 else ''}{delta}%)" if delta != 0 else ""
            with st.container(border=True):
                r1, r2 = st.columns([4, 1])
                with r1:
                    st.markdown(f"{icon} **{p['title']}**")
                    st.caption(f"Confidence: {conf}% {ds}  |  {p['status']}")
                    st.progress(conf / 100)
                with r2:
                    if st.button("View", key=p["id"]): go_to("detail", p["id"])
             