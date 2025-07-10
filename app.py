import streamlit as st
import datetime
from openai import OpenAI

# ---- CONFIG ----
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- FUNCTIONS ----
def generate_event_list(date_str):
    prompt = f"""
    You are a historical events researcher. Given the date {date_str}, return a list of 5–7 unique, strange, or little-known events from 1900 to the present. Prioritize topics in space, war, science, pop culture, or government history. Format as:

    1. Event Title (Year) – One-sentence hook
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error fetching events: {e}")
        return "Failed to fetch events."

def generate_script(event_title, style, conspiracy):
    conspiracy_prompt = "Include known conspiracy theories." if conspiracy else "Do not include any conspiracies."
    prompt = f"""
    You are a voice-over narrator creating a 2-minute script for a short-form video on the event: "{event_title}". Write in a compelling tone with short, vivid sentences. Add visual suggestions in brackets. Style: {style}. {conspiracy_prompt}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating script: {e}")
        return "Script generation failed."

# ---- UI ----
st.title("📅 Daily Historical Event Script Generator")

# 1. Date Picker
date_input = st.date_input("Choose a date:", value=datetime.date.today())
formatted_date = date_input.strftime("%B %d")

# 2. Generate Events Button
if st.button("🔍 Generate Events for this Day"):
    with st.spinner("Fetching unique events..."):
        events = generate_event_list(formatted_date)
    st.session_state["events_list"] = events

# 3. Show Events List
if "events_list" in st.session_state:
    st.subheader("Choose an Event:")
    events_lines = st.session_state["events_list"].splitlines()
    selected = st.radio("", options=events_lines, key="event_select")

    # Style and Toggle
    st.subheader("Style Options")
    style = st.selectbox("Narration Style", ["Old Newsreel", "Modern Documentary", "TikTok Style", "Neutral/Narrative"])
    conspiracy = st.checkbox("Include Conspiracy Angle")

    if st.button("🎬 Generate Script"):
        with st.spinner("Generating your script..."):
            script = generate_script(selected, style, conspiracy)
        st.subheader("🎙️ Narration Script")
        st.text_area("Copy your script:", script, height=400)
