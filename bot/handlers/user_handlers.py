from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards import start_keyboard, menu_keyboard, add_task_keyboard, new_task_add_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    builder = await start_keyboard()
    await msg.answer(f'Привет, {msg.from_user.first_name}!\nЯ могу сохранять твои задачки!', reply_markup=builder.as_markup())


@router.message(Command("add"))
async def start_handler(msg: Message):
    user_task = msg.text[5:]
    await msg.answer(f'Твоя задача: "{user_task}" была добавлена!')


@router.message()
async def message_check(msg: Message, state: FSMContext):
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
        print(previous_message)


@router.callback_query(lambda callback: callback.data == 'help')
async def help(callback: types.CallbackQuery):
    builder = await menu_keyboard()
    await callback.message.edit_text("Я могу добавлять твои задачи в БД\nИ показывать их список.", reply_markup=builder.as_markup())


@router.callback_query(lambda callback: callback.data == 'menu')
async def menu(callback: types.CallbackQuery):
    builder = await start_keyboard()
    await callback.message.edit_text(f'Привет, {callback.message.chat.first_name}!\nЯ могу сохранять твои задачки!', reply_markup=builder.as_markup())


@router.callback_query(lambda callback: callback.data == 'addTask')
async def help(callback: types.CallbackQuery):
    builder = await add_task_keyboard()
    await callback.message.edit_text("Напиши задачу, которую хочешь добавить", reply_markup=builder.as_markup())


@router.callback_query(lambda callback: callback.data == 'confirm')
async def help(callback: types.CallbackQuery, state: FSMContext):
    builder = await add_task_keyboard()
    data = await state.get_data()
    previous_message = data.get("text")

    if (previous_message == None):
        await callback.answer()
        await callback.message.edit_text("Ты не написал задачу!", reply_markup=builder.as_markup())
        return

    builder = await new_task_add_keyboard()
    await callback.message.edit_text("Твоя задача была добавлена!", reply_markup=builder.as_markup())
