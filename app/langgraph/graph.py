from langgraph.graph import StateGraph, START, END
from .agent import *

graph_builder = StateGraph(State)

graph_builder.add_node("parallel_query_gen", parallel_query_gen)
graph_builder.add_node("researcher", researcher)
graph_builder.add_node("feedback", feedback)
graph_builder.add_node("writer", writer)

graph_builder.add_edge(START, "parallel_query_gen")
graph_builder.add_edge("parallel_query_gen", "researcher")
graph_builder.add_conditional_edges("researcher", route_after_research, 
                                    {"feedback": "feedback", "writer": "writer"})
graph_builder.add_edge("feedback", "researcher")
graph_builder.add_edge("writer", END)

graph = graph_builder.compile()


async def main():
    state = {"topic": "What is Black Cobra"}
    response = await graph.ainvoke(state)
    return response

if __name__ == "__main__":
    response = asyncio.run(main())
    print(response)



