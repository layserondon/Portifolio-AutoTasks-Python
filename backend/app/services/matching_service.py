from app.services.jobs_service import ScoredJobListing, fetch_scored_jobs
from app.services.parser_service import ResumeSections, split_resume_sections

MIN_COMPATIBILITY_FLOOR = 10.0
MAX_COMPATIBILITY = 100.0


def _normalize_score_minimo(score_minimo: float) -> float:
    return max(MIN_COMPATIBILITY_FLOOR, min(MAX_COMPATIBILITY, score_minimo))


def match_resume_sections(
    resume: ResumeSections,
    score_minimo: float = MIN_COMPATIBILITY_FLOOR,
) -> list[ScoredJobListing]:

    threshold = _normalize_score_minimo(score_minimo)
    scored_jobs = fetch_scored_jobs(resume)

    filtered = [
        job
        for job in scored_jobs
        if job["compatibilidade"] >= threshold
        and job["compatibilidade"] >= MIN_COMPATIBILITY_FLOOR
    ]

    filtered.sort(key=lambda job: job["compatibilidade"])
    return filtered


def match_resume_to_jobs(
    resume_text: str,
    score_minimo: float = MIN_COMPATIBILITY_FLOOR,
    job_ids: list[str] | None = None,
) -> list[ScoredJobListing]:
    sections = split_resume_sections(resume_text)
    results = match_resume_sections(sections, score_minimo=score_minimo)

    if not job_ids:
        return results

    job_ids_set = {str(job_id) for job_id in job_ids}
    return [job for job in results if str(job["id"]) in job_ids_set]
