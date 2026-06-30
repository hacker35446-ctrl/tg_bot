import requests
from aiogram import Router, types, F

router = Router()


@router.message(F.text.regexp(r"^\d+$"))
async def numbers_handler(message: types.Message):
    try:
        resp = requests.get(f"http://numbersapi.com/{message.text.strip()}", timeout=10)
        if resp.ok:
            await message.answer(resp.text)
        else:
            await message.answer("Не удалось получить факт.")
    except Exception as e:
        print(f"NUMBERSAPI ERROR: {e}")
        await message.answer("Ошибка при запросе факта.")


@router.message(F.text & ~F.text.startswith("/"))
async def fallback_handler(message: types.Message):
    await message.answer("Напишите число, чтобы получить факт, или нажмите одну из кнопок меню.")