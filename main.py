from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule
import asyncio

from utils import create_logger
from services import check_message
from settings import API_TOKEN, ADMINS_ID


logger = create_logger('Message handler')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

sended_messages = []


async def throtling_handler(*args, **kwargs):
    message = args[0]
    await message.delete()
    logger.info('Сообщение удалено из-за частой отправки')


@dp.message_handler()
@dp.throttled(throtling_handler, rate=1)
async def message_handler(message: types.Message):
    chat_id = message['chat']['id']
    username = message['from']['username']
    user_id = message['from']['id']

    if str(user_id) not in ADMINS_ID:
        answear = await check_message(message=message)

        if answear['deleted']:
            try:
                await message.delete()
            except Exception:
                logger.warning('Сообщение уже было удалено')

            message_id = await bot.send_message(chat_id, f'@{username} {answear["message"]}')
            message_id = message_id['message_id']
            sended_messages.append({'chat_id': chat_id, 'message_id': message_id})


@dp.message_handler(content_types = ['new_chat_members', 'left_chat_member'])
async def delete_system_messages(message: types.Message):
    """Удаляет сообщения о присоединении или удалнеии пользователя"""
    await message.delete()
    logger.info('Служебное сообщение удалено')


async def delete_sended_messages():
    """Удаляет отправленные сообщения ботом"""
    for message in sended_messages:
        try:
            await bot.delete_message(message['chat_id'], message['message_id'])
        except Exception:
            logger.warning('Сообщение уже было удалено')

    sended_messages.clear()
    logger.info('Список отправленных сообщений был очищен')


async def sheduler():
    """Устанавливает выполнение определенной задачи"""
    aioschedule.every(2).minutes.do(delete_sended_messages)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    await delete_sended_messages()
    asyncio.create_task(sheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
