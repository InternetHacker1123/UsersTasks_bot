from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from bot.buttons.buttons import HELP_BUTTON, MENU_BUTTON, ADD_TASK_BUTTON, SHOW_TASKS_BUTTON, CONFIRM_TASK_BUTTON


async def start_keyboard():
    help_button_text = HELP_BUTTON.get("text")
    help_button_callback_data = HELP_BUTTON.get("callback_data")

    add_task_button_text = ADD_TASK_BUTTON.get("text")
    add_task_button_callback_data = ADD_TASK_BUTTON.get("callback_data")

    show_tasks_button_text = SHOW_TASKS_BUTTON.get("text")
    show_tasks_button_callback_data = SHOW_TASKS_BUTTON.get("callback_data")

    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text=help_button_text,
        callback_data=help_button_callback_data)
    )

    builder.add(types.InlineKeyboardButton(
        text=add_task_button_text,
        callback_data=add_task_button_callback_data)
    )

    builder.add(types.InlineKeyboardButton(
        text=show_tasks_button_text,
        callback_data=show_tasks_button_callback_data)
    )

    builder.adjust(1)

    return builder


async def add_task_keyboard():
    menu_button_text = MENU_BUTTON.get("text")
    menu_button_callback_data = MENU_BUTTON.get("callback_data")
    confirm_task_button_text = CONFIRM_TASK_BUTTON.get("text")
    confirm_task_button_callback = CONFIRM_TASK_BUTTON.get("callback_data")

    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text=menu_button_text,
        callback_data=menu_button_callback_data)
    )

    builder.add(types.InlineKeyboardButton(
        text=confirm_task_button_text,
        callback_data=confirm_task_button_callback)
    )

    builder.adjust(1)

    return builder


async def new_task_add_keyboard():
    menu_button_text = MENU_BUTTON.get("text")
    menu_button_callback_data = MENU_BUTTON.get("callback_data")
    add_task_button_text = ADD_TASK_BUTTON.get("text")
    add_task_button_callback_data = ADD_TASK_BUTTON.get("callback_data")

    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text=menu_button_text,
        callback_data=menu_button_callback_data)
    )

    builder.add(types.InlineKeyboardButton(
        text=add_task_button_text,
        callback_data=add_task_button_callback_data)
    )

    builder.adjust(1)

    return builder


async def menu_keyboard():
    menu_button_text = MENU_BUTTON.get("text")
    menu_button_callback_data = MENU_BUTTON.get("callback_data")

    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text=menu_button_text,
        callback_data=menu_button_callback_data)
    )

    return builder
