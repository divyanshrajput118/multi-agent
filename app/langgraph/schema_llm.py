from pydantic import BaseModel, Field
from typing import List, Optional

class QueriesSubSchemaPyD(BaseModel):
    query: str = Field(description="Generated query")


class QueriesSchemaPyD(BaseModel):
    queries: List[QueriesSubSchemaPyD] = Field(
        description="3 focused sub-queries"
    )


class SearchSchemaPyD(BaseModel):
    idx: int = Field(description="Index of the respective query")
    content: str = Field(description="Content extracted")
    url: str = Field(description="URL extracted")


class ResearchSchemaPyD(BaseModel):
    idx: int = Field(description="Index of the original query")
    query: str = Field(description="Queries")
    findings: str = Field(description="Content related to the query")
    url: str = Field(description="URL of the content found")


class JudgeSchemaPyD(BaseModel):
    idx: int = Field(description="The original index of the query item evaluated")
    score: int = Field(description="Relevance score from 1 to 5 based on findings")
    feedback: str = Field(description="Reasoning for the score given and missing information")
    is_weak: bool = Field(description="True if score < 4, indicating the query needs rewriting strict boolean should be followed True/False")
    rewritten_query: Optional[str] = Field(default="",
                        description="A refined search query if the item is weak, else None")