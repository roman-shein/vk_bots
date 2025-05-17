import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import TOKEN
import datetime


users = {}


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 230452724)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message["from_id"]
            if user_id not in users:
                users[user_id] = None
                vk.messages.send(
                    user_id=user_id,
                    message="Привет! Напиши мне дату в формате YYYY-MM-DD, и я скажу какой это день недели",
                    random_id=0
                )
            else:
                text = event.obj.message["text"].split('-')
                arr = list(map(lambda x: x.isdigit(), text))
                if len(arr) != 3 or not all(arr):
                    vk.messages.send(
                        user_id=user_id,
                        message="Неверный формат даты!",
                        random_id=0
                    )
                    continue
                text = list(map(int, text))
                try:
                    md = datetime.date(text[0], text[1], text[2])
                except ValueError:
                    vk.messages.send(
                        user_id=user_id,
                        message="Неверный формат даты!",
                        random_id=0
                    )
                    continue

                vk.messages.send(
                    user_id=user_id,
                    message=md.strftime("%A"),
                    random_id=0
                )


if __name__ == "__main__":
    main()
