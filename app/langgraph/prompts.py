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

def get_feedback_prompt(results):
    return [
        SystemMessage(
            content="""You are a research quality evaluator.

            Evaluate the research findings provided by the user.

            Your task is to:
            1. Check whether every research query has been adequately answered.
            2. Check whether the findings are relevant to their respective queries.
            3. Identify queries whose findings are weak, incomplete, vague, or missing.
            4. Decide whether the overall research is sufficient to write a report.

            Set is_sufficient to True only when all queries have adequate
            and relevant findings.

            If the research is insufficient, list only the queries that need
            additional research in missing_queries."""
        ),
        HumanMessage(
            content=f"Research findings:\n{results}"
        )
    ]

def get_writer_prompt(results):
    return [
        SystemMessage(
            content="""You are an expert research report writer.

            Using the research findings provided below, write a clear,
            well-structured and factual report.

            Requirements:
            - Create a concise and descriptive title.
            - The report should be upto 1 page only.
            - Write a brief introduction.
            - Create one section for each researched query.
            - Each section should have a meaningful heading.
            - Synthesize the findings instead of simply copying them.
            - Include the relevant source URLs if they are available.
            - Write a concise conclusion.
            - Do not invent sources or facts that are not present in the research."""
        ),
        HumanMessage(
            content=f"Research findings:\n{results}"
        )
    ]