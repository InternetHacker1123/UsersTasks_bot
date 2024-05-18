#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import start_keyboard, menu_keyboard, add_task_keyboard, new_task_add_keyboard, delete_task_keyboard, delete_new_task_keyboard, update_task_keyboard, update_new_task_keyboard
from bot.DB.requests import add_task, check_task_number, delete_task, show_user_tasks, update_task

router = Router()

# обработчик команды /start


@router.message(Command("start"))
async def start_handler(msg: Message):
    builder = await start_keyboard()
    await msg.answer(f'Привет, {msg.from_user.first_name}!\nЯ бот, созданный для демонстрации навыков программирования на Python!', reply_markup=builder.as_markup())

# обработчик команды /add


@router.message(Command("add"))
async def add_handler(msg: Message):
    user_task = msg.text[5:]
    user_id = msg.from_user.id
    task_number = await check_task_number(user_id)
    await add_task(user_task, user_id, task_number+1)
    await msg.answer(f'Твоя задача: "{user_task}" была добавлена!')

# обработчик команды /tsk


@router.message(Command("tsk"))
async def show_user_tasks_cmd_handler(msg: Message):
    user_id = msg.from_user.id
    text = await show_user_tasks(user_id)
    await msg.answer(text)

# обработчик нажатия на кнопку "Показать задачи"


@router.callback_query(lambda callback: callback.data == 'showTasks')
async def show_user_tasks_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    msg = await show_user_tasks(user_id)
    await callback.answer()
    await callback.message.answer(msg)

# обработчик нажатия на кнопку "Изменить задачу"


@router.callback_query(lambda callback: callback.data == 'updateTask')
async def add_task_handler(callback: types.CallbackQuery):
    builder = await update_task_keyboard()
    await callback.message.edit_text("Напиши номер задачи, которую хочешь изменить и текст. Например: 1 купить хлеб", reply_markup=builder.as_markup())

# Обработчик всех поступающих сообщений от пользователя


@router.message()
async def message_check_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    previous_message = data.get("text")

    if (previous_message == None):
        await state.set_data({'text': msg.text})
        data = await state.get_data()
        previous_message = data.get("text")
    else:
        await state.set_data({'text': msg.text})
        data = await state.get_data()
        previous_message = data.get("text")

# обработчик нажатия на кнопку "функции бота"


@router.callback_query(lambda callback: callback.data == 'help')
async def help_handler(callback: types.CallbackQuery):
    builder = await menu_keyboard()
    await callback.message.edit_text("Этот бот может:\n-Добавлять задачи в БД\n-Удалять задачи из БД\n-Редактировать задачи\n-Выводить задачи из БД", reply_markup=builder.as_markup())

# обработчик нажатия на кнопку "в меню"


@router.callback_query(lambda callback: callback.data == 'menu')
async def menu_handler(callback: types.CallbackQuery):
    builder = await start_keyboard()
    await callback.message.edit_text(f'Привет, {callback.from_user.first_name}!\nЯ бот, созданный для демонстрации навыков программирования на Python!', reply_markup=builder.as_markup())

# обработчик нажатия на кнопку "Добавить задачу"


@router.callback_query(lambda callback: callback.data == 'addTask')
async def add_task_handler(callback: types.CallbackQuery):
    builder = await add_task_keyboard()
    await callback.message.edit_text("Напиши задачу, которую хочешь добавить", reply_markup=builder.as_markup())

# обработчик нажатия на кнопку "Удалить задчу"


@router.callback_query(lambda callback: callback.data == 'deleteTask')
async def delete_task_handler(callback: types.CallbackQuery):
    builder = await delete_task_keyboard()
    await callback.message.edit_text("Напиши номер задачи, которую хочешь удалить", reply_markup=builder.as_markup())

# обработчик нажатия на кнопку "Подтвердить" при удалении задачи


@router.callback_query(lambda callback: callback.data == 'confirmDelete')
async def confirm_delete_task_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_number = data.get("text")
    user_id = callback.from_user.id
    if (task_number == None):
        await callback.answer()
        await callback.message.edit_text("Ты не написал номер задачи!", reply_markup=builder.as_markup())
        return
    msg = await delete_task(user_id, task_number)
    builder = await delete_new_task_keyboard()
    await callback.message.edit_text(f"{msg}", reply_markup=builder.as_markup())

# обработчик нажатия на кнопку "Подтвердить" при добавлении задачи


@router.callback_query(lambda callback: callback.data == 'confirm')
async def confirm_add_task_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_task = data.get("text")
    user_id = callback.from_user.id

    if (user_task == None):
        await callback.answer()
        await callback.message.edit_text("Ты не написал задачу!", reply_markup=builder.as_markup())
        return
    task_number = await check_task_number(user_id)
    await add_task(user_task, user_id, task_number+1)

    builder = await new_task_add_keyboard()
    await callback.message.edit_text("Твоя задача была добавлена!", reply_markup=builder.as_markup())

# обработчик нажатия на кнопку "Подтвердить" при изменеии задачи


@router.callback_query(lambda callback: callback.data == 'confirmUpdate')
async def confirm_update_task_handler(callback: types.CallbackQuery, state: FSMContext):
    builder = await update_new_task_keyboard()
    data = await state.get_data()
    user_text = data.get("text")
    if (user_text is None or user_text == "" or len(user_text) < 3):
        await callback.answer()
        await callback.message.edit_text("Ты не написал задачу!", reply_markup=builder.as_markup())
        return
    task_number, updated_task = user_text.split(" ", 1)
    task_number = int(task_number)
    user_id = callback.from_user.id

    msg = await update_task(user_id, task_number, updated_task)

    await callback.message.edit_text(msg,  reply_markup=builder.as_markup())
