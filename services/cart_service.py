# services/cart_service.py
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.commerce import Cart, CartItem
from models.product import Product
from schemas.commerce import CartItemCreate


async def get_or_create_cart_service(
    user_id: int,
    session: AsyncSession,
) -> Cart:
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


async def add_item_to_cart_service(
    user_id: int,
    payload: CartItemCreate,
    session: AsyncSession,
) -> Cart:
    cart = await get_or_create_cart_service(user_id, session)

    product = await session.get(Product, payload.product_id)
    if product is None:
        raise ValueError("Товар не найден")

    if product.quantity < payload.quantity:
        raise ValueError(f"Недостаточно товара на складе. Доступно: {product.quantity} шт.")

    result = await session.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id, CartItem.product_id == product.id)
        .options(selectinload(CartItem.product))
    )
    cart_item = result.scalar_one_or_none()

    if cart_item:
        new_qty = cart_item.quantity + payload.quantity
        if new_qty > product.quantity:
            raise ValueError(f"Нельзя добавить столько товара. Доступно: {product.quantity} шт.")
        cart_item.quantity = new_qty
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=payload.quantity,
        )
        session.add(cart_item)

    await session.commit()
    await session.refresh(cart)
    return cart


async def delete_cart_item_service(
    user_id: int,
    item_id: int,
    session: AsyncSession,
) -> Cart:
    cart = await get_or_create_cart_service(user_id, session)

    result = await session.execute(
        select(CartItem)
        .where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    )
    cart_item = result.scalar_one_or_none()
    if cart_item is None:
        raise ValueError("Позиция не найдена")

    await session.delete(cart_item)
    await session.commit()
    await session.refresh(cart)
    return cart


async def clear_cart_service(
    user_id: int,
    session: AsyncSession,
) -> Cart:
    cart = await get_or_create_cart_service(user_id, session)

    for item in list(cart.items):
        await session.delete(item)

    await session.commit()
    await session.refresh(cart)
    return cart
