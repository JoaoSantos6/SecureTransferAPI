import sqlalchemy as sa
import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()

class CustomerModel(Base):
    __tablename__ = 'Customers'
    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    cpf = sa.Column(sa.String(14), nullable=False)
    email = sa.Column(sa.String(255), nullable=False)
    full_name = sa.Column(sa.String(255), nullable=False)
    birthday = sa.Column(sa.Date, nullable=False)
    phone_number = sa.Column(sa.String(20), nullable=False)
    balance = sa.Column(sa.Numeric(precision=12, scale=2), nullable=False)
    currency = sa.Column(sa.String(3), nullable=False) 
    account_number = sa.Column(sa.String(20), nullable=False)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    is_verified = sa.Column(sa.Boolean, nullable=False, default=False)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    
    def __repr__(self):
        return (
            f"<CustomerModel(id={self.id}, cpf='{self.cpf}', email='{self.email}', "
            f"full_name='{self.full_name}', is_active={self.is_active}, is_verified={self.is_verified})>"
        )