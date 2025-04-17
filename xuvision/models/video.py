from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    videos = relationship("Video", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Video(db.Model):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(255), nullable=False)
    thumbnail_path = Column(String(255))
    duration = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="videos")
    transcription = relationship("Transcription", back_populates="video", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Video {self.title}>"


class Transcription(db.Model):
    __tablename__ = "transcriptions"
    
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    content = Column(Text)
    language = Column(String(10), default="en")
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    video = relationship("Video", back_populates="transcription")
    segments = relationship("TranscriptionSegment", back_populates="transcription", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Transcription for video_id={self.video_id}>"


class TranscriptionSegment(db.Model):
    __tablename__ = "transcription_segments"
    
    id = Column(Integer, primary_key=True)
    transcription_id = Column(Integer, ForeignKey("transcriptions.id"), nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    speaker = Column(String(64))
    confidence = Column(Float)
    transcription = relationship("Transcription", back_populates="segments")
    
    def __repr__(self):
        return f"<Segment {self.start_time}-{self.end_time}: {self.text[:30]}...>"
