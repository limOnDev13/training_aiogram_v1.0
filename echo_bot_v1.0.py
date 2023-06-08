from aiogram import Bot, Dispatcher
# апдейты типа Message будут отлавливаться в эхо-боте
from aiogram.types import Message
# Этот модуль есть только в aiogram 3.x,
# а так как она еще в разработке, то нужно устанавливать через pip
# (можно прямо в консоли в PyCharm'e, нужно написать
# pip install -U --pre aiogram. Сам модуль необходим
# для фильтрации апдейтов по наличию в них команд.
from aiogram.filters import Command
from add_functions import read_token_from_txt


API_TOKEN: str = read_token_from_txt()
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь!')


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
