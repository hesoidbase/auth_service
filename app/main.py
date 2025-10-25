from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.routes.v1.users import router as user_router
from app.routes.v1.tenants import router as tenant_router
from app.db.connection import get_db

app = FastAPI()
app.include_router(user_router)
app.include_router(tenant_router)

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM users"))
    users = result.fetchall()
    users_dict = [dict(row._mapping) for row in users]
    return {"message": users_dict}



