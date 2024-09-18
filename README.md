# Running in Docker

Make sure that you have installed Docker and Docker Compose. Copy the ´.env.example´ file,

´´´
cp .env.example .env
´´´

and fill in your own Azure OpenAI information. Launch services,

´´´
docker-compose up
´´´

The app should now be available at http://localhost:8050/.

# Running locally

Make sure that you have installed Python and Poetry. Setup the environment,

´´´
poetry install
´´´

Copy the ´.env.example´ file,

´´´
cp .env.example .env
´´´

and fill in your own Azure OpenAI information. Launch the api service in one terminal,

´´´
poetry run python api.py
´´´

and the app service in another,

´´´
poetry run python app.py
´´´

The app should now be available at http://localhost:8050/.
