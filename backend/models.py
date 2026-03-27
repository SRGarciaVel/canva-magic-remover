from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class ImageHistory(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)