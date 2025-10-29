from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.tenants_model import CreateTenant

class TenantRepository:
    @staticmethod
    async def insert_tenant(db: AsyncSession, data: CreateTenant):
        query = text("""
            INSERT INTO tenants (
                name, code, type, registration_number, affiliation,
                logo_url, contact_email, contact_phone, address,
                subscription_plan, feature_flags, status, created_by
            ) VALUES (
                :name, :code, :type, :registration_number, :affiliation,
                :logo_url, :contact_email, :contact_phone, :address,
                :subscription_plan, :feature_flags, :status, :created_by
            )
            RETURNING *
        """)
        result = await db.execute(query, {
            "name": data.name, 
            "code": data.code, 
            "type": data.type, 
            "subscription_plan": data.subscription_plan, 
            "status": data.status, 
            "registration_number": data.registration_number, 
            "affiliation": data.affiliation, 
            "logo_url": data.logo_url, 
            "contact_email": data.contact_email, 
            "contact_phone": data.contact_phone, 
            "address": data.address, 
            "feature_flags": data.feature_flags, 
            "created_by": None # System-created tenant
        })
        return result.fetchone()