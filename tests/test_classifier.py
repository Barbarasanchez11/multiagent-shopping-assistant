from schemas import GraphState
from agents.intent_classifier import classify_intent_agent

state = GraphState(user_input="I want 3 apples and 2 bottles of water")
new_state = classify_intent_agent(state)

print("Detected products:")
if new_state.detected_products:
    for product in new_state.detected_products:
        print(f"- {product.name}: {product.quantity}")
else:
    print("No products detected.")
