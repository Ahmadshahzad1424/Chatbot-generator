import streamlit as st
import streamlit_shadcn_ui as ui

st.set_page_config(page_title="Shadcn Test", layout="wide")

# Mock session state for testing logic
if "last_preset" not in st.session_state:
    st.session_state.last_preset = "Custom"
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "Initial Prompt"

st.title("Shadcn UI Isolation Test")

# 1. Test Card & Badge
with ui.card(key="card1"):
    st.subheader("🤖 Nexus AI")
    ui.badges(badge_list=[("Status: Online", "default"), ("Model: Llama3", "outline")], key="badges1")

# 2. Test Buttons (Export & Reset)
st.divider()
col1, col2 = st.columns(2)
with col1:
    if ui.button(text="🚀 Download Bot (.py)", key="btn_export", variant="default"):
        st.success("Export Button Clicked")
with col2:
    if ui.button(text="🗑️ Reset Chat", key="btn_reset", variant="destructive"):
        st.warning("Reset Button Clicked")

# 3. Test Logic (Preset vs Manual)
st.divider()
PRESETS = {"Custom": "", "Chef": "Metaphor Chef", "Tutor": "Helpful Tutor"}
preset = st.selectbox("Select Preset", list(PRESETS.keys()))

if preset != st.session_state.last_preset:
    if preset != "Custom":
        st.session_state.system_prompt = PRESETS[preset]
    st.session_state.last_preset = preset

prompt_input = st.text_area("Persona", value=st.session_state.system_prompt)
st.session_state.system_prompt = prompt_input

st.write("Current session_state.system_prompt:", st.session_state.system_prompt)
st.write("Current session_state.last_preset:", st.session_state.last_preset)
