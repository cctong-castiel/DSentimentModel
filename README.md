# DSentimentModel2
It is a regex sentiment model based on sentiment words and emoji dictionary without using any machine learning model to do prediction.

### Pipe
##### call /ping
- GET 
- return "pong"

##### call /run
- POST
- request
```
{
    "data": [{"live_sid": 1, "message": "..."}, {"live_sid": 2, "message": "..."}, {"live_sid": 3, "message": "..."}]
}
```
- return
```
{
    "result": [{"live_sid": 1, "message": "...", "pred": 1}, {"live_sid": 2, "message": "...", "pred": 0}, {"live_sid": 3, "message": "...", "pred": 1}] 
}
```

### start a docker host server
prerequisites:
- install docker desktop

start a docker host server
- in command line, type 
```
docker-compose up --build
```
- it needs time to start a docker server. Please wait patiently.

Testing api
- /ping (GET)
```
url: http://0.0.0.0:8964/ping
```
- /pipe (POST)
```
url: http://0.0.0.0:8964/run
body: 
{
    "result": [{"live_sid": 1, "message": "...", "pred": 1}, {"live_sid": 2, "message": "...", "pred": 0}, {"live_sid": 3, "message": "...", "pred": 1}] 
}
```

Stop a docker host server
- in command line, type
```
docker-compose down
```