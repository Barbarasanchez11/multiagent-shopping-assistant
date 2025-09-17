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
    initial_sidebar_state="collapsed"
)

# CSS personalizado para interfaz básica pero funcional
st.markdown("""
<style>
    /* Variables de color - Solo verde oliva, vainilla y negro */
    :root {
        --olive: #8BA070;
        --olive-dark: #6B7C4A;
        --vanilla: #F5F5DC;
        --vanilla-light: #FDF7E4;
        --black: #000000;
        --white: #ffffff;
    }

    /* Estilos globales */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .stApp {
        background-color: var(--vanilla-light);
    }

    /* Hero Section */
    .hero-section {
        background: var(--olive);
        color: var(--black);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(139, 160, 112, 0.2);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: -0.025em;
        color: var(--black);
    }
    
    .subtitle {
        font-size: 1.125rem;
        opacity: 0.8;
        margin-bottom: 0;
        line-height: 1.6;
        color: var(--black);
    }

    /* Cards de productos */
    .product-card {
        background: var(--vanilla);
        border: 1px solid var(--olive);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 160, 112, 0.3);
        border-color: var(--olive-dark);
    }
    
    .product-name {
        font-size: 1rem;
        font-weight: 600;
        color: var(--black);
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .product-price {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--black);
        margin: 0.5rem 0;
    }

    /* Botones de cantidad */
    .stButton > button[data-testid*="decrease_"],
    .stButton > button[data-testid*="increase_"],
    .stButton > button[key*="decrease_"],
    .stButton > button[key*="increase_"] {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        min-width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    
    .stButton > button[data-testid*="decrease_"]:hover:not(:disabled),
    .stButton > button[data-testid*="increase_"]:hover:not(:disabled),
    .stButton > button[key*="decrease_"]:hover:not(:disabled),
    .stButton > button[key*="increase_"]:hover:not(:disabled) {
        background: var(--olive-dark) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button[data-testid*="decrease_"]:disabled,
    .stButton > button[data-testid*="increase_"]:disabled,
    .stButton > button[key*="decrease_"]:disabled,
    .stButton > button[key*="increase_"]:disabled {
        background: var(--vanilla) !important;
        color: var(--black) !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    /* Botón Añadir */
    .stButton > button[data-testid*="add_"],
    .stButton > button[key*="add_"] {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        min-width: 120px !important;
        height: 44px !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    
    .stButton > button[data-testid*="add_"]:hover:not(:disabled),
    .stButton > button[key*="add_"]:hover:not(:disabled) {
        background: var(--olive-dark) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 160, 112, 0.3) !important;
    }
    
    .stButton > button[data-testid*="add_"]:disabled,
    .stButton > button[key*="add_"]:disabled {
        background: var(--vanilla) !important;
        color: var(--black) !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }

    /* Botones de paginación */
    .stButton > button[data-testid*="first_"],
    .stButton > button[data-testid*="prev_"],
    .stButton > button[data-testid*="next_"],
    .stButton > button[data-testid*="last_"] {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.025em !important;
        height: 44px !important;
        min-width: 80px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button[data-testid*="first_"]:hover:not(:disabled),
    .stButton > button[data-testid*="prev_"]:hover:not(:disabled),
    .stButton > button[data-testid*="next_"]:hover:not(:disabled),
    .stButton > button[data-testid*="last_"]:hover:not(:disabled) {
        background: var(--olive-dark) !important;
        color: var(--black) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 160, 112, 0.3) !important;
    }
    
    .stButton > button[data-testid*="first_"]:disabled,
    .stButton > button[data-testid*="prev_"]:disabled,
    .stButton > button[data-testid*="next_"]:disabled,
    .stButton > button[data-testid*="last_"]:disabled {
        background: var(--vanilla) !important;
        color: var(--black) !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }

    /* Inputs y selectores */
    .stTextInput > div > div > input {
        border: 2px solid var(--olive);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        background: var(--vanilla);
        color: var(--black);
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--olive-dark);
        outline: none;
        box-shadow: 0 0 0 3px rgba(139, 160, 112, 0.1);
    }
    
    .stSelectbox > div > div {
        background: var(--vanilla);
        border: 2px solid var(--olive);
        border-radius: 8px;
        color: var(--black);
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--olive-dark);
    }

    /* Carrito */
    .cart-section {
        background: var(--vanilla);
        border: 1px solid var(--olive);
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(139, 160, 112, 0.1);
    }

    /* Estilos generales para TODOS los botones de Streamlit */
    .stButton > button {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    
    .stButton > button:hover:not(:disabled) {
        background: var(--olive-dark) !important;
        color: var(--black) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 160, 112, 0.3) !important;
    }
    
    .stButton > button:disabled {
        background: var(--vanilla) !important;
        color: var(--black) !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    /* Forzar estilos para botones específicos que puedan estar heredando otros estilos */
    .stButton > button[type="button"],
    .stButton > button[role="button"] {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Botones de descarga específicos */
    .stDownloadButton > button {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    
    .stDownloadButton > button:hover:not(:disabled) {
        background: var(--olive-dark) !important;
        color: var(--black) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 160, 112, 0.3) !important;
    }
    
    .stDownloadButton > button:disabled {
        background: var(--vanilla) !important;
        color: var(--black) !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    /* Asegurar que todos los botones de descarga tengan el estilo correcto */
    .stDownloadButton > button[type="button"],
    .stDownloadButton > button[role="button"] {
        background: var(--olive) !important;
        color: var(--black) !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
        }
        
        .product-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="main-title">DESCUBRE NUEVOS SABORES</h1>
        <p class="subtitle">Asistente de compras inteligente para productos de supermercado con precios actualizados</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Inicializar estados de la sesión
if 'cart_products' not in st.session_state:
    st.session_state.cart_products = []

if 'search_cache' not in st.session_state:
    st.session_state.search_cache = {}

if 'categories_cache' not in st.session_state:
    st.session_state.categories_cache = None

# Input de búsqueda
st.markdown("### 🔍 ¿Qué necesitas comprar?")
user_input = st.text_input(
    "Escribe tu lista de la compra aquí...",
    placeholder="Ejemplo: 2 de agua, 3 kg de arroz, un pan, leche desnatada...",
    help="Escribe los productos que necesitas y te ayudaremos a encontrarlos con los mejores precios",
    label_visibility="collapsed"
)

# Lógica de búsqueda y procesamiento
if user_input and user_input.strip():
    # Verificar caché
    cache_key = user_input.strip().lower()
    
    if cache_key in st.session_state.search_cache:
        final_state = st.session_state.search_cache[cache_key]
    else:
        with st.spinner("🔍 Buscando productos..."):
            state = GraphState(user_input=user_input)
            final_state = app_with_options.invoke(state)
            st.session_state.search_cache[cache_key] = final_state
    
    if "product_options" in final_state and final_state["product_options"]:
        
        for product_group in final_state["product_options"]:
            # Inicializar paginación
            pagination_key = f"page_{product_group.original_query}"
            if pagination_key not in st.session_state:
                st.session_state[pagination_key] = 1
            
           
            col1, col2 = st.columns(2)
            
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
                    index=1,
                    key=f"per_page_{product_group.original_query}"
                )
            
            # Aplicar ordenación
            filtered_options = product_group.options.copy()
            
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
            
            # Validar página actual
            if current_page > total_pages:
                st.session_state[pagination_key] = 1
                current_page = 1
            elif current_page < 1:
                st.session_state[pagination_key] = 1
                current_page = 1
            
            # Obtener elementos de la página actual
            start_idx = (current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_options = filtered_options[start_idx:end_idx]
            
            # Controles de paginación
            if total_pages > 1:
                st.markdown("### 📄 Navegación")
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                
                with col1:
                    if st.button("Primera", key=f"first_{product_group.original_query}", 
                               disabled=(current_page == 1), use_container_width=True):
                        st.session_state[pagination_key] = 1
                        st.rerun()
                
                with col2:
                    if st.button("Anterior", key=f"prev_{product_group.original_query}", 
                               disabled=(current_page == 1), use_container_width=True):
                        if current_page > 1:
                            st.session_state[pagination_key] = current_page - 1
                            st.rerun()
                
                with col3:
                    st.info(f"Página {current_page} de {total_pages}")
                
                with col4:
                    if st.button("Siguiente", key=f"next_{product_group.original_query}", 
                               disabled=(current_page == total_pages), use_container_width=True):
                        if current_page < total_pages:
                            st.session_state[pagination_key] = current_page + 1
                            st.rerun()
                
                with col5:
                    if st.button("Última", key=f"last_{product_group.original_query}", 
                               disabled=(current_page == total_pages), use_container_width=True):
                        st.session_state[pagination_key] = total_pages
                        st.rerun()
            
            # Mostrar productos en columnas
            st.markdown("### 🛍️ Productos Encontrados")
            cols = st.columns(3)
            
            for i, option in enumerate(page_options):
                with cols[i % 3]:
                    # Crear tarjeta de producto
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-name">{option.product_name.upper()}</div>
                        <div class="product-price">{option.price}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # ID único del producto
                    global_idx = start_idx + i
                    product_id = f"{product_group.original_query}_{global_idx}"
                    
                    # Manejar cantidad temporal
                    temp_quantity_key = f"temp_quantity_{product_id}"
                    if temp_quantity_key not in st.session_state:
                        st.session_state[temp_quantity_key] = 0
                    
                    temp_quantity = st.session_state[temp_quantity_key]
                    
                    # Control de cantidad
                    col_left, col_center, col_right = st.columns([1, 1, 1])
                    
                    with col_left:
                        if st.button("−", key=f"decrease_{product_id}", 
                                   disabled=(temp_quantity == 0), use_container_width=True):
                            st.session_state[temp_quantity_key] -= 1
                            st.rerun()
                    
                    with col_center:
                        st.markdown(f"""
                        <div style="
                            background: var(--vanilla);
                            border: 2px solid var(--olive);
                            border-radius: 8px;
                            padding: 0.5rem;
                            text-align: center;
                            font-weight: 700;
                            font-size: 1.2rem;
                            color: var(--black);
                            height: 40px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">
                            {temp_quantity}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_right:
                        if st.button("+", key=f"increase_{product_id}", use_container_width=True):
                            st.session_state[temp_quantity_key] += 1
                            st.rerun()
                    
                    # Botón añadir al carrito
                    if st.button("Añadir", key=f"add_{product_id}", 
                               disabled=(temp_quantity == 0), use_container_width=True):
                        
                        # Buscar si el producto ya existe en el carrito
                            existing_product = None
                            for cart_product in st.session_state.cart_products:
                                if cart_product.product_id == product_id:
                                    existing_product = cart_product
                                    break
                            
                            if existing_product:
                                existing_product.quantity += temp_quantity
                                st.success(f"✅ Cantidad actualizada: {existing_product.quantity}")
                            else:
                                selected_product = FoundProduct(
                                    product_name=option.product_name,
                                    price=float(option.price),
                                    quantity=temp_quantity,
                                    product_id=product_id
                                )
                                st.session_state.cart_products.append(selected_product)
                                st.success(f"✅ {option.product_name} añadido al carrito!")
                            
                        # Reiniciar cantidad temporal
                            st.session_state[temp_quantity_key] = 0
                            st.rerun()

            st.info(f"📊 Mostrando {len(page_options)} de {len(filtered_options)} opciones")
            st.divider()
    else:
        st.warning("⚠️ No se pudieron encontrar productos para tu lista. Intenta con otros productos.")

# Carrito de compras
if st.session_state.cart_products:
    st.markdown('<div class="cart-section">', unsafe_allow_html=True)
    st.header("🛒 Tu Carrito de Compras")
    
    total = 0
    for i, product in enumerate(st.session_state.cart_products):
        subtotal = product.price * product.quantity
        total += subtotal
        
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{product.product_name}**")
        
        with col2:
            st.write(f"Cantidad: {product.quantity}")
        
        with col3:
            st.write(f"{product.price:.2f}€")
        
        with col4:
            st.write(f"**{subtotal:.2f}€**")
        
        with col5:
            if st.button("🗑️", key=f"remove_{i}", help="Eliminar del carrito"):
                st.session_state.cart_products.pop(i)
                st.rerun()

    st.metric("💰 Total", f"{total:.2f}€")
    
    # Botones de descarga y limpieza
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Descargar TXT", use_container_width=True):
            ticket = type('Ticket', (), {
                'products': st.session_state.cart_products, 
                'total_price': total
            })()
            txt_file = generate_txt(ticket).encode("utf-8")
            st.download_button("📄 Descargar TXT", txt_file, "lista_compra.txt", use_container_width=True)
    
    with col2:
        if st.button("📋 Descargar JSON", use_container_width=True):
            ticket = {
                "products": [p.dict() for p in st.session_state.cart_products], 
                "total_price": total
            }
            json_file = json.dumps(ticket, indent=2, ensure_ascii=False).encode("utf-8")
            st.download_button("📋 Descargar JSON", json_file, "lista_compra.json", use_container_width=True)
    
    with col3:
        if st.button("🧹 Limpiar Carrito", use_container_width=True):
            st.session_state.cart_products = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👋 ¡Bienvenido a tu Asistente de Compras! Introduce tu lista de la compra para comenzar.")