# Setting Up the Project
## Run the API server
`docker compose up -d`

## Run the migration
`docker compose exec api python manage.py migrate`

*Now, you can access the API at http://localhost:8000*