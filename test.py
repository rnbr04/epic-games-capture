from epicstore_api import EpicGamesStoreAPI
import pprint

api = EpicGamesStoreAPI()
free_games = api.get_free_games()
free_games_data = free_games.get('data')
free_games_catalog = free_games_data.get('Catalog')
free_games_search = free_games_catalog.get('searchStore')
free_games_list = free_games_search.get('elements')
columns = ['title', 'description', 'effectiveDate', 'expiryDate', 'productSlug']
actual_free_games = [{col: game.get(col) for col in columns} for game in free_games_list if game['price']['totalPrice']['discountPrice'] == 0 and 
                     game['productSlug'] != '[]']
pprint.pprint(actual_free_games)