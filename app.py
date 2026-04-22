"""
AI Chatbot Generator Pro - Batch 3 Activity
Developed with Antigravity AI
Features: Groq integration, Memory Depth, Persona Presets, Standalone Exporter.
"""

import streamlit as st
import os
from groq import Groq
import base64
import time
from datetime import datetime
from dotenv import load_dotenv
import streamlit_shadcn_ui as ui

# Load environment variables
load_dotenv()
GROQ_API_ENV = os.getenv("GROQ_API_KEY")

# --- SETTINGS ---
st.set_page_config(page_title="NEXUS CORE v2.0", page_icon="🤖", layout="wide")

# --- CUSTOM CSS (Premium Look) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        background-image: radial-gradient(circle at 50% -20%, #1c2c4c 0%, #0e1117 80%);
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        background-color: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
    }
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #3d444d;
    }
    h1, h2, h3 {
        background: linear-gradient(90deg, #00d4ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff 0%, #0072ff 100%);
        color: white;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "started" not in st.session_state:
    st.session_state.started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "messages_b" not in st.session_state:
    st.session_state.messages_b = []
if "last_system_prompt" not in st.session_state:
    st.session_state.last_system_prompt = ""
if "system_prompt_input" not in st.session_state:
    st.session_state.system_prompt_input = "You are a helpful and intelligent AI assistant."
if "last_preset" not in st.session_state:
    st.session_state.last_preset = "Custom"
if "analytics" not in st.session_state:
    st.session_state.analytics = {"total_tokens": 0, "avg_speed": 0, "calls": 0, "cost": 0.0}
if "arena_mode" not in st.session_state:
    st.session_state.arena_mode = False
if "reasoning_mode" not in st.session_state:
    st.session_state.reasoning_mode = False
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False

# --- COST RATES (Mock pricing per 1M tokens) ---
COST_RATES = {
    "llama-3.3-70b-versatile": 0.59,
    "llama-3.1-8b-instant": 0.05,
    "qwen/qwen3-32b": 0.20
}

# --- PRESETS ---
PRESETS = {
    "Custom": "You are a helpful and intelligent AI assistant.",
    "🍳 Chef Bot": "You are a world-class chef who explains everything using food metaphors.",
    "📐 Math Tutor": "You are a patient math tutor. Always show step-by-step working.",
    "😏 Sarcastic Assistant": "You are helpful but deeply sarcastic. Answer correctly but with attitude.",
    "🛒 Customer Support": "You are a polite customer support agent for an e-commerce store.",
    "🧘 Life Coach": "You are a calm, motivational life coach. Use positive reinforcement.",
}

# --- HELPER FUNCTIONS ---
def enhance_dna(prompt, api_key):
    if not api_key: return prompt
    try:
        temp_client = Groq(api_key=api_key)
        optimizer_prompt = f"Rewrite this system prompt to be highly professional, structured, and effective for an LLM. Output ONLY the rewritten prompt: {prompt}"
        response = temp_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": optimizer_prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except:
        return prompt

def generate_standalone_code(name, prompt, model, temp, mem):
    safe_prompt = prompt.replace('"""', r'\"\"\"')
    return f'''import streamlit as st
from groq import Groq

BOT_NAME = "{name}"
SYSTEM_PROMPT = """{{safe_prompt}}"""
MODEL = "{model}"
TEMPERATURE = {temp}
MEMORY_WINDOW = {mem}

st.set_page_config(page_title=BOT_NAME, page_icon="🤖")
st.title(f"🤖 {{BOT_NAME}}")

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    api_key = st.text_input("Enter Groq API Key", type="password")
    if st.button("Reset"): st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if p := st.chat_input("Say something..."):
    if not api_key: st.error("Need API Key")
    else:
        client = Groq(api_key=api_key)
        st.session_state.messages.append({{"role": "user", "content": p}})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            full = ""
            ph = st.empty()
            history = st.session_state.messages[-MEMORY_WINDOW:]
            m = [{{ "role": "system", "content": SYSTEM_PROMPT }}] + history
            comp = client.chat.completions.create(model=MODEL, messages=m, temperature=TEMPERATURE, stream=True)
            for c in comp:
                content = c.choices[0].delta.content
                if content:
                    full += content
                    ph.markdown(full + "▌")
            ph.markdown(full)
        st.session_state.messages.append({{"role": "assistant", "content": full}})
'''

# --- LANDING PAGE ---
def show_landing_page():
    st.components.v1.html(
        """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r121/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
        <div id="vanta-bg" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;"></div>
        <script>
            VANTA.NET({
              el: "#vanta-bg",
              mouseControls: true,
              touchControls: true,
              gyroControls: false,
              minHeight: 200.00, minWidth: 200.00,
              scale: 1.00, scaleMobile: 1.00,
              color: 0x00d4ff, backgroundColor: 0x0e1117,
              points: 12.00, maxDistance: 20.00, spacing: 15.00
            })
        </script>
        """, height=0,
    )

    st.markdown("""
        <div style="text-align: center; padding-top: 50px;">
            <p style="color: #00d4ff; font-weight: bold; letter-spacing: 2px;">NAVTTC BATCH 3</p>
            <h1 style="font-size: 5rem; line-height:1; margin-bottom: 20px; background: linear-gradient(135deg, #fff 30%, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NEXUS CORE v2.0</h1>
            <p style="font-size: 1.4rem; color: #888; max-width: 800px; margin: 0 auto 40px auto;">Advanced Multi-Persona LLM Lifecycle Management System. Automated Prompt Engineering, Real-Time Analytics, and Compiled Exporter.</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 50px auto; max-width: 1200px;">
            <div style="background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                <h4 style="color: #00d4ff;">🧠 DNA Enrichment</h4>
                <p style="color: #888; font-size: 0.9rem;">Meta-Prompt Engineering Engine that upgrades basic instructions into professional system personas.</p>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                <h4 style="color: #00d4ff;">📈 Live Analytics</h4>
                <p style="color: #888; font-size: 0.9rem;">Real-time tracking of Tokens/Sec, Inference Latency, and Cost metrics using Groq Telemetry.</p>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                <h4 style="color: #00d4ff;">🏗️ Script Compiler</h4>
                <p style="color: #888; font-size: 0.9rem;">One-click generation of fully functional, self-contained Python bots for commercial deployment.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c2:
        if st.button("🚀 INITIALIZE WORKSPACE", use_container_width=True):
            st.session_state.started = True
            st.rerun()

# --- ENTRY CONTROL ---
if not st.session_state.started:
    show_landing_page()
    st.stop()

# --- CALLBACKS ---
def handle_dna_enhancement():
    with st.spinner("Optimizing Persona DNA..."):
        enhanced = enhance_dna(st.session_state.system_prompt_input, GROQ_API_ENV)
        st.session_state.system_prompt_input = enhanced

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.title("🛡️ Command Center")
    bot_name = st.text_input("Bot Identifier", value="Nexus AI")
    
    preset_choice = st.selectbox("Archetype Library", list(PRESETS.keys()))
    if preset_choice != st.session_state.last_preset:
        if preset_choice != "Custom":
            st.session_state.system_prompt_input = PRESETS[preset_choice]
        st.session_state.last_preset = preset_choice
    
    system_prompt = st.text_area("Persona DNA", key="system_prompt_input", height=120)
    st.button("✨ Enhance DNA (Auto-Prompt)", on_click=handle_dna_enhancement, use_container_width=True)

    with st.expander("⚔️ Arena & Advanced Modules"):
        st.session_state.arena_mode = st.toggle("Arena Mode (Dual Model)", value=st.session_state.arena_mode)
        st.session_state.reasoning_mode = st.toggle("Recursive Reasoning", value=st.session_state.reasoning_mode)
        st.session_state.voice_mode = st.toggle("Vocalizer Engine (TTS)", value=st.session_state.voice_mode)
        if st.session_state.arena_mode:
            model_b_choice = st.selectbox("Secondary Model (B)", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "qwen/qwen3-32b"])
        
    with st.expander("🛠️ Engine Specifications"):
        model_choice = st.selectbox("Primary Model (A)", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "qwen/qwen3-32b"])
        ct, cm = st.columns(2)
        with ct: temperature = st.slider("Entropy", 0.0, 1.0, 0.7)
        with cm: memory_window = st.slider("Memory", 1, 50, 10)
    
    with st.expander("🔑 Access & Security", expanded=True):
        st.markdown("### 🛠️ Bot Builder")
        st.info("Each user provides their own free API key from Groq. Your key is saved locally to your session and never shared with the developer.")
        
        # We leave this empty by default for security
        groq_api_key = st.text_input(
            "Your Groq API Key", 
            placeholder="gsk_...",
            help="🔗 Get your free API key at console.groq.com/keys",
            type="password"
        )
        
        st.markdown("[🔗 Get your free API key at console.groq.com/keys →](https://console.groq.com/keys)")
        
        if not groq_api_key:
            st.warning("⚠️ Please enter and save your Groq API key above before building a chatbot.")
        
        if st.button("🗑️ Purge Buffer (Reset)", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with st.expander("🏗️ Compiler Vault"):
        st.subheader("Autonomous Script Compiler")
        standalone_code = generate_standalone_code(bot_name, system_prompt, model_choice, temperature, memory_window)
        st.download_button(
            label="🚀 Compile Standalone Bot",
            data=standalone_code,
            file_name=f"{bot_name.lower()}_bot.py",
            mime="text/x-python",
            use_container_width=True
        )
        if st.session_state.messages:
            def export_chat(messages, name):
                lines = [f"=== {name} Export ===\n"]
                for m in messages:
                    role = "User" if m["role"] == "user" else name
                    lines.append(f"{role}: {m['content']}\n")
                return "\n".join(lines)
            st.download_button(
                label="💾 Export History (.txt)",
                data=export_chat(st.session_state.messages, bot_name),
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True
            )

# --- MAIN WORKSPACE ---
# Custom Header with HUD (Heads-Up Display)
st.markdown(f"""
    <div style="background: rgba(17, 25, 40, 0.75); backdrop-filter: blur(16px); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.125); padding: 25px; margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin:0; padding:0; font-size: 2rem;">⚡ Live Sandbox: {bot_name}</h1>
                <p style="color: #888; font-size: 0.85rem; margin-top: 5px;">Accelerator: Groq LPU™ | Hardware-Layer Optimized</p>
            </div>
            <div style="display: flex; gap: 30px;">
                <div style="text-align: right;">
                    <div style="color: #00d4ff; font-weight: bold; font-size: 1.2rem;">{st.session_state.analytics['total_tokens']}</div>
                    <div style="color: #555; font-size: 0.7rem; text-transform: uppercase;">Total Tokens</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #0072ff; font-weight: bold; font-size: 1.2rem;">{st.session_state.analytics['avg_speed']:.1f}</div>
                    <div style="color: #555; font-size: 0.7rem; text-transform: uppercase;">Speed (w/s)</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #00ff88; font-weight: bold; font-size: 1.2rem;">${st.session_state.analytics['cost']:.4f}</div>
                    <div style="color: #555; font-size: 0.7rem; text-transform: uppercase;">Est. Cost (USD)</div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# TTS Script injection
if st.session_state.voice_mode:
    st.components.v1.html("""
        <script>
        window.speak = function(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.rate = 1.1;
            synth.speak(utter);
        }
        </script>
    """, height=0)

# --- ARENA LOGIC ---
if st.session_state.arena_mode:
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption(f"🅰️ ENGINE A: {model_choice}")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
    with col_b:
        st.caption(f"🅱️ ENGINE B: {model_b_choice}")
        for m in st.session_state.messages_b:
            with st.chat_message(m["role"]): st.markdown(m["content"])
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Input Neural Signal..."):
    if not groq_api_key: st.warning("Target Key Offline"); st.stop()
    client = Groq(api_key=groq_api_key)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    if st.session_state.arena_mode:
        st.session_state.messages_b.append({"role": "user", "content": prompt})

    # STREAM ENGINE A
    with (col_a if st.session_state.arena_mode else st.container()):
        with st.chat_message("assistant"):
            if st.session_state.reasoning_mode:
                with st.status("🧠 Recursive Reasoning Layer Activated...", expanded=False):
                    try:
                        reflection_prompt = f"Critically reflect on this user input and plan a response strategy for persona: {system_prompt}\nUser: {prompt}"
                        refl = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": reflection_prompt}], timeout=5.0)
                        st.write(refl.choices[0].message.content)
                    except Exception as e:
                        st.warning(f"Reasoning Layer Bypass: {e}")

            st.write("---")
            start = time.time()
            res_a = ""
            ph = st.empty()
            hist = st.session_state.messages[-memory_window:]
            comp = client.chat.completions.create(model=model_choice, messages=[{"role": "system", "content": system_prompt}] + hist, stream=True, temperature=temperature)
            for c in comp:
                txt = c.choices[0].delta.content
                if txt: res_a += txt; ph.markdown(res_a + "▌")
            ph.markdown(res_a)
            dur = time.time() - start
            tk = len(res_a.split())
            st.session_state.analytics["total_tokens"] += tk
            st.session_state.analytics["avg_speed"] = tk/dur if dur > 0 else 0
            st.session_state.analytics["cost"] += (tk/1000000) * COST_RATES.get(model_choice, 0.1)
            st.session_state.messages.append({"role": "assistant", "content": res_a})
            if st.session_state.voice_mode: st.components.v1.html(f"<script>window.speak('{res_a[:200].replace("'", "")}')</script>", height=0)

    # STREAM ENGINE B (Arena Only)
    if st.session_state.arena_mode:
        with col_b:
            with st.chat_message("assistant"):
                res_b = ""
                phb = st.empty()
                histb = st.session_state.messages_b[-memory_window:]
                compb = client.chat.completions.create(model=model_b_choice, messages=[{"role": "system", "content": system_prompt}] + histb, stream=True)
                for c in compb:
                    txt = c.choices[0].delta.content
                    if txt: res_b += txt; phb.markdown(res_b + "▌")
                phb.markdown(res_b)
                st.session_state.messages_b.append({"role": "assistant", "content": res_b})
    
    st.rerun()
