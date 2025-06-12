from graphs.shopping_graph import app
from schemas import GraphState



state = GraphState(user_input="I want 2 tomatoes and 1 milk")
final_state = app.invoke(state)

print(final_state)
