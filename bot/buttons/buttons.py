from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


HELP_BUTTON = {"text": "Функции бота", "callback_data": "help"}

ADD_TASK_BUTTON = {"text": "Добавить задачу", "callback_data": "addTask"}

SHOW_TASKS_BUTTON = {"text": "Показать задачи", "callback_data": "showTasks"}

MENU_BUTTON = {"text": "В меню", "callback_data": "menu"}

CONFIRM_TASK_BUTTON = {"text": "Подтвердить", "callback_data": "confirm"}
