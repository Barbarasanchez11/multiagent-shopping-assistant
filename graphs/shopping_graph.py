from langgraph.graph import StateGraph, END
from agents.intent_classifier import classify_intent_agent
from agents.mercadona_search import mercadona_search_agent
from agents.price_calculator import total_price_agent
from schemas import GraphState

graph = StateGraph(GraphState)

graph.add_node("intent_classifier", classify_intent_agent)
graph.add_node("mercadona_search", mercadona_search_agent)
graph.add_node("total_price", total_price_agent)



graph.set_entry_point("intent_classifier")
graph.add_edge("intent_classifier", "mercadona_search")
graph.add_edge("mercadona_search", "total_price")
graph.add_edge("total_price", END)

app = graph.compile()

