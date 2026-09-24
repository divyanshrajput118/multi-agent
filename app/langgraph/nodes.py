from .prompts import *
import asyncio
from .schema_state import *
from .llm import *
from .tools import search_web


async def parallel_query_gen(state: State):
    topic = state["topic"]
    messages = get_parallel_queries_prompt(topic)
    response = await query_llm.ainvoke(messages)
    queries = [{"idx": idx, "query": obj.query} for idx, obj in enumerate(response.queries)]

    return {
            "queries": queries,
            "attempt": 0
            }
    

async def researcher(state: State):
    queries = state["queries"]
    judge_result = state.get("judge_result", [])
    re_query = [
        {
            "idx": item["idx"],
            "query": item["rewritten_query"]
        }
        for item in judge_result
        if item["is_weak"] is True
    ]
    final_queries = re_query if re_query else queries
    coroutine = [search_web(item) for item in final_queries]
    search_results = await asyncio.gather(*coroutine)
    search_queries = [research_llm.ainvoke(get_research_prompt(idx=item['idx'], 
                                                               query=item['query'], 
                                                               context=search_result.content,
                                                               url=search_result.url)) 
                                                               for item, search_result in zip(final_queries, search_results)]
    outputs = await asyncio.gather(*search_queries)
    result: List[Result] = [item.model_dump() for item in outputs]
    old_results = state.get("result", [])
    result_map = {
    item["idx"]: item
    for item in old_results
                    }
    for item in result:
        result_map[item["idx"]] = item

    final_result = list(result_map.values())
    return {
        "result": final_result
    }


async def my_judge(state: State):
    topic = state['topic']
    result = state['result']
    judge_coroutine = [judge_llm.ainvoke(get_judge_prompt(topic=topic,
                                        item=item)) for item in result]
    judge_output = await asyncio.gather(*judge_coroutine)
    judge_result: List[Judge] = [item.model_dump() for item in judge_output]
    return {
        "attempt": state['attempt'] + 1,
        "judge_result": judge_result
    }



async def router(state: State):
    judge_result = state.get("judge_result", []) 
    if judge_result:
        average_score = int(sum(item["score"] for item in judge_result) / len(judge_result))
    else:
        average_score = 0

    if state["attempt"] >= 2 or average_score>=4:
        return "writer"
    else:
        return "my_judge"


async def writer(state: State):
    return state

# async def writer(state: State):
#     results = state["result"]
#     prompt = get_writer_prompt(results)
#     response_ = await writer_llm.ainvoke(prompt)
#     return {
#         "report": response_.model_dump_json()
#     }





    

    