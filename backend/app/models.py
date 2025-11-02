from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, JSON
from datetime import datetime
from .db import Base

class Applicant(Base):
    __tablename__ = "applicants"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="applicant")

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))
    status: Mapped[str] = mapped_column(String(50), default="submitted")
    form_data: Mapped[dict] = mapped_column(JSON, default={})
    extracted_text: Mapped[str] = mapped_column(Text, default="")
    decision_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    applicant: Mapped["Applicant"] = relationship("Applicant", back_populates="applications")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="application")

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    filename: Mapped[str] = mapped_column(String(400))
    filetype: Mapped[str] = mapped_column(String(40))
    path: Mapped[str] = mapped_column(String(600))
    text: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    application: Mapped["Application"] = relationship("Application", back_populates="documents")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
