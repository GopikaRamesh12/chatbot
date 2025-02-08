from bs4 import BeautifulSoup
import requests
from langchain.schema import Document  # Importing LangChain's Document class

def scrape_brainlox_courses():
    url = "https://brainlox.com/courses/category/technical"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch page. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    documents = []
    for course in soup.find_all("div", class_="single-courses-box"):  
        title_tag = course.find("h3")
        desc_tag = course.find("p")

        title = title_tag.text.strip() if title_tag else "No title"
        description = desc_tag.text.strip() if desc_tag else "No description"

        # Create a LangChain Document object
        doc = Document(
            page_content=f"{title}: {description}",
            metadata={"title": title}
        )
        documents.append(doc)

    return documents

# Example usage
if __name__ == "__main__":
    courses = scrape_brainlox_courses()
    print(f"Scraped {len(courses)} courses successfully")

 

