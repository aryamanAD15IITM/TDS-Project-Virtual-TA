from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import base64, io
from PIL import Image
import pytesseract

from .scraper import scrape_course_content, scrape_discourse

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

@app.get("/scrape/")
def run_scraper():
    c1 = scrape_course_content()
    c2 = scrape_discourse()
    return {"course": c1, "discourse": c2}

def load_content():
    texts = []
    links = {}
    try:
        with open("content/course.txt", "r",encoding="utf-8") as f:
            for l in f:
                texts.append(l.strip())
    except:
        pass
    try:
        with open("content/discourse.txt","r",encoding="utf-8") as f:
            for l in f:
                if "\t" in l:
                    title, url = l.strip().split("\t",1)
                    texts.append(title)
                    links[title] = url
    except:
        pass
    return texts, links

def extract_image_text(b64):
    data = base64.b64decode(b64)
    img = Image.open(io.BytesIO(data))
    return pytesseract.image_to_string(img)

@app.post("/")
async def answer_question(req: QuestionRequest):
    q = req.question
    if req.image:
        q += " " + extract_image_text(req.image)

    texts, links_map = load_content()
    answer = None
    found_links = []

    for text in texts:
        if q.lower() in text.lower() or any(w in text.lower() for w in q.lower().split()):
            answer = text
            if text in links_map:
                found_links.append({"url": links_map[text], "text": text})
            break

    if not answer:
        answer = "Sorry, I could not find an answer based on the available course or discourse content."
    return {"answer": answer, "links": found_links}

