from schemas import GraphState, FoundProduct, TotalPrice

def total_price_agent(state: GraphState) -> GraphState:
    print('-TOTAL AGENT ENTRANDA-')
    print('total_price_agent',state.found_products)
    print('-TOTAL AGENT SALIDA-')
    if not state.found_products:

        return state
    
    products_price = []
    for item in state.found_products:
        product_dict = item.dict()
        products_price.append(product_dict)
    print('-'*20)
    print(products_price,'products_price')
    print('-'*20)
    
    total_price = calculate_total_price(products_price)
    print('-'*20)
    print('total_price',total_price)
    print('-'*20)
    state.total_tickect = TotalPrice(
    products=state.found_products,
    total_price=total_price   
    )
    print('-'*20)
    print('state.total_tickect',state.total_tickect)
    print('-'*20)
  
  

    #total_price = calculate_total_price(state.found_products)
    #state.total_price = total_price
    return state

def calculate_total_price(found_products: list) -> float:
  total_price = 0
  total_ticket = []
  for product in found_products:
    total_price += product['price'] * product['quantity']
    print('-'*20)
    print('total_price',total_price)
    print('-'*20)
    total_ticket.append(product)
    

  
  
  total_ticket.append({'total_price':total_price})
  print('-'*20)
  print('total_ticket',total_ticket)
  print('-'*20)
  return total_price

