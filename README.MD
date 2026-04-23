[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/alex0515-ui/flight_tracker)
# FlyWatch API for monitoring flight prices and managing user subscriptions. Built with Django, Django Rest Framework (DRF), Celery, and Redis.

## Core Functionality
- **Flight Search**: Integration with SerpApi (Google Flights) to find real-time flight data.
- **Caching**: Results are cached in Redis for 5 minutes to optimize API usage.
- **Resilience**: Implemented Exponential Backoff to handle external API downtime.
- **Price Monitoring**: Celery background tasks check active subscriptions every 6 hours.
- **Notifications**: Users are notified only when a price drop is detected relative to the last notified price.
- **Security**: Strict data isolation for subscriptions and notifications.


## InstallationClone the repository:
```bash
git clone <repo_url>
cd flywatch


Create a .env file (see .env.example for a template) with your environment variables:

SECRET_API_KEY=Your_serpapi_key
POSTGRES_USER=Your_DB_user
POSTGRES_PASSWORD=Your_password
POSTGRES_DB=Your_DB_name
DJANGO_SECRET_KEY=Your_django_secret_key


Docker
The easiest way to run the project is using Docker Compose:

docker-compose up --build

Containers:

* API  — port 8000
* PostgreSQL — port 5432
* Redis — port 6379
* Celery Worker & Beat 


Local Development
If you prefer running the project locally:

   1. Install dependencies: pip install -r requirements.txt
   2. Run migrations: python manage.py migrate
   3. Start the server: python manage.py run_server


Note: Ensure Redis and PostgreSQL are running and accessible.
Testing: The project is covered by 23 Unit and Integration tests.

Run tests inside the Docker container:

docker-compose exec web python manage.py test

Tests cover:

* Serializer validation 
* Service mocking 
* Celery task logic
* Security & Permissions 


Swagger
Interactive API documentation is available at:
http://localhost:8000/api/docs/


Tips

* Use the Admin Panel (/admin/) to manage subscriptions manually if needed.
* Docker ensures a consistent environment for Redis, Celery, and PostgreSQL.





