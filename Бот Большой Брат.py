import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from config import TOKEN


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 230452724)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message["from_id"]
            vk = vk_session.get_api()
            response = vk.users.get(user_id=user_id, fields=["city"])
            # print(response, file=open('data.json', 'w', encoding="utf8"))
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Привет, {response[0]['first_name']}!",
                             random_id=0)
            if "city" in response[0]:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Как поживает {response[0]['city']['title']}?",
                                 random_id=0)


if __name__ == '__main__':
    main()
