from pydantic import BaseModel, Field
from typing import Literal, Optional


class TaskSchema(BaseModel):
    topic: str = Field(..., description="Topic asked by the user")
    status: Literal[
        "Initiated", 
        "Queued", 
        "Processing", 
        "Research_Completed", 
        "Insufficient Balance Error", 
        "Failed"
        "Converting_to_PDF"
        "PDF_Generated"
    ] = Field(default="Initiated", description="Status of the user query(topic)")
    report: dict = Field(default_factory=dict, description="Final Report")
    error_details: Optional[str] = Field(default=None)