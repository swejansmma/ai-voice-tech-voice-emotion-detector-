from pydantic import BaseModel
class AnalyticsResult(BaseModel):
    intent: str
    topic: str
    sentiment: str
    tone: str
    escalation_risk: str
class Message(BaseModel):
    sender: str
    text: str
