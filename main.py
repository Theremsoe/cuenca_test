from contextlib import asynccontextmanager
from fastapi import FastAPI


from bootstrap.kernel import api_router

# from providers.database import migrate_db


# @asynccontextmanager
# async def run_migrations(_: FastAPI):
#     migrate_db()
#     yield


app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
