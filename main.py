from graphs.shopping_graph import app
from schemas import GraphState

if __name__ == "__main__":
    state = GraphState(user_input="")
    final_state = app.invoke(state)
    print("Final state:")
    print(final_state)

