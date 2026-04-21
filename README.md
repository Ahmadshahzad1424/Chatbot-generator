# AI Chatbot Generator (Pro)

A professional-grade tool to design, test, and export custom AI chatbots powered by Groq.

## 🚀 Pro Features
- **Persona Context**: Real-time system prompt injection for deep character roleplay.
- **Sliding Window Memory**: Choose how many past messages the bot remembers (**Memory Depth**) to optimize speed and cost. 
    - **Default**: 10 messages.
    - **Behavior**: Older messages are dropped automatically once the window is exceeded.
- **Response Control**: Precise `max_tokens` and `temperature` settings.
- **Auto-Reset**: The chat automatically clears if you change the bot's persona mid-conversation to prevent identity confusion.
- **Standalone Export**: Download a single-file Python script to run your custom bot anywhere. The exported file includes a dedicated sidebar field for the runner to input their own Groq API key.

## 🛠️ Setup
1. Requirement: **Python 3.9+**
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your API key in a `.env` file: `GROQ_API_KEY=your_key_here`
4. Launch: `streamlit run app.py`

## 📦 Standalone Bots
The exported bots are self-contained. The runner only needs to provide their own **Groq API Key** in the generated app's sidebar to start chatting with your specific configuration.
