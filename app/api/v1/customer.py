from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.adapters.repository_factory import get_customer_repository
from app.domain.adapters.customer_repository_interface import CustomerRepositoryInterface
from app.domain.schemas.customer_schema import CustomerPrivate, CustomerPublic


router = APIRouter()


@router.get("/", response_model=List[CustomerPublic])
async def get_customers(
    skip: int = 0, 
    limit: int = 100,
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)
):
    """Lista todos os clientes (dados públicos)"""
    customers = await repository.get_all_customers(skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=CustomerPublic)
async def get_customer(
    customer_id: int,
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)
):
    """Busca um cliente por ID (dados públicos)"""
    customer = await repository.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.get("/{customer_id}/private", response_model=CustomerPrivate)
async def get_customer_private(
    customer_id: int,
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)
):
    """Busca um cliente por ID (dados privados - requer autenticação)"""
    customer = await repository.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.post("/{customer_id}/activate", response_model=CustomerPublic)
async def activate_customer(
    customer_id: int,
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)
):
    """Ativa um cliente"""
    customer = await repository.activate_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.post("/{customer_id}/deactivate", response_model=CustomerPublic)
async def deactivate_customer(
    customer_id: int,
    repository: CustomerRepositoryInterface = Depends(get_customer_repository)
):
    """Desativa um cliente"""
    customer = await repository.deactivate_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer