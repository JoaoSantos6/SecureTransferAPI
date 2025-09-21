from typing import List, Optional
from datetime import datetime, date
from app.domain.adapters.customer_repository_interface import CustomerRepositoryInterface
from app.domain.models.customer_model import CustomerModel


class CustomerMockRepository(CustomerRepositoryInterface):
    """
    Implementação mock do repositório de clientes usando dados em memória.
    Útil para testes e desenvolvimento sem necessidade de banco de dados.
    """
    
    def __init__(self):
        # Dados mockados em memória
        self._customers = [
            CustomerModel(
                id=1,
                cpf="123.456.789-00",
                email="joao.silva@email.com",
                full_name="João Silva",
                birthday=date(1990, 5, 15),
                phone_number="+55 11 98765-4321",
                balance=1500.50,
                currency="BRL",
                account_number="12345-6",
                is_active=True,
                is_verified=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            CustomerModel(
                id=2,
                cpf="987.654.321-00",
                email="maria.santos@email.com",
                full_name="Maria Santos",
                birthday=date(1985, 8, 22),
                phone_number="+55 11 87654-3210",
                balance=2300.75,
                currency="BRL",
                account_number="65432-1",
                is_active=True,
                is_verified=False,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            CustomerModel(
                id=3,
                cpf="456.789.123-00",
                email="pedro.oliveira@email.com",
                full_name="Pedro Oliveira",
                birthday=date(1992, 12, 3),
                phone_number="+55 11 76543-2109",
                balance=850.25,
                currency="BRL",
                account_number="98765-4",
                is_active=False,
                is_verified=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        self._next_id = 4
    
    async def create_customer(self, customer_data: dict) -> CustomerModel:
        """Cria um novo cliente no mock"""
        new_customer = CustomerModel(
            id=self._next_id,
            **customer_data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._customers.append(new_customer)
        self._next_id += 1
        return new_customer
    
    async def get_customer_by_id(self, customer_id: int) -> Optional[CustomerModel]:
        """Busca cliente por ID no mock"""
        return next((c for c in self._customers if c.id == customer_id), None)
    
    async def get_customer_by_cpf(self, cpf: str) -> Optional[CustomerModel]:
        """Busca cliente por CPF no mock"""
        return next((c for c in self._customers if c.cpf == cpf), None)
    
    async def get_customer_by_email(self, email: str) -> Optional[CustomerModel]:
        """Busca cliente por email no mock"""
        return next((c for c in self._customers if c.email == email), None)
    
    async def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerModel]:
        """Lista clientes com paginação no mock"""
        return self._customers[skip:skip + limit]
    
    async def update_customer(self, customer_id: int, customer_data: dict) -> Optional[CustomerModel]:
        """Atualiza cliente no mock"""
        customer = await self.get_customer_by_id(customer_id)
        if customer:
            for key, value in customer_data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            customer.updated_at = datetime.now()
            return customer
        return None
    
    async def delete_customer(self, customer_id: int) -> bool:
        """Remove cliente do mock"""
        customer = await self.get_customer_by_id(customer_id)
        if customer:
            self._customers.remove(customer)
            return True
        return False
    
    async def activate_customer(self, customer_id: int) -> Optional[CustomerModel]:
        """Ativa cliente no mock"""
        return await self.update_customer(customer_id, {"is_active": True})
    
    async def deactivate_customer(self, customer_id: int) -> Optional[CustomerModel]:
        """Desativa cliente no mock"""
        return await self.update_customer(customer_id, {"is_active": False})