import os
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from epicstore_api import EpicGamesStoreAPI
from .utils import get_product_link, is_bundle, get_key_image, send_webhook
from .models import CurrentOffer

# add authentication to the main view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    # create api object to handle api calls
    api = EpicGamesStoreAPI()
    
    # get all the free games
    free_games = api.get_free_games()
    
    # cleaning the get_free_games() request
    free_games_data = free_games.get('data')
    free_games_catalog = free_games_data.get('Catalog')
    free_games_search = free_games_catalog.get('searchStore')
    free_games_list = free_games_search.get('elements')

    # filter out these columns
    columns = ['title', 'description', 'expiryDate', 'productSlug', 'categories', 'keyImages']

    # capture the actually free games by looking at
    # their price and productSlug (if it even exists)
    actual_free_games = [{col: game.get(col) for col in columns} for game in free_games_list if game['price']['totalPrice']['discountPrice'] == 0 and 
                        game['productSlug'] != '[]']
    # create a clean JSON response with productLink
    # and updated description in case of a bundle
    games = {}
    for index, product in enumerate(actual_free_games):
        
        product_categories = product['categories']
        
        # check if the product is a bundle
        product_is_bundle = is_bundle(product_categories)
        
        # get the page link accordingly
        product['productLink'] = get_product_link(product['productSlug'], type_bundle=product_is_bundle)
        
        # get wide image
        product['keyImages'] = get_key_image(product['keyImages']) 

        # update the description in case of a bundle
        if product_is_bundle:
            bundle_info = api.get_bundle(product['productSlug'])
            bundle_description = bundle_info['data']['about']['shortDescription']
            product['description'] = bundle_description
        
        # delete unrequired keys
        del product['categories']

        # commit the product into database if not present 
        if not CurrentOffer.objects.filter(productSlug = product['productSlug']):
            g = CurrentOffer(**product)
            g.save()
            send_webhook(webhook_url = os.environ.get("WEBHOOK_URL"),
                         game_title = product["title"],
                         game_expiry_date = f"<t:{int(datetime.fromisoformat(product["expiryDate"]).timestamp())}>",
                         game_url = product["productLink"],
                         game_description = product["description"],
                         game_image = product["keyImages"])
    # return OK
    return Response(status=status.HTTP_200_OK)
