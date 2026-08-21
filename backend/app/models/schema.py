# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    companies = relationship("Company", back_populates="owner")
    social_accounts = relationship("SocialAccount", back_populates="user")


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String)
    logo_url = Column(String)
    brand_colors = Column(JSONB) # All 9 hex values with names
    primary_color = Column(String)
    secondary_color = Column(String)
    text_color = Column(String)
    background_color = Column(String)
    website = Column(String)
    
    # v2 additions
    apply_link = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    why_join_us = Column(ARRAY(String), nullable=True)

    owner = relationship("User", back_populates="companies")
    jobs = relationship("Job", back_populates="company")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    title = Column(String, index=True)
    experience = Column(String)
    location = Column(String)
    remote_type = Column(String) # Remote, Hybrid, On-site
    skills = Column(ARRAY(String))
    salary = Column(String, nullable=True)
    description = Column(Text)
    deadline = Column(String)
    
    # v2 additions
    apply_link = Column(String, nullable=True)
    min_experience = Column(Integer, nullable=True)
    max_experience = Column(Integer, nullable=True)
    education_requirements = Column(ARRAY(String), nullable=True)
    salary_disclosure = Column(String, nullable=True)
    salary_max = Column(String, nullable=True)
    match_threshold = Column(Float, default=30.0)
    number_of_openings = Column(Integer, nullable=True)
    
    # v3 additions
    role_objective = Column(Text, nullable=True)
    key_responsibilities = Column(ARRAY(String), nullable=True)
    krm_measurement = Column(Text, nullable=True)
    preferred_certifications = Column(ARRAY(String), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="jobs")
    candidates = relationship("Candidate", back_populates="job")
    banners = relationship("Banner", back_populates="job")
    posts = relationship("Post", back_populates="job")
    search_history = relationship("CandidateSearchHistory", back_populates="job")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    name = Column(String)
    skills = Column(ARRAY(String))
    experience = Column(String)
    location = Column(String)
    source = Column(String) # e.g. GitHub, CSV upload
    profile_url = Column(String)
    match_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="candidates")


class CandidateSearchHistory(Base):
    __tablename__ = "candidate_search_history"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    searched_at = Column(DateTime(timezone=True), server_default=func.now())
    filters_used = Column(JSONB)

    job = relationship("Job", back_populates="search_history")


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="banners")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    content = Column(Text)
    hashtags = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="posts")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String) # e.g. LinkedIn
    connected = Column(Integer) # Boolean 0 or 1, or boolean type depending on pg
    connected_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="social_accounts")
