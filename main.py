from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- DOCTOR APIs --------------------

@app.post("/doctors")
def create_doctor(doctor: schemas.Doctor, db: Session = Depends(get_db)):
    db_doctor = models.DoctorDB(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(models.DoctorDB).all()


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.DoctorDB).filter(models.DoctorDB.id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return doctor

# -------------------- PATIENT APIs --------------------

@app.post("/patients")
def create_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
    db_patient = models.PatientDB(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    return db.query(models.PatientDB).all()