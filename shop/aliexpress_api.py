import requests

def fetch_aliexpress_products(query="cleaning equipment", page=1):
    url = "https://ali-express1.p.rapidapi.com/search"
    querystring = {
        "query": query,
        "page": page
    }

    headers = {
        "X-RapidAPI-Key": "9ae6ea7b43msh14942b68a1a1256p19fc12jsn6f308b978720",
        "X-RapidAPI-Host": "ali-express1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        raw_products = response.json().get("docs", [])
        
        # Convert to template-friendly format
        formatted_products = []
        for item in raw_products:
            formatted_products.append({
                "title": item.get("product_title", "No Title"),
                "price": f"${item.get('app_sale_price', '0')}",
                "image_url": item.get("product_main_image_url", ""),
                "product_url": item.get("product_detail_url", "#")
            })

        return formatted_products

    return []
