from typing import List, Optional
from pydantic import BaseModel

class DetectedProduct(BaseModel):
    name: str
    quantity: int

class GraphState(BaseModel):
    user_input: str
    detected_products: Optional[List[DetectedProduct]] = None