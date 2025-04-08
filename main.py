from typing import List, Sequence
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph
from chains import generate_chain, reflect_chain

REFLECT = "reflect"
GENERATE = "generate"

# Nó de geração: chama o chain de geração e retorna a resposta já formatada como AIMessage
def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

# Nó de reflexão: chama o chain de reflexão e retorna a resposta já formatada como AIMessage
def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

# Configura o grafo com os nós e as condições de parada
builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

def should_continue(state: List[BaseMessage]):
  
    if len(state) >= 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

# Função para extrair o tweet final da lista de mensagens
def extrair_tweet_final(state: Sequence[BaseMessage]) -> str:
    for msg in reversed(state):
        if isinstance(msg, AIMessage):
            # Ignora mensagens com análise/reflexão
            if not any(keyword in msg.content.lower() for keyword in ["avaliação", "recomendações", "dicas", "sugestões"]):
                return msg.content.strip()
    return "Tweet final não encontrado."

if __name__ == "__main__":
    print("Iniciando o fluxo com LangGraph + Gemini...\n")

    entrada = HumanMessage(content="""Melhore este tweet:
@LangChainAI — o novo recurso Tool Calling está seriamente subestimado.

Após uma longa espera, finalmente chegou – facilitando a implementação de agentes entre diferentes modelos via chamadas de função.

Fiz um vídeo cobrindo o novo post do blog deles.
""")

    resultado = graph.invoke([entrada])

    print("\nEstado final:")
    for i, msg in enumerate(resultado):
        tipo = msg.__class__.__name__
        print(f"\nMensagem {i+1} ({tipo}):\n{msg.content.strip()}")

    tweet_final = extrair_tweet_final(resultado)
    print("\nTweet final pronto para publicação:")
    print(tweet_final)

    print("\nFluxo finalizado com sucesso.")
