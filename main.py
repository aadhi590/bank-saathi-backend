from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import chat_with_bank_saathi

app = FastAPI(
    title="Bank Saathi Chatbot",
    description="Decision-scoped AI assistant for transaction risk explanation",
    version="1.0.0"
)

# ✅ CORS (safe for hackathon demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Models
# -----------------------------
class ChatRequest(BaseModel):
    message: str
    transaction_context: dict


class ChatResponse(BaseModel):
    reply: str


# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"status": "Bank Saathi backend running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    reply = chat_with_bank_saathi(
        user_message=req.message,
        context=req.transaction_context
    )
    return {"reply": reply}
