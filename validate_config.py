import json

with open("langgraph.json") as f:
    cfg = json.load(f)

print("ENTRY POINT:", cfg["graphs"]["default"]["entry_point"])
print("NODE FUNCTION:", cfg["graphs"]["default"]["nodes"]["intent_classifier"]["function"])
print("EDGE TARGET:", cfg["graphs"]["default"]["edges"]["intent_classifier"])
