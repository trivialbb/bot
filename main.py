from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "TOKEN"

# Вопросы сгруппированы по темам
QUESTIONS_BY_TOPIC = {
    "mechanics": [
        {
            "question": "Что такое инерция?",
            "options": [
                "Способность тела сохранять свою скорость",
                "Сила, действующая на тело",
                "Изменение скорости тела",
                "Энергия движения"
            ],
            "correct_answer": 0,
            "difficulty": "easy"
        },
        {
            "question": "Что характеризует ускорение свободного падения на Земле?",
            "options": ["9,8 м/с²", "6,67 м/с²", "3,14 м/с²", "10 м/с²"],
            "correct_answer": 0,
            "difficulty": "easy"
        },
        {
            "question": "Какой закон Ньютона гласит: 'Действию всегда есть равное и противоположное противодействие'?",
            "options": [
                "Первый закон Ньютона",
                "Второй закон Ньютона",
                "Третий закон Ньютона",
                "Закон всемирного тяготения"
            ],
            "correct_answer": 2,
            "difficulty": "medium"
        },
        {
            "question": "Что измеряется в ньютонах?",
            "options": ["Масса", "Сила", "Энергия", "Мощность"],
            "correct_answer": 1,
            "difficulty": "easy"
        },
        {
            "question": "Как называется траектория тела, брошенного под углом к горизонту?",
            "options": ["Окружность", "Парабола", "Гипербола", "Эллипс"],
            "correct_answer": 1,
            "difficulty": "medium"
        }
    ],
    "thermodynamics": [
        {
            "question": "Какой закон термодинамики гласит о сохранении энергии?",
            "options": [
                "Первый закон термодинамики",
                "Второй закон термодинамики",
                "Третий закон термодинамики",
                "Нулевой закон термодинамики"
            ],
            "correct_answer": 0,
            "difficulty": "medium"
        },
        {
            "question": "Как называется процесс передачи тепла без переноса вещества?",
            "options": ["Конвекция", "Теплопроводность", "Излучение", "Диффузия"],
            "correct_answer": 1,
            "difficulty": "medium"
        },
        {
            "question": "При каком процессе работа газа равна нулю?",
            "options": [
                "Изотермическом",
                "Изобарном",
                "Изохорном",
                "Адиабатном"
            ],
            "correct_answer": 2,
            "difficulty": "hard"
        }
    ],
    "electricity": [
        {
            "question": "Как называется единица измерения электрического сопротивления?",
            "options": ["Вольт", "Ампер", "Ом", "Ватт"],
            "correct_answer": 2,
            "difficulty": "easy"
        },
        {
            "question": "Какой прибор измеряет силу тока?",
            "options": ["Вольтметр", "Амперметр", "Омметр", "Ваттметр"],
            "correct_answer": 1,
            "difficulty": "easy"
        },
        {
            "question": "Как называется явление возникновения тока в замкнутом контуре при изменении магнитного потока?",
            "options": [
                "Электростатическая индукция",
                "Электромагнитная индукция",
                "Термоэлектронная эмиссия",
                "Фотоэффект"
            ],
            "correct_answer": 1,
            "difficulty": "hard"
        },
        {
            "question": "Какой закон описывает силу взаимодействия точечных зарядов?",
            "options": [
                "Закон Ома",
                "Закон Кулона",
                "Закон Фарадея",
                "Закон Джоуля-Ленца"
            ],
            "correct_answer": 1,
            "difficulty": "medium"
        }
    ],
    "optics": [
        {
            "question": "Как называется явление изменения направления света на границе двух сред?",
            "options": ["Дифракция", "Рефракция", "Интерференция", "Поляризация"],
            "correct_answer": 1,
            "difficulty": "medium"
        },
        {
            "question": "Какое явление объясняет радугу?",
            "options": [
                "Дифракция света",
                "Дисперсия света",
                "Интерференция света",
                "Поляризация света"
            ],
            "correct_answer": 1,
            "difficulty": "medium"
        },
        {
            "question": "Как называется точка, где собираются параллельные лучи после прохождения линзы?",
            "options": [
                "Центр линзы",
                "Оптический центр",
                "Фокус",
                "Главная плоскость"
            ],
            "correct_answer": 2,
            "difficulty": "hard"
        }
    ],
    "atomic": [
        {
            "question": "Как называется минимальная порция света?",
            "options": ["Электрон", "Фотон", "Протон", "Квант"],
            "correct_answer": 1,
            "difficulty": "medium"
        },
        {
            "question": "Кто открыл явление радиоактивности?",
            "options": [
                "Мария Кюри",
                "Анри Беккерель",
                "Эрнест Резерфорд",
                "Нильс Бор"
            ],
            "correct_answer": 1,
            "difficulty": "medium"
        }

    ]
}

# Для хранения состояния пользователей
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Предлагаем выбрать тему теста"""
    chat_id = update.effective_chat.id
    user_data[chat_id] = {"state": "choosing_topic"}

    keyboard = [
        [InlineKeyboardButton("Механика", callback_data="mechanics")],
        [InlineKeyboardButton("Термодинамика", callback_data="thermodynamics")],
        [InlineKeyboardButton("Электричество", callback_data="electricity")],
        [InlineKeyboardButton("Оптика", callback_data="optics")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выберите тему теста:",
        reply_markup=reply_markup
    )


async def handle_topic_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатываем выбор темы и начинаем тест"""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    topic = query.data

    user_data[chat_id] = {
        "topic": topic,
        "questions": QUESTIONS_BY_TOPIC[topic].copy(),
        "current_question": 0,
        "score": 0
    }

    await send_question(update, context)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляем текущий вопрос"""
    chat_id = update.effective_chat.id
    user_state = user_data[chat_id]

    if user_state["current_question"] < len(user_state["questions"]):
        question_data = user_state["questions"][user_state["current_question"]]
        keyboard = [
            [InlineKeyboardButton(option, callback_data=str(i))]
            for i, option in enumerate(question_data["options"])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = (f"Тема: {user_state['topic'].capitalize()}\n"
                f"Вопрос {user_state['current_question'] + 1}/{len(user_state['questions'])}:\n"
                f"{question_data['question']}")

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup
            )
    else:
        score = user_state["score"]
        total = len(user_state["questions"])
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Тест по теме '{user_state['topic']}' завершен!\nВаш результат: {score}/{total}"
        )
        del user_data[chat_id]


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатываем ответ пользователя"""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    user_state = user_data[chat_id]

    current_question = user_state["current_question"]
    selected_answer = int(query.data)
    correct_answer = user_state["questions"][current_question]["correct_answer"]

    if selected_answer == correct_answer:
        user_state["score"] += 1
        await query.answer("Правильно! ✅")
    else:
        correct_option = user_state["questions"][current_question]["options"][correct_answer]
        await query.answer(f"Неправильно! ❌ Правильный ответ: {correct_option}")

    user_state["current_question"] += 1
    await send_question(update, context)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        CallbackQueryHandler(handle_topic_choice, pattern="^(mechanics|thermodynamics|electricity|optics)$"))
    application.add_handler(CallbackQueryHandler(handle_answer))

    application.run_polling()


if __name__ == "__main__":
    main()
