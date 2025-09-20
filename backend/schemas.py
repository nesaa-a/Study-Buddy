from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Document schemas
class DocumentBase(BaseModel):
    filename: str
    original_content: str
    summary: Optional[str] = None
    file_size: Optional[int] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Study Session schemas
class StudySessionBase(BaseModel):
    session_name: str
    questions: Optional[str] = None
    answers: Optional[str] = None
    score: Optional[float] = None

class StudySessionCreate(StudySessionBase):
    document_id: int

class StudySessionResponse(StudySessionBase):
    id: int
    user_id: int
    document_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Upload response schema
class UploadResponse(BaseModel):
    filename: str
    status: str
    extracted_text: str
    summary: str
    text_length: int
    document_id: Optional[int] = None
