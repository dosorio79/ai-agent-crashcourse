from pydantic import BaseModel
from typing import List


class EvaluationCheck(BaseModel):
    """
    A single evaluation check for an answer.
    """
    check_name: str
    justification: str
    check_pass: bool


class EvaluationChecklist(BaseModel):
    """
    A structured checklist returned by the evaluation agent.
    """
    checklist: List[EvaluationCheck]
    summary: str

class QuestionsList(BaseModel):
    questions: list[str]
