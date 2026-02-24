import requests
import time
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://www.firstcry.com/svcs/SearchResult.svc/GetSearchResultProductsFilters?PageNo=1&PageSize=40&SortExpression=PriceLowToHigh&OnSale=5&SearchString=brand&MasterBrand=113&pcode=695024&isclub=0"

CHECK_INTERVAL = 300  # 5 minutes

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def load_seen():
    try:
        with open("seen.json", "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open("seen.json", "w") as f:
        json.dump(list(seen), f)

def get_products():
    response = requests.get(API_URL)
    return response.json()

def main():
    seen = load_seen()

    while True:
        print("Checking for new Hot Wheels...")
        try:
            data = get_products()

            products = data.get("d", {}).get("ProductList", [])

            for product in products:
                product_id = str(product.get("ProductId"))
                name = product.get("ProductName")
                price = product.get("Price")
                url = "https://www.firstcry.com" + product.get("Url")

                if product_id not in seen:
                    message = f"🔥 <b>New Hot Wheels Listed!</b>\n\n{name}\n💰 ₹{price}\n🔗 {url}"
                    send_telegram(message)
                    seen.add(product_id)
                    save_seen(seen)

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
