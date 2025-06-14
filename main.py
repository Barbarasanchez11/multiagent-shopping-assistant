from schemas import GraphState, DetectedProduct
from agents.mercadona_search import mercadona_search_agent

if __name__ == "__main__":
    test_state = GraphState(
        user_input="",
        detected_products=[
            DetectedProduct(name="leche", quantity=1),
            DetectedProduct(name="pan", quantity=2),
            DetectedProduct(name="huevos", quantity=4)
        ]
    )

    result = mercadona_search_agent(test_state)

    print("Result:", result)
