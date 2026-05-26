from fastapi import APIRouter, Query

from app.models.schemas import JobsMatchResponse, ResumeSectionsResponse
from app.services.matching_service import match_resume_sections

jobs_router = APIRouter(prefix="/api", tags=["jobs"])


@jobs_router.post("/jobs", response_model=JobsMatchResponse)
def search_jobs(
    resume: ResumeSectionsResponse,
    score_minimo: float = Query(
        default=10.0,
        ge=10.0,
        le=100.0,
        description="Compatibilidade mínima (%) para exibir a vaga (10–100).",
    ),
):
    vagas = match_resume_sections(resume.model_dump(), score_minimo=score_minimo)
    return JobsMatchResponse(
        total=len(vagas),
        score_minimo=score_minimo,
        vagas=vagas,
    )
