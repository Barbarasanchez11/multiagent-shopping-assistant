from pydantic import BaseModel
from typing import List, Optional

class DetectedProduct(BaseModel):
    name: str
    quantity: int

class FoundProduct(BaseModel):
    product_name: str
    price: float
    quantity: int
    product_id: Optional[str] = None 

class ProductOption(BaseModel):
    """Opción individual de producto encontrada en la API"""
    product_name: str
    price: float
    quantity: int
    original_query: str

class ProductOptions(BaseModel):
    """Múltiples opciones para un producto específico"""
    original_query: str
    quantity: int
    options: List[ProductOption]

class TotalPrice(BaseModel):
    products: List[FoundProduct]
    total_price: float

class GraphState(BaseModel):
    user_input: str
    detected_products: Optional[List[DetectedProduct]] = None
    found_products: List[FoundProduct] = []
    product_options: List[ProductOptions] = [] 
    selected_products: List[FoundProduct] = []  
    total_tickect: Optional[TotalPrice] = None

