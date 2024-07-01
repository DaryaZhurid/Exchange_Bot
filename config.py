from dotenv import dotenv_values

env_keys = dotenv_values()
TELEGRAM_TOKEN = env_keys.get("TELEGRAM_TOKEN")
keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'

}
