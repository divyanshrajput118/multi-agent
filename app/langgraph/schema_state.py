from typing import TypedDict, List, Optional

class Query(TypedDict):
    idx: int
    query: str


class Result(TypedDict):
    idx: int
    query: str
    findings: str
    url: str


class Judge(TypedDict):
    idx: int
    score: int
    feedback: str
    is_weak: bool
    rewritten_query: Optional[str]

class State(TypedDict):
    topic: str
    queries: List[Query]
    attempt: int
    result: List[Result]
    judge_result: List[Judge]
    report: dict