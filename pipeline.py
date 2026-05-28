from agents import build_scrape_agent , build_search_agent , writer_chain , critic_chain, revision_chain
from langchain_core.messages import HumanMessage
import re

def extract_score(feedback: str):
    match = re.search(r"Score:\s*(\d+)/10", feedback)
    if match:
        return int(match.group(1))
    return 0

def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [HumanMessage(content=f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])

    #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = build_scrape_agent()
    reader_result = reader_agent.invoke({
        "messages": [HumanMessage(
           content=f"""
            Based on the following search results about '{topic}', identify the 3 most relevant and reliable URLs.

            Scrape all 3 sources and combine their key findings into one detailed research context.

            Prioritize:
            - recent information
            - reliable sources
            - technical depth
            - factual consistency

            Search Results:
            {state['search_results'][:1200]}
            """
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    score = extract_score(state["feedback"])

    if score < 8:
        print("\n" + "="*50)
        print("Step 5 - Revising report using critic feedback...")
        print("="*50)

        state["revised_report"] = revision_chain.invoke({
            "report": state["report"],
            "feedback": state["feedback"]
        })

        print("\nRevised Report:\n", state["revised_report"])
    else:
        state["revised_report"] = state["report"]
        
    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
