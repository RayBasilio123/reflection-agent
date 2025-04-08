import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv(dotenv_path="c:/Users/rayba/Music/Analista/LangGraph_Develop_LLM_powered_AI_agents/reflection-agent/.env")




reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é um influenciador viral do Twitter avaliando um tweet. Gere uma crítica e recomendações detalhadas para o tweet do usuário, com até 200 caracteres. Sempre forneça recomendações detalhadas, incluindo sugestões sobre comprimento, viralidade, estilo, etc."
    ),
    MessagesPlaceholder(variable_name="messages"),
])

generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é um assistente de um influenciador tech do Twitter encarregado de escrever excelentes publicações. Gere o melhor tweet possível com base no pedido do usuário, com até 200 caracteres. Se o usuário fornecer críticas, responda com uma versão revisada de suas tentativas anteriores."
    ),
    MessagesPlaceholder(variable_name="messages"),
])

# Modelo Anthropic (utilizando Claude – escolha um modelo compatível; aqui usamos "claude-3-haiku")
# llm = ChatAnthropic(
#     model="claude-3-haiku-20240307",
#     anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
# )
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature= 0.7,
    max_tokens=500,
    top_p=0.9
)

# Chains
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm 
 # Modelo Gemini

# Modelo Anthrop