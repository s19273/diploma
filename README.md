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

http://127.0.0.1:8000/admin/

http://127.0.0.1:8000/api/

http://127.0.0.1:8000/api/log-items/

http://127.0.0.1:8000/api/images/

http://127.0.0.1:8000/api/send-image-for-detection/

# Frontend

### Required versions

| Package    | Version |
| ---------- | ------- |
| Angular    | 15.2.0  |
| Node.js    | 14.17.3 |
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
