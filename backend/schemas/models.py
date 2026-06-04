from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from core.database import Base

class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True)
    concurrency = Column(Integer)
    total_requests = Column(Integer)
    successful_requests = Column(Integer)
    failed_requests = Column(Integer)
    average_latency_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
