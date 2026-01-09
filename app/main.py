from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Health Outlook API",
        version="0.1.0",
        description="Collect clinician inputs, generate risk reports, and summarize via LLM.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
