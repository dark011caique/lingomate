from flask import Flask, render_template, request, Response
import os
import google.generativeai as genai
from dotenv import load_dotenv
from time import sleep
from helper import carrega, salva
from selecionar_persona import personas, selecionar_persona
from gerenciar_historico import remover_mensagens_mais_antigas
from resumir_historico import resumir_historico
import uuid
from gerar_imagem import gerar_iamgem_gemini

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API do arquivo .env
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
if not CHAVE_API_GOOGLE:
    raise ValueError("A chave da API não foi encontrada. Verifique o arquivo .env.")

print(f"Chave da API: {CHAVE_API_GOOGLE}")

# Configura a API com a chave
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-pro"

app = Flask(__name__)
app.secret_key = 'alura'

caminho_imagem_enviada = None
UPLOAD_FOLDER = "imagens_temporarias"

print(f"Caminho atual: {os.getcwd()}")
contexto = carrega("C:/Users/Win10/OneDrive/Área de Trabalho/alura/LingoMate/venv/dados/limgomate.txt")
if contexto is None: 
    raise ValueError("Erro ao carregar o contexto do arquivo.")


def criar_chatbot():
    personalidade = personas["Neutro"]

    prompt_do_sistema = f"""
    # PERSONA

    Você é um chatbot especializado em conversação em inglês. 
    Seu nome é LingoMate. Seu objetivo é ajudar o usuário a praticar e melhorar suas habilidades no idioma.
    Você deve adaptar suas respostas de acordo com o nível de inglês do usuário, variando de iniciante (A1) a avançado (C2). 
    Nunca forneça respostas que não se relacionem com a prática da língua inglesa.

    Você deve responder em português quando a pessoa não entender, e assumir o papel de professor quando a pessoa começar a escrever em inglês.
    

    # CONTEXTO
    {contexto}

    # PERSONALIDADE
    {personalidade}

    # Histórico
    Acesse sempre o histórico de mensagens, e recupere informações ditas anteriormente.
    """

    configuracao_modelo = {
        "temperature": 0.1,
        "max_output_tokens": 8192
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_do_sistema,
        generation_config=configuracao_modelo
    )

    chatbot = llm.start_chat(history=[])
    return chatbot

chatbot = criar_chatbot()

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    global caminho_imagem_enviada

    while True:
        try:
            # Garantir que a persona tenha a primeira letra maiúscula
            persona_escolhida = selecionar_persona(prompt).capitalize()  # Usar capitalize() para corrigir a capitalização
            personalidade = personas.get(persona_escolhida, personas["Neutro"])  # Usar .get() para evitar KeyError

            mensagem_usuario = f"""
            Considere esta personalidade para responder a mensagem:
            {personalidade}
            
            Responda a seguinte mensagem, sempre lembrando do histórico:
            {prompt}
            """

            if caminho_imagem_enviada:
                mensagem_usuario += "\n Utilize as características da imagem em sua resposta"
                arquivo_imagem = gerar_iamgem_gemini(caminho_imagem_enviada)
                resposta = chatbot.send_message([arquivo_imagem, mensagem_usuario])
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None
            else:
                resposta = chatbot.send_message(mensagem_usuario)

            if len(chatbot.history) > 10:
                chatbot.history = remover_mensagens_mais_antigas(chatbot.history)

            if len(chatbot.history) > 10:
                chatbot.history = resumir_historico(chatbot.history)

            print(f"Quantidade: {len(chatbot.history)}\n {chatbot.history}")

            return resposta.text
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no Gemini: %s" % erro

            if caminho_imagem_enviada:
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None

            sleep(50)

@app.route("/upload_imagem", methods=["POST"])
def upload_imagem():
    global caminho_imagem_enviada

    if "imagem" in request.files:
        imagem_enviada = request.files["imagem"]
        nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo
        return "Imagem enviada com sucesso", 200
    return "Nenhum arquivo enviado", 400

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    return resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
