import streamlit as st
import pandas as pd
import requests

# --- Page Settings ---
st.set_page_config(layout="wide", page_title="Qlik Capability API + Gemini AI")

st.title("📊 Qlik + Gemini Hybrid Dashboard")

# --- Define Qlik Capability API iframe URLs ---
iframe_urls = {
    "Total Sales KPI": "http://localhost:4848/single/?appid=C%3A%5CUsers%5CAdmin%5CDocuments%5CQlik%5CSense%5CApps%5CSalesAppFromQVD.qvf&obj=KkmztG&opt=ctxmenu,currsel",
    "Sales by Region": "http://localhost:4848/single/?appid=C%3A%5CUsers%5CAdmin%5CDocuments%5CQlik%5CSense%5CApps%5CSalesAppFromQVD.qvf&obj=VYTMvY&opt=ctxmenu,currsel",
    "Sales Over Time": "http://localhost:4848/single/?appid=C%3A%5CUsers%5CAdmin%5CDocuments%5CQlik%5CSense%5CApps%5CSalesAppFromQVD.qvf&obj=pxhXYbA&opt=ctxmenu,currsel",
    "Filter Pane": "http://localhost:4848/single/?appid=C%3A%5CUsers%5CAdmin%5CDocuments%5CQlik%5CSense%5CApps%5CSalesAppFromQVD.qvf&obj=KBjuBja&opt=ctxmenu,currsel"
}

# --- Sidebar Tabs ---
selected_tab = st.sidebar.radio("Select View", ["Total Sales KPI", "Sales by Region", "Sales Over Time", "Filter Pane", "AI Dashboard"])

# --- Individual Iframe View ---
if selected_tab in iframe_urls:
    st.subheader(f"🧩 {selected_tab}")
    st.components.v1.iframe(iframe_urls[selected_tab], height=600, scrolling=True)

# --- Combined AI + Dashboard View ---
elif selected_tab == "AI Dashboard":
    st.subheader("🤖 Gemini AI Assistant on Qlik Data")

    # Gemini Assistant Section
    question = st.text_input("Ask a question about your Qlik data:", "Which product had highest sales?")
    if st.button("Ask Gemini"):
        with st.spinner("Fetching data and querying Gemini..."):
            try:
                res = requests.get("http://localhost:8000/ask", params={"question": question})
                if res.status_code == 200:
                    output = res.json()
                    st.success(output["answer"])
                    st.markdown("📦 **Raw Qlik Data:**")
                    df = pd.DataFrame(output["data"])
                    st.dataframe(df)
                else:
                    st.error("❌ Failed to get response from backend.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.markdown("---")
    st.subheader("📊 Full Qlik Dashboard")

    # Reduced height for tighter layout
    col1, col2 = st.columns(2)

    with col1:
        st.components.v1.iframe(iframe_urls["Total Sales KPI"], height=250, scrolling=True)
        st.components.v1.iframe(iframe_urls["Sales by Region"], height=300, scrolling=True)

    with col2:
        st.components.v1.iframe(iframe_urls["Sales Over Time"], height=300, scrolling=True)
        st.components.v1.iframe(iframe_urls["Filter Pane"], height=300, scrolling=True)

    st.caption("✅ All visualizations are synced and reflect dynamic selections using Qlik Capability API.")
