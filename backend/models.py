from sqlalchemy import Column, Integer, String, Text, JSON, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sourcematch.db")

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'recruiter' or 'candidate'
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default={})
    company = Column(String, nullable=True)  # Company name
    location = Column(String, nullable=True)  # Job location
    salary_min = Column(Integer, nullable=True)  # Minimum salary in thousands
    salary_max = Column(Integer, nullable=True)  # Maximum salary in thousands
    experience_level = Column(String, default="Mid-level")  # Junior, Mid-level, Senior
    required_skills = Column(String, nullable=True)  # Comma-separated skills
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    recruiter = relationship("User")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("users.id"))
    resume_path = Column(String)
    resume_text = Column(Text)
    score = Column(Float)
    status = Column(String, default="applied") # applied, shortlisted, rejected
    explanation = Column(JSON)
    fingerprint = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    job = relationship("Job")
    candidate = relationship("User")

class Block(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    candidate_fingerprint = Column(String, nullable=False)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class MatchSearch(Base):
    __tablename__ = "match_searches"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resume_path = Column(String)
    fingerprint = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("match_searches.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    job_title = Column(String)
    score = Column(Float)
    explanation = Column(JSON)
    matched_skills = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
