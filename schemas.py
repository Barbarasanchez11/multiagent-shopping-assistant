from pydantic import BaseModel
from typing import List, Optional

class DetectedProduct(BaseModel):
    name: str
    quantity: int

class FoundProduct(BaseModel):
    product_name:str
    price: float
    quantity: int
   

class TotalPrice(BaseModel):
    products: List[FoundProduct]
    total_price: float


class GraphState(BaseModel):
    user_input: str
    detected_products: Optional[List[DetectedProduct]] = None
    found_products:List[FoundProduct] = []
    total_tickect: Optional[TotalPrice] = None

