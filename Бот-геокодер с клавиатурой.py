import vk_api
from config import LOGIN, PASSWORD, TOKEN
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
import requests

users = {}


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


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 230452724)
    upload = vk_api.VkUpload(vk_session)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message["from_id"]
            if user_id not in users:
                users[user_id] = [False, False]
                vk.messages.send(
                    user_id=user_id,
                    message="Привет! Напиши мне название географического объекта, и я пришлю его фото на карте",
                    random_id=0
                )
            elif not users[user_id][0]:
                name = event.obj.message["text"]
                try:
                    ll, spn = get_coords(name)
                    users[user_id][0] = True
                    vk.messages.send(
                        user_id=user_id,
                        message="Укажите тип карты",
                        random_id=0,
                        keyboard=create_keyboard()
                    )
                except NameError:
                    vk.messages.send(
                        user_id=user_id,
                        message="Ошибка! Объект не найден",
                        random_id=0
                    )
            elif not users[user_id][1]:
                users[user_id] = [False, False]
                text = event.obj.message["text"]
                image = get_image(ll, spn, text)
                if image is None:
                    vk.messages.send(
                        user_id=user_id,
                        message=f"Ошибка! Объект не найден. Что вы еще хотите увидеть?",
                        random_id=0,
                        keyboard=VkKeyboard.get_empty_keyboard()
                    )
                else:
                    upload_image = upload.photo_messages(photos="map.png")
                    res = f"photo{upload_image[0]['owner_id']}_{upload_image[0]['id']}"
                    vk.messages.send(
                        user_id=user_id,
                        message=f"Это {name}. Что вы еще хотите увидеть?",
                        random_id=0,
                        keyboard=VkKeyboard.get_empty_keyboard(),
                        attachment=res
                    )


def create_keyboard():
    keyboard = VkKeyboard(one_time=True)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться

    keyboard.add_button("map", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("driving", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)

    keyboard.add_line()  # Обозначает добавление новой строки
    keyboard.add_button("transit", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("admin ", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def get_coords(name_obj):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_api_key = "cf79098a-155e-47b7-9b49-b55b4461472d"
    geocoder_params = {
        "apikey": geocoder_api_key,
        "geocode": name_obj,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params).json()
    response = response["response"]["GeoObjectCollection"]["featureMember"]
    if not response:
        raise NameError
    lower_corner = response[0]["GeoObject"]['boundedBy']['Envelope']['lowerCorner']
    upper_corner = response[0]["GeoObject"]['boundedBy']['Envelope']['upperCorner']

    lon1, lat1 = map(float, lower_corner.split())
    lon2, lat2 = map(float, upper_corner.split())

    ll = ','.join(response[0]["GeoObject"]["Point"]["pos"].split())

    spn = str(abs(lon1 - lon2)), str(abs(lat1 - lat2))
    spn = ",".join(spn)
    return ll, spn


def get_image(ll, spn, maptype):
    static_api_server = "https://static-maps.yandex.ru/v1?"
    static_api_key = "318965a9-b51c-41fb-a672-2acad73bc050"
    static_api_params = {
        "apikey": static_api_key,
        "ll": ll,
        "spn": spn,
        "maptype": maptype
    }
    response = requests.get(static_api_server, params=static_api_params)
    if not response:
        return None

    map_file = "map.png"

    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


if __name__ == "__main__":
    main()
