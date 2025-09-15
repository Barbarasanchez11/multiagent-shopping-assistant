import streamlit as st
from utils.exporter import generate_txt, generate_json
from graphs.shopping_graph import app_with_options
from schemas import GraphState, FoundProduct
import json
import functools
import time

# Configurar página
st.set_page_config(
    page_title="Asistente de Compras",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la UI
st.markdown("""
<style>
    /* Resetear estilos de Streamlit para botones */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        min-width: 120px !important;
        height: 40px !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        background: linear-gradient(45deg, #5a6fd8, #6a4190) !important;
    }
    
    .stButton > button:disabled {
        background: #6c757d !important;
        cursor: not-allowed !important;
        transform: none !important;
        opacity: 0.6 !important;
    }
    
    /* Botones de productos específicos */
    .stButton > button[data-testid*="select_"] {
        background: linear-gradient(45deg, #28a745, #20c997) !important;
        min-width: 100px !important;
        height: 36px !important;
        font-size: 0.85rem !important;
    }
    
    .stButton > button[data-testid*="select_"]:hover {
        background: linear-gradient(45deg, #218838, #1ea085) !important;
    }
    
    /* Botones de carrito */
    .stButton > button[data-testid*="remove_"] {
        background: linear-gradient(45deg, #dc3545, #c82333) !important;
        min-width: 40px !important;
        height: 36px !important;
        font-size: 0.8rem !important;
    }
    
    .stButton > button[data-testid*="remove_"]:hover {
        background: linear-gradient(45deg, #c82333, #bd2130) !important;
    }
    
    /* Botones de descarga */
    .stButton > button[data-testid*="Descargar"] {
        background: linear-gradient(45deg, #fd7e14, #e83e8c) !important;
        min-width: 140px !important;
        height: 40px !important;
    }
    
    .stButton > button[data-testid*="Descargar"]:hover {
        background: linear-gradient(45deg, #e8710a, #d63384) !important;
    }
    
    /* Botón limpiar carrito */
    .stButton > button[data-testid*="Limpiar"] {
        background: linear-gradient(45deg, #6c757d, #5a6268) !important;
        min-width: 140px !important;
        height: 40px !important;
    }
    
    .stButton > button[data-testid*="Limpiar"]:hover {
        background: linear-gradient(45deg, #5a6268, #495057) !important;
    }
    
    /* Título principal */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Tarjetas de productos */
    .product-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    /* Filtros */
    .filter-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Carrito */
    .cart-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-top: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .cart-item {
        background: rgba(255,255,255,0.15);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Información de paginación */
    .pagination-info {
        background: linear-gradient(45deg, #17a2b8, #6f42c1);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        font-size: 1rem;
    }
    
    /* Mejorar selectboxes */
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea !important;
    }
    
    /* Mejorar text input */
    .stTextInput > div > div > input {
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛒 Tu Asistente de Compras</h1>', unsafe_allow_html=True)

# Inicializar carrito en session state
if 'cart_products' not in st.session_state:
    st.session_state.cart_products = []

# Inicializar caché de búsquedas
if 'search_cache' not in st.session_state:
    st.session_state.search_cache = {}

# Inicializar caché de categorías
if 'categories_cache' not in st.session_state:
    st.session_state.categories_cache = None

# El caché funciona internamente sin mostrar botones al usuario

user_input = st.text_input("Introduce tu lista de la compra (en español)")

if user_input and user_input.strip():
    # Verificar caché antes de hacer la búsqueda
    cache_key = user_input.strip().lower()
    
    if cache_key in st.session_state.search_cache:
        # Usar caché silenciosamente
        final_state = st.session_state.search_cache[cache_key]
    else:
        with st.spinner("🔍 Buscando productos..."):
            state = GraphState(user_input=user_input)
            final_state = app_with_options.invoke(state)
            # Guardar en caché
            st.session_state.search_cache[cache_key] = final_state
    
    if "product_options" in final_state and final_state["product_options"]:
        st.subheader("Opciones Encontradas")
        
        selected_products = []
        
        for product_group in final_state["product_options"]:
            st.write(f"**{product_group.original_query.upper()}** (cantidad: {product_group.quantity}) - {len(product_group.options)} opciones encontradas")
            
            # Inicializar paginación en session state
            pagination_key = f"page_{product_group.original_query}"
            if pagination_key not in st.session_state:
                st.session_state[pagination_key] = 1
            
            # Añadir filtros y ordenación con diseño mejorado
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            st.markdown("### 🔍 Filtros y Ordenación")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sort_by = st.selectbox(
                    "📊 Ordenar por:",
                    ["Precio (menor a mayor)", "Precio (mayor a menor)", "Nombre A-Z", "Nombre Z-A"],
                    key=f"sort_{product_group.original_query}"
                )
            
            with col2:
                items_per_page = st.selectbox(
                    "📄 Productos por página:",
                    [12, 24, 36, 48, 60],
                    index=1,  # Por defecto 24
                    key=f"per_page_{product_group.original_query}"
                )
            
            with col3:
                search_term = st.text_input(
                    "🔎 Filtrar por nombre:",
                    key=f"filter_{product_group.original_query}",
                    placeholder="Ej: integral, sin gluten..."
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
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
            
            # Mostrar controles de paginación mejorados
            if total_pages > 1:
                st.markdown("### 📄 Navegación")
                
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                
                with col1:
                    if st.button("⏮️ Primera", key=f"first_{product_group.original_query}", 
                               disabled=(current_page == 1), use_container_width=True):
                        st.session_state[pagination_key] = 1
                        st.rerun()
                
                with col2:
                    if st.button("⬅️ Anterior", key=f"prev_{product_group.original_query}", 
                               disabled=(current_page == 1), use_container_width=True):
                        if current_page > 1:
                            st.session_state[pagination_key] = current_page - 1
                            st.rerun()
                
                with col3:
                    st.markdown(f'<div class="pagination-info">Página {current_page} de {total_pages}</div>', 
                               unsafe_allow_html=True)
                
                with col4:
                    if st.button("Siguiente ➡️", key=f"next_{product_group.original_query}", 
                               disabled=(current_page == total_pages), use_container_width=True):
                        if current_page < total_pages:
                            st.session_state[pagination_key] = current_page + 1
                            st.rerun()
                
                with col5:
                    if st.button("Última ⏭️", key=f"last_{product_group.original_query}", 
                               disabled=(current_page == total_pages), use_container_width=True):
                        st.session_state[pagination_key] = total_pages
                        st.rerun()
            
            # Mostrar opciones en columnas (3 columnas) con diseño mejorado
            cols = st.columns(3)
            
            for i, option in enumerate(page_options):
                with cols[i % 3]:
                    # Crear tarjeta de producto simplificada
                    st.markdown(f"""
                    <div class="product-card">
                        <h4 style="margin: 0.5rem 0; color: #2c3e50; font-size: 1.1rem;">{option.product_name}</h4>
                        <div style="text-align: center; margin: 1rem 0;">
                            <span style="font-size: 1.5rem; font-weight: bold; color: #28a745;">{option.price}€</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Usar índice global para el key único
                    global_idx = start_idx + i
                    product_id = f"{product_group.original_query}_{global_idx}"
                    
                    # Verificar si el producto ya está en el carrito para mostrar la cantidad
                    current_quantity = 0
                    for cart_product in st.session_state.cart_products:
                        if cart_product.product_id == product_id:
                            current_quantity = cart_product.quantity
                            break
                    
                    # Inicializar cantidad temporal si no existe
                    temp_quantity_key = f"temp_quantity_{product_id}"
                    if temp_quantity_key not in st.session_state:
                        st.session_state[temp_quantity_key] = 0
                    
                    temp_quantity = st.session_state[temp_quantity_key]
                    
                    # Crear layout: Botón Añadir + Selector de cantidad compacto
                    col1, col2 = st.columns([2, 3])
                    
                    with col1:
                        # Botón Añadir solo activo si hay cantidad > 0
                        if st.button("Añadir", key=f"add_{product_id}", help="Añadir al carrito", disabled=(temp_quantity == 0)):
                            # Verificar si el producto ya existe en el carrito
                            existing_product = None
                            for cart_product in st.session_state.cart_products:
                                if cart_product.product_id == product_id:
                                    existing_product = cart_product
                                    break
                            
                            if existing_product:
                                # Si existe, aumentar cantidad
                                existing_product.quantity += temp_quantity
                                st.success(f"✅ Cantidad actualizada: {existing_product.quantity}")
                            else:
                                # Si no existe, añadir nuevo producto
                                selected_product = FoundProduct(
                                    product_name=option.product_name,
                                    price=float(option.price),
                                    quantity=temp_quantity,
                                    product_id=product_id
                                )
                                st.session_state.cart_products.append(selected_product)
                                st.success(f"✅ {option.product_name} añadido al carrito!")
                            
                            # Resetear cantidad temporal
                            st.session_state[temp_quantity_key] = 0
                            st.rerun()

                    with col2:
                        # Mostrar cantidad temporal en el centro
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(45deg, #667eea, #764ba2);
                            color: white;
                            padding: 0.6rem 1rem;
                            border-radius: 10px;
                            text-align: center;
                            font-weight: bold;
                            font-size: 1.2rem;
                            margin: 0.5rem 0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            border: 2px solid rgba(255,255,255,0.2);
                        ">
                            {temp_quantity}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botones en una fila horizontal usando st.columns en el nivel principal
                        # Necesitamos salir del contexto de col2 para crear nuevas columnas
                        pass
                    
                    # Crear botones fuera del contexto de col2 para evitar anidación
                    btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])
                    
                    with btn_col1:
                        # Espacio vacío para alinear con el botón Añadir
                        st.write("")
                    
                    with btn_col2:
                        # Botón izquierdo: - o papelera según la cantidad temporal
                        if temp_quantity > 1:
                            if st.button("➖", key=f"decrease_{product_id}", help="Disminuir cantidad", use_container_width=True):
                                st.session_state[temp_quantity_key] -= 1
                                # Solo rerun si hay cambio real
                                if st.session_state[temp_quantity_key] >= 0:
                                    st.rerun()
                        elif temp_quantity == 1:
                            if st.button("🗑️", key=f"remove_{product_id}", help="Eliminar cantidad", use_container_width=True):
                                st.session_state[temp_quantity_key] = 0
                                st.rerun()
                    
                    with btn_col3:
                        # Botón derecho: siempre + para aumentar cantidad temporal
                        if st.button("➕", key=f"increase_{product_id}", help="Aumentar cantidad", use_container_width=True):
                            st.session_state[temp_quantity_key] += 1
                            # Solo rerun si hay cambio real
                            if st.session_state[temp_quantity_key] > 0:
                                st.rerun()
            
            # Mostrar información de paginación
            st.info(f"Mostrando {len(page_options)} de {len(filtered_options)} opciones filtradas (de {len(product_group.options)} total)")
            
            st.divider()
    else:
        st.warning("No se pudieron encontrar productos para tu lista. Intenta con otros productos.")

# Mostrar carrito con diseño mejorado
if st.session_state.cart_products:
    st.markdown('<div class="cart-section">', unsafe_allow_html=True)
    st.markdown("### 🛒 Tu Carrito de Compras")
    
    total = 0
    for i, product in enumerate(st.session_state.cart_products):
        subtotal = product.price * product.quantity
        total += subtotal
        
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            cart_item_html = f"""
            <div class="cart-item">
                <strong>{product.product_name}</strong>
            </div>
            """
            st.markdown(cart_item_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div class='cart-item'><strong>Cantidad: {product.quantity}</strong></div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"<div class='cart-item'>{product.price:.2f}€</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"<div class='cart-item'><strong>{subtotal:.2f}€</strong></div>", unsafe_allow_html=True)
        
        with col5:
            if st.button("🗑️", key=f"remove_{i}", help="Eliminar del carrito"):
                st.session_state.cart_products.pop(i)
                st.rerun()

    # Total destacado
    total_html = f"""
    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; text-align: center; margin: 1rem 0;">
        <h3 style="margin: 0; color: white;">💰 Total: {total:.2f}€</h3>
    </div>
    """
    st.markdown(total_html, unsafe_allow_html=True)
    
    # Botones de descarga mejorados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Descargar TXT", use_container_width=True):
            ticket = type('Ticket', (), {'products': st.session_state.cart_products, 'total_price': total})()
            txt_file = generate_txt(ticket).encode("utf-8")
            st.download_button("📄 Descargar TXT", txt_file, "lista_compra.txt", use_container_width=True)
    
    with col2:
        if st.button("📋 Descargar JSON", use_container_width=True):
            ticket = {"products": [p.dict() for p in st.session_state.cart_products], "total_price": total}
            json_file = json.dumps(ticket, indent=2, ensure_ascii=False).encode("utf-8")
            st.download_button("📋 Descargar JSON", json_file, "lista_compra.json", use_container_width=True)
    
    with col3:
        if st.button("🧹 Limpiar Carrito", use_container_width=True):
            st.session_state.cart_products = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Introduce tu lista de la compra para comenzar. Ejemplo: '2 de agua, 3 kg de arroz, un pan'")

