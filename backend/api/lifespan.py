from contextlib import asynccontextmanager

from fastapi import FastAPI

from scheduler.scheduler import start_scheduler
from storage.action_history import ActionHistoryRepository
from storage.flagged_emails import FlaggedMessageRepository


def create_database_tables():
    FlaggedMessageRepository().initialize_db()
    ActionHistoryRepository().initialize_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    start_scheduler()
    yield