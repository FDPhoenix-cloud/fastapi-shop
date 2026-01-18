# routes/orders.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.database import get_async_session
from models.commerce import Cart, CartItem, Order, OrderItem
from models.product import Product
from schemas.commerce import OrderCreate, OrderRead
from auth import current_active_user
from utils.telegram import send_telegram_message  

router = APIRouter()

@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    background_tasks: BackgroundTasks,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    background_tasks.add_task(
        send_telegram_message,
        f"🆕 Новый заказ #{order.id}\n"
        f"Пользователь: {user.email}\n"
        f"Сумма: {order.total_amount} шмекелей\n"
        f"Адрес: {order.delivery_address}",
    )
    
    return order
