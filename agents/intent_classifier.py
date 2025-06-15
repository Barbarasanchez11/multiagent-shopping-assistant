from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import DetectedProduct, GraphState
import os
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(model_name="llama3-8b-8192",  api_key=os.getenv("GROQ_API_KEY"))

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


chain = prompt | llm

def parse_output(text: str):
  
    try:
        data = json.loads(text)
        products = [
            DetectedProduct(name=item["name"].lower(), quantity=int(item["quantity"]))
            for item in data
        ]
        return products
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return []

def classify_intent_agent(state: GraphState) -> GraphState:
    response = chain.invoke({"user_input": state.user_input})
    state.detected_products = parse_output(response.content)
   
    return state
