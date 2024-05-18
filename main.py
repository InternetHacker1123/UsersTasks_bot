#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from bot.handlers.user_handlers import router
from bot.DB.models import async_main


async def main() -> None:
    load_dotenv('.env')
    await async_main()
    token = os.getenv("BOT_TOKEN")
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f'Exception - {_ex}')

if __name__ == "__main__":
    asyncio.run(main())
