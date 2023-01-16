from environs import Env

env = Env()
env.read_env()


API_TOKEN = env.str('TELEGRAM_API_TOKEN')
ADMINS_ID = env.list('TELEGRAM_ADMINS_IDS')

class MessagesAnswear:
    message_with_link_answear = 'Отправлять ссылки в чат НЕ администраторам ЗАПРЕЩЕНО!'
    message_without_english = 'В чате писать только на Английском языке!'