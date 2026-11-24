# NightFall_AI_Assistant

# NightFall AI Assistant 

An advanced, low-latency AI voice assistant inspired by J.A.R.V.I.S. from Iron Man. NightFall is designed to handle real-time VoIP (Voice over IP) conversations, execute system commands, and interact with external APIs. 

This project originally started as a foundational Python-based "Jarvis" assistant and is being actively evolved into a fully-fledged, conversational AI companion.

## Features
- **Jarvis-like Capabilities:** Function calling to execute system commands (e.g., "Open my browser," "Check the weather," "Send an email").
- **Real-Time VoIP (Planned):** Speak to NightFall over a phone call or WebRTC connection with ultra-low latency.
- **Voice Cloning/TTS (Planned):** High-quality, natural-sounding text-to-speech responses.
- **Dynamic Conversation:** Powered by modern Large Language Models (LLMs) for fluid, context-aware dialogue.

## Tech Stack
- **Core Language:** Python
- **LLM & Voice:** OpenAI API (or alternative LLMs)
- **Telephony/VoIP:** Twilio (for actual phone calls) or LiveKit (for WebRTC)
- **Speech-to-Text:** OpenAI Whisper or Deepgram
- **Text-to-Speech:** ElevenLabs or OpenAI TTS

## Architecture & Workflow
1. **Audio Input:** User speaks via microphone or VoIP call.
2. **Speech-to-Text (STT):** Audio is transcribed into text.
3. **LLM Processing:** The text is sent to an LLM to determine the user's intent and formulate a response.
4. **Action Execution:** The LLM triggers external APIs or local system commands (function calling).
5. **Text-to-Speech (TTS):** The AI's response is converted back into audio and played back to the user.

## Local Development

To run this project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AbeerImran1/NightFall_AI_Assistant.git
   cd NightFall_AI_Assistant

2. Set up a virtual environment (Recommended):
   python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Environment Variables:
   Create a .env file in the root directory and add your API keys (e.g., OPENAI_API_KEY=your_key_here). (Note: The .env file is gitignored for security)

5. Run the application:
   python app.py

   Roadmap
☑ Base assistant functionality (imported from previous Jarvis project).
□ Integrate an LLM for dynamic, context-aware conversation.
□ Add WebRTC (via LiveKit) for browser-based voice chat.
□ Integrate Twilio for actual phone number VoIP calls.
□ Add "Function Calling" to control smart home devices and local apps.
□ Implement wake-word detection (e.g., "Hey NightFall").
  Disclaimer
This project is for educational and personal use. Ensure you keep your API keys secure and do not commit them to version control.


### Push it to GitHub
In your VS Code terminal (make sure you are in the `NightFall_AI_Assistant` folder), run:

```bash
git add README.md
git commit -m "docs: add comprehensive README with roadmap and architecture"
git push origin main
