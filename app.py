import streamlit as st
from utils.exporter import generate_txt, generate_json
from graphs.shopping_graph import app_with_options
from schemas import GraphState, FoundProduct
import json

st.title("Tu Asistente de Compras")

# Inicializar carrito en session state
if 'cart_products' not in st.session_state:
    st.session_state.cart_products = []

user_input = st.text_input("Introduce tu lista de la compra (en español)")

if user_input and user_input.strip():
    state = GraphState(user_input=user_input)
    final_state = app_with_options.invoke(state)
    
    if "product_options" in final_state and final_state["product_options"]:
        st.subheader("Opciones Encontradas")
        
        selected_products = []
        
        for product_group in final_state["product_options"]:
            st.write(f"**{product_group.original_query.upper()}** (cantidad: {product_group.quantity})")
            
            # Crear columnas para mostrar opciones
            cols = st.columns(min(len(product_group.options), 3))
            
            for i, option in enumerate(product_group.options):
                with cols[i % 3]:
                    with st.container():
                        st.write(f"**{option.product_name}**")
                        st.write(f"Precio: {option.price}€")
                        st.write(f"Total: {float(option.price) * option.quantity:.2f}€")
                        
                        if st.button(f"Elegir", key=f"select_{product_group.original_query}_{i}"):
                            # Crear producto seleccionado
                            selected_product = FoundProduct(
                                product_name=option.product_name,
                                price=float(option.price),
                                quantity=option.quantity
                            )
                            
                            # Añadir al carrito
                            st.session_state.cart_products.append(selected_product)
                            st.success(f"✅ {option.product_name} añadido al carrito!")
                            st.rerun()
            
            st.divider()
    else:
        st.warning("No se pudieron encontrar productos para tu lista. Intenta con otros productos.")

# Mostrar carrito
if st.session_state.cart_products:
    st.subheader("Tu Carrito")
    
    total = 0
    for i, product in enumerate(st.session_state.cart_products):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(f"{product.product_name} x{product.quantity}")
        
        with col2:
            st.write(f"{product.price:.2f}€")
        
        with col3:
            subtotal = product.price * product.quantity
            st.write(f"{subtotal:.2f}€")
            total += subtotal
        
        with col4:
            if st.button("🗑️", key=f"remove_{i}"):
                st.session_state.cart_products.pop(i)
                st.rerun()
    
    st.write(f"**Total: {total:.2f}€**")
    
    # Botones de descarga
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Descargar TXT"):
            ticket = type('Ticket', (), {'products': st.session_state.cart_products, 'total_price': total})()
            txt_file = generate_txt(ticket).encode("utf-8")
            st.download_button("Descargar TXT", txt_file, "lista_compra.txt")
    
    with col2:
        if st.button("Descargar JSON"):
            ticket = {"products": [p.dict() for p in st.session_state.cart_products], "total_price": total}
            json_file = json.dumps(ticket, indent=2, ensure_ascii=False).encode("utf-8")
            st.download_button("Descargar JSON", json_file, "lista_compra.json")
    
    with col3:
        if st.button("🧹 Limpiar Carrito"):
            st.session_state.cart_products = []
            st.rerun()

else:
    st.info("Introduce tu lista de la compra para comenzar. Ejemplo: '2 de agua, 3 kg de arroz, un pan'")

    