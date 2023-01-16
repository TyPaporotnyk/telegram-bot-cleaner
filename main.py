from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils import create_logger
from services import check_message
from settings import API_TOKEN, ADMINS_ID


logger = create_logger('Message handler')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


async def throtling_handler(*args, **kwargs):
    message = args[0]
    await message.delete()
    logger.info('Сообщение удалено из-за частой отправки')


@dp.message_handler()
@dp.throttled(throtling_handler, rate=1)
async def message_handler(message: types.Message):
    chat_id = message['chat']['id']
    username = message['from']['username']

    if message['from']['id'] not in ADMINS_ID:
        answear = await check_message(message=message)

        if answear['deleted']:
            await bot.send_message(chat_id, f'@{username} {answear["message"]}')
    else:
        await bot.send_message(chat_id, f'{message}')


@dp.message_handler(content_types = ['new_chat_members', 'left_chat_member'])
async def delete_system_messages(message: types.Message):
    """Удаляет сообщения о присоединении или удалнеии пользователя"""
    await message.delete()
    logger.info('Служебное сообщение удалено')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
