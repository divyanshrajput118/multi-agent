from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from .prompts import *


class State(TypedDict):
    topic: str
    queries: List[str]
    result: List[str]

class QueriesSchema(BaseModel):
    queries: List[str]

llm = ChatOpenAI(model="gpt-4o-mini")
str_llm = llm.with_structured_output(QueriesSchema)


def parallel_query_gen(state: State):
    topic = state["topic"]
    messages = get_parallel_queries_prompt(topic)
    queries = str_llm.invoke(messages).queries

    return {"queries": queries}
    

def researcher(state: State):
    queries = state["queries"]
    results = []
    for query in queries:
        messages = get_research_prompt(query)
        ai_res = llm.invoke(messages)
        results.append(ai_res.content)

    return {"result": results}

graph_builder = StateGraph(State)

graph_builder.add_node("query_generator", parallel_query_gen)
graph_builder.add_node("researcher", researcher)

graph_builder.add_edge(START, "query_generator")
graph_builder.add_edge("query_generator", "researcher")
graph_builder.add_edge("researcher", END)

graph = graph_builder.compile()

state = {
    "topic": "Hii"
}

response = graph.invoke(state)

