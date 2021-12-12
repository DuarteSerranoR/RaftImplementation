from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Logs(Base):
    __tablename__ = 'Logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=func.now())
    replica_id = Column(Integer)
    label = Column(String)
    data = Column(String)
    Base = Base

    def __repr__(self):
        return 'id: {}'.format(self.id)
