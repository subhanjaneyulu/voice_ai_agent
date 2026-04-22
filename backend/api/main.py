import os
import shutil
import uuid
import time

from fastapi import FastAPI, UploadFile, File, WebSocket
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator 

from agent.reasoning.ai_agent import process_text
from agent.tools.orchestrator import handle_tools 
from memory.session_memory.session_memory import save_context, get_context 
from services.text_to_speech.text_to_speech import text_to_speech
from scheduler.appointment_engine.database import appointments_db

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

app = FastAPI()

@app.get("/")
def health():
    return {"status": "Server is running"}


model = WhisperModel("small", device="cpu", compute_type="int8")

LANG_NAMES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "en": "English",
    "ur": "Hindi"
}

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text


def translate_from_english(text, target_lang):
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except:
        return text

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...), session_id: str = None):
    
    if not session_id:
        session_id = str(uuid.uuid4())

    temp_filename = f"temp_{file.filename}"
    
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        start_total = time.time()

        
        segments, info = model.transcribe(temp_filename, beam_size=5)
        full_text = "".join([segment.text for segment in segments]).strip()

        detected_code = info.language
        language_name = LANG_NAMES.get(detected_code, detected_code.upper())

       
        english_text = translate_to_english(full_text)
        agent_result = process_text(english_text)

       
        if not agent_result or agent_result.get("intent") == "unknown":
            fallback = "I'm having trouble processing that request. Could you repeat?"
            return {
                "session_id": session_id,
                "speech": {
                    "original_text": full_text,
                    "detected_language": language_name
                },
                "message": fallback
            }

       
        if not isinstance(agent_result, dict):
            return {"error": "Invalid agent output"}

        
        previous_context = get_context(session_id)

        if previous_context:
            agent_result["doctor"] = agent_result.get("doctor") or previous_context.get("doctor")
            agent_result["date"] = agent_result.get("date") or previous_context.get("date")
            agent_result["time"] = agent_result.get("time") or previous_context.get("time")

       
        tool_result = handle_tools(agent_result)

        
        save_context(session_id, agent_result)

        
        if isinstance(tool_result, dict):
            original_message = tool_result.get("message", "")
            tool_response = tool_result.copy()
        else:
            original_message = str(tool_result)
            tool_response = {"message": original_message}

       
        final_message = translate_from_english(original_message, detected_code)
        tool_response["message"] = final_message

        
        audio_file = text_to_speech(final_message)

        end_total = time.time()

        return {
            "session_id": session_id,
            "speech": {
                "original_text": full_text,
                "detected_language": language_name,
                "english_text": english_text
            },
            "agent": agent_result,
            "tool": tool_response,
            "audio": audio_file,
            "latency_ms": round((end_total - start_total) * 1000, 2)
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Something went wrong. Please try again."
        }

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_text()

            
            if any("\u0900" <= ch <= "\u097F" for ch in data):
                lang = "hi"
            elif any("\u0B80" <= ch <= "\u0BFF" for ch in data):
                lang = "ta"
            else:
                lang = "en"

            english_text = translate_to_english(data)
            agent_result = process_text(english_text)

            if not agent_result or agent_result.get("intent") == "unknown":
                await websocket.send_text("I'm having trouble processing that request.")
                continue

            if not isinstance(agent_result, dict):
                await websocket.send_text("Invalid input")
                continue

            tool_result = handle_tools(agent_result)

            message = tool_result.get("message", "") if isinstance(tool_result, dict) else str(tool_result)

            final_message = translate_from_english(message, lang)

            await websocket.send_text(final_message)

        except Exception as e:
            await websocket.send_text("Something went wrong. Please try again.")
            break 

@app.get("/appointments")
def get_appointments():
    return {
        "appointments": appointments_db
    }