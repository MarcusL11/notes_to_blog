from typing import List, Optional
from pydantic import BaseModel


class SubHeader(BaseModel):
    subheader: str
    subheader_description: str


class Header(BaseModel):
    header: str
    header_description: str
    subheader: List[SubHeader]


class BlogOutline(BaseModel):
    sections: List[Header]


class BlogFrontMatter(BaseModel):
    title: str
    topic: str
    goal: str
    writing_style: str
    word_count: str


class Section(BaseModel):
    title: str
    content: str


class VerifyBlog(BaseModel):
    feedback: Optional[str] = None
    valid: bool = False
