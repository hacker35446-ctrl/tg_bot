import requests
from aiogram import Router, types
from config import КЛЮЧ_ПОГОДЫ

router = Router()

@router.callback_query(lambda c: c.data == "weather")
async def weather_handler(callback: types.CallbackQuery):
    await callback.answer()
    try:
        params = {"q": "Astana", "appid": КЛЮЧ_ПОГОДЫ, "units": "metric", "lang": "ru"}
        resp = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        data = resp.json()
        if resp.ok and "main" in data:
            text = f"Погода в Астане: {data['weather'][0]['description'].capitalize()}, температура {data['main']['temp']}°C"
        else:
            text = "Не удалось получить данные о погоде."
    except Exception:
        text = "Ошибка при запросе погоды."
    await callback.message.answer(text)