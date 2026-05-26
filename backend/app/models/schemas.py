from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    habilidades: str = ""
    experiencia: str = ""
    formacao: str = ""
    cursos: str = ""
    idiomas: str = ""
    score_minimo: float = Field(
        default=10.0,
        ge=10.0,
        le=100.0,
        description="Compatibilidade mínima (%) para exibir a vaga (10–100).",
    )


class ResumeSectionsResponse(BaseModel):
    habilidades: str = ""
    experiencia: str = ""
    formacao: str = ""
    cursos: str = ""
    idiomas: str = ""


class JobListingResponse(BaseModel):
    nome: str
    empresa: str
    descricao: str
    compatibilidade: float = Field(
        description="Score de compatibilidade com o currículo (0–100%)."
    )
    id: int | None = None


class JobsMatchResponse(BaseModel):
    total: int
    score_minimo: float
    vagas: list[JobListingResponse]


class MatchResponse(BaseModel):
    total: int
    score_minimo: float
    matches: list[JobListingResponse]
