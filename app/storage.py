import threading
from typing import Dict, Optional
from uuid import UUID

from .models import Patient, RiskReport


class InMemoryStore:
    def __init__(self) -> None:
        self._patients: Dict[UUID, Patient] = {}
        self._reports: Dict[UUID, RiskReport] = {}
        self._lock = threading.Lock()

    def add_patient(self, patient: Patient) -> Patient:
        with self._lock:
            self._patients[patient.id] = patient
        return patient

    def get_patient(self, patient_id: UUID) -> Optional[Patient]:
        return self._patients.get(patient_id)

    def add_report(self, report: RiskReport) -> RiskReport:
        with self._lock:
            self._reports[report.id] = report
        return report

    def get_report(self, report_id: UUID) -> Optional[RiskReport]:
        return self._reports.get(report_id)


store = InMemoryStore()
