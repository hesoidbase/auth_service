from pydantic import BaseModel, Json, field_validator, ConfigDict
from app.utils.enums import TenantType, Plan, TenantStatus
from typing import Dict, Any, Optional
from datetime import datetime

class CreateTenant(BaseModel):

    model_config = ConfigDict(extra='forbid')

    name: str
    code: str
    type: TenantType
    registration_number: Optional[str] = None
    affiliation: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[Json[Dict[str,Any]]] = None
    subscription_plan: Plan
    feature_flags: Optional[Json[Dict[str,Any]]] = None
    status: TenantStatus

    @field_validator('name','code','type','subscription_plan','status')
    @classmethod
    def validate_non_empty(cls,input):
        if not input or not input.strip():
            raise ValueError('Field cannot be empty')
        return input.strip()
    

class TenantResponse(CreateTenant):
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None