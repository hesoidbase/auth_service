from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.tenants_model import CreateTenant
from app.controllers.tenants_controller import TenantController

router = APIRouter(prefix="/tenant", tags=["tenant"])


@router.post("/create")
async def create_tenant(tenant_data: CreateTenant):
    try:
        return await TenantController.create_tenant(tenant_data)
    except ValueError as e:
        return HTTPException(status_code=400,detail=str(e))
    

