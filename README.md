# cam-miner
# Extract stream from ipcamera and publish with imagezmq

## Setup
```
config/app.ini
```

## Run
```
$ docker-compose up -d --force-recreate
```

### Gerando requirements.txt
```
$ pip freeze > requirements.txt
```


### Gerando imagem

```
$ docker build --tag cam-miner .

$ docker tag cam-miner:latest cam-miner:v1.0.0

$ docker rmi cam-miner:v1.0.0
```
