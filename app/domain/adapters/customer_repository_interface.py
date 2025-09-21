from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.customer_model import CustomerModel


class CustomerRepositoryInterface(ABC):
    """
    Interface abstrata para operações de repositório de clientes.
    Implementa o padrão Adapter para permitir diferentes sources de dados.
    """
    
    @abstractmethod
    async def create_customer(self, customer_data: dict) -> CustomerModel:
        """Cria um novo cliente"""
        pass
    
    @abstractmethod
    async def get_customer_by_id(self, customer_id: int) -> Optional[CustomerModel]:
        """Busca um cliente pelo ID"""
        pass
    
    @abstractmethod
    async def get_customer_by_cpf(self, cpf: str) -> Optional[CustomerModel]:
        """Busca um cliente pelo CPF"""
        pass
    
    @abstractmethod
    async def get_customer_by_email(self, email: str) -> Optional[CustomerModel]:
        """Busca um cliente pelo email"""
        pass
    
    @abstractmethod
    async def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerModel]:
        """Lista todos os clientes com paginação"""
        pass
    
    @abstractmethod
    async def update_customer(self, customer_id: int, customer_data: dict) -> Optional[CustomerModel]:
        """Atualiza um cliente existente"""
        pass
    
    @abstractmethod
    async def delete_customer(self, customer_id: int) -> bool:
        """Remove um cliente"""
        pass
    
    @abstractmethod
    async def activate_customer(self, customer_id: int) -> Optional[CustomerModel]:
        """Ativa um cliente"""
        pass
    
    @abstractmethod
    async def deactivate_customer(self, customer_id: int) -> Optional[CustomerModel]:
        """Desativa um cliente"""
        pass