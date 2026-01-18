# routes/cart.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from models.commerce import Cart
from schemas.commerce import CartRead, CartItemCreate
from auth import current_active_user

from services.cart_service import (
    get_or_create_cart_service,
    add_item_to_cart_service,
    delete_cart_item_service,
    clear_cart_service,
)

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartRead)
async def get_cart(
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    cart = await get_or_create_cart_service(user.id, session)
    return cart


@router.post("/items", response_model=CartRead, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    payload: CartItemCreate,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        cart = await add_item_to_cart_service(user.id, payload, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return cart


@router.delete("/items/{item_id}", response_model=CartRead)
async def delete_item(
    item_id: int,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        cart = await delete_cart_item_service(user.id, item_id, session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return cart


@router.delete("", response_model=CartRead)
async def clear_cart(
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    cart = await clear_cart_service(user.id, session)
    return cart
