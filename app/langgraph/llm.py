from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
load_dotenv()
from .schema import *

llm = ChatOpenAI(model="gpt-4o-mini")

str_llm = llm.with_structured_output(QueriesSchema)
llm_as_judge = llm.with_structured_output(FeedbackJudge)
writer_llm = llm.with_structured_output(ReportSchema)