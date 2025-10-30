import os
import google.generativeai as genai
from dotenv import load_dotenv

def configurar_ia():
    """
    Carrega a API Key do .env e configura o modelo Generative AI.
    Retorna o objeto do modelo.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Erro: A variável de ambiente GOOGLE_API_KEY não foi definida.")
        return None
        
    try:
        genai.configure(api_key=api_key)
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            safety_settings=safety_settings
        )
        print("Modelo de IA configurado com sucesso.")
        return model
    except Exception as e:
        print(f"Erro ao configurar o modelo de IA: {e}")
        return None
    