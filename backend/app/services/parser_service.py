import re
from typing import TypedDict

from app.services.pdf_service import extract_text_from_pdf

SECTION_HEADERS: dict[str, str] = {
    "habilidades": r"(?:habilidades|skills|compet[eê]ncias|conhecimentos)",
    "experiencia": r"(?:experi[eê]ncia(?:\s+profissional)?|experience)",
    "formacao": r"(?:forma[cç][aã]o(?:\s+acad[eê]mica)?|educa[cç][aã]o|education)",
    "cursos": r"(?:cursos(?:\s+e\s+certifica[cç][oõ]es)?|certifica[cç][oõ]es|certifications)",
    "idiomas": r"(?:idiomas|languages)",
}

_HEADER_PATTERN = re.compile(
    r"(?im)^\s*(" + "|".join(SECTION_HEADERS.values()) + r")\s*:?\s*$"
)


class ResumeSections(TypedDict):
    habilidades: str
    experiencia: str
    formacao: str
    cursos: str
    idiomas: str


def _empty_sections() -> ResumeSections:
    return {
        "habilidades": "",
        "experiencia": "",
        "formacao": "",
        "cursos": "",
        "idiomas": "",
    }


def _header_to_field(header: str) -> str | None:
    normalized = header.strip().lower()
    for field, pattern in SECTION_HEADERS.items():
        if re.fullmatch(pattern, normalized, flags=re.IGNORECASE):
            return field
    return None


def split_resume_sections(text: str) -> ResumeSections:
    sections = _empty_sections()
    if not text or not text.strip():
        return sections

    matches = list(_HEADER_PATTERN.finditer(text))
    if not matches:
        sections["experiencia"] = text.strip()
        return sections

    for index, match in enumerate(matches):
        field = _header_to_field(match.group(1))
        if not field:
            continue

        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        if content:
            sections[field] = content

    return sections


def parse_resume_pdf(content: bytes) -> ResumeSections:
    text = extract_text_from_pdf(content)
    return split_resume_sections(text)
