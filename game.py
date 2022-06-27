from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
import json
import requests
from forfun.databasegame import DatBase
from testjson import all_to_Json

db = DatBase()

bot = Bot(token="5311104145:AAF2iwSJDqmiOCH5LSFUnPOLnmXtruHrTDk")
dp = Dispatcher(bot, storage=MemoryStorage())


class reg(StatesGroup):
    ready = State()
    # game
    remove = State()

    # world
    addWorld_title = State()
    addWorld_ecology_end = State()
    # country
    addCountry = State()
    addCity = State()


zin_button = KeyboardButton('Позвать Ведущего')
startgame_button = KeyboardButton('Начать игру')
exit_button = KeyboardButton('Выйти')
pool_countrys_choose = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add(startgame_button).add(zin_button).add(exit_button)
##### Кнопки
choose_country = KeyboardButton('Выбрать страну')
add_button_country = KeyboardButton('Добавить')
startround_button = KeyboardButton('Старт игры')
pool = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(add_button_country) \
    .add(choose_country).add(startround_button).add(exit_button)
back_button = KeyboardButton('Назад')
# ДЛЯ Мира menu
inline_choose_menu = InlineKeyboardMarkup()
inline_choose_world = InlineKeyboardButton('Создать мир', callback_data='world_menu_1')
inline_choose_join = InlineKeyboardButton('Войти в мир (посмотреть) ', callback_data='world_menu_2')
inline_choose_menu.add(inline_choose_world, inline_choose_join)

# Список стран
available_country_names = ['США', 'Россия', 'Украина', 'Белорусь', 'Австралия',
                           'Албания', 'Великобритания', 'Мексика', 'Норвегия',
                           'Сирия', 'Франция', 'Чехия', 'Япония']
USA_city_names = ['Нью-Йорк', 'Лос-Анджелес', 'Сан-Франциско', 'Чикаго']
RU_city_names = ['Геленджик', 'Москва', 'Калининград', 'Самара']
Ukr_city_names = ['Киев', 'Харьков', 'Одесса', 'Днепр']
Bel_city_names = ['Минск', 'Витебск', 'Брест', 'Гродно']
AUS_city_names = ['Сидней', 'Канберра', 'Мельбурн', 'Кэрнс']
ALB_city_names = ['Тирана', 'Берат', 'Дуррес', 'Влёра']
UK_city_names = ['Лондон', 'Бирмингем', 'Кардифф', 'Глазго']
Mexico_city_names = ['Мехико', 'Тихуана', 'Пуэбла-де-Сарагоса', 'Сапопан']
Norvegia_city_names = ['Осло', 'Берген', 'Тронхейм', 'Саннвика']
Siria_city_names = ['Алеппо', 'Дамаск', 'Хама', 'Хомс']
France_city_names = ['Париж', 'Марсель', 'Лион', 'Тулуза']
Czh_city_names = ['Прага', 'Брно', 'Острава', 'Пльзень']
JAPAN_city_names = ['Токио', 'Иокогама', 'Осака', 'Нагоя']

## ПЕРЕМЕННЫЕ И ДРУГОЕ КОТОРОЕ ИСПОЛЬЗУЕТСЯ
newListCities = []
user_data = {}
country1 = ""
rezhim3_data = {}
sn = ""
sanctions_data = {}
development_data = {}
shield_data = {}
to_rocket_data = {}
newListCounties = []
ecology_data = {}
nuclear_data = {}
rockets_data = {}
development_data_0 = {}
development_data_1 = {}
development_data_2 = {}
development_data_3 = {}
shield_data_0 = {}
shield_data_1 = {}
shield_data_2 = {}
shield_data_3 = {}
sanctin = {"Title": [newListCounties],
           "Sanc": [False, False, False, False]}
bomb_process = {
    "Title": [newListCities],
    "Bomb": [False, False, False, False, False, False, False, False,
             False, False, False, False, False, False, False, False]
}


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Добрый день! Это бот BIGJOPA",
                        reply_markup=pool_countrys_choose)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(
        '/start - стартовая точка бота\n Начать игру - создать мир \n Выйти - выход и закрытие кнопок'
        '\n Назад - открывает меню (создать и выбрать страну)\n Добавить - добавление стран(совет:не больше 4)'
        '\n Выбрать страну - (пока не работает) выбор страны в которую приходишь')


@dp.message_handler(content_types=['text'])
async def start_command(message: types.Message):
    if message.text == "Начать игру":
        await message.reply("Начнем игру! Создадим мир ",
                            reply_markup=inline_choose_menu)
    elif message.text == "Выйти":
        await message.reply("Покидаем игру! и очищается список выбранных",
                            reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Назад":
        await message.reply("Вернулись назад", reply_markup=pool)

    elif message.text == "Добавить":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in available_country_names:
            keyboard.add(name)
        keyboard.row(back_button)
        await message.reply("Выберете страну используя клавиатуру ниже! ", reply_markup=keyboard)
        await reg.addCountry.set()
    elif message.text == "Старт игры":
        await bot.send_message(message.from_user.id, "*****ROUND 1*****\n **Вы в роли Ведущего**\n"
                                                     "Задача:Необходимо сходить в каждую страну\n"
                                                     "Можете несколько раз сходить, если страна захочет изменить данные\n"
                                                     "Стартовый баланс каждой страны: 1000\n"
                                                     "В данный момент они могут:\n"
                                                     "Развить ядерную программу/ Развивать города/ Улучшать экологию\n"
                                                     "Следите за кажд")
    elif message.text == "Выбрать страну":
        user_data[message.from_user.id] = ""
        await message.answer("Укажите Страну: ", reply_markup=get_keyboard())
    elif message.text == "id":
        print(message.from_user.id)
        await message.answer(f"Ваш id = {message.from_user.id}")
    elif message.text == "Позвать Ведущего":
        # TODO: Add sleep, dont spam
        await bot.send_message(766668581,
                               f"Вас позвали\n KTO? = {message.from_user.first_name} {message.from_user.last_name}")
        await message.reply("Вы позвали Ведущего\nОжидайте")
        # димы
        # await bot.send_message(145582175, f"Вас позвал {message.from_user.first_name}")
    else:
        await message.reply("Возможно вы ввели текст который не является командой")


#### Выбор Inline Создать или Войти но пока выполняют одну функцию
# TODO: Сделать вход в страну
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('world_menu_'))
async def call_pool_button_menu(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали Создать мир\n Укажите Название')
        await reg.addWorld_title.set()
    if code == 2:
        await bot.send_message(callback_query.from_user.id, "Вы выбрали войти в мир\n но пока только можно создать")
        list_countries = db.select_countries()
        print(list_countries[0][1])
        i = 0
        list_2 = []
        for l in list_countries:
            list_2.insert(i, list_countries[i][1])
            i += 1
        await bot.send_message(callback_query.from_user.id, 'Все страны которые имеются в бд:\n %s' % '\n'.join(list_2))


#### Добавление мира (1)
@dp.message_handler(state=reg.addWorld_title)
async def addWorld_process_choose_title(message: types.Message, state=FSMContext):
    await state.update_data(title=message.text)
    await bot.send_message(message.from_user.id, 'Экология *** % (Введите число)')
    await reg.addWorld_ecology_end.set()


#### Добавление мира (2)



@dp.message_handler(state=reg.addWorld_ecology_end)
async def addWorld_process_choose_to_inline(message: types.Message, state=FSMContext):
    await state.update_data(ecology=message.text)
    await reg.ready.set()
    user_data = await state.get_data()
    data = tuple(user_data.values())
    try:
        db.add_world(data)
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"Ошибка\nПри добавлении Мира:{ex}")
    await message.reply('Мир создан ITS TIME TO CHOOSE ', reply_markup=pool)
    newListCounties.clear()
    await state.reset_state()


#### Удаление города
@dp.message_handler(state=reg.remove)
async def remove_process_choose(message: types.Message, state=FSMContext):
    await state.update_data(title=message.text)
    Id_country = db.get_max_id_select_country()
    await state.update_data(counttydi=Id_country)
    remove_data = await state.get_data()
    data = tuple(remove_data.values())
    db.delete_city(data)
    await bot.send_message(message.from_user.id, 'Вы убрали(удалили) город')
    await state.reset_state()




def get_keyboard():
    print(newListCounties)
    buttons = [
        types.InlineKeyboardButton(text=newListCounties[0], callback_data="choosectr_1"),
        types.InlineKeyboardButton(text=newListCounties[1], callback_data="choosectr_2"),
        types.InlineKeyboardButton(text=newListCounties[2], callback_data="choosectr_3"),
        types.InlineKeyboardButton(text=newListCounties[3], callback_data="choosectr_4"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="choosectr_finish")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


balance_data = {}


def get_keyboard2(country: str):
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    def shield_devemo(country: str, i: int):
        if (country == newListCounties[i]):
            newbuttons = [
                types.InlineKeyboardButton(text="Развить", callback_data="balance_developmnet0"),
                types.InlineKeyboardButton(text=newListCities[4*i], callback_data="balance_title_country"),
                types.InlineKeyboardButton(text="Щит", callback_data="balance_shield0"),
                types.InlineKeyboardButton(text="Развить", callback_data="balance_developmnet1"),
                types.InlineKeyboardButton(text=newListCities[4*i + 1], callback_data="balance_title_country"),
                types.InlineKeyboardButton(text="Щит", callback_data="balance_shield1"),
                types.InlineKeyboardButton(text="Развить", callback_data="balance_developmnet2"),
                types.InlineKeyboardButton(text=newListCities[4*i + 2], callback_data="balance_title_country"),
                types.InlineKeyboardButton(text="Щит", callback_data="balance_shield2"),
                types.InlineKeyboardButton(text="Развить", callback_data="balance_developmnet3"),
                types.InlineKeyboardButton(text=newListCities[4*i + 3], callback_data="balance_title_country"),
                types.InlineKeyboardButton(text="Щит", callback_data="balance_shield3"),
            ]
        return newbuttons

    if (country == newListCounties[0]):
        buttoncountries = shield_devemo(country, 0)
        keyboard.add(*buttoncountries)
    elif (country == newListCounties[1]):
        buttoncountries = shield_devemo(country, 1)
        keyboard.add(*buttoncountries)
    elif (country == newListCounties[2]):
        buttoncountries = shield_devemo(country, 2)
        keyboard.add(*buttoncountries)
    elif (country == newListCounties[3]):
        buttoncountries = shield_devemo(country, 3)
        keyboard.add(*buttoncountries)
    buttons = [
        types.InlineKeyboardButton(text="+1", callback_data="balance_rocketinc"),
        types.InlineKeyboardButton(text="Ракеты", callback_data="balance_rtitle"),
        types.InlineKeyboardButton(text="-1", callback_data="balance_rocketdec"),
        types.InlineKeyboardButton(text="Развить", callback_data="balance_nuclearprograminc"),
        types.InlineKeyboardButton(text="Ядерка", callback_data="balance_ntitle"),
        types.InlineKeyboardButton(text="Нет", callback_data="balance_nuclearprogramdec"),
        types.InlineKeyboardButton(text="+5", callback_data="balance_ecologyinc"),
        types.InlineKeyboardButton(text="Экология", callback_data="balance_ecology"),
        types.InlineKeyboardButton(text="-5", callback_data="balance_ecologydec"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="balance_finish")
    ]
    keyboard.add(*buttons)
    return keyboard


def get_keyboard3():
    # Генерация клавиатуры.
    buttons2 = [
        types.InlineKeyboardButton(text="Санкции", callback_data="sanc_title_s"),
        types.InlineKeyboardButton(text=newListCounties[0], callback_data="sanc_san1"),
        types.InlineKeyboardButton(text=newListCounties[1], callback_data="sanc_san2"),
        types.InlineKeyboardButton(text=newListCounties[2], callback_data="sanc_san3"),
        types.InlineKeyboardButton(text=newListCounties[3], callback_data="sanc_san4"),
        types.InlineKeyboardButton(text="Бросить бомбу", callback_data="sanc_title_b"),
        types.InlineKeyboardButton(text=newListCities[0], callback_data="sanc_bomb1"),
        types.InlineKeyboardButton(text=newListCities[1], callback_data="sanc_bomb2"),
        types.InlineKeyboardButton(text=newListCities[2], callback_data="sanc_bomb3"),
        types.InlineKeyboardButton(text=newListCities[3], callback_data="sanc_bomb4"),
        #
        types.InlineKeyboardButton(text="НИЧЕГО", callback_data="sanc_empty1"),
        types.InlineKeyboardButton(text=newListCities[4], callback_data="sanc_bomb5"),
        types.InlineKeyboardButton(text=newListCities[5], callback_data="sanc_bomb6"),
        types.InlineKeyboardButton(text=newListCities[6], callback_data="sanc_bomb7"),
        types.InlineKeyboardButton(text=newListCities[7], callback_data="sanc_bomb8"),
        #
        types.InlineKeyboardButton(text="..", callback_data="sanc_empty2"),
        types.InlineKeyboardButton(text=newListCities[8], callback_data="sanc_bomb9"),
        types.InlineKeyboardButton(text=newListCities[9], callback_data="sanc_bomb10"),
        types.InlineKeyboardButton(text=newListCities[10], callback_data="sanc_bomb11"),
        types.InlineKeyboardButton(text=newListCities[11], callback_data="sanc_bomb12"),
        #
        types.InlineKeyboardButton(text="..", callback_data="sanc_empty3"),
        types.InlineKeyboardButton(text=newListCities[12], callback_data="sanc_bomb13"),
        types.InlineKeyboardButton(text=newListCities[13], callback_data="sanc_bomb14"),
        types.InlineKeyboardButton(text=newListCities[14], callback_data="sanc_bomb15"),
        types.InlineKeyboardButton(text=newListCities[15], callback_data="sanc_bomb16"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="sanc_title_finish")
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    newkeybord = types.InlineKeyboardMarkup(row_width=5)
    newkeybord.add(*buttons2)
    return newkeybord


async def update_num_text(message: types.Message, new_value: int):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"Странa: {new_value}", reply_markup=get_keyboard())


async def update_country_text(message: types.Message, country: str, balance: int, ecology: int,
                              nuclear: bool, rockets: int, city_0: str, ls_0: int, shield_0: bool,
                              city_1: str, ls_1: int, shield_1: bool,
                              city_2: str, ls_2: int, shield_2: bool,
                              city_3: str, ls_3: int, shield_3: bool):
    await message.edit_text(f"Страна: {country}\n"
                            f"Баланс : {balance}\n "
                            f"Экология: {ecology}\n "
                            f"Ракеты: {rockets}\n "
                            f"Яд Программа: {nuclear}\n\n"
                            f"Город: {city_0}\n"
                            f"Ур Жизни: {ls_0}\n"
                            f"Щит: {shield_0}\n\n"
                            f"Город: {city_1}\n"
                            f"Ур Жизни: {ls_1}\n"
                            f"Щит: {shield_1}\n\n"
                            f"Город: {city_2}\n"
                            f"Ур Жизни: {ls_2}\n"
                            f"Щит: {shield_2}\n\n"
                            f"Город: {city_3}\n"
                            f"Ур Жизни: {ls_3}\n"
                            f"Щит: {shield_3}\n",
                            reply_markup=get_keyboard2(country))


async def update_sanctions(message: types.Message, country: str, sn_ctr_0: dict, rocket_dic: dict):
    await message.edit_text(
        f"Вы в стране  --> {country}\n"
        f"\U0001F30FСтрана \t\t\t \U0001F30FСанкции\n"
        f"{newListCounties[0]} \t ------> {sn_ctr_0['Sanc'][0]}\n"
        f"{newListCounties[1]} \t ------> {sn_ctr_0['Sanc'][1]}\n"
        f"{newListCounties[2]} \t ------> {sn_ctr_0['Sanc'][2]}\n"
        f"{newListCounties[3]} \t ------> {sn_ctr_0['Sanc'][3]}\n"
        f"\U0001F680 Города \t\t\t\t \U0001F680 Бомба\n"
        f"{rocket_dic['Title'][0][0]} \t ----> {rocket_dic['Bomb'][0]}\n"
        f"{rocket_dic['Title'][0][1]} \t ----> {rocket_dic['Bomb'][1]}\n"
        f"{rocket_dic['Title'][0][2]} \t ----> {rocket_dic['Bomb'][2]}\n"
        f"{rocket_dic['Title'][0][3]} \t ----> {rocket_dic['Bomb'][3]}\n"
        f"{rocket_dic['Title'][0][4]} \t ----> {rocket_dic['Bomb'][4]}\n"
        f"{rocket_dic['Title'][0][5]} \t ----> {rocket_dic['Bomb'][5]}\n"
        f"{rocket_dic['Title'][0][6]} \t ----> {rocket_dic['Bomb'][6]}\n"
        f"{rocket_dic['Title'][0][7]} \t ----> {rocket_dic['Bomb'][7]}\n"
        f"{rocket_dic['Title'][0][8]} \t ----> {rocket_dic['Bomb'][8]}\n"
        f"{rocket_dic['Title'][0][9]} \t ----> {rocket_dic['Bomb'][9]}\n"
        f"{rocket_dic['Title'][0][10]} \t ----> {rocket_dic['Bomb'][10]}\n"
        f"{rocket_dic['Title'][0][11]} \t ----> {rocket_dic['Bomb'][11]}\n"
        f"{rocket_dic['Title'][0][12]} \t ----> {rocket_dic['Bomb'][12]}\n"
        f"{rocket_dic['Title'][0][13]} \t ----> {rocket_dic['Bomb'][13]}\n"
        f"{rocket_dic['Title'][0][14]} \t ----> {rocket_dic['Bomb'][14]}\n"
        f"{rocket_dic['Title'][0][15]} \t ----> {rocket_dic['Bomb'][15]}\n",
        reply_markup=get_keyboard3())


###JSOn

@dp.callback_query_handler(Text(startswith="sanc_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data.split("sanc_")[1]
    country2 = user_data.get(call.from_user.id, call.message.text)
    id_country = db.get_id_select_country(country2)
    list_city_choos = db.get_all_cities(id_country)

    id_city_0 = db.select_id_cities(id_country, list_city_choos[0][0])
    id_city_1 = db.select_id_cities(id_country, list_city_choos[1][0])
    id_city_2 = db.select_id_cities(id_country, list_city_choos[2][0])
    id_city_3 = db.select_id_cities(id_country, list_city_choos[3][0])

    old_balance_value = balance_data.get(id_country, call.message.text)
    old_nuclear_value = nuclear_data.get(id_country, call.message.text)
    old_ecology_value = ecology_data.get(id_country, call.message.text)
    old_rockets_value = rockets_data.get(id_country, call.message.text)

    old_dev_0_value = development_data_0.get(id_city_0, call.message.text)
    old_dev_1_value = development_data_1.get(id_city_1, call.message.text)
    old_dev_2_value = development_data_2.get(id_city_2, call.message.text)
    old_dev_3_value = development_data_3.get(id_city_3, call.message.text)

    old_shield_0_value = shield_data_0.get(id_city_0, call.message.text)
    old_shield_1_value = shield_data_1.get(id_city_1, call.message.text)
    old_shield_2_value = shield_data_2.get(id_city_2, call.message.text)
    old_shield_3_value = shield_data_3.get(id_city_3, call.message.text)

    rezhim3_value = rezhim3_data.get(call.from_user.id, "")
    sanctions_value = sanctions_data.get(call.from_user.id, "")
    to_rocket_value = to_rocket_data.get(call.from_user.id, "")
    development_value = development_data.get(call.from_user.id, "")
    shield_value = shield_data.get(call.from_user.id, "")

    async def san(id_list_country: int):
        if sanctin["Sanc"][id_list_country] == False:
            sanctin["Sanc"][id_list_country] = True
        else:
            sanctin["Sanc"][id_list_country] = False
        sanctions_data[call.from_user.id] = sanctin
        to_rocket_data[call.from_user.id] = bomb_process
        await update_sanctions(call.message, country2, sanctin, bomb_process)

    async def bombProcess(id_list: int):
        if bomb_process['Bomb'][id_list] == False:
            bomb_process['Bomb'][id_list] = True
        else:
            bomb_process['Bomb'][id_list] = False
        sanctions_data[call.from_user.id] = sanctin
        to_rocket_data[call.from_user.id] = bomb_process
        await update_sanctions(call.message, country2, sanctin, bomb_process)

    ## САНКЦИИ ДЕЛАЕМ
    if action == "san1" and country2 != newListCounties[0]:
        await san(0)
    if action == "san2" and country2 != newListCounties[1]:
        await san(1)
    if action == "san3" and country2 != newListCounties[2]:
        await san(2)
    if action == "san4" and country2 != newListCounties[3]:
        await san(3)
    if action == "bomb1":
        await bombProcess(0)
    if action == "bomb2":
        await bombProcess(1)
    if action == "bomb3":
        await bombProcess(2)
    if action == "bomb4":
        await bombProcess(3)
    if action == "bomb5":
        await bombProcess(4)
    if action == "bomb6":
        await bombProcess(5)
    if action == "bomb7":
        await bombProcess(6)
    if action == "bomb8":
        await bombProcess(7)
    if action == "bomb9":
        await bombProcess(8)
    if action == "bomb10":
        await bombProcess(9)
    if action == "bomb11":
        await bombProcess(10)
    if action == "bomb12":
        await bombProcess(11)
    if action == "bomb13":
        await bombProcess(12)
    if action == "bomb14":
        await bombProcess(13)
    if action == "bomb15":
        await bombProcess(14)
    if action == "bomb16":
        await bombProcess(15)

    if action == "title_finish":
        await call.message.edit_text(
            f"Итогo\n"
            f"Страна: {country2}\n"
            f"Баланс: {old_balance_value}\n"
            f"Экология: {old_ecology_value}\n"
            f"Ракет: {old_rockets_value}\n"
            f"Ядерная программа: {old_nuclear_value}\n"
            f"Города:\n"
            f"\U000027A1{list_city_choos[0][0]} \t Ур. Жизни: {old_dev_0_value} \t Щит: {old_shield_0_value}\n"
            f"\U000027A1{list_city_choos[1][0]} \t Ур. Жизни: {old_dev_1_value} \t Щит: {old_shield_1_value}\n"
            f"\U000027A1{list_city_choos[2][0]} \t Ур. Жизни: {old_dev_2_value} \t Щит: {old_shield_2_value}\n"
            f"\U000027A1{list_city_choos[3][0]} \t Ур. Жизни: {old_dev_3_value} \t Щит: {old_shield_3_value}\n")
        list_development_fr_city = [old_dev_0_value, old_dev_1_value, old_dev_2_value, old_dev_3_value]
        list_shield_fr_city = [old_shield_0_value, old_shield_1_value, old_shield_2_value, old_shield_3_value]
        list_CityId_fr = [id_city_0, id_city_1, id_city_2, id_city_3]
        dic_fr_cities = {"Title": list_city_choos,
                         "Development": list_development_fr_city,
                         "Shield": list_shield_fr_city,
                         "CityId": list_CityId_fr}
        list_en_ctr = newListCounties.copy()
        list_en_ctr.remove(country2)
        id_country_en_0 = db.get_max_id_select_country()
        list_all_id_country = [id_country_en_0, id_country_en_0-1, id_country_en_0-2, id_country_en_0-3]
        list_id_country_en = list_all_id_country.copy()
        list_id_country_en.remove(id_country)
        from_db_list_id_city_en_0 = db.get_all_id_cities(list_id_country_en[0])
        from_db_list_id_city_en_1 = db.get_all_id_cities(list_id_country_en[1])
        from_db_list_id_city_en_2 = db.get_all_id_cities(list_id_country_en[2])
        list_cityId_en = [from_db_list_id_city_en_0, from_db_list_id_city_en_1, from_db_list_id_city_en_2]
        dic_ctrId_CityId = {"CountryId": list_id_country_en, "CityId": list_cityId_en}
        js = all_to_Json()
        Idworld = db.get_max_id_select_world()
        ### JSON
        js.convert_Json(Idworld, old_rockets_value, old_ecology_value, id_country,
                        dic_fr_cities, bomb_process, dic_ctrId_CityId, sanctin)
    await call.answer()


############################### ВЫБОР СТРАНЫ
@dp.callback_query_handler(Text(startswith="choosectr_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data.split("choosectr_")[1]
    user_value = user_data.get(call.from_user.id, "")
    if action == "1":
        country1 = newListCounties[0]
        user_value = country1
        user_data[call.from_user.id] = user_value
        await update_num_text(call.message, user_value)
    elif action == "2":
        country1 = newListCounties[1]
        user_value = country1
        user_data[call.from_user.id] = user_value
        await update_num_text(call.message, user_value)
    elif action == "3":
        country1 = newListCounties[2]
        user_value = country1
        user_data[call.from_user.id] = user_value
        await update_num_text(call.message, user_value)
    elif action == "4":
        country1 = newListCounties[3]
        user_value = country1
        user_data[call.from_user.id] = user_value
        await update_num_text(call.message, user_value)
    elif action == "finish":
        await call.message.edit_text(f"Итого: {user_value}", reply_markup=get_keyboard2(user_value))
        print(user_data)
    await call.answer()



@dp.callback_query_handler(Text(startswith="balance_"))
async def balance_call(call: types.CallbackQuery):
    country2 = user_data.get(call.from_user.id, call.message.text)
    try:
        balance = db.select_balance_ctr(country2)
        id_country = db.get_id_select_country(country2)
    except Exception as e:
        await bot.send_message(call.from_user.id, e)
    balance_value = balance_data.get(id_country, balance)
    actionbalance = call.data.split("_")[1]
    ##
    ecology = db.select_ecology()
    nuclear = db.select_nuclear(country2)
    rockets = db.select_rockets(country2)
    #
    list_city_choos = db.get_all_cities(id_country)
    id_city_0 = db.select_id_cities(id_country, list_city_choos[0][0])
    ls_city_0 = db.select_ls_city(id_country, list_city_choos[0][0])
    sh_city_0 = db.select_shield_city(id_country, list_city_choos[0][0])

    id_city_1 = db.select_id_cities(id_country, list_city_choos[1][0])
    ls_city_1 = db.select_ls_city(id_country, list_city_choos[1][0])
    sh_city_1 = db.select_shield_city(id_country, list_city_choos[1][0])

    id_city_2 = db.select_id_cities(id_country, list_city_choos[2][0])
    ls_city_2 = db.select_ls_city(id_country, list_city_choos[2][0])
    sh_city_2 = db.select_shield_city(id_country, list_city_choos[2][0])

    id_city_3 = db.select_id_cities(id_country, list_city_choos[3][0])
    ls_city_3 = db.select_ls_city(id_country, list_city_choos[3][0])
    sh_city_3 = db.select_shield_city(id_country, list_city_choos[3][0])

    dev_0_value = development_data_0.get(id_city_0, ls_city_0)
    dev_1_value = development_data_1.get(id_city_1, ls_city_1)
    dev_2_value = development_data_2.get(id_city_2, ls_city_2)
    dev_3_value = development_data_3.get(id_city_3, ls_city_3)
    shield_0_value = shield_data_0.get(id_city_0, sh_city_0)
    shield_1_value = shield_data_1.get(id_city_1, sh_city_1)
    shield_2_value = shield_data_2.get(id_city_2, sh_city_2)
    shield_3_value = shield_data_3.get(id_city_3, sh_city_3)
    #
    ecology_value = ecology_data.get(id_country, ecology)
    nuclear_value = nuclear_data.get(id_country, nuclear)
    rockets_value = rockets_data.get(id_country, rockets)
    async def balance_trat(b: int, n: bool, e: int, r: int, d_0: int, d_1: int,
                           d_2: int, d_3: int, s_0: bool, s_1: bool, s_2: bool, s_3: bool):
        balance_data[id_country] = balance_value + b
        nuclear_data[id_country] = nuclear_value = n
        ecology_data[id_country] = ecology_value + e
        rockets_data[id_country] = rockets_value + r
        development_data_0[id_city_0] = dev_0_value + d_0
        development_data_1[id_city_1] = dev_1_value + d_1
        development_data_2[id_city_2] = dev_2_value + d_2
        development_data_3[id_city_3] = dev_3_value + d_3
        shield_data_0[id_city_0] = shield_0_value = s_0
        shield_data_1[id_city_1] = shield_1_value = s_1
        shield_data_2[id_city_2] = shield_2_value = s_2
        shield_data_3[id_city_3] = shield_3_value = s_3
        await update_country_text(call.message, country2, balance_value + b, ecology_value + e,
                                  nuclear_value, rockets_value + r,
                                  list_city_choos[0][0], dev_0_value + d_0, shield_0_value,
                                  list_city_choos[1][0], dev_1_value + d_1, shield_1_value,
                                  list_city_choos[2][0], dev_2_value + d_2, shield_2_value,
                                  list_city_choos[3][0], dev_3_value + d_3, shield_3_value)

    if actionbalance == "rocketinc":
        await balance_trat(-150, nuclear_value, 0, 1, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "rocketdec":
        await balance_trat(150, nuclear_value, 0, -1, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "nuclearprograminc" and nuclear == False:
        await balance_trat(-500, True, 0, 0, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "nuclearprogramdec":
        await balance_trat(500, False, 0, 0, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "ecologyinc":
        await balance_trat(-150, nuclear_value, 5, 0, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "ecologydec":
        await balance_trat(150, nuclear_value, -5, 0, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "developmnet0" and dev_0_value == 60:
        await balance_trat(-150, nuclear_value, 0, 0, 20, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "developmnet1" and dev_1_value == 60:
        await balance_trat(-150, nuclear_value, 0, 0, 0, 20, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "developmnet2" and dev_2_value == 60:
        await balance_trat(-150, nuclear_value, 0, 0, 0, 0, 20, 0,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "developmnet3" and dev_3_value == 60:
        await balance_trat(-150, nuclear_value, 0, 0, 0, 0, 0, 20,
                           shield_0_value, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "shield0" and shield_0_value == False:
        await balance_trat(-300, nuclear_value, 0, 0, 0, 0, 0, 0,
                           True, shield_1_value, shield_2_value, shield_3_value)

    elif actionbalance == "shield1" and shield_1_value == False:
        await balance_trat(-300, nuclear_value, 0, 0, 0, 0, 0, 0,
                           shield_0_value, True, shield_2_value, shield_3_value)

    elif actionbalance == "shield2" and shield_2_value == False:
        await balance_trat(-300, nuclear_value, 0, 0, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, True, shield_3_value)

    elif actionbalance == "shield3" and shield_3_value == False:
        await balance_trat(-300, nuclear_value, 0, 0, 0, 0, 0, 0,
                           shield_0_value, shield_1_value, shield_2_value, True)

    elif actionbalance == "finish":
        await call.message.edit_text(
            f"Итого для {country2} Баланс:{balance_value}\n"
            f"Экология: {ecology_value}\n"
            f"Ядерная программа: {nuclear_value}\n"
            f"Ракет: {rockets_value}\n"
            f"Города: \n"
            f"\U000027A1 {list_city_choos[0][0]} \t Ур.Ж: {dev_0_value} \t Щит: {shield_0_value}\n"
            f"\U000027A1 {list_city_choos[1][0]} \t Ур.Ж: {dev_1_value} \t Щит: {shield_1_value}\n"
            f"\U000027A1 {list_city_choos[2][0]} \t Ур.Ж: {dev_2_value} \t Щит: {shield_2_value}\n"
            f"\U000027A1 {list_city_choos[3][0]} \t Ур.Ж: {dev_3_value} \t Щит: {shield_3_value}\n",
            reply_markup=get_keyboard3())
    await call.answer()


#### Добавление страны и городов
@dp.message_handler(state=reg.addCountry)
async def Balance_process_addCountry(message: types.Message, state=FSMContext):
    if message.text in available_country_names:
        await state.update_data(title=message.text)
        await state.update_data(balance='1000')
        await state.update_data(lifestandard='60')
        await state.update_data(nuclearProgram='false')
        await state.update_data(rocekt='0')
        Idworld = db.get_max_id_select_world()
        await state.update_data(worldId = Idworld)
        await bot.send_message(message.from_user.id, "Отлично все для заполнения страны готово")
        await reg.ready.set()
        user_data = await state.get_data()
        data = tuple(user_data.values())
        print(data)
        try:
            db.add_country(data)
        except Exception as ex:
            await bot.send_message(message.from_user.id, f"Ошибка\n При добавлении страны: {ex}")
        await message.reply('Страна успешно создана ITS TIME TO CHOOSE ', reply_markup=pool)
        Id_country = db.get_max_id_select_country()
        await state.reset_data()

        async def inserting(list_city):
            for c in list_city:
                await state.update_data(title=c)
                await state.update_data(lifestandard='60')
                await state.update_data(condition='true')
                await state.update_data(shield='false')
                await state.update_data(countryId=Id_country)
                user_data = await state.get_data()
                data = tuple(user_data.values())
                db.insert_city(data)
                newListCities.append(c)

        if message.text == "США":
            await inserting(USA_city_names)
            newListCounties.append("США")
            await bot.send_message(message.from_user.id, "США заполнена городами")
        elif message.text == "Россия":
            await inserting(RU_city_names)
            newListCounties.append("Россия")
            await bot.send_message(message.from_user.id, "Россия заполнена городами")
        elif message.text == "Украина":
            await inserting(Ukr_city_names)
            newListCounties.append("Украина")
            await bot.send_message(message.from_user.id, "Украина заполнена городами")
        elif message.text == "Белорусь":
            await inserting(Bel_city_names)
            newListCounties.append("Белорусь")
            await bot.send_message(message.from_user.id, "Белорусь заполнена городами")
        elif message.text == "Австралия":
            await inserting(AUS_city_names)
            newListCounties.append("Австралия")
            await bot.send_message(message.from_user.id, "Австралия заполнена городами")
        elif message.text == "Албания":
            await inserting(ALB_city_names)
            newListCounties.append("Албания")
            await bot.send_message(message.from_user.id, "Албания заполнена городами")
        elif message.text == "Великобритания":
            await inserting(UK_city_names)
            newListCounties.append("Великобритания")
            await bot.send_message(message.from_user.id, "Великобритания заполнена городами")
        elif message.text == "Мексика":
            await inserting(Mexico_city_names)
            newListCounties.append("Мексика")
            await bot.send_message(message.from_user.id, "Мексика заполнена городами")
        elif message.text == "Норвегия":
            await inserting(Norvegia_city_names)
            newListCounties.append("Норвегия")
            await bot.send_message(message.from_user.id, "Норвегия заполнена городами")
        elif message.text == "Сирия":
            await inserting(Siria_city_names)
            newListCounties.append("Сирия")
            await bot.send_message(message.from_user.id, "Сирия заполнена городами")
        elif message.text == "Франция":
            await inserting(France_city_names)
            newListCounties.append("Франция")
            await bot.send_message(message.from_user.id, "Франция заполнена городами")
        elif message.text == "Чехия":
            await inserting(Czh_city_names)
            newListCounties.append("Чехия")
            await bot.send_message(message.from_user.id, "Чехия заполнена городами")
        elif message.text == "Япония":
            await inserting(JAPAN_city_names)
            newListCounties.append("Япония")
            await bot.send_message(message.from_user.id, "Япония заполнена городами")
        else:
            await bot.send_message(message.from_user.id, "Похоже, что страна не заполнена городами")
    else:
        await message.reply("Пожалуйста выберете страну из списка клавиатуры")
    await state.reset_state()
    return newListCounties


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
