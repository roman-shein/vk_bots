import vk_api
from config import LOGIN, PASSWORD, TOKEN


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
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




if __name__ == "__main__":
    main()
