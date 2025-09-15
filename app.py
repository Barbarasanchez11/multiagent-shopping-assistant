import streamlit as st
from utils.exporter import generate_txt, generate_json

from graphs.shopping_graph import app
from schemas import GraphState

st.title("Tu Asistente de Compras")

user_input = st.text_input("Introduce tu lista de la compra (en español)")

if user_input and user_input.strip():
    state = GraphState(user_input=user_input)
    final_state = app.invoke(state)
    
    if "total_tickect" in final_state and final_state["total_tickect"]:
        ticket = final_state["total_tickect"]

        st.subheader("Lista Generada")

        st.text(generate_txt(ticket))

        txt_file = generate_txt(ticket).encode("utf-8")
        st.download_button("Descargar TXT", txt_file, "lista_compra.txt")

        json_file = generate_json(ticket).encode("utf-8")
        st.download_button("Descargar JSON", json_file, "lista_compra.json")
    else:
        st.warning("No se pudieron encontrar productos para tu lista. Intenta con otros productos.")
else:
    st.info("Introduce tu lista de la compra para comenzar. Ejemplo: '2 de agua, 3 kg de arroz, un pan'")

    