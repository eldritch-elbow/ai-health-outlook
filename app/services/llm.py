import os
from typing import Optional

from openai import OpenAI, OpenAIError

from ..models import RiskReport


class LLMSummarizer:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def summarize(self, report: RiskReport) -> str:
        if not self.client or not self.api_key:
            return self._fallback_summary(report)

        prompt = (
            "You are a clinical assistant summarizing a patient risk report "
            "for a clinician. Avoid diagnoses; keep it concise and actionable."
        )
        content = (
            f"Risk level: {report.risk_level} ({report.risk_score}/100).\n"
            f"Factors: vitals={report.factors.elevated_vitals}, "
            f"conditions={report.factors.flagged_conditions}, "
            f"notes={report.factors.notes}.\n"
            "Provide a short summary and suggest next follow-up steps."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content},
                ],
                max_tokens=150,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except OpenAIError:
            # Fall back to deterministic summary if API errors occur.
            return self._fallback_summary(report)

    def _fallback_summary(self, report: RiskReport) -> str:
        return (
            f"Risk level is {report.risk_level} ({report.risk_score}/100). "
            f"Elevated factors: {', '.join(report.factors.elevated_vitals) or 'none'}. "
            f"Conditions noted: {', '.join(report.factors.flagged_conditions) or 'none'}. "
            "Consider a follow-up assessment and review of vitals."
        )
