import httpx    
from schemas import GraphState, DetectedProduct, ProductOptions, ProductOption
import json

def mercadona_search_agent(state: GraphState) -> GraphState:
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
    """
    Busca productos en la API de Mercadona y devuelve múltiples opciones por producto.
    """
    base_url = "https://tienda.mercadona.es/api/categories/"
    
    try:
        response = httpx.get(base_url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error obteniendo categorías: {e}")
        return []

    found_products = []

    for product in products:
        product_name = product['name'].lower()
        quantity = product['quantity']
        product_options = []
        category_id = None

        # Buscar categoría que contenga el producto
        for category in data['results']:
            for subcategory in category['categories']:
                if product_name in subcategory['name'].lower():
                    category_id = subcategory['id']
                    break
            if category_id:
                break

        if not category_id:
            print(f"⚠️ No se encontró categoría para: {product_name}")
            continue

        detail_url = f"{base_url}{category_id}"

        try:
            response_category = httpx.get(detail_url, timeout=10.0)
            response_category.raise_for_status()
            data_category = response_category.json()
        except Exception as e:
            print(f"❌ Error obteniendo categoría {category_id}: {e}")
            continue

        # Buscar TODAS las opciones que coincidan
        for inner_cat in data_category['categories']:
            for product_category in inner_cat['products']:
                if product_name.lower() in product_category['display_name'].lower():
                    try:
                        price = product_category['price_instructions']['unit_price']
                        display_name = product_category['display_name']
                        
                        product_options.append({
                            'product_name': display_name,
                            'price': price,
                            'quantity': quantity,
                            'original_query': product_name
                        })
                    except (KeyError, TypeError) as e:
                        continue

        # Si encontramos opciones, añadir la mejor (más barata)
        if product_options:
            # Ordenar por precio y tomar la más barata
            best_option = min(product_options, key=lambda x: x['price'])
            found_products.append(best_option)
            print(f"✅ {product_name}: {len(product_options)} opciones encontradas, seleccionada: {best_option['product_name']} - {best_option['price']}€")
        else:
            print(f"⚠️ No se encontraron productos para: {product_name}")

    return found_products

def search_products_with_options(products: list, max_options: int = 5):
    """
    Busca productos en la API de Mercadona y devuelve múltiples opciones por producto.
    Permite al usuario elegir entre diferentes opciones.
    """
    base_url = "https://tienda.mercadona.es/api/categories/"
    
    try:
        response = httpx.get(base_url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error obteniendo categorías: {e}")
        return []

    all_product_options = []

    for product in products:
        product_name = product['name'].lower()
        quantity = product['quantity']
        product_options = []
        category_id = None

        # Buscar categoría que contenga el producto
        for category in data['results']:
            for subcategory in category['categories']:
                if product_name in subcategory['name'].lower():
                    category_id = subcategory['id']
                    break
            if category_id:
                break

        if not category_id:
            print(f"⚠️ No se encontró categoría para: {product_name}")
            continue

        detail_url = f"{base_url}{category_id}"

        try:
            response_category = httpx.get(detail_url, timeout=10.0)
            response_category.raise_for_status()
            data_category = response_category.json()
        except Exception as e:
            print(f"❌ Error obteniendo categoría {category_id}: {e}")
            continue

        # Buscar TODAS las opciones que coincidan
        for inner_cat in data_category['categories']:
            for product_category in inner_cat['products']:
                if product_name.lower() in product_category['display_name'].lower():
                    try:
                        price = product_category['price_instructions']['unit_price']
                        display_name = product_category['display_name']
                        
                        product_options.append({
                            'product_name': display_name,
                            'price': price,
                            'quantity': quantity,
                            'original_query': product_name
                        })
                    except (KeyError, TypeError) as e:
                        continue

        # Ordenar por precio y limitar opciones
        product_options.sort(key=lambda x: x['price'])
        product_options = product_options[:max_options]
        
        if product_options:
            all_product_options.append({
                'original_query': product_name,
                'quantity': quantity,
                'options': product_options
            })
            print(f"✅ {product_name}: {len(product_options)} opciones encontradas")
        else:
            print(f"⚠️ No se encontraron productos para: {product_name}")

    return all_product_options

def mercadona_search_with_options_agent(state: GraphState) -> GraphState:
    """
    Nuevo agente que busca productos y devuelve múltiples opciones para que el usuario elija.
    """
    if not state.detected_products:
        return state
    
    products = []
    
    for item in state.detected_products:
        product_dict = item.dict()
        products.append(product_dict)

    # Buscar opciones múltiples
    product_options_data = search_products_with_options(products, max_options=5)
    
    # Convertir a objetos ProductOptions
    product_options = []
    for item in product_options_data:
        options = [ProductOption(**option) for option in item['options']]
        product_options.append(ProductOptions(
            original_query=item['original_query'],
            quantity=item['quantity'],
            options=options
        ))
    
    state.product_options = product_options
    return state

if __name__ == "__main__":
    print(search_products_by_name([
        {"name": "leche", "quantity": 1},
        {"name": "agua", "quantity": 2},
        {"name": "pan", "quantity": 1}
    ]))