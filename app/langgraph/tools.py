import asyncio
from langchain_tavily import TavilySearch
from .schema_llm import SearchSchemaPyD

async def search_web(item: dict) -> SearchSchemaPyD:
    """
        Search the web for factual information related to the given query.
    """

    tool = TavilySearch(
                    max_results=1,
                    topic="general",)
    
    result = await asyncio.to_thread(tool.invoke, item['query'])
    
    data = result["results"][0]

    return SearchSchemaPyD(idx=item['idx'],
                            content=data.get("content",""),
                            url=data.get("url",""))