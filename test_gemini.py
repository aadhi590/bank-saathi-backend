from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

# Configure using env var
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=api_key)

print("✅ API key loaded")

# List available models
print("\n📦 Available Gemini models:\n")
for model in genai.list_models():
    print("MODEL:", model.name)
    print("SUPPORTED METHODS:", model.supported_generation_methods)
    print("-" * 50)
