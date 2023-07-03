import time
import json

import telebot
from telebot import types

from markups import CHOICE_MARKUPS


CHOICE_TEXTS = {
    "a": "Выберите ранг аркана",
    "e": "Выберите номер старшего аркана",
    "j": "Выберите номер числового аркана",
    "y": "Выберите титул придворного аркана",
}
ELEMENT_TYPES = ["w", "e", "f", "a"]
PREV_MSG_IDS = []
PREV_ARKAN_TYPE = ""
ARKAN_TYPE = ""
DEST_DIR = "imgs/"


with open("token.cfg", "r", encoding="utf-8") as f:
    token = f.read().rstrip()


bot = telebot.TeleBot(token)


def get_imgs(arkan_type, arkan_label):
    global DEST_DIR
    global ELEMENT_TYPES
    """assemble arkan images to be sent in one message based on their arkan type"""
    imgs = []
    if arkan_type == "e":
        name = f"{arkan_type}_{arkan_label}"
        file = open(f"{DEST_DIR}{name}.jpg", "rb")
    else:
        for element_type in ELEMENT_TYPES:
            name = f"{arkan_type}_{arkan_label}_{element_type}"
            file = open(f"{DEST_DIR}{name}.jpg", "rb")
            img = types.InputMediaPhoto(file)
            imgs.append(img)
    return imgs, file


def get_descs(arkan_type, arkan_label):
    global ELEMENT_TYPES
    descs = []
    with open("taro_info.json", "r", encoding="utf-8") as f:
        info = json.load(f)
    if arkan_type != "e":
        descs.append(info.get(f"{arkan_type}_{arkan_label}_h_desc", "..."))
        for element_type in ELEMENT_TYPES:
            descs.append(
                info.get(f"{arkan_type}_{arkan_label}_{element_type}_desc", "..."))
    else:
        descs.append(info.get(f"{arkan_type}_{arkan_label}_desc", "..."))
    desc = "\n\n".join(descs)
    return desc


def del_prev_msgs(chat_id, level):
    global PREV_MSG_IDS
    for msg_id in PREV_MSG_IDS[level:]:
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception as exc:
            print(exc)
    PREV_MSG_IDS = PREV_MSG_IDS[:level]


@bot.message_handler(content_types="text")
def get_text_messages(message):
    global PREV_MSG_IDS
    global CHOICE_TEXTS
    global CHOICE_MARKUPS
    match message.text:
        case "/taro":
            markup = CHOICE_MARKUPS["a"]
            text = CHOICE_TEXTS["a"]
            msg = bot.send_message(message.from_user.id,
                                   text=text, reply_markup=markup)
            PREV_MSG_IDS.append(msg.message_id)
        case "/start" | "/help":
            welcome_text = "Введите /taro чтобы начать выбор карты"
            bot.send_message(message.from_user.id, text=welcome_text)
        case _:
            error_text = "Я не знаю таких команд, напишите /help для помощи"
            bot.send_message(message.from_user.id, error_text)


@bot.callback_query_handler(func=lambda call: call.data == "re")
def callback_worker_0(call):
    global PREV_MSG_IDS
    global CHOICE_TEXTS
    global CHOICE_MARKUPS
    level = 0
    del_prev_msgs(call.message.chat.id, level)
    markup = CHOICE_MARKUPS["a"]
    text = CHOICE_TEXTS["a"]
    msg = bot.send_message(call.message.chat.id,
                           text=text, reply_markup=markup)
    PREV_MSG_IDS.append(msg.message_id)


@bot.callback_query_handler(func=lambda call: len(call.data) == 1)
def callback_worker_1(call):
    global PREV_MSG_IDS
    global CHOICE_TEXTS
    global CHOICE_MARKUPS
    level = 1
    del_prev_msgs(call.message.chat.id, level)
    match call.data:
        case "e":
            markup = CHOICE_MARKUPS["e"]
            text = CHOICE_TEXTS["e"]
        case "j":
            markup = CHOICE_MARKUPS["j"]
            text = CHOICE_TEXTS["j"]
        case "y":
            markup = CHOICE_MARKUPS["y"]
            text = CHOICE_TEXTS["y"]
    msg = bot.send_message(call.message.chat.id,
                           text=text, reply_markup=markup)
    PREV_MSG_IDS.append(msg.message_id)


@bot.callback_query_handler(func=lambda call: len(call.data) > 2)
def callback_worker_2(call):
    global PREV_ARKAN_TYPE
    global PREV_MSG_IDS
    level = 2
    del_prev_msgs(call.message.chat.id, level)
    arkan_type = call.data[0]
    arkan_label = call.data[2:]
    imgs, file = get_imgs(arkan_type, arkan_label)
    text = get_descs(arkan_type, arkan_label)
    match arkan_type:
        case "e":
            msg = bot.send_photo(call.message.chat.id, file)
            PREV_MSG_IDS.append(msg.message_id)
            for i in range(2):
                msg = bot.send_message(call.message.chat.id, text=text.split("|")[i], parse_mode="Markdown")
                PREV_MSG_IDS.append(msg.message_id)
        case "j" | "y":
            msgs = bot.send_media_group(call.message.chat.id, imgs)
            PREV_MSG_IDS += [msg.message_id for msg in msgs]
            msg = bot.send_message(call.message.chat.id, text=text, parse_mode="Markdown")
            PREV_MSG_IDS.append(msg.message_id)
    file.close()
    PREV_ARKAN_TYPE = arkan_type


def main():
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as exc:
            print(exc)
            time.sleep(15)


if __name__ == "__main__":
    main()
