from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class UserCreate(BaseModel):
    email: str
    password: str
    role: str
    full_name: Optional[str]

class UserOut(BaseModel):
    id: int
    email: str
    role: str
    full_name: Optional[str]

    class Config:
        orm_mode = True

class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[Dict[str, Any]] = {}
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience_level: Optional[str] = "Mid-level"
    required_skills: Optional[str] = None

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    requirements: Dict[str, Any]
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience_level: str
    required_skills: Optional[str] = None

    class Config:
        orm_mode = True

class ApplyResult(BaseModel):
    status: str
    application_id: int


class JobScore(BaseModel):
    job_id: int
    job_title: str
    job_description: str
    score: float
    explanation: Dict[str, Any]
    matched_skills: List[str] = []

    class Config:
        orm_mode = True

