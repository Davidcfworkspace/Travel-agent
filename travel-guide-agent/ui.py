import streamlit as st
from travel_agent import build_travel_guide
import os

st.set_page_config(page_title="Travel Guide Agent", layout="centered")

st.title("🧭 Travel Guide Agent")
city = st.text_input("Destination city", "Tokyo")
start = st.text_input("Start date (YYYY-MM-DD)")
days = st.slider("Days", 1, 10, 4)
style = st.text_input("Trip style", "foodie")
budget = st.number_input("Budget per day (USD)", 0, 10000, 150)

if st.button("Build my guide"):
    guide = build_travel_guide(city, start, days, style, budget)
    
    if guide.startswith("Error"):
        st.error(guide)
    else:
        # Save to file for optional download
        with open("guide.md", "w", encoding="utf-8") as f:
            f.write(guide)

        st.download_button("Download guide.md", guide, file_name="guide.md")
        st.success("Guide generated! Scroll to preview below.")
        st.markdown(guide)
