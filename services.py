from aiogram import types
import re

from utils import create_logger
from settings import MessagesAnswear


logger = create_logger('Message operations')


async def check_message(message: types.Message):
    """Проверяет сообщения на наличие ссылок и не английских слов"""
    if _messages_with_links(message):
        logger.info('Удалено сообщение содержащие ссылку')
        return {'deleted': True, 'message': MessagesAnswear.message_with_link_answear}

    if _messages_without_english_words(message):
        logger.info('Удалено сообщение не содержащие английские слова')
        return {'deleted': True, 'message': MessagesAnswear.message_without_english}

    return {'deleted': False}


def _messages_with_links(message: types.Message) -> bool:
    """Проверяет наличие в сообщении ссылки"""
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            return True
    return False


def _messages_without_english_words(message: types.Message) -> bool:
    """Проверяет наличие в сообщении не английских слов"""
    message = re.sub(r'[\W_]+', '', message['text'])
    return len(re.findall(r'[^a-zA-Z0-9]', message)) > 0