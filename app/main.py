import uvicorn
from fastapi import FastAPI
from app.routes.reports import router

app = FastAPI(title="AI Reports API")

app.include_router(
    router,
    prefix="/api/v1/reports",
    tags=["Reports"]
)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8081,
        reload=False,
        log_level="debug"
    )