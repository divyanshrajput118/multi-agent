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

def get_writer_prompt(topic: str, context: str, urls: list[str]):
    return [
        SystemMessage(
            content="""
                    You are an expert research report writer.

                    Create a concise, factual, and well-structured research report using ONLY
                    the provided topic, research context, and source URLs.

                    The output must strictly follow the StructuredReportPyD schema.

                    FIELD REQUIREMENTS:

                    1. `title`
                    - Create a concise and descriptive title for the overall report.
                    - The title should accurately represent the research topic.

                    2. `topic`
                    - Return the main research topic provided by the user.
                    - Do not modify the meaning of the topic.

                    3. `introduction`
                    - Write a short introduction to the topic.
                    - Briefly explain what the report examines.
                    - Do not include unsupported facts.

                    4. `sections`
                    - Create meaningful sections based on the research findings.
                    - Each section must contain:
                        
                        `heading`
                        - A clear and meaningful heading describing the section.

                        `content`
                        - A concise synthesis of the relevant research findings.
                        - Do not simply copy the research context.
                        - Include important facts, statistics, comparisons, or findings when
                        supported by the research.

                        `sources`
                        - Include the source URL(s) supporting the section.
                        - Use ONLY URLs provided in the input.
                        - Do not invent or modify URLs.
                        - A section may contain one or more URLs if multiple sources support it.

                    - The three provided URLs correspond to the three research queries.
                    - Use each URL where its research findings are relevant.
                    - Related findings from different queries may be combined into one section
                        when that produces a better report.
                    - Do not create unnecessary sections merely to match the number of queries.

                    5. `conclusion`
                    - Concisely summarize the major findings of the report.
                    - Do not introduce new facts or information.
                    - Base the conclusion only on the research context.

                    GENERAL RULES:
                    - Use ONLY the provided research context.
                    - Do not invent facts, statistics, claims, or sources.
                    - Do not use external knowledge.
                    - Keep the complete report concise and approximately one page.
                    - Use professional and factual language.
                    - Synthesize the findings rather than copying them.
                    - The final report should read as one coherent report.
                    """
                            ),

                            HumanMessage(
                                content=f"""
                    MAIN RESEARCH TOPIC:
                    {topic}

                    RESEARCH CONTEXT:
                    {context}

                    SOURCE URLS:
                    {urls}
                    """
                            )
                        ]