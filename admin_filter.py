from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message
from add_functions import read_token_from_txt, MY_ID


API_TOKEN: str = read_token_from_txt()
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()
admin_ids: list = [MY_ID]


class IsAdmin(BaseFilter):
    def __init__(self, list_admin_ids: list[int]) -> None:
        self.list_admin_ids = list_admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.list_admin_ids


@dp.message(IsAdmin(admin_ids))
async def process_if_admin_update(message: Message):
    await message.answer('Это админ')


@dp.message()
async def process_if_not_admin(message: Message):
    print(message)
    await message.answer('Это не админ')


if __name__ == '__main__':
    dp.run_polling(bot)
