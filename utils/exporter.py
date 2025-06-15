import json
from io import StringIO
from schemas import TotalPrice

def generate_txt(ticket: TotalPrice) -> str:
    buffer = StringIO()
    for item in ticket.products:
        line = f"{item.product_name} x{item.quantity} = {item.price * item.quantity:.2f}€\n"
        buffer.write(line)
    buffer.write(f"\nTotal: {ticket.total_price:.2f}€\n")
    return buffer.getvalue()

def generate_json(ticket: TotalPrice) -> str:
    return json.dumps(ticket.model_dump(), indent=2, ensure_ascii=False)
