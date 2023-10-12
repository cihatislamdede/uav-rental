UAV Rental Project with Django
===============

This is a Django project for UAV rental. Also there is a web application that allows users to rent UAVs and manage their rental history.

![initial-page](
    ./screenshots/1.png
)

## Features

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

* [Django](https://www.djangoproject.com/)
  * [*Django REST Framework (DRF)*](https://github.com/encode/django-rest-framework)
  * [*django-filter*](https://pypi.org/project/django-filter/)
  * [*django-cors-headers*](https://pypi.org/project/django-cors-headers/)
  * [*python-decouple*](https://pypi.org/project/python-decouple/)
* [PostgreSQL](https://www.postgresql.org/)
* [Tailwind CSS](https://tailwindcss.com/)
* [Vite.js](https://vitejs.dev/)
  * [*axios*](https://axios-http.com)
  * [*react-cookie*](https://www.npmjs.com/package/react-cookie)
  * [*react-router-dom*](https://github.com/remix-run/react-router)
  * [*react-toastify*](https://fkhadra.github.io/react-toastify/introduction/)
  * [*material-tailwind*](https://material-tailwind.com/)
* [Docker support](https://www.docker.com/)
* Git
* GitHub

## Installation

You can run this project with Docker. You can follow the steps below. If you don't want to use Docker, you can follow the steps in the [without docker](#without-docker) section.

Before the following steps, you need to create a `.env` file in the `backend` folder. You can use this template:

```bash
SECRET_KEY=<any-secret-key>
DEBUG=True
POSTGRES_DB=<your-db-name>
POSTGRES_USER=<your-username>
POSTGRES_HOST=<your-host>
POSTGRES_PASSWORD=<your-password>
```

### With Docker

> If you have not installed Docker yet, you can install it from [here](https://docs.docker.com/get-docker/).

```bash
git clone https://github.com/cihatislamdede/uav-rental
cd uav-rental
docker-compose build
docker-compose up
```

### Without Docker

```bash
git clone git clone https://github.com/cihatislamdede/uav-rental
cd uav-rental

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate # (Linux)
# venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py test # (Optional)
python manage.py runserver

# Frontend
cd ../frontend
npm install
npm run dev
```

You can access:

* Backend: <http://localhost:8000>
* Frontend: <http://localhost:5173>

## Screenshots

* Login and Signup Pages
![login-signup-pages](
    ./screenshots/0.png
)

* Home Page
![home-page](
    ./screenshots/2.png
)

* UAV List Page
![uavs-page](
    ./screenshots/3.png
)

* UAV Creation Page
![create-uav-page](
    ./screenshots/4.png
)

* Reservation Creation Page
![create-reservation-page](
    ./screenshots/5.png
)

* Database Schema
![reservations-page](
    ./screenshots/database.png
)
