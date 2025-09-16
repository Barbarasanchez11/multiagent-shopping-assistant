from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import DetectedProduct, GraphState
import streamlit as st

import json

def get_llm():

    api_key = st.secrets["secrets"]["GROQ_API_KEY"]
    
    if not api_key:
        raise ValueError("GROQ_API_KEY no está configurada. Por favor, configura la variable de entorno.")
    
    return ChatGroq(
        model_name="llama-3.1-8b-instant",
        api_key=api_key
    )

prompt = ChatPromptTemplate.from_template("""
Eres un asistente de compras.

Tu tarea es extraer todos los productos mencionados por el usuario y sus cantidades. Siempre debes devolver al menos un producto si hay alguno reconocible.

- Acepta productos aunque no tengan unidad clara.
- Si hay confusión, asume que se trata de una unidad por defecto (1).
- Siempre responde SOLO en formato JSON con una lista de objetos como:

[
  {{"name": "manzanas", "quantity": 3}},
  {{"name": "agua", "quantity": 2}},
  {{"name": "arroz", "quantity": 1}}
]

No añadas texto ni explicaciones adicionales.

Entrada del usuario: {user_input}
""")


def parse_output(text: str):
    try:
        data = json.loads(text)
        products = [
            DetectedProduct(name=item["name"].lower(), quantity=int(item["quantity"]))
            for item in data
        ]
        return products
    except json.JSONDecodeError as e:
        return []

def classify_intent_agent(state: GraphState) -> GraphState:
    
    llm = get_llm()
    chain = prompt | llm
    
    response = chain.invoke({"user_input": state.user_input})
    state.detected_products = parse_output(response.content)
   
    return state
