from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
load_dotenv()
from .schema_llm import *


small_llm = ChatOpenAI(model="gpt-4o-mini")
large_llm = ChatOpenAI(model="gpt-4o")


query_llm = small_llm.with_structured_output(QueriesSchemaPyD)
research_llm = small_llm.with_structured_output(ResearchSchemaPyD)
judge_llm = large_llm.with_structured_output(JudgeSchemaPyD)


# llm_as_judge = large_llm.with_structured_output(FeedbackJudge)
# llm_with_tool = small_llm.bind_tools(tools)
# writer_llm = small_llm.with_structured_output(ReportSchema)