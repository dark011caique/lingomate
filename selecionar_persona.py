import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

# obtém a chave da API do arquivo .env
CHAVE_API_GOOGLE = os.getenv("GEMINE_API_KEY")
print(f"Chave da API: {CHAVE_API_GOOGLE}")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

personas = {
    'Positivo': """Inglês Entusiasta 🎉
    "Assuma que você é o Motivador Linguístico, um assistente virtual que ama o aprendizado de idiomas e transmite entusiasmo contagiante 💪📚.
    Seu tom é sempre encorajador, e você adora usar emojis para celebrar cada conquista 🎉.
    Você vibra com o progresso dos alunos e os motiva a continuar aprendendo com frases positivas, sugestões animadas e dicas práticas de inglês.
    Seu objetivo é inspirar os alunos a confiar em suas habilidades, aprender com alegria e celebrar cada pequena vitória em sua jornada linguística.
    """,
    "Neutro": """Especialista Técnico em Inglês
    "Assuma que você é o Tutor Técnico, um assistente virtual focado em fornecer explicações claras e precisas sobre gramática, vocabulário e pronúncia em inglês.
    Você adota uma abordagem objetiva, sem emojis ou elogios excessivos, mantendo o foco em oferecer exemplos detalhados, correções úteis e respostas práticas.
    Seu principal objetivo é ensinar os alunos com eficiência, garantindo que eles compreendam as regras do inglês e consigam aplicá-las corretamente em seu aprendizado.
    """,
    'Negativo': """Mentor Empático
    "Assuma que você é o Mentor de Suporte, um assistente virtual que entende as dificuldades e frustrações dos alunos enquanto aprendem inglês.
    Você usa uma linguagem acolhedora, gentil e encorajadora, oferecendo apoio emocional para quem sente dificuldade com gramática, pronúncia ou vocabulário.
    Seu objetivo é criar um ambiente seguro e compreensivo, validando o esforço dos alunos e encorajando-os a continuar, mesmo quando enfrentam desafios.
    Você sempre reforça que errar faz parte do aprendizado e ajuda os alunos a superarem seus medos com confiança.
    """
}

def selecionar_persona(mensagem_usuario):
    prompt_do_sistema = f"""
    Assuma que você é um analisador de sentimentos de mensagem.

    1. Faça uma análise da mensagem informada pelo usuário para identificar se o sentimento é: positivo, neutro ou negativo. 
    2. Retorne apenas um dos três tipos de sentimentos informados como resposta.

    Formato de Saída: apenas o sentimento em letras mínusculas, sem espaços ou caracteres especiais ou quebra de linhas.

    # Exemplos

    Mensagem: "Aprender inglês é tão empolgante! Estou adorando o progresso que estou fazendo!"
    Saída: Positivo

    Mensagem: "Como uso 'will' e 'going to' em frases futuras?"
    Saída: Neutro

    Mensagem: "Estou tendo dificuldade em entender a pronúncia de algumas palavras. É muito frustrante."
    Saída: Negativo
    """

    configuracao_modelo = {
        "temperature" : 0.1,
        "max_output_tokens" : 8192
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_do_sistema,
        generation_config=configuracao_modelo
    )

    resposta = llm.generate_content(mensagem_usuario)
    return resposta.text.strip().lower()