source venv/bin/activate

cd /home/galkowskim/Desktop/Supervision2023/backend

python manage.py shell -c "from supervision_app.tasks import scrape_data; scrape_data()"

