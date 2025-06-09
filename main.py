from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel, Field
from chatbot.gemini_client import GeminiChatbot
from chatbot.utils import is_python_question
from chatbot.llm import ask_llm
import uvicorn

app = FastAPI(title="Gemini Chatbot API")
chatbot = GeminiChatbot()

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        description="Enter your question",
        example="What is AI?",  # This will show as placeholder in Swagger UI
    )

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Response from the chatbot")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    question: str = Form(
        ...,
        description="Enter your question",
        example="What is AI?",  # Example value
    )
):
    if not is_python_question(question):
        raise HTTPException(
            status_code=400,
            detail="❌ This chatbot only answers Python-related questions."
        )
    answer = await ask_llm(question)
    return {"answer": answer }