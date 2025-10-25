from enum import Enum

class Gender(str,Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class UserStatus(str,Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    archived = "archived"

class TenantStatus(str,Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    archived = "archived"

class TenantType(str,Enum):
    school = "school"
    college = "college"
    university = "university"
    coaching_center = "coaching_center"
    training_institute = "training_institute"

class Plan(str,Enum):
    free = "free"
    standard = "standard"
    premium = "premium"
    enterprise = "enterprise"