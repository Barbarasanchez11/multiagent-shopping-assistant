from schemas import GraphState
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="llama3-8b-8192")

prompt = ChatPromptTemplate.from_template("""
Translate this grocery item to Spanish. Respond with just the word.

Input: {word}
""")

chain = prompt | llm

def translate_to_spanish(word: str) -> str:
    response = chain.invoke({"word": word})
    return response.content.strip().replace('"', '').lower()

def translator_agent(state: GraphState) -> GraphState:
    if not state.detected_products:
        return state

    for item in state.detected_products:
        translated = translate_to_spanish(item.name)
        item.name = translated
    return state
