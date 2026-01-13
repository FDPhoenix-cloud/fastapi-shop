# routes/cart.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.database import get_async_session
from models.commerce import Cart, CartItem
from models.product import Product
from schemas.commerce import CartRead, CartItemCreate
from auth import current_active_user 

router = APIRouter()


async def get_or_create_cart(user_id: int, session: AsyncSession) -> Cart:
    result = await session.execute(
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )
    cart = result.scalar_one_or_none()
    if cart is None:
        cart = Cart(user_id=user_id)
        session.add(cart)
        await session.flush()
    return cart


@router.get("", response_model=CartRead)
async def get_cart(
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    cart = await get_or_create_cart(user.id, session)
    await session.commit()
    await session.refresh(cart)
    return cart

@router.post("/items", response_model=CartRead, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    payload: CartItemCreate,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    cart = await get_or_create_cart(user.id, session)

    product = await session.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if product.quantity < payload.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно товара на складе. Доступно: {product.quantity} шт.",
        )

    result = await session.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id, CartItem.product_id == product.id)
        .options(selectinload(CartItem.product))
    )
    cart_item = result.scalar_one_or_none()

    if cart_item:
        new_qty = cart_item.quantity + payload.quantity
        if new_qty > product.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя добавить столько товара. Доступно: {product.quantity} шт.",
            )
        cart_item.quantity = new_qty
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=payload.quantity,
        )
        session.add(cart_item)

    await session.commit()

    cart = await get_or_create_cart(user.id, session)
    await session.commit()
    await session.refresh(cart)
    return cart

@router.delete("/items/{item_id}", response_model=CartRead)
async def delete_item(
    item_id: int,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    cart = await get_or_create_cart(user.id, session)

    result = await session.execute(
        select(CartItem)
        .where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    )
    cart_item = result.scalar_one_or_none()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Позиция не найдена")

    await session.delete(cart_item)
    await session.commit()

    cart = await get_or_create_cart(user.id, session)
    await session.commit()
    await session.refresh(cart)
    return cart


@router.delete("", response_model=CartRead)
async def clear_cart(
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    cart = await get_or_create_cart(user.id, session)

    for item in list(cart.items):
        await session.delete(item)

    await session.commit()
    await session.refresh(cart)
    return cart
