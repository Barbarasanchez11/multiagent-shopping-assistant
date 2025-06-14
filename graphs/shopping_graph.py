from langgraph.graph import StateGraph, END
from agents.intent_classifier import classify_intent_agent
from agents.translator import translator_agent
from agents.mercadona_search import mercadona_search_agent

from schemas import GraphState

graph = StateGraph(GraphState)

graph.add_node("intent_classifier", classify_intent_agent)
graph.add_node("translator", translator_agent)
graph.add_node("mercadona_search", mercadona_search_agent)



graph.set_entry_point("intent_classifier")
graph.add_edge("intent_classifier", "translator")
graph.add_edge("translator", "mercadona_search")
graph.add_edge("mercadona_search", END)

app = graph.compile()

