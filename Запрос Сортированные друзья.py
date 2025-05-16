import vk_api
from config import LOGIN, PASSWORD
from datetime import datetime


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
    # Используем метод wall.get
    arr = []
    response = vk.friends.get(fields="city,bdate")
    # print(response, file=open("data.json", 'w', encoding="utf8"))
    if response["items"]:
        for friend in response["items"]:
            arr.append([])
            if "last_name" in friend:
                surname = friend["last_name"]
                arr[-1].append(surname)
            if "first_name" in friend:
                name = friend["first_name"]
                arr[-1].append(name)
            if "bdate" in friend:
                bdate = friend["bdate"]
                arr[-1].append(bdate)
            if "city" in friend:
                city = friend["city"]["title"]
                arr[-1].append(city)

    for el in sorted(arr, key=lambda x: x[0]):
        print(*el)


if __name__ == '__main__':
    main()