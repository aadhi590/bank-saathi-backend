import os
import google.generativeai as genai
from prompts import SYSTEM_PROMPT

# 🔐 Read API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-flash-latest")


def classify_intent(user_message: str) -> str:
    msg = user_message.lower()

    if "why" in msg or "risk" in msg:
        return "EXPLAIN"
    if "what if" in msg or "happen" in msg or "proceed" in msg:
        return "SIMULATE"
    if "confidence" in msg or "sure" in msg:
        return "CONFIDENCE"

    return "OUT_OF_SCOPE"


def build_prompt(intent: str, context: dict, user_message: str) -> str:
    base_context = f"""
Transaction Context:
- Amount: ₹{context['amount']}
- Receiver: {context['receiver']}
- Time: {context['time']}
- Decision: {context['decision']}
- Risk score: {context['risk_score']}
- Evidence score: {context['evidence_score']}%
- Missing data: {', '.join(context['missing_data'])}
- Budget status: {context['budget_status']}
"""

    if intent == "EXPLAIN":
        task = (
            "Explain in 2 short, formal sentences why the system flagged this transaction. "
            "Do not give advice."
        )
    elif intent == "SIMULATE":
        task = (
            "Describe potential consequences if the transaction proceeds, "
            "without recommending or discouraging the action."
        )
    elif intent == "CONFIDENCE":
        task = (
            "Explain how confident the system is and what factors reduce certainty."
        )
    else:
        return (
            "Politely state that you can only discuss the current transaction "
            "and cannot answer questions outside this scope."
        )

    return f"""
{SYSTEM_PROMPT}

{base_context}

User asked:
"{user_message}"

Task:
{task}
"""


def chat_with_bank_saathi(user_message: str, context: dict) -> str:
    intent = classify_intent(user_message)
    prompt = build_prompt(intent, context, user_message)

    response = model.generate_content(prompt)
    return response.text.strip()
