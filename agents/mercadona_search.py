import httpx    
from schemas import GraphState, DetectedProduct
import json

def mercadona_search_agent(state: GraphState) -> GraphState:
    print('mercadona_search_agent',state)
    if not state.detected_products:
        return state
    
    products = []
    
    for item in state.detected_products:
     
     product_dict = item.dict()
     products.append(product_dict)

    found_products = search_products_by_name(products)
    state.found_products = found_products
 
    return state

def search_products_by_name(products: list):
   
    base_url = "https://tienda.mercadona.es/api/categories/"
    response = httpx.get(base_url)
    data = response.json()

    found_products = []

    for product in products:
        product_name = product['name'].lower()
        quantity = product['quantity']
        price = None
        category_id = None

        for category in data['results']:
            for subcategory in category['categories']:
                if product_name in subcategory['name'].lower():
                    category_id = subcategory['id']
                    print(f"Subcategoría encontrada: {subcategory['name']} (ID: {category_id})")
                    break
            if category_id:
                break

        if not category_id:
            continue

        detail_url = f"{base_url}{category_id}"

        try:
            response_category = httpx.get(detail_url)
            data_category = response_category.json()
        except Exception as e:
          
            continue

       
        match_found = False
        for inner_cat in data_category['categories']:
            for product_category in inner_cat['products']:
                
                if product_name.lower() in product_category['display_name'].lower():
                    match_found = True
                    price = product_category['price_instructions']['unit_price']
                    break
                if match_found:
                    break
            if match_found:
                found_products.append({'product_name':product_name,
                     'price': price,
                     'quantity':quantity})
                break

                

    return found_products



if __name__ == "__main__":
    print(search_products_by_name([
        {"name": "leche", "quantity": 1},
        {"name": "agua", "quantity": 2},
        {"name": "pan", "quantity": 1}
    ]))