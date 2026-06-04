from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from schemas.auth import AuthConfig

class ScenarioStep(BaseModel):
    name: str
    method: str = "GET"
    url: str
    headers: Optional[Dict[str, str]] = None
    payload: Optional[Dict[str, str]] = None
    think_time_ms: int = 0
    extract_vars: Optional[Dict[str, str]] = None # Variable name to JSONPath

class Scenario(BaseModel):
    name: str
    steps: List[ScenarioStep]
    concurrency: int = Field(gt=0, le=10000)
    duration_seconds: Optional[int] = 60
    auth: Optional[AuthConfig] = None
