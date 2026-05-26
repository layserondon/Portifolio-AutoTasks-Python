from fastapi import APIRouter

from app.models.schemas import MatchRequest, MatchResponse
from app.services.matching_service import match_resume_sections

matching_router = APIRouter(prefix="/api", tags=["matching"])


@matching_router.post("/matching", response_model=MatchResponse)
def match_jobs(payload: MatchRequest):
    score_minimo = payload.score_minimo
    resume = payload.model_dump(
        include={"habilidades", "experiencia", "formacao", "cursos", "idiomas"}
    )
    matches = match_resume_sections(resume, score_minimo=score_minimo)
    return MatchResponse(
        total=len(matches),
        score_minimo=score_minimo,
        matches=matches,
    )
