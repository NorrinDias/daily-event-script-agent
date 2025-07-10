import streamlit as st
import datetime
import requests

# ---- CONFIG ----
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ---- FUNCTIONS ----
def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        st.error(f"Groq API Error: {response.status_code} - {response.text}")
        return ""

def generate_event_list(date_str):
    prompt = f"""
    You are a historical events researcher. Given the date {date_str}, return a list of 10 unique, strange, or little-known events from 1800 to the present. Prioritize topics in space, war, science, pop culture, or government history. Format as:

    1. Event Title (Year) – One-sentence hook
    """
    return call_groq(prompt)

def generate_script(event_title, style, conspiracy):
    conspiracy_prompt = "Include known conspiracy theories." if conspiracy else "Do not include any conspiracies."
    prompt = f"""
    You are a distinguished news journalist and narrator creating a 2-minute script for a short-form video on the event: "On {event_title}". Write in a compelling yet playful tone with short, vivid sentences starting the script wiht "On" and the date in question. Add visual suggestions in brackets. Style: {style}. {conspiracy_prompt}
    """
    return call_groq(prompt)

# ---- UI ----
st.title("📅 Daily Historical Event Script Generator (Groq LLaMA 3)")

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
