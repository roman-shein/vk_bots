import vk_api
from flask import Flask, render_template
from config import LOGIN, PASSWORD
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


def get_state(group_id):
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
        return error_msg
    vk = vk_session.get_api()
    arr = vk.stats.get(group_id=group_id, fields='reach')[:10]
    # with open("data.json", 'w', encoding="utf8") as fin:
    #     json.dump(arr, fin)
    # print(arr, file=open("data.json", 'w', encoding="utf8"))
    stats = []
    res = None
    for elem in arr:
        if elem['visitors']['visitors'] > 0:
            if 'activity' in elem:
                res = elem
            else:
                stats.append(elem)
    if res is not None:
        likes, comments, subscribed = 0, 0, 0
        if "activity" in res:
            if "likes" in res["activity"]:
                likes = res['activity']['likes']
            if "comments" in res["activity"]:
                comments = res['activity']['comments']
            if "subscribed" in res["activity"]:
                subscribed = res['activity']['likes']

        age = []
        for elem in res['visitors']['age']:
            age.append((elem['value'], elem['count']))

        cities = set()
        for elem in res['visitors']['cities']:
            cities.add(elem['name'])

        return likes, comments, subscribed, age, cities
    return None


@app.route("/vk_stat/<int:group_id>")
def index(group_id):
    arr = get_state(group_id)
    likes, comments, subscribed, age, cities = 0, 0, 0, 0, 0
    if arr is not None:
        likes, comments, subscribed, age, cities = arr
    params = {
        "likes": likes,
        "comments": comments,
        "subscribed": subscribed,
        "age": age,
        "cities": cities
    }
    return render_template("vk.html", **params)


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == "__main__":
    main()
