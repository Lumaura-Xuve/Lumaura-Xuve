from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = "code_projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    programming_language = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User")
    files = relationship("CodeFile", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.name}>"


class CodeFile(db.Model):
    __tablename__ = "code_files"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("code_projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    content = Column(Text)
    is_directory = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="files")
    
    def __repr__(self):
        return f"<CodeFile {self.path}/{self.filename}>"


class AICodeGeneration(db.Model):
    __tablename__ = "ai_code_generations"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("code_projects.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    generated_code = Column(Text)
    language = Column(String(50))
    status = Column(String(20), default="pending")  # pending, completed, failed
    model_used = Column(String(50))
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project")
    
    def __repr__(self):
        return f"<AICodeGeneration {self.id} for project {self.project_id}>"


class CodeReview(db.Model):
    __tablename__ = "code_reviews"
    
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("code_files.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    file = relationship("CodeFile")
    reviewer = relationship("User")
    
    def __repr__(self):
        return f"<CodeReview {self.id} for file {self.file_id}>"
