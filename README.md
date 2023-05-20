# Supervision2023

### Celery commands
```
docker run -d -p 6379:6379 redis

celery -A supervision_app worker  --loglevel=INFO -E
```

Also you need to remember to add script to crontab. It should be run every 10 minutes.
```