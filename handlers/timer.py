import asyncio
from aiogram import Router, types, Bot

router = Router()

@router.callback_query(lambda c: c.data == "timer")
async def timer_handler(callback: types.CallbackQuery, bot: Bot):
    await callback.answer("Таймер запущен на 1 минуту.")
    asyncio.create_task(timer_finished(bot, callback.message.chat.id))

async def timer_finished(bot: Bot, chat_id):
    await asyncio.sleep(60)
    await bot.send_message(chat_id, "Таймер на 1 минуту завершен!")