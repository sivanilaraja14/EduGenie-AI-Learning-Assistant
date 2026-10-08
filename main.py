from __future__ import annotations

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class TopicRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

@app.post("/qa")
async def qa(request: QuestionRequest):

    return {
        "question": request.question,
        "answer": answer_question(
            request.question
        )
    }


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

@app.post("/explain")
async def explain(request: TopicRequest):

    return {
        "topic": request.topic,
        "explanation": explain_topic(
            request.topic
        )
    }


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(request: TextRequest):

    return {
        "quiz": generate_quiz(
            request.text
        )
    }


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):

    return {
        "summary": summarize_text(
            request.text
        )
    }


# ---------------------------------------------------------
# Learning Recommendations
# ---------------------------------------------------------

@app.get("/learn/recommendations")
async def recommendations(
    topic: str = Query(
        ...,
        min_length=1,
        max_length=500
    )
):

    return {
        "topic": topic,
        "recommendation": get_learning_recommendations(
            topic
        )
    }