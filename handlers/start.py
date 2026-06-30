from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🌤 Погода в Астане", callback_data="weather")
    keyboard.button(text="🤖 Режим ИИ", callback_data="ai_mode")
    keyboard.button(text="💵 Курс валют (KZT)", callback_data="currency")
    keyboard.button(text="⏳ Таймер на 1 минуту", callback_data="timer")
    keyboard.adjust(2)
    await message.answer(
        "Вас приветствует корпорация Kuertovv, выберите что хотите сделать",
        reply_markup=keyboard.as_markup()
    )