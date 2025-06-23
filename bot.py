import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

API_TOKEN = '7716387026:AAGTl7Crv_fDvQO4a5Wh38FX694aiG6vqTg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

WEB_APP_URL = 'https://web-production-2ad89.up.railway.app/'

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Web ilova", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer('Web ilovani ochish', reply_markup=markup)

async def handle_webhook(request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return web.Response()

async def on_startup(app, WEBHOOK_URL=None):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.session.close()

async def main():
    app = web.Application()
    app.router.add_post(f'/{API_TOKEN}', handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    WEBHOOK_HOST = 'https://www.youtube.com/channel/UCNJjauL4Q8crg7msVPW-R5g'
    WEBHOOK_PATH = f'/{API_TOKEN}'
    WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

    await dp.start_polling(bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
