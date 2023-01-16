from aiogram import types
import re
import logging

from utils import create_logger


logger = create_logger('Message operations')

async def check_messages(message: types.Message):
    """Проверяет сообщения на наличие ссылок и не английских слов"""
    if _messages_with_links(message):
        await message.delete()
        logger.info('Удалено сообщение содержащие ссылку')
        return {'deleted': True, 'message': 'Отправлять ссылки в чат НЕ администраторам ЗАПРЕЩЕНО!'}

    if _messages_without_english_words(message):
        await message.delete()
        logger.info('Удалено сообщение не содержащие английские слова')
        return {'deleted': True, 'message': 'В чате писать только на Английском языке!'}

    return {'deleted': False}


def _messages_with_links(message: types.Message) -> bool:
    """Проверяет наличие в сообщении ссылки"""
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            return True
    return False


def _messages_without_english_words(message: types.Message) -> bool:
    """Проверяет наличие в сообщении не английских слов"""
    string = message['text']
    string = string.translate(str.maketrans('','','[@_!#$%^&*()<>?/|}{~:],. '))

    if len(re.findall(r'[^a-zA-Z]', string)) > 0:
       return True
    return False