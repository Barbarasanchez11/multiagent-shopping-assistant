import streamlit as st
from utils.exporter import generate_txt, generate_json
from graphs.shopping_graph import app_with_options
from schemas import GraphState, FoundProduct
import json
import functools
import time


st.set_page_config(
    page_title="Asistente de Compras",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    /* Importar fuentes de Google */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Variables CSS inspiradas en la estética de flavo */
    :root {
        --primary-color: #8BA070; /* Verde oliva principal como en la imagen */
        --primary-dark: #6B7A4F;
        --secondary-color: #F5DDE1; /* Rosa suave de fondo */
        --accent-color: #E8B94F; /* Amarillo dorado como en la imagen */
        --success-color: #A8D5BA; /* Verde menta suave */
        --danger-color: #FF8A80; /* Rojo coral suave */
        --warning-color: #FFD54F; /* Amarillo suave */
        --info-color: #B3E5FC; /* Azul cielo suave */
        --light-bg: #FDF7E4; /* Amarillo crema como en la imagen */
        --warm-bg: #FDF7E4; /* Amarillo crema */
        --pink-bg: #F5DDE1; /* Rosa de fondo como en la imagen */
        --olive-bg: #8BA070; /* Verde oliva principal */
        --dark-text: #000000; /* Negro como en la imagen */
        --gray-text: #666666; /* Gris medio */
        --border-color: #E0E0E0; /* Gris claro */
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
        --shadow-xl: 0 16px 32px rgba(0, 0, 0, 0.20);
    }
    
    /* Aplicar fuente a todo el body */
    .main .block-container {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section con estética de flavo */
    .hero-section {
        background: var(--olive-bg);
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        text-align: left;
        color: var(--dark-text);
        position: relative;
        overflow: hidden;
        border: none;
        box-shadow: var(--shadow-lg);
    }
    
    .hero-section::before {
        content: '⭐';
        position: absolute;
        top: 2rem;
        left: 2rem;
        font-size: 3rem;
        color: var(--accent-color);
        opacity: 0.8;
        animation: float 6s ease-in-out infinite;
    }
    
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -30%;
        right: -10%;
        width: 40%;
        height: 150%;
        background: radial-gradient(ellipse, var(--accent-color) 0%, transparent 70%);
        opacity: 0.1;
        border-radius: 50%;
        animation: float 8s ease-in-out infinite reverse;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        color: var(--dark-text);
        text-shadow: none;
        animation: fadeInUp 0.8s ease-out;
        letter-spacing: -0.02em;
        line-height: 1.1;
        text-transform: uppercase;
        margin-left: 4rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        color: var(--dark-text);
        margin-bottom: 2.5rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
        line-height: 1.5;
        max-width: 500px;
        margin-left: 4rem;
    }
    
    .hero-tip {
        background: rgba(255, 179, 71, 0.1);
        border: 1px solid rgba(255, 179, 71, 0.2);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        margin: 2rem auto;
        max-width: 500px;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    .search-container {
        max-width: 600px;
        margin: 0 auto;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    /* Animaciones */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Botones con estética de flavo */
    .stButton > button {
        background: var(--dark-text);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.8rem;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        min-width: 120px;
        height: 44px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        background: var(--primary-color);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    .stButton > button:disabled {
        background: #94a3b8;
        cursor: not-allowed;
        transform: none;
        opacity: 0.6;
    }
    
    /* Botones "Añadir" - estilos movidos a sección de correcciones críticas */
    
    .stButton > button[data-testid*="remove_"] {
        background: linear-gradient(135deg, var(--danger-color), #E57373);
        min-width: 48px;
        height: 40px;
        font-size: 0.85rem;
        border-radius: 10px;
    }
    
    .stButton > button[data-testid*="remove_"]:hover {
        background: linear-gradient(135deg, #E57373, #EF5350);
        animation: bounce 0.6s ease-in-out;
        transform: translateY(-2px);
    }
    
    .stButton > button[data-testid*="Descargar"] {
        background: linear-gradient(135deg, var(--accent-color), #FF9800);
        min-width: 180px;
        height: 48px;
        border-radius: 16px;
    }
    
    .stButton > button[data-testid*="Descargar"]:hover {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        transform: translateY(-2px);
    }
    
    .stButton > button[data-testid*="Limpiar"] {
        background: linear-gradient(135deg, var(--gray-text), #8D6E63);
        min-width: 180px;
        height: 48px;
        border-radius: 16px;
    }
    
    .stButton > button[data-testid*="Limpiar"]:hover {
        background: linear-gradient(135deg, #8D6E63, #6D4C41);
        transform: translateY(-2px);
    }
    
    /* Tarjetas de productos con estética de flavo */
    .product-card {
        background: var(--light-bg);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
        text-align: center;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 16px;
        transition: all 0.4s ease;
        z-index: 1;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-color);
    }
    
    .product-card:hover::before {
        opacity: 0.2;
    }
    
    .product-emoji {
        display: none;
    }
    
    .product-name {
        font-size: 1rem;
        font-weight: 600;
        color: #000000;
        margin-bottom: 1rem;
        line-height: 1.4;
        text-align: center;
        letter-spacing: 0.01em;
        text-transform: uppercase;
        position: relative;
        z-index: 10;
        min-height: 2.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        word-wrap: break-word;
        overflow-wrap: break-word;
        opacity: 1;
        visibility: visible;
    }
    
    .product-price {
        font-size: 1.6rem;
        font-weight: 800;
        color: #000000;
        text-align: center;
        margin: 1rem 0;
        position: relative;
        z-index: 10;
        opacity: 1;
        visibility: visible;
    }
    
    .product-badge {
        display: none;
    }
    
    /* Filtros con estética de flavo */
    .filter-section {
        background: var(--light-bg);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .filter-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-color), var(--primary-color), var(--accent-color));
    }
    
    .filter-section::after {
        content: '🔍';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.2rem;
        opacity: 0.3;
        color: var(--primary-color);
    }
    
    /* Carrito con estética moderna */
    .cart-section {
        background: linear-gradient(135deg, var(--pink-bg) 0%, var(--warm-bg) 100%);
        color: var(--dark-text);
        padding: 3rem;
        border-radius: 32px;
        margin-top: 3rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    .cart-section::before {
        content: '';
        position: absolute;
        top: -30%;
        right: -20%;
        width: 80%;
        height: 160%;
        background: radial-gradient(ellipse, var(--accent-color) 0%, transparent 70%);
        opacity: 0.08;
        border-radius: 50%;
        animation: gentle-rotate 15s linear infinite;
    }
    
    .cart-section::after {
        content: '';
        position: absolute;
        bottom: -20%;
        left: -10%;
        width: 60%;
        height: 120%;
        background: radial-gradient(ellipse, var(--secondary-color) 0%, transparent 70%);
        opacity: 0.06;
        border-radius: 50%;
        animation: gentle-rotate 20s linear infinite reverse;
    }
    
    @keyframes gentle-rotate {
        from { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.1); }
        to { transform: rotate(360deg) scale(1); }
    }
    
    .cart-content {
        position: relative;
        z-index: 1;
    }
    
    .cart-item {
        background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.6) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
    }
    
    .cart-item:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        transform: translateX(8px) translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Información de paginación */
    .pagination-info {
        background: var(--olive-bg);
        color: var(--dark-text);
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
        font-size: 0.85rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    
    /* Botones de paginación */
    .pagination-button {
        background: var(--olive-bg);
        color: var(--dark-text);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        text-transform: uppercase;
        letter-spacing: 0.02em;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .pagination-button:hover:not(:disabled) {
        background: var(--primary-color);
        color: white;
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    .pagination-button:disabled {
        background: #666666;
        color: #999999;
        cursor: not-allowed;
        opacity: 0.6;
    }
    
    /* Inputs con estética moderna */
    .stTextInput > div > div > input {
        border: 2px solid var(--border-color);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #ffffff 0%, var(--light-bg) 100%);
        box-shadow: var(--shadow-sm);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 4px rgba(255, 179, 71, 0.15);
        outline: none;
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--gray-text);
        font-weight: 400;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, var(--light-bg) 100%);
        border: 2px solid var(--border-color);
        border-radius: 16px;
        font-family: 'Inter', sans-serif;
        box-shadow: var(--shadow-sm);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--accent-color);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    /* Sidebar eliminado - CSS removido */
    
    /* Spinner personalizado */
    .stSpinner > div {
        border-color: var(--primary-color);
        border-top-color: var(--secondary-color);
    }
    
    /* Alertas mejoradas */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: var(--shadow-md);
    }
    
    /* Divider personalizado */
    .stDivider {
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        height: 2px;
        margin: 2rem 0;
    }
    
    /* Botones del selector de cantidad */
    .quantity-button {
        background: var(--dark-text);
        color: var(--olive-bg);
        border: none;
        border-radius: 6px;
        font-weight: bold;
        font-size: 1.2rem;
        min-width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quantity-button:hover:not(:disabled) {
        background: var(--primary-color);
        color: white;
        transform: translateY(-1px);
    }
    
    .quantity-button:disabled {
        background: #666666;
        color: #999999;
        cursor: not-allowed;
        opacity: 0.6;
    }
    
    /* Botones de cantidad - estilos movidos a sección de correcciones críticas */
    
    /* Botones de paginación con color verde oliva */
    .stButton > button[data-testid*="first_"],
    .stButton > button[data-testid*="prev_"],
    .stButton > button[data-testid*="next_"],
    .stButton > button[data-testid*="last_"] {
        background: var(--olive-bg) !important;
        color: var(--dark-text) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.02em !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button[data-testid*="first_"]:hover:not(:disabled),
    .stButton > button[data-testid*="prev_"]:hover:not(:disabled),
    .stButton > button[data-testid*="next_"]:hover:not(:disabled),
    .stButton > button[data-testid*="last_"]:hover:not(:disabled) {
        background: var(--primary-color) !important;
        color: white !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .stButton > button[data-testid*="first_"]:disabled,
    .stButton > button[data-testid*="prev_"]:disabled,
    .stButton > button[data-testid*="next_"]:disabled,
    .stButton > button[data-testid*="last_"]:disabled {
        background: #666666 !important;
        color: #999999 !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
        }
        
        .product-card {
            padding: 1rem;
        }
        
        .cart-section {
            padding: 1.5rem;
        }
    }
    
    /* ===== CORRECCIONES CRÍTICAS DE VISIBILIDAD ===== */
    
    /* 1. Botones de cards visibles - Verde oliva con texto blanco */
    .stButton > button[data-testid*="decrease_"],
    .stButton > button[data-testid*="increase_"],
    .stButton > button[key*="decrease_"],
    .stButton > button[key*="increase_"] {
        background: var(--olive-bg) !important;
        color: white !important;
        border: 1px solid var(--border-color) !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        font-size: 1.2rem !important;
        min-width: 32px !important;
        height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[data-testid*="decrease_"]:hover:not(:disabled),
    .stButton > button[data-testid*="increase_"]:hover:not(:disabled),
    .stButton > button[key*="decrease_"]:hover:not(:disabled),
    .stButton > button[key*="increase_"]:hover:not(:disabled) {
        background: var(--primary-color) !important;
        color: white !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button[data-testid*="decrease_"]:disabled,
    .stButton > button[data-testid*="increase_"]:disabled,
    .stButton > button[key*="decrease_"]:disabled,
    .stButton > button[key*="increase_"]:disabled {
        background: #666666 !important;
        color: #999999 !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    .stButton > button[data-testid*="add_"],
    .stButton > button[key*="add_"] {
        background: var(--olive-bg) !important;
        color: white !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 600 !important;
        min-width: 120px !important;
        height: 44px !important;
        font-size: 0.9rem !important;
        border-radius: 12px !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[data-testid*="add_"]:hover:not(:disabled),
    .stButton > button[key*="add_"]:hover:not(:disabled) {
        background: #059669 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stButton > button[data-testid*="add_"]:disabled,
    .stButton > button[key*="add_"]:disabled {
        background: #666666 !important;
        color: #999999 !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    /* 2. Selectboxes visibles */
    .stSelectbox > div > div > div[data-baseweb="select"] {
        background: white !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: var(--dark-text) !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox [data-baseweb="select"] [data-baseweb="base-input"] {
        color: var(--dark-text) !important;
        font-weight: 500 !important;
    }
    
    /* Dropdown menu options */
    .stSelectbox [role="listbox"] [role="option"] {
        background: white !important;
        color: var(--dark-text) !important;
    }
    
    .stSelectbox [role="listbox"] [role="option"]:hover {
        background: var(--light-bg) !important;
    }
    
    /* 3. Paginación consistente */
    div[data-testid="column"] .stButton > button {
        background: var(--olive-bg) !important;
        color: var(--dark-text) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    div[data-testid="column"] .stButton > button:hover:not(:disabled) {
        background: var(--primary-color) !important;
        color: white !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    div[data-testid="column"] .stButton > button:disabled {
        background: #666666 !important;
        color: #999999 !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    /* 4. Ocultar tooltip */
    .hero-tip {
        display: none !important;
    }
    
    div[class*="hero-tip"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="main-title">DESCUBRE NUEVOS SABORES</h1>
        <p class="subtitle">Asistente de compras inteligente para productos de supermercado con precios actualizados</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Inicializar carrito en session state
if 'cart_products' not in st.session_state:
    st.session_state.cart_products = []

# Inicializar caché de búsquedas
if 'search_cache' not in st.session_state:
    st.session_state.search_cache = {}

# Inicializar caché de categorías
if 'categories_cache' not in st.session_state:
    st.session_state.categories_cache = None


st.markdown("###  ¿Qué necesitas comprar?")
user_input = st.text_input(
    "Escribe tu lista de la compra aquí...",
    placeholder="Ejemplo: 2 de agua, 3 kg de arroz, un pan, leche desnatada...",
    help="Escribe los productos que necesitas y te ayudaremos a encontrarlos con los mejores precios",
    label_visibility="collapsed"
)

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
        selected_products = []
        
        for product_group in final_state["product_options"]:
            # Inicializar paginación en session state
            pagination_key = f"page_{product_group.original_query}"
            if pagination_key not in st.session_state:
                st.session_state[pagination_key] = 1
            
            # Añadir filtros y ordenación con diseño mejorado
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            
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
                    index=1,  # Por defecto 24
                    key=f"per_page_{product_group.original_query}"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Aplicar filtros y ordenación
            filtered_options = product_group.options
            
            # Ordenar
            if sort_by == "Precio (menor a mayor)":
                filtered_options.sort(key=lambda x: float(x.price))
            elif sort_by == "Precio (mayor a menor)":
                filtered_options.sort(key=lambda x: float(x.price), reverse=True)
            elif sort_by == "Nombre A-Z":
                filtered_options.sort(key=lambda x: x.product_name)
            elif sort_by == "Nombre Z-A":
                filtered_options.sort(key=lambda x: x.product_name, reverse=True)
            
         
            total_pages = (len(filtered_options) + items_per_page - 1) // items_per_page
            current_page = st.session_state[pagination_key]
            
           
            if current_page > total_pages:
                st.session_state[pagination_key] = 1
                current_page = 1
            elif current_page < 1:
                st.session_state[pagination_key] = 1
                current_page = 1
            
       
            start_idx = (current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_options = filtered_options[start_idx:end_idx]
            
          
            if total_pages > 1:
               
                
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
                    st.markdown(f'<div class="pagination-info">Página {current_page} de {total_pages}</div>', 
                               unsafe_allow_html=True)
                
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
            
           
            cols = st.columns(3)
            
            for i, option in enumerate(page_options):
                with cols[i % 3]:
                  
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-name">{option.product_name.upper()}</div>
                        <div class="product-price">{option.price}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                   
                    global_idx = start_idx + i
                    product_id = f"{product_group.original_query}_{global_idx}"
                    
                 
                    current_quantity = 0
                    for cart_product in st.session_state.cart_products:
                        if cart_product.product_id == product_id:
                            current_quantity = cart_product.quantity
                            break
                    
                  
                    temp_quantity_key = f"temp_quantity_{product_id}"
                    if temp_quantity_key not in st.session_state:
                        st.session_state[temp_quantity_key] = 0
                    
                    temp_quantity = st.session_state[temp_quantity_key]
                    
                  
                    col_left, col_center, col_right = st.columns([1, 1, 1])
                    
                    with col_left:
                       
                        if st.button("−", key=f"decrease_{product_id}", help="Disminuir cantidad", disabled=(temp_quantity == 0), use_container_width=True):
                            st.session_state[temp_quantity_key] -= 1
                            st.rerun()
                    
                    with col_center:
                       
                        st.markdown(f"""
                        <div style="
                            background: var(--light-bg);
                            border: 1px solid var(--border-color);
                            border-radius: 6px;
                            padding: 0.5rem;
                            text-align: center;
                            font-weight: bold;
                            font-size: 1.1rem;
                            color: var(--dark-text);
                            box-shadow: var(--shadow-sm);
                            height: 32px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">
                            {temp_quantity}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_right:
                      
                        if st.button("+", key=f"increase_{product_id}", help="Aumentar cantidad", use_container_width=True):
                            st.session_state[temp_quantity_key] += 1
                            st.rerun()
                    
                   
                    if st.button("Añadir", key=f"add_{product_id}", help="Añadir al carrito", disabled=(temp_quantity == 0), use_container_width=True):
                       
                        existing_product = None
                        for cart_product in st.session_state.cart_products:
                            if cart_product.product_id == product_id:
                                existing_product = cart_product
                                break
                        
                        if existing_product:
                           
                            existing_product.quantity += temp_quantity
                            st.success(f"Cantidad actualizada: {existing_product.quantity}")
                        else:
                            
                            selected_product = FoundProduct(
                                product_name=option.product_name,
                                price=float(option.price),
                                quantity=temp_quantity,
                                product_id=product_id
                            )
                            st.session_state.cart_products.append(selected_product)
                            st.success(f"{option.product_name} añadido al carrito!")
                        
                      
                        st.session_state[temp_quantity_key] = 0
                        st.rerun()
            
           
            st.info(f"Mostrando {len(page_options)} de {len(filtered_options)} opciones filtradas (de {len(product_group.options)} total)")
            
            st.divider()
    else:
        st.warning("No se pudieron encontrar productos para tu lista. Intenta con otros productos.")


if st.session_state.cart_products:
    st.markdown('<div class="cart-section">', unsafe_allow_html=True)
    st.markdown('<div class="cart-content">', unsafe_allow_html=True)
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

 
    total_html = f"""
    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; text-align: center; margin: 1rem 0;">
        <h3 style="margin: 0; color: white;">💰 Total: {total:.2f}€</h3>
    </div>
    """
    st.markdown(total_html, unsafe_allow_html=True)
    
   
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(" Descargar TXT", use_container_width=True):
            ticket = type('Ticket', (), {'products': st.session_state.cart_products, 'total_price': total})()
            txt_file = generate_txt(ticket).encode("utf-8")
            st.download_button(" Descargar TXT", txt_file, "lista_compra.txt", use_container_width=True)
    
    with col2:
        if st.button(" Descargar JSON", use_container_width=True):
            ticket = {"products": [p.dict() for p in st.session_state.cart_products], "total_price": total}
            json_file = json.dumps(ticket, indent=2, ensure_ascii=False).encode("utf-8")
            st.download_button(" Descargar JSON", json_file, "lista_compra.json", use_container_width=True)
    
    with col3:
        if st.button("🧹 Limpiar Carrito", use_container_width=True):
            st.session_state.cart_products = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  
    st.markdown('</div>', unsafe_allow_html=True) 

else:
   
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, var(--light-bg) 0%, var(--warm-bg) 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
        margin: 2rem 0;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
        <h3 style="color: var(--primary-color); margin-bottom: 1rem; font-size: 1.5rem;">
            ¡Bienvenido a tu Asistente de Compras!
        </h3>
        <p style="color: var(--gray-text); font-size: 1.1rem; line-height: 1.6;">
            Introduce tu lista de la compra para comenzar.<br>
            <strong>Ejemplo:</strong> "2 de agua, 3 kg de arroz, un pan"
        </p>
    </div>
    """, unsafe_allow_html=True)

