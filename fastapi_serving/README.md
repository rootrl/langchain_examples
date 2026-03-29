### RUN


#### Set API KEY to  .env file 


#### Server
```bash
fastapi dev
```

#### Client Simple Request
```bash
curl --json '{"message": "hello! what is the weather like in hefei"}' http://127.0.0.1:8000/chat

{"response":"Hello! The weather in **Hefei** is **always sunny**."}%
```

#### Client Sream Requst
```bash
curl --json '{"message": "hello! what is the weather like in hefei"}' http://127.0.0.1:8000/chat/stream

data: Hello

data: !

data:  In

data:  **

data: H

data: ef

data: ei

data: **,

data:  the

data:  weather

data:  is

data:  **

data: always

data:  sunny

data: **

data: .

data: [DONE]
```
