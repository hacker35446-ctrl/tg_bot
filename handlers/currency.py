import requests
from aiogram import Router, types
from config import EXCHANGE_KEY

router = Router()

@router.callback_query(lambda c: c.data == "currency")
async def currency_handler(callback: types.CallbackQuery):
    await callback.answer()
    try:
        resp = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/USD", timeout=10)
        data = resp.json()
        if resp.ok and "conversion_rates" in data and "KZT" in data["conversion_rates"]:
            rate = data["conversion_rates"]["KZT"]
            text = f"💵 Актуальный курс валют:\n1 USD = {rate} KZT"
        else:
            text = "Не удалось получить курс валют."
    except Exception:
        text = "Ошибка при запросе курса валют."
    await callback.message.answer(text)