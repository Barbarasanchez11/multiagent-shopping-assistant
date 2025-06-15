from graphs.shopping_graph import app
from schemas import GraphState
from utils.exporter import generate_txt, generate_json

if __name__ == "__main__":
    state = GraphState(user_input="2 de agua, 3 kg de arroz, un pan")
    final_state = app.invoke(state)
   
    
with open("lista_compra.txt", "w", encoding="utf-8") as f:
    f.write(generate_txt(final_state["total_tickect"]))

with open("lista_compra.json", "w", encoding="utf-8") as f:
    f.write(generate_json(final_state["total_tickect"]))

