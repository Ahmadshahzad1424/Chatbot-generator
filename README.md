# 🤖 NEXUS CORE v3.0 — AI Persona Engineering Workspace
### Advanced Multi-Persona LLM Lifecycle Management System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**NEXUS CORE v3.0** is an enterprise-grade AI development workspace designed for high-fidelity persona engineering, real-time benchmarking, and autonomous bot generation. Engineered for the **NAVTTC Batch 3 Final Year Project (FYP)**, this system leverages the elite speed of **Groq LPU Acceleration** to provide an instantaneous, data-driven AI engineering experience.

---

## 💎 Core Innovation & Features

### ⚔️ AI Arena (Dual-Stream Benchmarking)
Benchmark multiple LLM architectures side-by-side in real-time. NEXUS CORE allows you to send a single prompt to two dynamic engines (e.g., Llama-70b vs. 8b) to compare latency, quality, and persona adherence simultaneously.

### 🧠 Recursive Reasoning (Self-Reflection)
Implemented a "Self-Reflection" layer. When enabled, the AI performs a pre-inference critique of its own strategy (using a specialized reasoning model) before generating the final response—ensuring maximum precision and persona depth.

### ✨ DNA Meta-Enhancer
Stop writing basic prompts. Our **Meta-Prompt Layer** uses Automated Prompt Engineering (APE) to transform simple descriptions into high-fidelity, structured System Persona DNA with a single click.

### 💰 Live Fiscal Radar & Telemetry HUD
A professional heads-up display (HUD) that tracks:
- **Total Token Throughput**
- **Inference Speed (Words/Sec)**
- **Real-Time USD Cost Estimation** per session based on model-specific pricing.

### 🏗️ Standalone Bot Compiler
Instantly compile your custom-tuned bot into a self-contained, portable Python script. Export your neural "archetypes" for commercial deployment in seconds.

---

## 🛠️ Technical Stack
- **Engine**: [Groq Cloud LPU™](https://groq.com/) (Language Processing Units)
- **Framework**: Streamlit (High-Performance UI)
- **UI/UX**: `streamlit-shadcn-ui` & Vanta.js (3D Interactive Portal)
- **Neural Models**: Llama-3.3-70b, Llama-3.1-8b, Qwen-32b

---

## 🚀 Rapid Deployment

### Local Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ahmadshahzad1424/Chatbot-generator.git
   cd Chatbot-generator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Initialize Workspace**:
   ```bash
   streamlit run app.py
   ```

### ☁️ Cloud Deployment (Streamlit Cloud)
1. Commit your changes to GitHub (Ensure `.env` is excluded via `.gitignore`).
2. Log in to [Streamlit Cloud](https://share.streamlit.io/).
3. Connect this repository.
4. Add your `GROQ_API_KEY` to the **Secrets** section in the Streamlit Dashboard.
5. Deploy!

---

## 🎓 Academic Context
- **Project**: AI Chatbot Generator Pro (v3.0)
- **ID**: NEX-4402
- **Institution**: Department of Computer Science (NAVTTC Batch 3)

Developed with ❤️ for the future of AI engineering.
