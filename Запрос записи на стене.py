import vk_api
from config import LOGIN, PASSWORD, TOKEN
from datetime import datetime


def main():
    # login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    # try:
    #     vk_session.auth(token_only=True)
    # except vk_api.AuthError as error_msg:
    #     print(1, error_msg)
    #     return

    # Используем метод wall.get
    response = vk.wall.get(count=5, offset=1)
    # print(response, file=open("data.json", 'w', encoding="utf8"))
    if response['items']:
        for elem in response['items']:
            print(f'{elem["text"].rstrip()};')
            dt = str(datetime.fromtimestamp(elem["date"])).split()
            print(f"date: {dt[0]}, time: {dt[1]}")


if __name__ == '__main__':
    main()
