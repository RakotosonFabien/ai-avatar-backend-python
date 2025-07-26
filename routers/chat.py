# routers/chat.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/chat/test")
def chat_test():
    return {"response": "Chat router is working!"}
