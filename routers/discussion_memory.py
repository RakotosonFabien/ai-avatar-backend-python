from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from routers.memory import memory  # import your LangChain memory object

router = APIRouter()

class MessageInput(BaseModel):
    text: str

@router.post("/save-memory")
def save_memory(request: MessageInput):
    try:
        # Simulate saving a message into LangChain memory
        memory.chat_memory.add_user_message(request.text)
        memory.chat_memory.add_ai_message("Placeholder AI response")  # You'd use real response
        return {"message": "Memory updated with new message."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clean-memories")
def clean_memories():
    try:
        memory.clear()
        return {"message": "Memory cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-memory")
def get_memory():
    try:
        return {"messages": memory.chat_memory.messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
