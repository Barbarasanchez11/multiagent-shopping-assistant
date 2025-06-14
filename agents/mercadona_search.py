import httpx    
from schemas import GraphState

def mercadona_search_agent(state: GraphState) -> GraphState:
    if not state.detected_products:
        return state
    
def search_products_by_name(product_name: str):
    found_products = []
    url = "https://tienda.mercadona.es/api/categories/"
    response = httpx.get(url)

    data = response.json()
    categories = data.get("results", [])
    print(categories)

    for main_category in categories:
        subcategories = main_category.get("categories", [])
        print("categoria:", main_category.get("name", ""), "subcategorías")
 
        for sub in subcategories:
            sub_id = sub.get("id")
            sub_name = sub.get("name", "")
            print("Subcategoria:", sub_name, sub_id)

            sub_url = f"https://tienda.mercadona.es/api/categories/{sub_id}"
            sub_response = httpx.get(sub_url)
            sub_data = sub_response.json()
            products = sub_data.get("categories", [{}])[0].get("products", [])
            print( products)

          
                


    

if __name__ == "__main__":
    search_products_by_name("pan")