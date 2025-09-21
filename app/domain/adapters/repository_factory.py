import os
from app.domain.adapters.customer_repository_interface import CustomerRepositoryInterface
from app.db.mock.customer_mock_repository import CustomerMockRepository


class RepositoryFactory:
    """
    Factory para criar instâncias de repositórios baseado na configuração.
    Permite alternar facilmente entre mock e implementações reais.
    """
    
    @staticmethod
    def create_customer_repository() -> CustomerRepositoryInterface:
        """
        Cria e retorna uma instância do repositório de clientes.
        
        Usa a variável de ambiente USE_MOCK_DB para determinar
        qual implementação usar:
        - True: usa mock em memória
        - False: usa implementação real (banco de dados)
        """
        use_mock = os.getenv("USE_MOCK_DB", "true").lower() == "true"
        
        if use_mock:
            return CustomerMockRepository()
        else:
            # Aqui você importaria e retornaria a implementação real
            # from app.db.repositories.customer_db_repository import CustomerDBRepository
            # return CustomerDBRepository()
            raise NotImplementedError("Implementação real do repositório ainda não foi criada")


# Instância singleton para reutilizar o repositório
_customer_repository_instance: CustomerRepositoryInterface = None


def get_customer_repository() -> CustomerRepositoryInterface:
    """
    Retorna a instância do repositório de clientes.
    Implementa padrão Singleton para garantir uma única instância.
    """
    global _customer_repository_instance
    if _customer_repository_instance is None:
        _customer_repository_instance = RepositoryFactory.create_customer_repository()
    return _customer_repository_instance


def reset_repository():
    """
    Reseta a instância do repositório (útil para testes)
    """
    global _customer_repository_instance
    _customer_repository_instance = None