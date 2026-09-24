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

def get_research_prompt(idx: int, query: str, context: str, url: str):
    return [
        SystemMessage(
            content=(
                """You are a research assistant.
                Your task is to provide the answer to the query with the given context
                also preserve the index and url of the query correctly matched
                and return the output"""
                
            )
        ),
        HumanMessage(content=f"""Search for details on:
                                    index: {idx}
                                    query: {query}
                                    context: {context}
                                    url: {url}"""),
    ]

def get_judge_prompt(topic: str, item: dict):
    return [
        SystemMessage(
            content="""You are a strict, critical AI Judge evaluating search findings.
                        Your task is to assign a score from 1 to 5 based on how well the finding answers the core topic.

                        CRITICAL SCORING RUBRIC:
                        - Score 5: PERFECT & COMPLETE. Directly, comprehensively, and unambiguously answers the main topic goal.
                        - Score 4: GOOD. Relevant and accurate, but missing minor details or context.
                        - Score 3: WEAK. Contains related information, but DOES NOT directly answer the core question (e.g., gives team list instead of winner).
                        - Score 2: POOR. Barely relevant, outdated, or incomplete.
                        - Score 1: UNRELATED / IRRELEVANT.

                        RULES:
                        1. Be extremely critical. If the finding gives side information (e.g. schedule, team list) instead of answering the exact question (e.g. who won), you MUST give a score <= 3 and set `is_weak = True`.
                        2. Do not assume facts that are not explicitly stated in the findings text.
                        """
                            ),
                            HumanMessage(
                                content=f"""
                        Overall Topic goal : {topic}
                        Item to Evaluate are:
                            Index: {item['idx']}
                            Query Used: {item['query']}
                            Findings: {item['findings']}

                                        """
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