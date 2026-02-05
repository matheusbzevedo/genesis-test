### create migrations
```
docker compose exec web python manage.py makemigrations
```

### migrate
```
docker compose exec web python manage.py migrate
```

### create admin user
```
docker compose exec web python manage.py createsuperuser
```
