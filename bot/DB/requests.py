#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bot.DB.models import async_session
from bot.DB.models import Task
from sqlalchemy import select, delete, update


# добавление задачи в БД
async def add_task(task, user_id, task_number):
    async with async_session() as session:
        user_task = await session.scalar(select(Task).where(Task.user_id == user_id))

        if not user_task:
            session.add(Task(user_id=user_id, task=task, task_number=1))
            await session.commit()
            return

        session.add(Task(user_id=user_id, task=task, task_number=task_number))
        await session.commit()

# Проверка последнего номера задачи из списка задач пользователя в БД


async def check_task_number(user_id):
    async with async_session() as session:
        user_tasks = await session.scalar(select(Task).where(Task.user_id == user_id))
        user_tasks_list = await session.execute(select(Task).where(Task.user_id == user_id))
        tasks_list = user_tasks_list.scalars().all()
        task_numbers_list = []
        if user_tasks == None:
            return 0

        for task in tasks_list:
            task_number = task.task_number

            if task_number == None:
                continue

            task_number = int(task.task_number)
            task_numbers_list.append(task_number)

        last_task_number = max(task_numbers_list)

        return last_task_number

# формирование списка задач пользователя из БД


async def show_user_tasks(user_id):
    async with async_session() as session:
        user_tasks_test = await session.scalar(select(Task).where(Task.user_id == user_id))
        user_tasks = await session.execute(select(Task).where(Task.user_id == user_id))
        if user_tasks_test is None:
            msg = "Вы не добавили ни одной задачи!"
            return msg

        tasks_list = user_tasks.scalars().all()
        msg = "Ваши задачи:\n\n"
        for task in tasks_list:
            msg += f"Номер задачи: {task.task_number}\nЗадача: {task.task}\n\n"

        return msg

# удаление задачи пользователя из БД


async def delete_task(user_id, task_number):
    task_number = int(task_number)
    async with async_session() as session:
        user_task = await session.scalar(select(Task).where(Task.task_number == task_number).where(Task.user_id == user_id))

        if not user_task:
            msg = "У вас нет задачи с таким номером!"
            return msg

        await session.delete(user_task)
        msg = "Задача была успешно удалена!"
        await session.commit()

        return msg

# Изменениие задачи пользователя в БД


async def update_task(user_id, task_number, updated_task):
    async with async_session() as session:
        user_task = await session.scalar(select(Task).where(Task.task_number == task_number).where(Task.user_id == user_id))
        if not user_task:
            msg = "У вас нет задачи с таким номером!"
            return msg

        await session.execute(update(Task).where(Task.task_number == task_number).where(Task.user_id == user_id), {"task": updated_task})
        await session.commit()
        msg = "Ваша задача была изменена!"
        return msg
