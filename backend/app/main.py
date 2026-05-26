from fastapi import FastAPI

from app.routes.jobs import jobs_router
from app.routes.matching import matching_router
from app.routes.upload import upload_router

app = FastAPI(title="Find Job Tech API")

app.include_router(upload_router)
app.include_router(jobs_router)
app.include_router(matching_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
