from typing import TypedDict, List, Annotated
from pydantic import BaseModel, Field


class ResearchResult(TypedDict):
    query: str
    findings: str
    # sources: list[str] populate once a real search tool is added

def update_research_results(existing: List[ResearchResult], new: List[ResearchResult]) -> List[ResearchResult]:
    """Merges new research results into existing state by query key."""
    results_map = {item["query"]: item for item in existing}
    for item in new:
        results_map[item["query"]] = item        
    return list(results_map.values())


class State(TypedDict):
    topic: str
    queries: List[str]
    retry_cnt: int
    result: Annotated[List[ResearchResult], update_research_results]
    is_sufficient: bool
    missing_queries: List[str]
    report: str


class QueriesSchema(BaseModel):
    queries: List[str] = Field(description="3 focused sub-queries")


class FeedbackJudge(BaseModel):
    is_sufficient: bool = Field(description="True if every query is answered correctly")
    missing_queries: List[str] = Field(description="Queries which are weak and vague")
    reasoning: str = Field(description="LLM judgement")


class ReportSection(BaseModel):
    heading: str = Field(description="Section heading, derived from the query")
    content: str = Field(description="Synthesized findings for this section")
    sources: List[str] = Field(description="Source URLs cited in this section")


class ReportSchema(BaseModel):
    title: str = Field(description="A concise, descriptive title for the report")
    introduction: str = Field(description="1-2 paragraph introduction to the topic")
    sections: List[ReportSection] = Field(description="One section per researched query")
    conclusion: str = Field(description="Brief closing summary")