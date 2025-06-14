from pydantic import BaseModel
from typing import List, Optional

class DetectedProduct(BaseModel):
    name: str
    quantity: int

class FoundProduct(BaseModel):
    name:str
    price: float
    quantity: int
    total_price: float
    image: Optional[str] = None


class GraphState(BaseModel):
    user_input: str
    detected_products: Optional[List[DetectedProduct]] = None
    found_products: Optional[List[FoundProduct]] = None
