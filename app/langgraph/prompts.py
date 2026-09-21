from langchain_core.messages import HumanMessage, SystemMessage

def get_parallel_queries_prompt(topic: str):
    return [
        SystemMessage(
            content="""You are a strategic research planner. 

                        Your task is to generate exactly 3 concise, highly relevant search queries based on the user's topic.

                        Guidelines:
                        1. Disambiguate terms: If the topic uses a generic or ambiguous name (e.g., 'Black Cobra'), identify the primary intended subject and include scientific names or specific contexts to keep search results consistent.
                        2. Distinct aspects: Ensure each of the 3 queries targets a different key aspect (e.g., physical characteristics, native habitat/distribution, venom/biology).
                        3. Search-ready format: Output short, keyword-dense search queries, not long conversational questions. Avoid duplicate or overlapping queries."""
                                ),
                                HumanMessage(content=f"topic: {topic}")
                            ]

def get_research_prompt(query: str):
    return [
        SystemMessage(
            content=(
                "You are a research assistant. Your task is to use the provided search tool "
                "to find factual information about the query."
            )
        ),
        HumanMessage(content=f"Search for details on: {query}"),
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

                        If the research is insufficient, select and return ONLY the exact original 
                        queries from the input that failed evaluation in missing_queries. 
                        Do NOT write new queries or alter the existing query text.
                        """
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