from .prompts import *
import asyncio
from .schema import *
from .llm import *


async def parallel_query_gen(state: State):
    topic = state["topic"]
    messages = get_parallel_queries_prompt(topic)
    response = await str_llm.ainvoke(messages)
    queries = response.queries
    return {"queries": queries,
            "retry_cnt": 0,
            "is_sufficient": False
            }
    

async def researcher(state: State):
    queries = state["queries"]
    missing_queries = state["missing_queries"]

    queries_to_research = missing_queries if missing_queries else queries
    tasks = [llm.ainvoke(get_research_prompt(query)) for query in queries_to_research]
    response_ = await asyncio.gather(*tasks)
    results: List[ResearchResult] = [
        {"query": query, "findings": res.content}
        for query, res in zip(queries_to_research, response_)
    ]
    return {"result": results}


async def route_after_research(state: State):
    if state["retry_cnt"] >= 2:
        return "writer"
    elif state["is_sufficient"]:
        return "writer"
    else:
        return "feedback"


async def feedback(state: State):
    results = state["result"]
    response_ = await llm_as_judge.ainvoke(
        get_feedback_prompt(results)
    )
    return {
        "is_sufficient": response_.is_sufficient,
        "missing_queries": response_.missing_queries,
        "retry_cnt": state["retry_cnt"] + 1
    }

async def writer(state: State):
     results = state["result"]
     prompt = get_writer_prompt(results)
     response_ = await writer_llm.ainvoke(prompt)
     return {
         "report": response_.model_dump_json()
     }