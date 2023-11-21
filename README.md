# Backend

### Techstack

* Python3
* Redis
* Celery

`brew install redis`

`python3 -m pip install django djangorestframework celery django-celery-results torch opencv-python pillow facenet-pytorch`

### Run server

1. Open venv: `source venv/bin/activate`
2. Start Redis server `redis-server`
   1. If `redis` is already running kill it with `redis-cli shutdown`
3. Start Celery server `celery -A diploma_backend worker -l info`
4. Perform migration `./manage.py migrate`
5. Create admin with `python3 manage.py createsuperuser`
6. Run Django server `python3 manage.py runserver`

If `redis` is already running kill it with `redis-cli shutdown`

### Endpoints

https://api.19273.pl/admin/

https://api.19273.pl/api/

https://api.19273.pl/api/log-items/

https://api.19273.pl/api/images/

https://api.19273.pl/api/send-image-for-detection/

# Frontend

### Required versions

| Package    | Version |
| ---------- | ------- |
| Angular    | 15.2.0  |
| Node.js    | 20.93   |
| TypeScript | 4.8.4   |
| Zone.js    | 0.13.0  |

Open command line in the `diploma-frontend` catalog and run:

`npm install`

### How to run

Run server:

`npm start`

Angular application should be working now on https://localhost:4200/

*If method above is not working and privacy error displays (in Chromium based browsers) type on the error tab `thisisunsafe`*

Otherwise try running server with following command:

`ng serve --host 0.0.0.0 --public-host=0.0.0.0:0`

And use the following link to open it:

http://0.0.0.0:4200/

# Deploy

```bash
# Setup Docker containers
chmod +x entrypoint.prod.sh

docker compose -f docker-compose.prod.yml up -d --build

# When Docker containers run properly (test with "docker ps") create

docker compose -f docker-compose.prod.yml exec web python manage.py makemigrations --noinput

docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Enable SSL
ssl generate dry

docker compose -f docker-compose.prod.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d 19273.pl

ssl generate
docker compose -f docker-compose.prod.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d api.19273.pl
```