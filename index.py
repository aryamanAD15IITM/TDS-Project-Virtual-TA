from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import base64
import json
import os

from .scraper import scrape_tds_course_page

app = FastAPI()

with open("answers.json", "r") as f:
    ANSWERS = json.load(f)

class QuestionRequest(BaseModel):
    question: str
    files: Optional[List[str]] = None

@app.post("/")
async def answer_question(payload: QuestionRequest):
    q = payload.question.lower()
    
    # Check predefined answers
    for k, v in ANSWERS.items():
        if k.lower() in q:
            return {"answer": v}

    # Fallback to scraped content
    try:
        with open("content/tds_content.txt", "r", encoding="utf-8") as f:
            content = f.read()
        for line in content.split("\n"):
            if q.split()[0] in line.lower():  # naive match
                return {"answer": line.strip()}
    except:
        return {"answer": "No scraped content available. Please run /scrape."}

    return {"answer": "Sorry, I could not find an answer."}

@app.get("/scrape/")
def run_scraper():
    return {"status": scrape_tds_course_page()}
