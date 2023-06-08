from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from add_functions import read_token_from_txt


API_TOKEN: str = read_token_from_txt()
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь!')


async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается'
                            'методом end_copy')


dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)
