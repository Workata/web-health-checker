# Web Health Checker

App that monitors web sites and reports their availability. This tool is intended as a monitoring tool for web site administrators for detecting problems on their sites.


<p align="center">
  <img src="imgs/front_ss.png"  alt="ui"/>
</p>

#### Prerequisites
- docker (v. 20.10.23 or newer)

#### Running the app

1. Create a config file (based on example)
```sh
cd backend
cp -n config_example.yaml config.yaml
```

2. Run app with
```sh
docker compose up
```

#### Development

[Create config file](####running-the-app)

Run redis
```sh
docker run --rm --name some-redis -p 6379:6379 redis:latest
```

Run celery
```sh
cd backend
celery --app=src.main.celery_app worker --concurrency=1 --loglevel=DEBUG
```

Run backend
```sh
cd backend
uvicorn src.main:app --reload --port=8000
```

Run frontend
```sh
cd frontend
npm install --force
npm start
```


TODO:
- [ ] Logs (use python logging with custom setup)
- [ ] Code refactor (back/front), validation, typing etc
