from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Voter(Base):
    __tablename__ = "voters"
    id = Column(Integer, primary_key=True, index=True)
    nid = Column(String(20), unique=True, index=True)
    name = Column(String(100), nullable=False)  
    # ? dd/mm/yyyy format         
    birth_date = Column(String(10), nullable=False)       
    has_voted = Column(Boolean, default=False)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)             
    party = Column(String(50), nullable=False)              
    votes = relationship("Vote", back_populates="candidate")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))

    voter = relationship("Voter")
    candidate = relationship("Candidate", back_populates="votes")
