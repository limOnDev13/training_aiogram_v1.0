from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter, Text
from aiogram.types import Message
from add_functions import read_token_from_txt


API_BOT: str = read_token_from_txt()
bot: Bot = Bot(API_BOT)
dp: Dispatcher = Dispatcher()


class NumbersFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        result_numbers: list[int] = []

        for word in message.text.split():
            normalized_word = word.replace(',', '').replace('.', '').strip()
            if normalized_word.isdigit():
                result_numbers.append(int(normalized_word))

        if result_numbers:
            return {'numbers': result_numbers}
        return False


@dp.message(Text(startswith=['Найди числа'], ignore_case=True), NumbersFilter())
async def process_with_numbers(message: Message, numbers: list[int]):
    result_number_string = ''
    for number in numbers:
        result_number_string += str(number) + ' '

    await message.answer('Числа в этой строке: ' + result_number_string)


@dp.message(Text(startswith=['Найди числа'], ignore_case=True))
async def process_without_numbers(message: Message):
    await message.answer('Не могу найти чисел в этой строке...')


if __name__ == '__main__':
    dp.run_polling(bot)
