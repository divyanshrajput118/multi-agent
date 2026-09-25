from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
load_dotenv()
from .schema_llm import *


small_llm = ChatOpenAI(model="gpt-4o-mini")
large_llm = ChatOpenAI(model="gpt-4o")


query_llm = small_llm.with_structured_output(QueriesSchemaPyD)
research_llm = small_llm.with_structured_output(ResearchSchemaPyD)
judge_llm = large_llm.with_structured_output(JudgeSchemaPyD)
writer_llm = small_llm.with_structured_output(StructuredReportSchemaPyD)
