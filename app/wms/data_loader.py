from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Service(BaseModel):    
    name: str
    title: str
    abstract: Optional[str] = None
    keywords: Optional[str] = None