from base64 import b64encode
from IPython.display import Image, display, HTML

WITHOUT = {
    'desertcactus': 'Кактус в пустыне',
    'desertstone': 'Пустыня',
    'greenfield': 'Поле',
    'mountain': 'Гора',
    'rainbow': 'Радуга',
    'reeds': 'Поле с гречихой',
    'sea': 'Море',
    'swamp': 'Болото'
}

ANIMALS = {
    'barrel': 'Бочка',
    'criminals': 'Двое подозрительных личностей с топорами',
    'elephants': 'Слон',
    'geese': 'Гусь',
    'gekkons': 'Геккон',
    'koalas': 'Коала',
    'loafers': 'Ленивец',
    'zebras': 'Зеленая зебра'
}

LANDSCAPE = {
    'desertcactus': 'в пустыне с кактусами',
    'desertstone': 'в пустыне',
    'greenfield': 'в поле',
    'mountain': 'в горах',
    'rainbow': 'под радугой',
    'reeds': 'в гречишном поле',
    'sea': 'в море',
    'swamp': 'у болота'
}

class Album:
    def __init__(self, content):
        self.content = content

    def print_size(self):
        print(f"Количество фотографий в альбоме: {len(self.content)}")

    def print_avg_light(self):
        if len(self.content) == 0:
            print("В альбоме нет фотографий")
        else:
            lights = [int(_c["light"]) for _c in self.content]
            print(f"Средняя освещенность: {sum(lights) / len(lights)}")


    def show(self):
        if len(self.content) > 20:
            print("Слишком много фотографий. Не могу показать.")
        else:
            for _photo in self.content:
                display(HTML(f"<img src='{self.render_photo(_photo)}' width='130'>"))
                # display(self.render_photo(_photo))



    def get_info(self, photo_path):
        if "without_animals" in photo_path:
            for _key, _descr in WITHOUT.items():
                if _key in photo_path:
                    return _descr
            return 'Ничего не видно'
        who = 'Неопознанное животное'
        where = 'непонятно, где'
        for _key, _descr in ANIMALS.items():
            if _key in photo_path:
                who = _descr
        for _key, _descr in LANDSCAPE.items():
            if _key in photo_path:
                where = _descr
        return f"{who} {where}"


    def print_info(self):
        if len(self.content) > 20:
            print("Слишком много фотографий. Не могу их все описать.")
        for ind, _photo in enumerate(self.content):
            print(f"Фото №{ind + 1}: {self.get_info(_photo['img'])}")


    def render_photo(self, photo):
        try:
            path = photo["img"]
            img = open(path, 'rb').read()
        except:
            img = open("diopark/photos/without_animals/reeds.png", 'rb').read()
        data_url = 'data:image/jpeg;base64,' + b64encode(img).decode()
        return data_url
        # return Image(path)

