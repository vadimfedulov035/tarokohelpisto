import json

from telebot import types


BUTTON_RESTART = types.InlineKeyboardButton("Рестарт", callback_data="re")


def reload_info():
    with open("taro_info.json", "r", encoding="utf-8") as f:
        info = json.load(f)
    return info


def arkan_markup():
    """assemble inline keyboard for choosing arkan type"""
    info = reload_info()
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(info.get("e_name", "..."), callback_data="e")
    button2 = types.InlineKeyboardButton(info.get("j_name", "..."), callback_data="j")
    button3 = types.InlineKeyboardButton(info.get("y_name", "..."), callback_data="y")
    markup.row(button1)
    markup.row(button2, button3)
    return markup


def elder_markup():
    """assemble inline keyboard for choosing elder arkan number"""
    global BUTTON_RESTART
    info = reload_info()
    markup = types.InlineKeyboardMarkup()
    # initialize buttons
    buttons = [types.InlineKeyboardButton(
        info.get(f"e_{i}_name", "..."), callback_data=f"e_{i}")
        for i in range(22)]
    # set buttons
    for i in range(0, 21, 2):
        markup.row(buttons[i], buttons[i + 1])
    markup.row(BUTTON_RESTART)
    return markup


def junior_markup():
    """assemble inline keyboard for choosing junior arkan number"""
    global BUTTON_RESTART
    info = reload_info()
    markup = types.InlineKeyboardMarkup()
    # initialize buttons
    buttons = [types.InlineKeyboardButton(
        info.get(f"j_{i}_name", "..."), callback_data=f"j_{i}")
        for i in range(1, 11)]
    # set buttons
    for i in range(0, 9, 3):
        markup.row(buttons[i], buttons[i + 1], buttons[i + 2])
    markup.row(buttons[9])
    markup.row(BUTTON_RESTART)
    return markup


def yard_markup():
    """assemble inline keyboard for choosing yard arkan title"""
    global BUTTON_RESTART
    info = reload_info()
    shorts = ["pa", "kn", "ki", "qu"]
    markup = types.InlineKeyboardMarkup()
    # initialize buttons
    buttons = [types.InlineKeyboardButton(
        info.get(f"y_{short}_name", "..."), callback_data=f"y_{short}")
        for short in shorts]
    # set buttons
    for i in range(0, 4, 2):
        markup.row(buttons[i], buttons[i + 1])
    markup.row(BUTTON_RESTART)
    return markup


CHOICE_MARKUPS = {
    "a": arkan_markup(),
    "e": elder_markup(),
    "j": junior_markup(),
    "y": yard_markup()
}
