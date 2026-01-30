import google.generativeai as genai

genai.configure(api_key="AIzaSyAjN3a1znzl1QvZMkl7NnAqXddRDFFyz_s")

model = genai.GenerativeModel("models/gemini-flash-latest")

response = model.generate_content("Say hello in one sentence.")

print(response.text)
