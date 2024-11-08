from fastapi import APIRouter

from app.http.v1.controllers.puzzle import http_puzzle_router

api_router = APIRouter()

api_router.include_router(http_puzzle_router)
