from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from app.models.tenants_model import CreateTenant
from app.controllers.tenants_controller import TenantController
from app.db.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tenant", tags=["tenant"])


@router.post("/create")
async def create_tenant(tenant_data: CreateTenant, db: AsyncSession = Depends(get_db)):
    try:
        return await TenantController.create_tenant(tenant_data,db)
    except ValueError as e:
        return HTTPException(status_code=400,detail=str(e))
    

