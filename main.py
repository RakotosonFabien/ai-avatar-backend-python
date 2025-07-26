from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, speech

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React's dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(chat.router)
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(speech.router, prefix="/speech", tags=["speech"])

@app.get("/")
def read_root():
    return {"message": "Backend is live!"}
