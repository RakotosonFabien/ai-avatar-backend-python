# routers/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI
from routers.memory import memory  # import your LangChain memory object

load_dotenv()  # Load .env file

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@router.post("/ask")
def ask_chat(request: ChatRequest):
    try:
        #Use prior memory in prompt
        past_memory = memory.load_memory_variables({}).get("history", "")

        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a kind AI companion."},
                {"role": "system", "content": f"Here's the conversation history: {past_memory}"},
                {"role": "user", "content": request.message}
            ]
        )
        reply = response.choices[0].message.content.strip()

        # Save the new message to memory
        memory.chat_memory.add_user_message(request.message)
        memory.chat_memory.add_ai_message(reply)

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

