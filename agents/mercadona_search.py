import httpx    
from schemas import GraphState, FoundProduct

def mercadona_search_agent(state: GraphState) -> GraphState:
    print("Buscando en mercadona...",state.detected_products)
    if not state.detected_products:
        print("No encuentra. ")
        return state