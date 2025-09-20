import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = sqlalchemy.orm.declarative_base()

class BankModel(Base):
    __tablename__ = 'banks'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(255), nullable=False)
    short_name = sa.Column(sa.String(50), nullable=False)
    country = sa.Column(sa.String(50), nullable=False)
    allowed_operations = sa.Column(sa.ARRAY(sa.String), nullable=False)
    operation_hours = sa.Column(sa.JSON, nullable=True)
    supports_pix = sa.Column(sa.Boolean, nullable=False, default=False)
    supports_international = sa.Column(sa.Boolean, nullable=False, default=False)
    website = sa.Column(sa.String(255), nullable=True)
    support_phone = sa.Column(sa.String(20), nullable=True)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())

    def __repr__(self):
        return (
            f"<BankModel(id={self.id}, bacen_code='{self.bacen_code}', name='{self.name}', "
            f"country='{self.country}', is_active={self.is_active})>"
        )