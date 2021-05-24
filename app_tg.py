from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from models import *

bot = Bot(token='1812514445:AAGjfusZZZNtk_icteyixz25BKmxF9CQhrM')
dp = Dispatcher(bot=bot)


def check_if_me(f):
    async def wrapper(message: Message):
        if message.from_user.id != 488036932:
            return
        return await f(message)
    return wrapper


@check_if_me
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='hello there. this is integrated in telegram admin panel for knowledge base, created by @lexani42.\n'
             'commands:\n'
             '/start - this message\n'
             '/check {name} - get information about count of user rows/is user exist\n'
             '/add {name} - add new user\n'
             '/del {name} - del user and all his rows\n'
             '/addrow {name} {text} - add new row for user with text given\n'
             '/delrow {id} - delete row with id given\n'
             '/updrow {id} {text} - update selected row with given text'
    )


@check_if_me
@dp.message_handler(commands=['check'])
async def check(message: Message):
    try:
        uname = message.text.split()[1].split('@')[-1]
        u = User.get(name=uname)
        counter = 0
        for _ in u.notes:
            counter += 1
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'user {uname} have {counter} notes in db'
        )
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send user name'
        )
    except User.DoesNotExist:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'user with this name does not exist'
        )


@check_if_me
@dp.message_handler(commands=['add'])
async def add(message: Message):
    try:
        uname = message.text.split()[1].split('@')[-1]
        User.create(name=uname)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'user {uname} created'
        )
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send user name'
        )
    except IntegrityError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='user with this nickname is already exists'
        )


@check_if_me
@dp.message_handler(commands=['del'])
async def del_(message: Message):
    try:
        uname = message.text.split()[1].split('@')[-1]
        User.delete().where(User.name == uname).execute()
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'user {uname} deleted'
        )
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send user name'
        )


@check_if_me
@dp.message_handler(commands=['addrow'])
async def addrow(message: Message):
    try:
        uname = message.text.split()[1].split('@')[-1]
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send user name'
        )
        return
    try:
        text = ' '.join(message.text.split()[2:])
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send text'
        )
        return
    try:
        u = User.get(name=uname)
        n = Note.create(user=u, text=text)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'note with id {n.id} created. user: {u.name}. text:\n{n.text}'
        )
    except User.DoesNotExist:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'user with username {uname} does not exist'
        )


@check_if_me
@dp.message_handler(commands=['updrow'])
async def updrow(message: Message):
    try:
        id_ = message.text.split()[1]
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send note id'
        )
        return
    try:
        text = ' '.join(message.text.split()[2:])
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send new text'
        )
        return
    try:
        n = Note.get(id=id_)
        n.text = text
        n.save()
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'note with id {id_} updated. new text:\n{text}'
        )
    except Note.DoesNotExist:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'note with id {id_} does not exist'
        )


@check_if_me
@dp.message_handler(commands=['delrow'])
async def delrow(message: Message):
    try:
        id_ = message.text.split()[1]
        Note.delete().where(Note.id == id_).execute()
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'note with id {id_} deleted'
        )
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='please, send note id'
        )

executor.start_polling(dp, skip_updates=True)
