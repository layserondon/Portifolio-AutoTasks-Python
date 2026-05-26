from fastapi import APIRouter, File, UploadFile

from app.models.schemas import ResumeSectionsResponse
from app.services.parser_service import parse_resume_pdf

upload_router = APIRouter(prefix="/api", tags=["upload"])


@upload_router.post("/upload", response_model=ResumeSectionsResponse)
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    sections = parse_resume_pdf(content)
    return ResumeSectionsResponse(**sections)
