## fleet-management

REST API of a Fleet Management Software to query the locations of the vehicles of a taxi company in Beijing, China.

### Installation

Install my-project with npm

```bash
  git clone git@github.com:lourdilene/django-5-fleet-management.git
  cd my-project
  pip install -r requirements.txt
```

Make migrations

```bash
  python manage.py makemigrations
```

Migrate

```bash
  python manage.py migrate
```

Run server

```bash
  python manage.py runserver
```
### Installing and Run RabbitMQ

```bash
  # latest RabbitMQ 3.13
  docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

### Runing Celery

```bash
  celery -A fleet_management worker -l info
```
    
### Runing Tests

```bash
  pytest
```

### Features

### 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://personal-site-weld-six.vercel.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lourdilene-souza/)


### 🛠 Skills
Python3, Django, Queue, RabbitMQ, ORM, REST API.

#### Tools

* [Pytest]

