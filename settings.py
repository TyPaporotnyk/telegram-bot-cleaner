from environs import Env

env = Env()
env.read_env()


API_TOKEN = env.str('TELEGRAM_API_TOKEN')
ADMINS_ID = env.list('TELEGRAM_ADMINS_IDS')

class MessagesAnswear:
    message_with_link_answear = 'Hey, little douchebag! Did you want to scam our precious members? No way! Scam resist has been activated!'
    message_without_english = 'Listen, buddy! You ain\'t gonna talk shit here in your mother tongue! Either use English or we\'ll call your mommy, she\'s on the speed dial!'