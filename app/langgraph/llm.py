from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
load_dotenv()
from .schema import *
from langchain.tools import tool
from langchain_tavily import TavilySearch

small_llm = ChatOpenAI(model="gpt-4o-mini")
large_llm = ChatOpenAI(model="gpt-4o")

@tool
def search_web(query: str):
    """
        Search the web for factual information related to the given query.
    
        Args:
            query: The search query to look up on the web.
    
        Returns:
            A dictionary containing:
            - findings: The relevant information extracted from the search result.
            - sources: The URL of the source containing the information.
    """

    tool = TavilySearch(
                    max_results=1,
                    topic="general",)
    result = tool.invoke(query)

    if isinstance(result, dict) and "results" in result and result["results"]:
        data = result["results"][0]
        return {
            "query": query,
            "findings": data.get("content", "No content found."),
            "sources": data.get("url", "No URL found."),
        }
    return {"query": query,
            "findings": "No content found.", 
            "sources": "No URL found."}

tools = [search_web]

str_llm = small_llm.with_structured_output(QueriesSchema)
llm_as_judge = large_llm.with_structured_output(FeedbackJudge)
llm_with_tool = small_llm.bind_tools(tools)
writer_llm = small_llm.with_structured_output(ReportSchema)