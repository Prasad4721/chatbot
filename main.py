from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel, Field
from chatbot.gemini_client import GeminiChatbot
import uvicorn

app = FastAPI(title="Gemini Chatbot API")
chatbot = GeminiChatbot()

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        description="Enter your question",
        example="What is AI?",  # This will show as placeholder in Swagger UI
    )

class ChatResponse(BaseModel):
    response: str = Field(..., description="Response from the chatbot")

@app.post("/chat", response_model=ChatResponse)
def chat_with_bot(
    message: str = Form(
        ...,
        description="Enter your question",
        example="What is AI?",  # Example value
    )
):
    if not message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    response = chatbot.send_message(message)
    return {"response": response}