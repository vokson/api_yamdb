# API Yamdb Group Project

This is repository for group project in Yandex Praktikum

### Installation

Clone repository from GitHub
```sh
$ git clone https://github.com/vokson/api_yamdb.git
$ cd api_yamdb
```

Create vitrual enviroment
```sh
$ python -m venv venv
$ source venv/Scripts/activate
```

Install vendor modules
```sh
$ pip install -r requirements.txt
```

Perfom migrations of database
```sh
$ python manage.py migrate
```

Seed database with test data
```sh
$ python manage.py datatosqlite
```