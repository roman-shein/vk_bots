import vk_api
from config import LOGIN, PASSWORD, TOKEN
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import choice
from datetime import datetime


PHOTOS = []

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    # или код из приложения - генератора кодов
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def get_photos():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        captcha_handler=captcha_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.photos.get(album_id=305551664, group_id=230452724)
    # print(response, file=open("data.json", 'w', encoding="utf8"))
    if response["items"]:
        for el in response["items"]:
            url = el["orig_photo"]["url"]
            photo_id = el["id"]
            PHOTOS.append(photo_id)


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 230452724)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            photo_id = choice(PHOTOS)
            attachment = f'photo-230452724_{photo_id}'
            user_id = event.obj.message["from_id"]
            response = vk.users.get(user_id=user_id, fields=["city"])
            vk.messages.send(
                user_id=event.obj.message['from_id'],
                message=f"Привет, {response[0]['first_name']}!",
                random_id=0,
                attachment=attachment
            )


if __name__ == "__main__":
    get_photos()
    main()
