import httpx    
from schemas import GraphState, DetectedProduct
import json

def mercadona_search_agent(state: GraphState) -> GraphState:
    if not state.detected_products:
        return state
    
    products = []
    
    for item in state.detected_products:
     
     product_dict = item.dict()
     products.append(product_dict)

    print(products,'products')


    search_products_by_name(products)
 
    return state

def search_products_by_name(products: list):
    print('-'*20)   
    print('entra a search_products_by_name',products)
    print('-'*20)
    found_products = []
    url = "https://tienda.mercadona.es/api/categories/"

  
    response = httpx.get(url)


    data = response.json()

    for product in products:
        product_name = product['name']
        print('productos dentro del array de search_products_by_name',product_name)
        print('-'*20)
        for category in data['results']:
            category_found = 'No encontrada'
            category_id = 'No encontrado'
            for subcategory in category['categories']:
                #print('subcategory',subcategory)
                if product_name.lower() in subcategory['name'].lower():
                    category_found = subcategory['name']
                    category_id = subcategory['id']
                    break
            if category_found != 'No encontrada':
                break
        found_products.append({
                    'product_name': product['name'],
                    'cantidad': product['quantity'],
                    'category_found': category_found,
                    'category_id': category_id,
                    
                })
                
   
    print('found_products',found_products)
    for product in found_products:
        print('-'*20)
        print('product',product)
        print('-'*20)

   #for category in categories:
       # for subcategory in category[categories]:
           # print('-'*20)
            #print(subcategory)
            #print(category.name)
            #print('-'*20)
            #print(subcategory)
            #return

    return response

if __name__ == "__main__":
    print(search_products_by_name("pan"))
