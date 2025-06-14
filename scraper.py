import requests
from bs4 import BeautifulSoup
import datetime

def scrape_course_content(url="https://tds.s-anand.net/#/2025-01/"):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    texts = []
    for tag in soup.find_all(["h1","h2","p","li"]):
        t = tag.get_text(strip=True)
        if t:
            texts.append(t)
    with open("content/course.txt","w",encoding="utf-8") as f:
        f.write("\n".join(texts))
    return "Course content scraped."

def scrape_discourse(start="2025-01-01", end="2025-04-14"):
    base = "https://discourse.onlinedegree.iitm.ac.in"
    resp = requests.get(base + "/c/courses/tds-kb/34/l/latest")  # Rich listing
    soup = BeautifulSoup(resp.text, "html.parser")
    lines = []
    for link in soup.select("a.title"):
        date_tag = link.find_next("span", {"class":"relative-date"})
        if not date_tag: continue
        dt = datetime.datetime.strptime(date_tag["title"][:10], "%Y-%m-%d")
        if datetime.datetime.fromisoformat(start) <= dt <= datetime.datetime.fromisoformat(end):
            url = base + link["href"]
            title = link.get_text(strip=True)
            lines.append(f"{title}\t{url}")
    with open("content/discourse.txt","w",encoding="utf-8") as f:
        f.write("\n".join(lines))
    return f"Scraped {len(lines)} posts."
