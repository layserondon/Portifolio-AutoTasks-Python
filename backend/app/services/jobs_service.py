import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import TypedDict

from app.services.parser_service import ResumeSections

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"
USER_AGENT = "find-job-tech/1.0 (resume-job-matcher)"

STOPWORDS = frozenset(
    {
        "a",
        "o",
        "e",
        "de",
        "da",
        "do",
        "das",
        "dos",
        "em",
        "no",
        "na",
        "nos",
        "nas",
        "para",
        "com",
        "por",
        "um",
        "uma",
        "the",
        "and",
        "or",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "an",
        "as",
        "that",
        "this",
        "it",
        "from",
        "our",
        "your",
        "we",
        "you",
        "they",
        "will",
        "have",
        "has",
        "had",
        "not",
        "but",
        "can",
        "all",
        "any",
        "etc",
        "anos",
        "ano",
        "mes",
        "meses",
    }
)

_TOKEN_PATTERN = re.compile(r"[a-z0-9+#.]+(?:[-/][a-z0-9+#.]+)*", re.IGNORECASE)
_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


class JobListing(TypedDict):
    nome: str
    empresa: str
    descricao: str


class ScoredJobListing(JobListing):
    compatibilidade: float
    id: int


def _strip_html(text: str) -> str:
    without_tags = _HTML_TAG_PATTERN.sub(" ", text or "")
    return html.unescape(re.sub(r"\s+", " ", without_tags)).strip()


def _extract_keywords(text: str) -> set[str]:
    tokens: set[str] = set()
    for match in _TOKEN_PATTERN.finditer(text.lower()):
        token = match.group(0).strip(".")
        if len(token) < 2 or token in STOPWORDS:
            continue
        tokens.add(token)
    return tokens


def resume_keywords(sections: ResumeSections) -> set[str]:
    corpus = "\n".join(sections.get(field, "") or "" for field in sections)
    return _extract_keywords(corpus)


def _job_search_text(job: dict) -> str:
    tags = job.get("tags") or []
    tags_text = " ".join(tags) if isinstance(tags, list) else str(tags)
    parts = [
        job.get("title", ""),
        job.get("company_name", ""),
        job.get("category", ""),
        tags_text,
        _strip_html(job.get("description", "")),
    ]
    return " ".join(part for part in parts if part).lower()


def _fetch_remotive_jobs(
    search: str | None = None,
    category: str | None = None,
) -> list[dict]:
    params: dict[str, str] = {}
    if search:
        params["search"] = search
    if category:
        params["category"] = category

    query = f"?{urllib.parse.urlencode(params)}" if params else ""
    request = urllib.request.Request(
        f"{REMOTIVE_API_URL}{query}",
        headers={"User-Agent": USER_AGENT},
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.URLError as exc:
        raise RuntimeError("Não foi possível buscar vagas no Remotive.") from exc

    jobs = payload.get("jobs", [])
    return jobs if isinstance(jobs, list) else []


def _collect_jobs(keywords: set[str]) -> dict[int, dict]:
    jobs_by_id: dict[int, dict] = {}

    search_terms = sorted(keywords, key=len, reverse=True)[:5]
    for term in search_terms:
        for job in _fetch_remotive_jobs(search=term):
            jobs_by_id[job["id"]] = job

    if len(jobs_by_id) < 30:
        for job in _fetch_remotive_jobs():
            jobs_by_id[job["id"]] = job

    return jobs_by_id


def _matched_keywords_count(keywords: set[str], job: dict) -> int:
    text = _job_search_text(job)
    return sum(1 for keyword in keywords if keyword in text)


def compatibility_percent(keywords: set[str], job: dict) -> float:
    """Percentual de palavras-chave do currículo encontradas na vaga (0–100)."""
    if not keywords:
        return 0.0

    matches = _matched_keywords_count(keywords, job)
    percent = (matches / len(keywords)) * 100
    return round(min(100.0, percent), 2)


def _format_job(job: dict) -> JobListing:
    description = _strip_html(job.get("description", ""))
    if len(description) > 3000:
        description = f"{description[:3000].rstrip()}..."

    return {
        "nome": job.get("title", "").strip(),
        "empresa": job.get("company_name", "").strip(),
        "descricao": description,
    }


def fetch_scored_jobs(resume: ResumeSections) -> list[ScoredJobListing]:
    """
    Busca vagas no Remotive e calcula compatibilidade (%) para cada uma.
    Fonte: https://remotive.com/api/remote-jobs
    """
    keywords = resume_keywords(resume)
    if not keywords:
        return []

    jobs_by_id = _collect_jobs(keywords)
    scored_jobs: list[ScoredJobListing] = []

    for job in jobs_by_id.values():
        listing: ScoredJobListing = {
            **_format_job(job),
            "compatibilidade": compatibility_percent(keywords, job),
            "id": int(job["id"]),
        }
        scored_jobs.append(listing)

    return scored_jobs
