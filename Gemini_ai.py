import google.generativeai as genai
# from decouple import config
from dotenv import load_dotenv
load_dotenv()
import os
def Gemini(input:str):
    try:

        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(input)
        return response.text
    except Exception as ex:
        print(ex)
        return f"getting erroe {ex}"
prompt = """
temperature = st.slider("Temperature",0.0,0.2,0.4,0.6,0.8,1.0) update this
"""
result = Gemini(prompt)
print(result)
    