from schemas import GraphState, FoundProduct, TotalPrice

def total_price_agent(state: GraphState) -> GraphState:
    if not state.found_products:

        return state
    
    products_price = []
    for item in state.found_products:
        product_dict = item.dict()
        products_price.append(product_dict)
    
    total_price = calculate_total_price(products_price)
    
    state.total_tickect = TotalPrice(
    products=state.found_products,
    total_price=total_price   
    )
   
    return state

def calculate_total_price(found_products: list) -> float:
  total_price = 0
  total_ticket = []
  for product in found_products:
    total_price += product['price'] * product['quantity']
    total_ticket.append(product)
    

  
  
  total_ticket.append({'total_price':total_price})
  return total_price

