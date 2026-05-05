import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Предопределённые цитаты
quotes = [
    {
        "text": "Жизнь — это 10% того, что с тобой происходит, и 90% того, как ты на это реагируешь.",
        "author": "Коко Шанель",
        "topic": "Мотивация"
    },
    {
        "text": "Самое большое путешествие — это путешествие внутри себя.",
        "author": "Руми",
        "topic": "Душевное развитие"
    },
    {
        "text": "Будущее зависит от того, что вы делаете сегодня.",
        "author": "Махатма Ганди",
        "topic": "Мотивация"
    },
    {
        "text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.",
        "author": "Нельсон Мандела",
        "topic": "Образование"
    }
]

HISTORY_FILE = 'history.json'

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение истории в файл
def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Глобальная переменная истории
history = load_history()

# Создаем окно
root = tk.Tk()
root.title("Random Quote Generator")

# Переменные для фильтров
filter_author_var = tk.StringVar()
filter_topic_var = tk.StringVar()

# Функция генерации случайной цитаты
def generate_quote():
    quote = random.choice(quotes)
    display_quote(quote)
    # Добавляем в историю
    history.append(quote)
    save_history(history)
    update_history_list()

# Вывод цитаты
def display_quote(quote):
    quote_text.delete(1.0, tk.END)
    quote_text.insert(tk.END, f'"{quote["text"]}"\n\n— {quote["author"]} ({quote["topic"]})')

# Обновление отображения истории
def update_history_list(filtered_list=None):
    listbox_history.delete(0, tk.END)
    display_list = filtered_list if filtered_list is not None else history
    for q in display_list:
        listbox_history.insert(tk.END, f'"{q["text"]}" — {q["author"]} ({q["topic"]})')

# Применение фильтров
def apply_filter():
    auth_filter = filter_author_var.get().lower()
    topic_filter = filter_topic_var.get().lower()
    filtered = [
        q for q in history
        if (auth_filter in q["author"].lower() if auth_filter else True) and
           (topic_filter in q["topic"].lower() if topic_filter else True)
    ]
    update_history_list(filtered)

# Создаём интерфейс
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Кнопка «Сгенерировать цитату»
btn_generate = tk.Button(frame, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(pady=5)

# Текстовое поле для отображения цитаты
quote_text = tk.Text(frame, height=4, wrap=tk.WORD)
quote_text.pack(pady=5)

# Поля для фильтров
filter_frame = tk.Frame(frame)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
entry_author = tk.Entry(filter_frame, textvariable=filter_author_var)
entry_author.grid(row=0, column=1)

tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2)
entry_topic = tk.Entry(filter_frame, textvariable=filter_topic_var)
entry_topic.grid(row=0, column=3)

btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5)

# Заголовок для истории
tk.Label(frame, text="История цитат:").pack()

# список истории
listbox_history = tk.Listbox(frame, width=80, height=10)
listbox_history.pack()

# Запуск интерфейса
update_history_list()
root.mainloop()
