CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- ENUM types
CREATE TYPE GENDER_ENUM AS ENUM ('male', 'female', 'other', 'prefer_not_to_say');
CREATE TYPE USER_STATUS AS ENUM ('active', 'inactive', 'suspended', 'archived');
CREATE TYPE TENANT_STATUS AS ENUM ('active', 'inactive', 'suspended', 'archived');
CREATE TYPE TENANT_TYPE AS ENUM ('school', 'college', 'university', 'coaching_center', 'training_institute');
CREATE TYPE PLAN AS ENUM ('free', 'standard', 'premium', 'enterprise');


-- Departments
CREATE TABLE departments (
    department_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255)
);

-- Tenants table (created_by will be added later)
CREATE TABLE tenants (
    tenant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    code VARCHAR(255) UNIQUE,
    type TENANT_TYPE DEFAULT 'school',
    registration_number VARCHAR(255),
    affiliation VARCHAR(255),
    logo_url TEXT,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(255),
    address JSONB,
    subscription_plan PLAN DEFAULT 'free',
    feature_flags JSONB,
    status TENANT_STATUS DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
    -- created_by and updated_by will be added via ALTER TABLE to avoid circular FK
);

-- Roles
CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_name TEXT,
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id)
);

-- Classes
CREATE TABLE classes (
    class_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_id UUID not null references departments(department_id),
    class_name VARCHAR(255)
);

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id),
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    dob DATE,
    gender GENDER_ENUM,
    phone_number VARCHAR(255),
    status USER_STATUS DEFAULT 'active',
    role UUID NOT NULL REFERENCES roles(role_id),
    department_id UUID REFERENCES departments(department_id),
    class_id UUID REFERENCES classes(class_id),
    emergency_contact JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Add created_by and updated_by FKs to tenants AFTER users table exists
ALTER TABLE tenants
ADD COLUMN created_by UUID NOT NULL,
ADD COLUMN updated_by UUID,
ADD CONSTRAINT fk_tenants_created_by FOREIGN KEY (created_by) REFERENCES users(user_id),
ADD CONSTRAINT fk_tenants_updated_by FOREIGN KEY (updated_by) REFERENCES users(user_id);

-- Audit logs
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id),
    action TEXT,
    ip_address VARCHAR(255),
    user_agent VARCHAR(255),
    metadata JSONB,
    timestamp TIMESTAMP
);

-- Security
CREATE TABLE security (
    security_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    password_hash TEXT, 
    password_changed_at TIMESTAMP,
    failed_attempt INT,
    is_locked BOOLEAN DEFAULT FALSE,
    locked_at TIMESTAMP,
    locked_until TIMESTAMP,
    locked_by UUID REFERENCES users(user_id),
    locked_by_system BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP,
    last_login_ip VARCHAR(255),
    last_login_device VARCHAR(255),
    is_email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    phone_verified BOOLEAN DEFAULT FALSE
);



-- Unique index for email per tenant
CREATE UNIQUE INDEX uq_users_tenant_email ON users(tenant_id, email);

-- Trigger function for updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER trigger_user_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_tenants_updated_at
BEFORE UPDATE ON tenants
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
