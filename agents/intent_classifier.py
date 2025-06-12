from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import DetectedProduct, GraphState
import re

llm = ChatGroq(model_name="mixtral-8x7b-32768")

prompt = ChatPromptTemplate.from_template("""
You're a helpful assistant. From the following sentence, extract all items the user wants to buy.
For each item, return:
- The name of the product
- The quantity (as a number)

Sentence: {user_input}

Expected output:
- Product: <name>, Quantity: <number>
""")

chain = prompt | llm

def parse_output(text: str):
    products = []
    for line in text.split("\n"):
        match = re.match(r"- Product: (.*), Quantity: (\d+)", line.strip())
        if match:
            name = match.group(1).strip()
            quantity = int(match.group(2))
            products.append(DetectedProduct(name=name, quantity=quantity))
    return products

def classify_intent_agent(state: GraphState) -> GraphState:
    response = chain.invoke({"user_input": state.user_input})
    state.detected_products = parse_output(response.content)
    return state