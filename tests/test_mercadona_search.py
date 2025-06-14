from agents.mercadona_search import search_products_by_name

if __name__ == "__main__":
    results = search_products_by_name("pan")
    for r in results:
        print(r)
