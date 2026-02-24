import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://www.firstcry.com/svcs/SearchResult.svc/GetSearchResultProductsFilters?PageNo=1&PageSize=40&SortExpression=PriceLowToHigh&OnSale=5&SearchString=brand&MasterBrand=113&pcode=695024&isclub=0"

SEEN_FILE = "seen.json"


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
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def main():
    seen = load_seen()

    response = requests.get(API_URL)
    data = response.json()

    products = data.get("d", {}).get("ProductList", [])

    updated = False

    for product in products:
        product_id = str(product.get("ProductId"))
        name = product.get("ProductName")
        price = product.get("Price")
        url = "https://www.firstcry.com" + product.get("Url")

        if product_id not in seen:
            message = f"🔥 <b>New Hot Wheels Listed!</b>\n\n{name}\n💰 ₹{price}\n🔗 {url}"
            send_telegram(message)
            seen.add(product_id)
            updated = True

    if updated:
        save_seen(seen)


if __name__ == "__main__":
    main()
