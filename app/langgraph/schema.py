from typing import TypedDict, List, Annotated, Optional
from pydantic import BaseModel, Field


class ResearchResult(TypedDict):
    idx: int
    query: str
    findings: str
    sources: list[str]

class QueriesSchema(TypedDict):
    idx: int
    retry_query: str

class ScoreSchema(TypedDict):
    idx: int
    score: int


def update_research_results(existing: List[ResearchResult], new: List[ResearchResult]) -> List[ResearchResult]:
    """Merges new research results into existing state by query key."""
    results_map = {item["query"]: item for item in existing}
    for item in new:
        results_map[item["query"]] = item        
    return list(results_map.values())


class State(TypedDict):
    topic: str
    queries: List[QueriesSchema]
    retry_queries = List[QueriesSchema]
    attempt: int
    result: Annotated[List[ResearchResult], update_research_results]
    scores: List[ScoreSchema]
    report: str

class QueriesSubSchemaPyD(BaseModel):
    idx: int = Field(description="Index of the query")
    query: str = Field(description="Queries Generated")

class QueriesSchemaPyD(BaseModel):
    queries: List[QueriesSubSchemaPyD] = Field(description="3 focused sub-queries")


class JudgeSchema(BaseModel):
    idx: int = Field(description="Index of the original query")
    score: int = Field(description="Score from 1 (poor) to 5 (excellent)")
    improved_query: Optional[str] = Field(
        default=None, 
        description="Suggested refined search query if score is < 4"
    )


class FeedbackJudge(BaseModel):
    feedback: List[JudgeSchema] = Field(
        description="List of evaluations corresponding to each research item"
    )


class ReportSection(BaseModel):
    heading: str = Field(description="Section heading, derived from the query")
    content: str = Field(description="Synthesized findings for this section")
    sources: List[str] = Field(description="Source URLs cited in this section")


class ReportSchema(BaseModel):
    title: str = Field(description="A concise, descriptive title for the report")
    introduction: str = Field(description="1-2 paragraph introduction to the topic")
    sections: List[ReportSection] = Field(description="One section per researched query")
    conclusion: str = Field(description="Brief closing summary")