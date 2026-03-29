from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

app = FastAPI()

# Set up your client/origin
origins = [
    "http://localhost.example.com",
    "https://localhost.example.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = ChatOpenAI(
    model="gpt-5.4-nano",
    temperature=0.1,
    max_tokens=1000,
    timeout=30,
)

agent = create_agent(
    model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Simple
@app.post("/chat")
async def chat(req: ChatRequest):
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": req.message}]}
    )
    return {"response": response["messages"][-1].content}

# Stream version
@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def event_generator():
        async for event in agent.astream_events(
            {"messages": [{"role": "user", "content": req.message}]},
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream":
                token = event["data"]["chunk"].content
                if token:
                    yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
