from app.models.tenants_model import TenantResponse, CreateTenant
from app.services.tenants_services import TenantService
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class TenantController:
    @staticmethod
    async def create_tenant(data: CreateTenant, db: AsyncSession):
        tenant:TenantResponse = await TenantService.create_tenant(data,db)
        return tenant