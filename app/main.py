import spacy
from fastapi import FastAPI
from pydantic import BaseModel
from app.utils.redactor import redact_text
from app.utils.tokenizer import custom_tokenizer_factory
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.responses import HTMLResponse

app = FastAPI()
nlp = spacy.load("pii_redaction_model")  # Load your trained model
nlp.tokenizer = custom_tokenizer_factory(nlp)

class LogMessage(BaseModel):
    log_message: str

@app.post("/detect")
async def detect_pii(request: LogMessage):
    doc = nlp(request.log_message)
    return {"entities": [{"text": ent.text, "label": ent.label_} for ent in doc.ents]}

@app.post("/redact")
async def redact_pii(request: LogMessage):
    redacted = redact_text(request.log_messageg)
    return {"original": request.log_message, "redacted": redacted}


app.mount("/static", StaticFiles(directory="app/templates"), name="static")
@app.get("/ui")
async def ui_page():
    return FileResponse(os.path.join("app", "templates", "index.html"))


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>PII Redaction API</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1> Welcome to the PII Redaction Service!</h1>
            <p>Use the <a href="/docs">API docs</a> to detect and redact PII from your logs.</p>
        </body>
    </html>
    """
