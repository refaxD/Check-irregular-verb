import asyncio
import logging
import random
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

IRREGULAR_VERBS = {
    "be": "was were been",  # Тут сложно, но допустим так
    "become": "became become",
    "begin": "began begun",
    "break": "broke broken",
    "bring": "brought brought",
    "buy": "bought bought",
    "catch": "caught caught",
    "choose": "chose chosen",
    "come": "came come",
    "do": "did done",
    "drink": "drank drunk",
    "drive": "drove driven",
    "eat": "ate eaten",
    "fall": "fell fallen",
    "feel": "felt felt",
    "find": "found found",
    "fly": "flew flown",
    "forget": "forgot forgotten",
    "get": "got got",
    "give": "gave given",
    "go": "went gone",
    "have": "had had",
    "hear": "heard heard",
    "know": "knew known",
    "leave": "left left",
    "lose": "lost lost",
    "make": "made made",
    "meet": "met met",
    "pay": "paid paid",
    "put": "put put",
    "read": "read read",
    "run": "ran run",
    "say": "said said",
    "see": "saw seen",
    "sell": "sold sold",
    "send": "sent sent",
    "sing": "sang sung",
    "sit": "sat sat",
    "sleep": "slept slept",
    "speak": "spoke spoken",
    "stand": "stood stood",
    "swim": "swam swum",
    "take": "took taken",
    "teach": "taught taught",
    "tell": "told told",
    "think": "thought thought",
    "understand": "understood understood",
    "wear": "wore worn",
    "write": "wrote written"
}

# Просто буллинг
INSULTS = [
    "Ты вообще в школе учился? 🗿",
    "Позорище...",
    "Удали телеграм и иди учи уроки, школьник",
    "Мда... IQ как у завалявшейся плесени",
    "Неправильно! Ты опять ты несёшь дичь",
    "Хватит тыкать наугад, бездарь!",
    "Это фиаско, братан",
    "Стыд и срам",
    "Ты пытаешься меня разозлить или ты правда такой?",
    "Опять мимо, бездарность"
]

# Похвала с буллингом
PRAISES = [
    "Ну наконец-то. Давай дальше.",
    "Повезло, угадал.",
    "Ладно, сойдет. Следующий.",
    "Не прошло и года. Едем дальше.",
    "Правильно. Но не зазнавайся."
]

class QuizState(StatesGroup):
    waiting_for_answer = State()

async def ask_new_verb(message: types.Message, state: FSMContext):
    """Выбирает случайный глагол и задает вопрос"""
    verb, forms = random.choice(list(IRREGULAR_VERBS.items()))

    # Сохраняем правильный ответ в память состояния
    await state.update_data(verb=verb, correct_answer=forms)

    await message.answer(
        f"🤬 <b>Глагол:</b> <code>{verb}</code>\n\nПиши 2-ю и 3-ю формы через пробел (например: <i>went gone</i>):",
        parse_mode="HTML")
    await state.set_state(QuizState.waiting_for_answer)


# ручки \/

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет, неуч! 🤡\n"
        "Будем проверять твои знания неправильных глаголов\n"
        "За каждую ошибку я буду  бить тебя по лицу морально\n"
        "Готов? Погнали."
    )
    await ask_new_verb(message, state)


@dp.message(QuizState.waiting_for_answer)
async def process_answer(message: types.Message, state: FSMContext):
    user_answer = message.text.lower().strip()
    user_answer = " ".join(user_answer.split())

    data = await state.get_data()
    correct_answer = data['correct_answer']
    verb = data['verb']

    if user_answer == correct_answer:
        praise = random.choice(PRAISES)
        await message.answer(f"✅ {praise}")
        await ask_new_verb(message, state)
    else:
        insult = random.choice(INSULTS)
        await message.answer(
            f"❌ <b>{insult}</b>\n\n"
            f"Глагол: <b>{verb}</b>\n"
            f"Ты написал: <s>{user_answer}</s>\n"
            f"Правильно: <b>{correct_answer}</b>\n\n"
            f"Попробуй не опозорится на следующем глаголе:",
            parse_mode="HTML"
        )
        await ask_new_verb(message, state)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")