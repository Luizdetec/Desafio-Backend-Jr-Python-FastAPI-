from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.api.response_handler import error_response

app = FastAPI(
    title="Game Collection API",
    description="Desafio Backend Jr - FastAPI",
    version="1.0.0",
    docs_url="/docs"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content=error_response(message=str(exc), code="BAD_REQUEST")
    )

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "API is running. Access /docs for documentation."}