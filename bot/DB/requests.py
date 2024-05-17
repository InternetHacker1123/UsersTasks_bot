from bot.DB.models import async_session
from bot.DB.models import Task
from sqlalchemy import select, delete, update


async def add_task(task, user_id, task_number):
    async with async_session() as session:
        user_task = await session.scalar(select(Task).where(Task.user_id == user_id))

        if not user_task:
            session.add(Task(user_id=user_id, task=task, task_number=1))
            await session.commit()
            return

        session.add(Task(user_id=user_id, task=task, task_number=task_number))
        await session.commit()


async def check_task_number(user_id):
    async with async_session() as session:
        user_tasks = await session.scalar(select(Task).where(Task.user_id == user_id))
        user_tasks_list = await session.execute(select(Task).where(Task.user_id == user_id))
        tasks_list = user_tasks_list.scalars().all()
        if user_tasks == None:
            return 0

        for task in tasks_list:
            task_number = task.task_number

            if task_number == None:
                continue

            task_numbers_list = []
            task_number = int(task.task_number)
            task_numbers_list.append(task_number)
            last_task_number = max(task_numbers_list)
            print(last_task_number)

        return last_task_number


async def show_user_tasks(user_id):
    async with async_session() as session:
        user_tasks = await session.execute(select(Task).where(Task.user_id == user_id))

        if user_tasks == None:
            msg = "Вы не добавили ни одной задачи!"
            return msg

        tasks_list = user_tasks.scalars().all()
        msg = "Ваши задачи:\n\n"

        for task in tasks_list:
            msg += f"Номер задачи: {task.task_number}\nЗадача: {task.task}\n\n"

        return msg


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


async def update_task(user_id, task_number, updated_task):
    async with async_session() as session:
        user_task = await session.scalar(select(Task).where(Task.task_number == task_number).where(Task.user_id == user_id))

        if not user_task:
            msg = "У вас нет задачи с таким номером!"
            return msg

        await session.scalar(update(Task).where(Task.task_number == task_number).where(Task.user_id == user_id), {"task": updated_task})
        await session.commit()
        msg = "Ваша задача была изменена!"
        return msg
