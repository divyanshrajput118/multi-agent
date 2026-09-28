from langgraph.graph import StateGraph, START, END
from .schema_state import State
from .nodes import *


graph_builder = StateGraph(State)

graph_builder.add_node("parallel_query_gen", parallel_query_gen)
graph_builder.add_node("researcher", researcher)
graph_builder.add_node("my_judge", my_judge)
graph_builder.add_node("writer", writer)

graph_builder.add_edge(START, "parallel_query_gen")
graph_builder.add_edge("parallel_query_gen", "researcher")
graph_builder.add_conditional_edges("researcher", router, 
                                    {"my_judge": "my_judge", "writer": "writer"})
graph_builder.add_edge("my_judge", "researcher")
graph_builder.add_edge("writer", END)

my_graph = graph_builder.compile()


async def main():
    state = {"topic": "What is Taj Mahal"}
    response = await my_graph.ainvoke(state)
    return response

if __name__ == "__main__":
    response = asyncio.run(main())
    print(response['report'])



