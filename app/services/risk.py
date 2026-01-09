from datetime import datetime
from typing import List
from uuid import uuid4

from ..models import Patient, RiskFactors, RiskReport


def calculate_risk(patient: Patient) -> RiskReport:
    factors: List[str] = []
    elevated_vitals: List[str] = []
    flagged_conditions: List[str] = []

    # Simple rules for illustration; replace with domain logic later.
    if patient.age >= 65:
        factors.append("Age over 65 increases baseline risk.")
    if patient.vitals:
        if patient.vitals.systolic_bp and patient.vitals.systolic_bp >= 140:
            elevated_vitals.append("High systolic blood pressure")
        if patient.vitals.diastolic_bp and patient.vitals.diastolic_bp >= 90:
            elevated_vitals.append("High diastolic blood pressure")
        if patient.vitals.heart_rate and patient.vitals.heart_rate >= 100:
            elevated_vitals.append("Elevated heart rate")
    if patient.conditions:
        flagged_conditions.extend(patient.conditions)

    risk_score = 20
    risk_score += min(patient.age, 40)  # age contribution
    risk_score += 10 * len(elevated_vitals)
    risk_score += 5 * len(flagged_conditions)
    risk_score = min(risk_score, 100)

    if risk_score >= 75:
        risk_level = "high"
    elif risk_score >= 50:
        risk_level = "moderate"
    else:
        risk_level = "low"

    return RiskReport(
        id=uuid4(),
        patient_id=patient.id,
        risk_score=risk_score,
        risk_level=risk_level,
        factors=RiskFactors(
            elevated_vitals=elevated_vitals,
            flagged_conditions=flagged_conditions,
            notes=factors,
        ),
        generated_at=datetime.utcnow(),
    )
