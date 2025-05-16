import requests
import vk_api
import wikipedia
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import TOKEN

wikipedia.set_lang("ru")


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 230452724)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            text = event.obj.message["text"]
            try:
                search = wikipedia.page(text)
            except Exception:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Ваш запрос некорректен!",
                                 random_id=0)
                continue
            res = search.content[:100]
            link = search.url
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"{res}\n{link}",
                             random_id=0)



if __name__ == "__main__":
    main()
