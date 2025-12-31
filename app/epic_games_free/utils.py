def get_product_link(product_slug, type_bundle=False):
    if type_bundle:
        return f"https://store.epicgames.com/bundles/{product_slug}"
    return f"https://store.epicgames.com/p/{product_slug}"

def is_bundle(categories):
    return any('bundles' in category.get('path') for category in categories)

def get_key_image(keyImages):
    return [image['url'] for image in keyImages if image['type'] == 'OfferImageWide'][0]