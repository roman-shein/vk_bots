import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime
from config import TOKEN


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 230452724)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            text = event.obj.message['text']
            for word in ["время", "число", "дата", "день"]:
                if word in text:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=datetime.now().strftime("%A %H:%M:%S %d-%B-%Y"),
                                     random_id=0)
                    break
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Если вы напишите сообщение, где есть слова 'дата', 'число', 'день', 'время', то я напишу текущее время",
                                 random_id=0)


if __name__ == '__main__':
    main()
