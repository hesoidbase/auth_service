import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/EDULMS")

engine = create_async_engine(DATABASE_URL,echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)