from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting Machine API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "E-Voting System API is running 🚀"}


@app.post("/voter/register")
def register_voter(voter: schemas.VoterRegister, db: Session = Depends(get_db)):
    existing_voter = db.query(models.Voter).filter(models.Voter.nid == voter.nid).first()
    if existing_voter:
        raise HTTPException(status_code=400, detail="Voter already registered")

    new_voter = models.Voter(nid=voter.nid, name=voter.name, birth_date=voter.birth_date)
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return {"message": f"Voter {voter.name} registered successfully"}


@app.post("/candidate/add")
def add_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    new_candidate = models.Candidate(name=candidate.name, party=candidate.party)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return {"message": f"Candidate {candidate.name} added successfully"}


@app.post("/vote/{nid}/{candidate_id}")
def vote(nid: str, candidate_id: int, db: Session = Depends(get_db)):
    voter = db.query(models.Voter).filter(models.Voter.nid == nid).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found")

    if voter.has_voted:
        raise HTTPException(status_code=400, detail="Voter has already voted")

    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    new_vote = models.Vote(voter_id=voter.id, candidate_id=candidate.id)
    db.add(new_vote)
    voter.has_voted = True
    db.commit()

    return {"message": f"{voter.name} successfully voted for {candidate.name}"}


@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    results = []
    for candidate in candidates:
        vote_count = db.query(models.Vote).filter(models.Vote.candidate_id == candidate.id).count()
        results.append({
            "candidate": candidate.name,
            "party": candidate.party,
            "votes": vote_count
        })
    return {"results": results}
