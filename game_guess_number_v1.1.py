import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from add_functions import read_token_from_txt


BOT_TOKEN: str = read_token_from_txt()
ATTEMPTS: int = 10


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()
users: dict = {}


def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет! Давай сыграем в игру '
                         '"Угадай число"?\nЕсли хочешь узнать правила '
                         'отправь команду /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Правила весьма простые: \n\nЯ загадываю натуральное число от 1 до 100'
                         f', а твоя задача за {ATTEMPTS} попыток угадать это число.\n'
                         'Присылай мне любое натуральное число от 1 до 100, а я буду отвечать,'
                         ' мое число '
                         'больше, меньше или равно твоему.\nСможешь угадать за отведенное'
                         ' количество попыток - '
                         "ты победил, не уложишься - проиграл. Все просто:)\nТакже"
                         " ты можешь отправить команду "
                         '/cancel, чтобы отменить текущую игру; и /stat,'
                         ' чтобы посмотреть свою статистику.\n'
                         'Ну что, хочешь сыграть?')


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Количество проведенных игр: {users[message.from_user.id]["total_games"]}\n'
                         f'Количество побед: {users[message.from_user.id]["wins"]}')


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Завершаю текущую игру. Если захочешь еще разок сыграть, напиши мне.')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Мы и так с вами не играем. Может, сыграем разок?')


@dp.message(Text(text=['Да', "Давай", "Еще бы", "Погнали", "Поехали"], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['attempts'] = ATTEMPTS
        users[message.from_user.id]['secret_number'] = get_random_number()
        await message.answer(f'Ура! Я загадал число от 1 до 100. Сейчас у тебя осталось '
                             f'{users[message.from_user.id]["attempts"]}'
                             f' попыток(ки)(ка).\n'
                             f'Какое число я загадал?')
        users[message.from_user.id]['in_game'] = True
    else:
        await message.answer('Я довольно ограниченный бот.\n Пока мы играем, я могу реагировать'
                             ' либо на числа от 1 до 100, либо на команды /stat и /cancel')


@dp.message(Text(text=['Не', "Нет", "Не буду", "Не хочу", "Отстань", "Отвали"]))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль:(\nЕсли передумаешь - пиши мне!')
    else:
        await message.answer('Мы же с тобой играем. Если вдруг забыл правила, напиши /help.\n'
                             'Напиши мне число от 1 до 100 и мы продолжим;)')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_suitable_number(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура! Ты угадал мое число! Поздравляю!!!)))')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Мое число меньше...')
            users[message.from_user.id]['attempts'] -= 1
        else:
            await message.answer('Мое число большее...')
            users[message.from_user.id]['attempts'] -= 1
        if users[message.from_user.id]['attempts'] == 0:
            await message.answer('У тебя закончились попытки! Ты проиграл. Сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы же с тобой пока не играем, забыл?\nТы хочешь начать игру?')


@dp.message()
async def other_answers_process(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Напишите мне натуральное число от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот\n:( Хотите сыграть в "Угадай число"?')


if __name__ == '__main__':
    dp.run_polling(bot)
