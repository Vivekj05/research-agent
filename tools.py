from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_tavily import TavilySearch
from bs4 import BeautifulSoup
import os
import requests
tavily = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_web(query: str) -> str:
    """search the web for the given query and return the results as a string"""
    results = tavily.invoke(query, max_results=5)

    out=[]

    for r in results['results']:
        out.append(f"Title:{r['title']}\nURL:{r['url']}\nsnippet:{r['content'][:300]}\n")
    return "\n".join(out)

print(search_web.invoke("latest news on AI"))

@tool
def scrape_url(url: str) -> str:
    """scrape the given url and return the text content as a string"""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style','nav','footer']):
            tag.decompose()    
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Error occurred while scraping url:{str(e)}"

# print(scrape_url.invoke("https://timesofindia.indiatimes.com/sports/cricket"))