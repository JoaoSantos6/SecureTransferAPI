# Teoria - Documentação Técnica do Projeto SecureTransferAPI

## Sumário
- [1. Visão Geral do Projeto](#1-visão-geral-do-projeto)
- [2. Clean Architecture (Arquitetura Limpa)](#2-clean-architecture-arquitetura-limpa)
- [3. Padrões de Design Utilizados](#3-padrões-de-design-utilizados)
- [4. Tecnologias e Bibliotecas](#4-tecnologias-e-bibliotecas)
- [5. Estrutura de Diretórios](#5-estrutura-de-diretórios)
- [6. Componentes do Sistema](#6-componentes-do-sistema)
- [7. Fluxo de Dados](#7-fluxo-de-dados)
- [8. Como Tudo se Conecta](#8-como-tudo-se-conecta)

---

## 1. Visão Geral do Projeto

O **SecureTransferAPI** é uma API REST desenvolvida em Python usando FastAPI para gerenciar transferências bancárias de forma segura. O projeto segue os princípios da Clean Architecture (Arquitetura Limpa) e utiliza vários padrões de design para garantir código limpo, testável e maintível.

### Objetivos principais:
- **Segurança**: Proteção de dados sensíveis dos clientes
- **Escalabilidade**: Facilidade para adicionar novas funcionalidades
- **Testabilidade**: Possibilidade de testar componentes isoladamente
- **Manutenibilidade**: Código organizado e fácil de manter

---

## 2. Clean Architecture (Arquitetura Limpa)

### O que é Clean Architecture?

Clean Architecture é um padrão arquitetural criado por Robert "Uncle Bob" Martin que organiza o código em camadas concêntricas, onde as camadas internas não conhecem as externas. Isso torna o sistema independente de frameworks, bancos de dados e interfaces externas.

### Camadas da Clean Architecture:

```
┌─────────────────────────────────────┐
│     Frameworks & Drivers           │  ← FastAPI, SQLAlchemy, PostgreSQL
│  ┌───────────────────────────────┐  │
│  │    Interface Adapters        │  │  ← Controllers, Repositories
│  │  ┌─────────────────────────┐  │  │
│  │  │   Application Business  │  │  │  ← Use Cases, Services
│  │  │  ┌─────────────────────┐ │  │  │
│  │  │  │   Enterprise Core   │ │  │  │  ← Entities, Domain Models
│  │  │  └─────────────────────┘ │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┐  │
└─────────────────────────────────────┘
```

### Como aplicamos no projeto:

- **Enterprise Core**: `app/models/` - Entidades de domínio (Customer, Bank)
- **Application Business**: `app/domain/services/` - Lógica de negócio
- **Interface Adapters**: `app/adapters/` - Interfaces e implementações de repositórios
- **Frameworks & Drivers**: `app/api/` - Controllers FastAPI

### Vantagens:
- **Independência de Framework**: Podemos trocar FastAPI por Flask sem afetar a lógica de negócio
- **Independência de Banco**: Podemos usar PostgreSQL, MySQL ou até mesmo mocks
- **Testabilidade**: Cada camada pode ser testada independentemente
- **Flexibilidade**: Mudanças externas não afetam o núcleo da aplicação

---

## 3. Padrões de Design Utilizados

### 3.1 Factory Pattern (Padrão Fábrica)

#### O que é?
O Factory Pattern é um padrão de criação que fornece uma interface para criar objetos sem especificar suas classes concretas. É como uma "fábrica" que produz objetos baseada em algum critério.

#### Como usamos no projeto:
```python
# app/adapters/repository_factory.py
class RepositoryFactory:
    @staticmethod
    def create_customer_repository() -> CustomerRepositoryInterface:
        use_mock = os.getenv("USE_MOCK_DB", "true").lower() == "true"
        
        if use_mock:
            return CustomerMockRepository()  # Retorna implementação mock
        else:
            return CustomerDBRepository()    # Retorna implementação real
```

#### Por que é útil?
- **Flexibilidade**: Podemos alternar entre diferentes implementações facilmente
- **Configuração Centralizada**: Um só lugar para decidir qual implementação usar
- **Facilita Testes**: Podemos usar mocks durante testes e implementações reais em produção

### 3.2 Adapter Pattern (Padrão Adaptador)

#### O que é?
O Adapter Pattern permite que interfaces incompatíveis trabalhem juntas. É como um adaptador de tomada que permite conectar um plugue americano numa tomada brasileira.

#### Como usamos no projeto:
```python
# Interface que define o "contrato"
class CustomerRepositoryInterface(ABC):
    @abstractmethod
    async def get_customer_by_id(self, customer_id: int) -> Optional[CostumerModel]:
        pass

# Implementações diferentes que seguem o mesmo "contrato"
class CustomerMockRepository(CustomerRepositoryInterface):  # Para desenvolvimento/teste
class CustomerDBRepository(CustomerRepositoryInterface):    # Para produção
```

#### Por que é útil?
- **Intercambiabilidade**: Podemos trocar implementações sem mudar o código que as usa
- **Isolamento**: A lógica de negócio não precisa saber se os dados vêm de um mock ou banco real
- **Testabilidade**: Facilita a criação de mocks para testes

### 3.3 Dependency Injection (Injeção de Dependência)

#### O que é?
É um padrão onde um objeto recebe suas dependências de uma fonte externa, ao invés de criar essas dependências internamente.

#### Como usamos no projeto:
```python
# Sem injeção de dependência (ruim):
async def get_customer(customer_id: int):
    repository = CustomerMockRepository()  # ← Dependência "hard-coded"
    return await repository.get_customer_by_id(customer_id)

# Com injeção de dependência (bom):
async def get_customer(
    customer_id: int,
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)  # ← Injetada
):
    return await repository.get_customer_by_id(customer_id)
```

#### Por que é útil?
- **Flexibilidade**: Podemos usar diferentes implementações sem mudar o código
- **Testabilidade**: Facilita a injeção de mocks durante testes
- **Desacoplamento**: Reduz a dependência entre componentes

---

## 4. Tecnologias e Bibliotecas

### 4.1 FastAPI

#### O que é?
FastAPI é um framework web moderno e rápido para construir APIs com Python, baseado em type hints.

#### Funções e recursos utilizados:

##### `FastAPI()`
```python
app = FastAPI(title="SecureTransfer API", version="1.0.0")
```
- **O que faz**: Cria a instância principal da aplicação
- **Parâmetros**:
  - `title`: Nome da API (aparece na documentação)
  - `version`: Versão da API (para controle de versionamento)

##### `APIRouter()`
```python
router = APIRouter()
```
- **O que faz**: Cria um grupo de rotas que podem ser incluídas na aplicação principal
- **Por que usar**: Organiza endpoints relacionados em módulos separados

##### `Depends()`
```python
repository: CustomerRepositoryInterface = Depends(get_customer_repository)
```
- **O que faz**: Sistema de injeção de dependências do FastAPI
- **Como funciona**: Executa a função `get_customer_repository()` e injeta o resultado no parâmetro
- **Vantagens**: Reutilização, testabilidade, organização

##### `HTTPException()`
```python
raise HTTPException(status_code=404, detail="Cliente não encontrado")
```
- **O que faz**: Levanta uma exceção HTTP que será convertida em resposta de erro
- **Parâmetros**:
  - `status_code`: Código HTTP (404 = Not Found)
  - `detail`: Mensagem de erro para o cliente

##### Decorators de Rotas:
```python
@router.get("/", response_model=List[CustomerPublic])
@router.post("/{customer_id}/activate", response_model=CustomerPublic)
```
- **@router.get()**: Define um endpoint que responde a requisições GET
- **@router.post()**: Define um endpoint que responde a requisições POST
- **`response_model`**: Define o schema de resposta (validação e documentação automática)

### 4.2 Pydantic

#### O que é?
Biblioteca para validação de dados usando type hints do Python.

#### Como usamos:
```python
class CustomerPublic(BaseModel):
    id: int
    full_name: str
    birthday: date
    is_active: bool
```

#### Benefícios:
- **Validação Automática**: Garante que os dados estão no formato correto
- **Serialização**: Converte objetos Python em JSON automaticamente
- **Documentação**: Gera documentação da API automaticamente

### 4.3 SQLAlchemy

#### O que é?
ORM (Object-Relational Mapping) que permite trabalhar com banco de dados usando objetos Python.

#### Recursos utilizados:

##### `sa.Column()`
```python
id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
name = sa.Column(sa.String(255), nullable=False)
```
- **O que faz**: Define uma coluna na tabela do banco de dados
- **Tipos**: `sa.Integer`, `sa.String()`, `sa.Boolean`, `sa.Date`, etc.
- **Parâmetros**: `primary_key`, `nullable`, `unique`, `default`, etc.

##### `sa.func.now()`
```python
created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
```
- **O que faz**: Função que retorna a data/hora atual do servidor de banco
- **Uso**: Timestamps automáticos de criação e atualização

### 4.4 Python Standard Library

#### `ABC` (Abstract Base Class)
```python
from abc import ABC, abstractmethod

class CustomerRepositoryInterface(ABC):
    @abstractmethod
    async def get_customer_by_id(self, customer_id: int):
        pass
```
- **O que é**: Classe base abstrata que define interfaces
- **@abstractmethod**: Força classes filhas a implementar o método
- **Por que usar**: Garante que todas as implementações sigam o mesmo contrato

#### `os.getenv()`
```python
use_mock = os.getenv("USE_MOCK_DB", "true").lower() == "true"
```
- **O que faz**: Lê variáveis de ambiente do sistema
- **Parâmetros**: Nome da variável e valor padrão
- **Uso**: Configuração da aplicação sem hard-coding

#### `typing`
```python
from typing import List, Optional
```
- **List[CustomerPublic]**: Lista de objetos CustomerPublic
- **Optional[Customer]**: Pode retornar Customer ou None
- **Por que usar**: Type hints melhoram legibilidade e permitem detecção de erros

---

## 5. Estrutura de Diretórios

```
SecureTransferAPI/
├── app/
│   ├── __init__.py                    # Torna 'app' um pacote Python
│   ├── main.py                        # Ponto de entrada da aplicação
│   │
│   ├── models/                        # Modelos de dados (Entities)
│   │   ├── __init__.py
│   │   ├── customer_model.py          # Modelo do cliente
│   │   └── bank_model.py              # Modelo do banco
│   │
│   ├── domain/                        # Camada de domínio
│   │   ├── __init__.py
│   │   └── schemas/                   # Schemas Pydantic (DTOs)
│   │       ├── __init__.py
│   │       └── customer_schema.py     # Schemas de entrada/saída
│   │
│   ├── adapters/                      # Padrão Adapter
│   │   ├── __init__.py
│   │   ├── customer_repository_interface.py  # Interface abstrata
│   │   └── repository_factory.py      # Factory para repositórios
│   │
│   ├── db/                           # Camada de dados
│   │   ├── __init__.py
│   │   └── mock/                     # Implementações mock
│   │       ├── __init__.py
│   │       └── customer_mock_repository.py
│   │
│   └── api/                          # Camada de apresentação
│       ├── __init__.py
│       └── v1/                       # Versionamento da API
│           ├── __init__.py
│           └── customer.py           # Endpoints de clientes
│
├── .env.example                      # Exemplo de variáveis de ambiente
├── .gitignore                        # Arquivos ignorados pelo Git
├── requirements.txt                  # Dependências Python
├── README.md                         # Documentação do projeto
└── Teoria.md                         # Este arquivo!
```

### Por que essa estrutura?

1. **Separação por Responsabilidade**: Cada diretório tem uma responsabilidade específica
2. **Escalabilidade**: Fácil adicionar novos módulos sem bagunça
3. **Testabilidade**: Cada componente pode ser testado isoladamente
4. **Manutenibilidade**: Mudanças ficam localizadas em áreas específicas

---

## 6. Componentes do Sistema

### 6.1 Models (Modelos de Dados)

#### O que são?
Representam as entidades do domínio e sua estrutura no banco de dados.

```python
class CostumerModel(Base):
    __tablename__ = 'costumers'
    
    id = sa.Column(sa.Integer, primary_key=True)
    cpf = sa.Column(sa.String(14), nullable=False)
    # ... outros campos
```

#### Responsabilidades:
- Definir estrutura das tabelas
- Estabelecer relacionamentos
- Validações básicas de dados

### 6.2 Schemas (Esquemas de Dados)

#### O que são?
Definem como os dados entram e saem da API, usando Pydantic.

```python
class CustomerPublic(BaseModel):  # Para dados públicos
    id: int
    full_name: str
    is_active: bool

class CustomerPrivate(CustomerPublic):  # Para dados sensíveis
    cpf: str
    email: str
    balance: float
```

#### Por que dois schemas?
- **CustomerPublic**: Para endpoints públicos (sem dados sensíveis)
- **CustomerPrivate**: Para endpoints administrativos (com dados completos)

### 6.3 Repository Interface (Interface de Repositório)

#### O que é?
Define o "contrato" que todas as implementações de repositório devem seguir.

```python
class CustomerRepositoryInterface(ABC):
    @abstractmethod
    async def get_customer_by_id(self, customer_id: int) -> Optional[CostumerModel]:
        pass
    
    @abstractmethod
    async def create_customer(self, customer_data: dict) -> CostumerModel:
        pass
```

#### Por que usar?
- **Padronização**: Todas as implementações têm os mesmos métodos
- **Intercambiabilidade**: Podemos trocar implementações facilmente
- **Testabilidade**: Facilita criação de mocks

### 6.4 Mock Repository (Repositório Mock)

#### O que é?
Implementação fake que armazena dados em memória, útil para desenvolvimento e testes.

```python
class CustomerMockRepository(CustomerRepositoryInterface):
    def __init__(self):
        self._customers = [
            # Dados mockados pré-definidos
        ]
    
    async def get_customer_by_id(self, customer_id: int):
        return next((c for c in self._customers if c.id == customer_id), None)
```

#### Vantagens:
- **Rapidez**: Não precisa de banco de dados
- **Previsibilidade**: Dados controlados para testes
- **Simplicidade**: Não requer configuração externa

### 6.5 Factory (Fábrica)

#### Como funciona no projeto:
```python
class RepositoryFactory:
    @staticmethod
    def create_customer_repository() -> CustomerRepositoryInterface:
        use_mock = os.getenv("USE_MOCK_DB", "true").lower() == "true"
        
        if use_mock:
            return CustomerMockRepository()
        else:
            return CustomerDBRepository()  # Implementação real (futura)
```

#### Controle por Variável de Ambiente:
- `USE_MOCK_DB=true` → Usa dados mockados
- `USE_MOCK_DB=false` → Usa banco de dados real

### 6.6 API Endpoints (Pontos de Acesso da API)

#### Estrutura típica de um endpoint:
```python
@router.get("/{customer_id}", response_model=CustomerPublic)
async def get_customer(
    customer_id: int,  # ← Parâmetro da URL
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)  # ← Dependência
):
    customer = await repository.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer  # ← Automaticamente convertido para JSON
```

#### O que acontece quando alguém chama a API:
1. **Recebimento**: FastAPI recebe a requisição HTTP
2. **Validação**: Valida parâmetros da URL e corpo da requisição
3. **Injeção**: Injeta as dependências (repository)
4. **Execução**: Executa a lógica do endpoint
5. **Serialização**: Converte o resultado para JSON
6. **Resposta**: Retorna a resposta HTTP

---

## 7. Fluxo de Dados

### Exemplo: Buscar um cliente por ID

```
1. Cliente HTTP                    2. FastAPI Router
   GET /api/v1/customers/1   →        @router.get("/{customer_id}")
                                           ↓
6. Resposta JSON              5. CustomerPublic Schema
   {"id": 1, "name": "João"}  ←     (serialização automática)
                                           ↑
                              4. CostumerModel
                                 (objeto Python)
                                           ↑
                              3. Repository
                                 get_customer_by_id(1)
```

### Passos detalhados:

1. **Requisição HTTP**: Cliente faz GET `/api/v1/customers/1`
2. **Roteamento**: FastAPI identifica o endpoint correto
3. **Injeção**: `Depends()` injeta o repositório configurado
4. **Busca**: Repositório busca o cliente (mock ou banco real)
5. **Validação**: Pydantic valida e serializa a resposta
6. **Resposta**: JSON é retornado para o cliente

---

## 8. Como Tudo se Conecta

### 8.1 Inicialização da Aplicação

```python
# main.py
app = FastAPI(title="SecureTransfer API", version="1.0.0")
app.include_router(customer.router, prefix="/api/v1/customers", tags=["customers"])
```

### 8.2 Configuração de Ambiente

```python
# .env
USE_MOCK_DB=true  # Usa mock para desenvolvimento
```

### 8.3 Factory Decision

```python
# repository_factory.py
use_mock = os.getenv("USE_MOCK_DB", "true").lower() == "true"
if use_mock:
    return CustomerMockRepository()  # ← Retorna implementação mock
```

### 8.4 Dependency Injection

```python
# customer.py (endpoint)
repository: CustomerRepositoryInterface = Depends(get_customer_repository)
# ↑ FastAPI automaticamente chama get_customer_repository() e injeta o resultado
```

### 8.5 Execução

```python
customer = await repository.get_customer_by_id(customer_id)
# ↑ Chama o método da implementação atual (mock ou real)
```

---

## Vantagens desta Arquitetura

### 1. **Flexibilidade**
- Podemos trocar de mock para banco real mudando apenas uma variável
- Podemos adicionar novas implementações (Redis, MongoDB, etc.) facilmente

### 2. **Testabilidade**
- Cada componente pode ser testado isoladamente
- Mocks facilitam testes rápidos e previsíveis

### 3. **Manutenibilidade**
- Código organizado em camadas bem definidas
- Mudanças ficam localizadas em áreas específicas
- Fácil de entender e modificar

### 4. **Escalabilidade**
- Estrutura permite crescimento sem refatoração major
- Novos recursos seguem os mesmos padrões

### 5. **Segurança**
- Separação entre dados públicos e privados
- Controle granular de acesso a informações sensíveis

---

## Próximos Passos

Para expandir este projeto, você pode:

1. **Implementar Repository Real**: Criar `CustomerDBRepository` que usa PostgreSQL
2. **Adicionar Autenticação**: Implementar JWT para proteger endpoints sensíveis
3. **Criar Testes**: Escrever testes unitários e de integração
4. **Adicionar Logging**: Implementar sistema de logs
5. **Cache**: Adicionar cache Redis para performance
6. **Validações**: Implementar validações mais complexas de CPF, etc.
7. **Documentação**: Expandir documentação da API

---

**Lembre-se**: Esta arquitetura pode parecer "over-engineered" para um projeto simples, mas ela brilha quando o sistema cresce. É melhor começar com uma base sólida do que refatorar tudo depois!