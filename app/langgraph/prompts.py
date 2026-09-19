from langchain_core.messages import HumanMessage, SystemMessage

def get_parallel_queries_prompt(topic: str):
    return [
        SystemMessage(content="""You are an AI assistant which generates 3 more concise and
                                topic related similar queries related to topic asked by user"""),
        HumanMessage(content=f"topic: {topic}")
    ]

def get_research_prompt(query: str):
    return [
            SystemMessage(content="""You are an AI assistant which generates one line about the query"""),
            HumanMessage(content=f"query: {query}")
        ]