import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# 1. Carrega as variáveis do .env
load_dotenv()

# 2. Recupera a chave da API
api_key = os.getenv("GOOGLE_API_KEY")

# 3. Valida se a chave foi carregada
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY não encontrada no .env")

print("🔑 Chave carregada com sucesso:", api_key[:10], "...")

# 4. Instancia o modelo do Gemini com LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",  # ou gemini-1.5-pro-latest
    google_api_key=api_key
)

# 5. Mensagem de entrada
mensagem = [HumanMessage(content="Me diga uma curiosidade sobre Marte.")]

# 6. Chamada ao modelo
resposta = llm.invoke(mensagem)

# 7. Imprime a resposta
print("\n🤖 Resposta do Gemini:")
print(resposta.content)
