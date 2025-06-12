from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import DetectedProduct, GraphState
import json

llm = ChatGroq(model_name="llama3-8b-8192")

prompt = ChatPromptTemplate.from_template("""
You are a shopping assistant.

Your task is to extract product names and their quantities from the user input.

Respond ONLY with a JSON array like this:

[
  {{"name": "apples", "quantity": 3}},
  {{"name": "water", "quantity": 2}}
]

Do not include any extra text or explanations.

User input: {user_input}
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
