from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ..models import Patient, PatientInput, ReportResponse, RiskReportRequest
from ..services.llm import LLMSummarizer
from ..services.risk import calculate_risk
from ..storage import store

router = APIRouter()


@router.post("/patients", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient_input: PatientInput) -> Patient:
    patient = Patient.from_input(patient_input)
    store.add_patient(patient)
    return patient


@router.get("/patients/{patient_id}", response_model=Patient)
def read_patient(patient_id: UUID) -> Patient:
    patient = store.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(request: RiskReportRequest) -> ReportResponse:
    patient = store.get_patient(request.patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    report = calculate_risk(patient)

    if request.summarize:
        summarizer = LLMSummarizer()
        report.llm_summary = summarizer.summarize(report)

    store.add_report(report)
    return ReportResponse(report=report)


@router.get("/reports/{report_id}", response_model=ReportResponse)
def read_report(report_id: UUID) -> ReportResponse:
    report = store.get_report(report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return ReportResponse(report=report)
