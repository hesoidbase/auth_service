from app.models.tenants_model import CreateTenant
from app.utils.logger import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app.utils.helpers import row_to_dict
from app.repositories.tenants_repository import TenantRepository

class TenantService: 
    @staticmethod
    async def create_tenant(data: CreateTenant, db):
        try:
            row = await TenantRepository.insert_tenant(db, data)
            await db.commit()
            return row_to_dict(row)
        except IntegrityError as e:
            await db.rollback()
            logging.info(e)
            if "name" in str(e.orig):
                raise ValueError("Tenant name already exists")
            elif "code" in str(e.orig):
                raise ValueError("Tenant code already exists")
            else:
                raise ValueError("Tenant with this information already exists")