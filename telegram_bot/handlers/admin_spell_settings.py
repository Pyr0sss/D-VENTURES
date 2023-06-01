import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from database.db_processing.spell_create import new_spell
from telegram_bot.keyboards.callback_datas import spell_class_callback, confirmation_callback
from telegram_bot.keyboards.inline_keyboards.spell_class_keyboard import spell_class
from telegram_bot.keyboards.reply import main_menu


class FSMSpell(StatesGroup):
    spell_name = State()
    spell_level = State()
    spell_description = State()
    spell_classes = State()


async def start_spell_creation(message: types.Message, state=FSMContext):
    await FSMSpell.spell_name.set()
    await message.answer(
        f'🪄 Сотворение заклинания\n\nДля начала введи то, как великие чародеи будут называть твоё заклинание, например, _Пивосмерч_', parse_mode="Markdown")


async def spell_add_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMSpell.next()
    await message.answer(f'🪄 Сотворение заклинания\n\n`{data["name"].upper()}`\n\nТеперь введи уровень, при котором твое великое'
                         f' заклинание будет доступно обычному смертному', parse_mode="Markdown")


async def spell_add_level(message: types.Message, state=FSMContext):
    try:
        if int(message.text) < 0:
            await message.reply("Ого! Где это видано, где это слыхано, что уровень такой существует, балбес!")
            return
        if int(message.text) > 20:
            await message.reply(
                "Это я что?! Должен игр 1000 сыграть, чтобы им воспользоваться? У меня вообще-то личная жизнь еще есть!")
            return

        async with state.proxy() as data:
            data['level'] = int(message.text)
        await FSMSpell.next()
        await message.answer(
            f'🪄 Сотворение заклинания\n\n`{data["name"].upper()}`\n{data["level"]}-й уровень\n\nЯ предчувствую, как этот'
            f'мир уже трепещет перед твоим заклинанием! Давай теперь опишем, в чем его сила!', parse_mode="Markdown")
    except Exception as err:
        await message.reply("Что-то тут не так... Я думал тут нужно было число вводить...")
        print(err)


async def spell_add_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        data['classes'] = ""
        data['class'] = []
    await FSMSpell.next()
    await message.answer(f'🪄Сотворение заклинания\n\n`{data["name"].upper()}`\n{data["level"]}-й уровень\n\n{data["description"]}\n\n'
                         f'Вот это заклинание! Теперь осталось добавить те классы, которые могут его использовать', reply_markup=spell_class, parse_mode="Markdown")


async def spell_add_class(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    async with state.proxy() as data:
        text: str = data["classes"]
        class_list: list = data["class"]
        if callback_data.get("name") in text:
            text = text.replace(f'{callback_data.get("name")}', '')
            class_list.remove(callback_data.get("clas"))
        else:
            text = text + callback_data.get("name")
            class_list.append(callback_data.get("clas"))
        data["classes"] = text
    await call.message.edit_text(f'🪄Сотворение заклинания\n\n`{data["name"].upper()}`\n{data["level"]}-й уровень, заклинание {text[:-2]}\n\n{data["description"]}\n\n'
                         f'Вот это заклинание! Теперь осталось добавить те классы, которые могут его использовать', reply_markup=spell_class, parse_mode="Markdown")


async def spell_save(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        name: str = data["name"]
        level: int = data["level"]
        clas: str = data["classes"][:-2]
        text: str = data["description"]
        classes: list = data["class"]
    await call.message.edit_text(f'🪄Сотворение заклинания\n\nСтану благословясь, пойду перекрестясь, из избы дверьми, '
                                 f'из ворот воротами, на широкий двор, в чисто поле *ПУФ*\n\n Заклинание готово!', parse_mode="Markdown")
    time.sleep(3)
    await call.message.edit_text(f'`{name.upper()}`\n{str(level)}-й уровень, заклинание {clas}\n\n{text}', parse_mode="Markdown")
    await state.finish()
    new_spell(name, level, classes, text)


def register_admin_spell_settings(dp: Dispatcher):
    dp.register_message_handler(start_spell_creation, Text(equals='Добавить заклинание', ignore_case=True),
                                is_admin=True, state='*')
    dp.register_message_handler(spell_add_name, is_admin=True, state=FSMSpell.spell_name)
    dp.register_message_handler(spell_add_level, is_admin=True, state=FSMSpell.spell_level)
    dp.register_message_handler(spell_add_description, is_admin=True, state=FSMSpell.spell_description)
    dp.register_callback_query_handler(spell_add_class, spell_class_callback.filter(turn="off"), is_admin=True, state=FSMSpell.spell_classes)
    dp.register_callback_query_handler(spell_save, confirmation_callback.filter(choice="yes"), is_admin=True,
                                       state=FSMSpell.spell_classes)
