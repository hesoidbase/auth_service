from app.models.tenants_model import TenantResponse, CreateTenant
from app.services.tenants_services import TenantService
from fastapi import HTTPException

class TenantController:
    @staticmethod
    async def create_tenant(data: CreateTenant ):
        tenant:TenantResponse = await TenantService.create_tenant(data)
        return { "info": tenant["id"]}