import asyncio
import time
import requests
from datetime import datetime
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import GROQ_KEY

router = Router()

user_modes = {}
chat_history = {}


@router.callback_query(F.data == "ai_mode")
async def ai_mode_handler(callback: types.CallbackQuery):
    user_modes[callback.from_user.id] = "ai"
    chat_history[callback.from_user.id] = []

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔴 Выключить режим ИИ", callback_data="ai_mode_off")
    await callback.answer("Режим ИИ включен!")
    await callback.message.answer(
        "Режим ИИ включен! Пишите вопросы, я буду помнить наш диалог, пока вы не выключите режим.",
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data == "ai_mode_off")
async def ai_mode_off_handler(callback: types.CallbackQuery):
    user_modes[callback.from_user.id] = None
    chat_history.pop(callback.from_user.id, None)
    await callback.answer("Режим ИИ выключен!")
    await callback.message.answer("Режим ИИ выключен. История диалога очищена.")


async def ask_groq(user_id, text):
    chat_history.setdefault(user_id, [])
    chat_history[user_id].append({"role": "user", "content": text})

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history[user_id]
    }
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_KEY}"}

    response_text = "Ошибка при запросе к AI."
    for attempt in range(2):
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending request to Groq API (attempt {attempt + 1})...")
            resp = requests.post(url, json=payload, headers=headers, timeout=60)
            print(f"Groq API Response Status: {resp.status_code}")

            if resp.status_code == 200:
                data = resp.json()
                try:
                    response_text = data['choices'][0]['message']['content']
                    chat_history[user_id].append({"role": "assistant", "content": response_text})
                except (KeyError, IndexError) as parse_err:
                    print(f"Groq API parsing error: {parse_err}. Response body: {resp.text}")
                    response_text = "Не удалось получить ответ, попробуйте переформулировать вопрос."
                break
            elif resp.status_code == 429:
                print(f"Groq API Error 429: {resp.text}")
                if attempt == 0:
                    time.sleep(5)
                    continue
                else:
                    response_text = "Слишком много запросов, подождите немного и попробуйте снова."
            else:
                print(f"Groq API Error {resp.status_code}: {resp.text}")
                response_text = "Ошибка при запросе к AI."
                break
        except requests.RequestException as e:
            print(f"AI Connection/Timeout error on attempt {attempt + 1}/2: {e}")
            if attempt == 1:
                response_text = "Ошибка при запросе к AI."
            else:
                await asyncio.sleep(1)

    return response_text


@router.message(F.text & ~F.text.startswith("/"))
async def ai_message_handler(message: types.Message):
    user_id = message.from_user.id
    if user_modes.get(user_id) != "ai":
        return

    response_text = await ask_groq(user_id, message.text)

    try:
        if len(response_text) > 4000:
            for i in range(0, len(response_text), 4000):
                await message.answer(response_text[i:i+4000])
        else:
            await message.answer(response_text)
    except Exception as e:
        print(f"ERROR sending AI response: {e}")
        await message.answer("Произошла ошибка при отправке сообщения.")