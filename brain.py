import ollama
import os
import json
import webbrowser
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
# SET TO TRUE TO USE OLLAMA, FALSE TO USE GEMINI
USE_LOCAL = True 

LOCAL_MODEL = "qwen2.5:1.5b" 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLOUD_MODEL = "gemini-2.5-flash" 

SYSTEM_PROMPT = "You are NightFall, a concise AI assistant like Jarvis. Keep answers brief."

# Initialize the native Google GenAI client (Only used if USE_LOCAL = False)
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# ==========================================
# 1. DEFINE THE PYTHON FUNCTIONS
# ==========================================
def open_app(app_name):
    app_name = app_name.lower()
    try:
        if "google" in app_name or "browser" in app_name or "web" in app_name:
            webbrowser.open("https://www.google.com")
            return "Opened Google in the default browser."
        elif "calculator" in app_name or "calc" in app_name:
            os.system("calc.exe")
            return "Opened Calculator."
        elif "steam" in app_name:
            os.system("start steam://open/main")
            return "Opened Steam."
        elif "notepad" in app_name:
            os.system("notepad.exe")
            return "Opened Notepad."
        else:
            os.system(f"start {app_name}")
            return f"Attempted to open {app_name}."
    except Exception as e:
        return f"Failed to open {app_name}: {e}"

def close_app(app_name):
    app_name = app_name.lower()
    try:
        if "calculator" in app_name or "calc" in app_name:
            os.system("taskkill /f /im CalculatorApp.exe >nul 2>&1")
            os.system("taskkill /f /im Calculator.exe >nul 2>&1")
            return "Closed Calculator."
        elif "notepad" in app_name:
            os.system("taskkill /f /im notepad.exe >nul 2>&1")
            return "Closed Notepad."
        else:
            return f"I don't know how to close {app_name} yet."
    except Exception as e:
        return f"Failed to close {app_name}: {e}"

# ==========================================
# 2. DEFINE TOOLS FOR BOTH SYSTEMS
# ==========================================
# Format for Ollama
OLLAMA_TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'open_app',
            'description': 'Open an application or website (e.g., google, calculator, steam, notepad)',
            'parameters': {
                'type': 'object',
                'properties': {'app_name': {'type': 'string'}},
                'required': ['app_name'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'close_app',
            'description': 'Close an application that is currently running',
            'parameters': {
                'type': 'object',
                'properties': {'app_name': {'type': 'string'}},
                'required': ['app_name'],
            },
        },
    }
]

# Format for Gemini
GEMINI_TOOLS = [types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="open_app",
        description="Open an application or website",
        parameters=types.Schema(type="OBJECT", properties={"app_name": types.Schema(type="STRING")}, required=["app_name"])
    ),
    types.FunctionDeclaration(
        name="close_app",
        description="Close an application that is currently running",
        parameters=types.Schema(type="OBJECT", properties={"app_name": types.Schema(type="STRING")}, required=["app_name"])
    )
])]

# ==========================================
# 3. THE MAIN BRAIN FUNCTION
# ==========================================
def ask_ai(user_input, chat_history=[]):
    
    # --- LOCAL OLLAMA LOGIC ---
    if USE_LOCAL:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_input})
        
        try:
            print("[Brain] Thinking locally...")
            response = ollama.chat(model=LOCAL_MODEL, messages=messages, tools=OLLAMA_TOOLS)
            
            if response.get('message', {}).get('tool_calls'):
                for tool in response['message']['tool_calls']:
                    function_name = tool['function']['name']
                    app_name = tool['function']['arguments']['app_name']
                    
                    if function_name == 'open_app':
                        print(f"[Action] NightFall is opening {app_name}...")
                        result = open_app(app_name)
                    elif function_name == 'close_app':
                        print(f"[Action] NightFall is closing {app_name}...")
                        result = close_app(app_name)
                    else:
                        result = "Unknown tool."

                    messages.append(response['message'])
                    messages.append({'role': 'tool', 'content': result})
                    
                    final_response = ollama.chat(model=LOCAL_MODEL, messages=messages)
                    return final_response['message']['content']
            
            return response['message']['content']
            
        except Exception as e:
            return f"Local brain error: {e}"

    # --- GOOGLE GEMINI CLOUD LOGIC ---
    else:
        contents = []
        for msg in chat_history:
            contents.append(types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]))
        contents.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

        try:
            print("[Brain] Thinking with Gemini Cloud...")
            response = client.models.generate_content(
                model=CLOUD_MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=GEMINI_TOOLS,
                    system_instruction=SYSTEM_PROMPT
                )
            )

            if response.function_calls:
                for function_call in response.function_calls:
                    function_name = function_call.name
                    app_name = function_call.args.get('app_name', '')
                    
                    if function_name == 'open_app':
                        print(f"[Action] NightFall is opening {app_name}...")
                        result = open_app(app_name)
                    elif function_name == 'close_app':
                        print(f"[Action] NightFall is closing {app_name}...")
                        result = close_app(app_name)
                    else:
                        result = "Unknown tool."

                    function_response_part = types.Part.from_function_response(
                        name=function_name,
                        response={"result": result}
                    )
                    contents.append(response.candidates[0].content)
                    contents.append(types.Content(role="tool", parts=[function_response_part]))

                final_response = client.models.generate_content(
                    model=CLOUD_MODEL,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        tools=GEMINI_TOOLS, 
                        system_instruction=SYSTEM_PROMPT
                    )
                )
                return final_response.text
            
            return response.text
            
        except Exception as e:
            return f"Gemini brain error: {e}"