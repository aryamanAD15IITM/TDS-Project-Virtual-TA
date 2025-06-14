import requests
from bs4 import BeautifulSoup

def scrape_tds_course_page(url: str = "https://example.com/tds") -> str:
    """
    Scrapes content from a course page and returns extracted text.
    Replace with actual course URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text from paragraphs and headers
        content = []
        for tag in soup.find_all(["p", "h1", "h2", "li"]):
            text = tag.get_text(strip=True)
            if text:
                content.append(text)

        # Save to local file
        with open("content/tds_content.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        return "Scraping complete."
    except Exception as e:
        return f"Scraping failed: {str(e)}"
