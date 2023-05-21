source venv/bin/activate

cd backend

python manage.py shell -c "from supervision_app.tasks import scrape_data; scrape_data()"

