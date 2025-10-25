from app.models.tenants_model import CreateTenant
from app.db.connection import get_db

class TenantService: 
    @staticmethod
    async def create_tenant(data: CreateTenant):
        return { "id": "12344"}