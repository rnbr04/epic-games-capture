# Epic Games Free Games Capture

A Django-based API service that monitors and captures free game offers from the Epic Games Store. The service automatically tracks currently free games and sends webhook notifications when new offers are detected.

## Features

- Fetches current free games from Epic Games Store
- Webhook notifications for new free game offers
- Database persistence of game offers to prevent duplicate offers during scheduled API calls to Epic Games for checking new offers. 

## Technology Stack

- **Framework**: Django + Django REST Framework
- **API Client**: epicstore-api (forked for my use-case, look at requirements.txt for the forked version)
- **Authentication**: Token Authentication
- **Database**: Django ORM (configurable)
- **Deployment**: Heroku-ready

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd epic-games-capture
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export WEBHOOK_URL="your-discord-webhook-url"
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser and generate an auth token:
```bash
python manage.py createsuperuser
python manage.py drf_create_token <username>
```

7. Ensure that you save this token. In case you want to regenerate the token again:
```bash
python manage.py drf_create_token -r <username>
```

## Configuration

### Environment Variables

- `WEBHOOK_URL`: Discord webhook URL for game notifications

### Database

The project uses Django's default database configuration. Update `settings.py` for production databases (PostgreSQL recommended for Heroku).

## API Usage

### Endpoint

**GET** `/epic_games_free/`

### Authentication

Include the token in the request header:
```
Authorization: Token <your-token>
```

### Example Request

```bash
curl -H "Authorization: Token your-token-here" \
     http://localhost:8000/epic_games_free/
```

### Response

- **200 OK**: Successfully fetched and processed free games
- **401 Unauthorized**: Invalid or missing token

## How It Works

1. The API fetches current free games from Epic Games Store
2. Filters games with `discountPrice == 0` and valid product slugs
3. Extracts relevant information (title, description, expiry date, images)
4. Detects if offer is a bundle and updates description accordingly
5. Saves new offers to the database
6. Sends webhook notification for newly detected games

## Webhook Notification Format

Notifications include:
- Game title
- Expiry date (Unix timestamp format)
- Product URL
- Description
- Key image

## Deployment

### Heroku

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set WEBHOOK_URL="your-webhook-url"
```

3. Deploy:
```bash
git push heroku main
```

4. Run migrations:
```bash
heroku run python manage.py migrate
```

## Models

### CurrentOffer

Stores information about current free game offers:
- `title`: Game title
- `description`: Game description
- `expiryDate`: When the offer expires
- `productSlug`: Unique product identifier
- `productLink`: URL to the game page
- `keyImages`: Featured image URL

## Contributing

This was more of a practice project for me but contributions are welcome! Please feel free to submit a Pull Request.

## License

Distributed under the `GNU AGPLv3` License. See [LICENSE](./LICENSE) for more information.

## Acknowledgments

- [epicstore-api](https://github.com/SD4RK/epicstore_api) for Epic Games Store API wrapper
