import requests

def get_product_link(product_slug, type_bundle=False):
    if type_bundle:
        return f"https://store.epicgames.com/bundles/{product_slug}"
    return f"https://store.epicgames.com/p/{product_slug}"

def is_bundle(categories):
    return any('bundles' in category.get('path') for category in categories)

def get_key_image(keyImages):
    return [image['url'] for image in keyImages if image['type'] == 'OfferImageWide'][0]

def send_webhook(webhook_url, username, avatar_url, game_title, game_expiry_date, game_url, game_description, game_image):
    payload = {
        "embeds": [
            {
                "title": game_title,
                "description": f"**Free** until {game_expiry_date}\n\n[**Open in browser ↗**]({game_url})\n\n{game_description}",
                "image": {
                    "url": game_image
                },
                "thumbnail": {
                    "url": "https://dripgoku.s-ul.eu/epic-games-bot/I8ih4lph.png"
                }
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=payload, headers={'Content-Type': 'application/json'})
        # Raise an exception for bad status codes
        response.raise_for_status()
        print("Webhook sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")


