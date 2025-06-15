from graphs.shopping_graph import app
from schemas import GraphState

if __name__ == "__main__":
    state = GraphState(user_input="2 de agua, 3 kg de arroz, un pan")
    final_state = app.invoke(state)
    print("Final state- final_state")
   
    
