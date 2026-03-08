from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
try:
    from .analytics import analyze_conversation
except ImportError:
    from analytics import analyze_conversation
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
conversation_history = []
@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            sender = message_data.get("sender", "User")
            text = message_data.get("text", "")
            conversation_history.append(f"{sender}: {text}")
            full_context = " ".join(conversation_history)
            results = analyze_conversation(full_context)
            response = {
                "message": {"sender": sender, "text": text},
                "analytics": results
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        conversation_history.clear()
