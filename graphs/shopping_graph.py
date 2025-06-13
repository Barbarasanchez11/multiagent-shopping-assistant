from langgraph.graph import StateGraph, END
from schemas import GraphState
from agents.intent_classifier import classify_intent_agent

graph = StateGraph(GraphState)
graph.add_node("intent_classifier", classify_intent_agent)
graph.set_entry_point("intent_classifier")
graph.add_edge("intent_classifier", END)
app = graph.compile()

