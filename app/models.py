from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class VitalSigns(BaseModel):
    heart_rate: Optional[int] = Field(None, ge=20, le=220)
    systolic_bp: Optional[int] = Field(None, ge=60, le=250)
    diastolic_bp: Optional[int] = Field(None, ge=40, le=150)


class PatientInput(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    sex: str = Field(..., pattern="^(male|female|other)$")
    conditions: List[str] = Field(default_factory=list)
    vitals: Optional[VitalSigns] = None
    clinical_notes: Optional[str] = None


class Patient(PatientInput):
    id: UUID

    @classmethod
    def from_input(cls, patient_input: PatientInput) -> "Patient":
        return cls(
            id=uuid4(),
            first_name=patient_input.first_name,
            last_name=patient_input.last_name,
            age=patient_input.age,
            sex=patient_input.sex,
            conditions=patient_input.conditions,
            vitals=patient_input.vitals,
            clinical_notes=patient_input.clinical_notes,
        )


class RiskReportRequest(BaseModel):
    patient_id: UUID
    summarize: bool = True


class RiskFactors(BaseModel):
    elevated_vitals: List[str] = Field(default_factory=list)
    flagged_conditions: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class RiskReport(BaseModel):
    id: UUID
    patient_id: UUID
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    factors: RiskFactors
    generated_at: datetime
    llm_summary: Optional[str] = None


class ReportResponse(BaseModel):
    report: RiskReport
