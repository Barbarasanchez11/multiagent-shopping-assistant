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
            st.write(f"**{product_group.original_query.upper()}** (cantidad: {product_group.quantity}) - {len(product_group.options)} opciones encontradas")
            
            # Inicializar paginación en session state
            pagination_key = f"page_{product_group.original_query}"
            if pagination_key not in st.session_state:
                st.session_state[pagination_key] = 1
            
            # Añadir filtros y ordenación
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sort_by = st.selectbox(
                    "Ordenar por:",
                    ["Precio (menor a mayor)", "Precio (mayor a menor)", "Nombre A-Z", "Nombre Z-A"],
                    key=f"sort_{product_group.original_query}"
                )
            
            with col2:
                items_per_page = st.selectbox(
                    "Productos por página:",
                    [12, 24, 36, 48, 60],
                    index=1,  # Por defecto 24
                    key=f"per_page_{product_group.original_query}"
                )
            
            with col3:
                search_term = st.text_input(
                    "Filtrar por nombre:",
                    key=f"filter_{product_group.original_query}",
                    placeholder="Ej: integral, sin gluten..."
                )
            
            # Aplicar filtros y ordenación
            filtered_options = product_group.options
            
            # Filtrar por término de búsqueda
            if search_term:
                filtered_options = [opt for opt in filtered_options if search_term.lower() in opt.product_name.lower()]
            
            # Ordenar
            if sort_by == "Precio (menor a mayor)":
                filtered_options.sort(key=lambda x: float(x.price))
            elif sort_by == "Precio (mayor a menor)":
                filtered_options.sort(key=lambda x: float(x.price), reverse=True)
            elif sort_by == "Nombre A-Z":
                filtered_options.sort(key=lambda x: x.product_name)
            elif sort_by == "Nombre Z-A":
                filtered_options.sort(key=lambda x: x.product_name, reverse=True)
            
            # Calcular paginación
            total_pages = (len(filtered_options) + items_per_page - 1) // items_per_page
            current_page = st.session_state[pagination_key]
            
            # Asegurar que la página actual sea válida
            if current_page > total_pages:
                st.session_state[pagination_key] = 1
                current_page = 1
            elif current_page < 1:
                st.session_state[pagination_key] = 1
                current_page = 1
            
            # Calcular índices de inicio y fin
            start_idx = (current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_options = filtered_options[start_idx:end_idx]
            
            # Mostrar controles de paginación
            if total_pages > 1:
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                
                with col1:
                    if st.button("⏮️ Primera", key=f"first_{product_group.original_query}"):
                        st.session_state[pagination_key] = 1
                        st.rerun()
                
                with col2:
                    if st.button("⬅️ Anterior", key=f"prev_{product_group.original_query}"):
                        if current_page > 1:
                            st.session_state[pagination_key] = current_page - 1
                            st.rerun()
                
                with col3:
                    st.write(f"Página {current_page} de {total_pages}")
                
                with col4:
                    if st.button("Siguiente ➡️", key=f"next_{product_group.original_query}"):
                        if current_page < total_pages:
                            st.session_state[pagination_key] = current_page + 1
                            st.rerun()
                
                with col5:
                    if st.button("Última ⏭️", key=f"last_{product_group.original_query}"):
                        st.session_state[pagination_key] = total_pages
                        st.rerun()
            
            # Mostrar opciones en columnas (3 columnas)
            cols = st.columns(3)
            
            for i, option in enumerate(page_options):
                with cols[i % 3]:
                    with st.container():
                        # Mostrar categoría si está disponible
                        if hasattr(option, 'category') and option.category:
                            st.caption(f"📂 {option.category}")
                        
                        st.write(f"**{option.product_name}**")
                        st.write(f"💰 {option.price}€")
                        st.write(f"📊 Total: {float(option.price) * option.quantity:.2f}€")
                        
                        # Usar índice global para el key único
                        global_idx = start_idx + i
                        if st.button(f"➕ Elegir", key=f"select_{product_group.original_query}_{global_idx}"):
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
            
            # Mostrar información de paginación
            st.info(f"Mostrando {len(page_options)} de {len(filtered_options)} opciones filtradas (de {len(product_group.options)} total)")
            
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

    