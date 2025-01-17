import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Obtém a chave da API do arquivo .env
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
if not CHAVE_API_GOOGLE:
    raise ValueError("A chave da API não foi encontrada. Verifique o arquivo .env.")

print(f"Chave da API: {CHAVE_API_GOOGLE}")

# Configura a API com a chave
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-pro"

def gerar_iamgem_gemini(caminho_iamgem):
    arquivo_temporario = genai.upload_file(
        path=caminho_iamgem,
        display_name="Imagem Enviada"
    )

    print(F"Imagem Enviada: {arquivo_temporario.uri}")

    return arquivo_temporario