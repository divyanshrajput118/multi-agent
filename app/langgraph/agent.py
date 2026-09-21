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
    missing_queries = state.get("missing_queries")
    queries = state.get("queries", [])
    queries_to_research = missing_queries if missing_queries else queries
    tasks = [llm_with_tool.ainvoke(get_research_prompt(query)) 
             for query in queries_to_research]
    ai_messages = await asyncio.gather(*tasks)
    tool_task = []
    for msg in ai_messages:
        if msg.tool_calls:
            args = msg.tool_calls[0]["args"]
            tool_task.append(search_web.ainvoke(args))

    resposne_ = await asyncio.gather(*tool_task) 
    results: List[ResearchResult] = resposne_
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