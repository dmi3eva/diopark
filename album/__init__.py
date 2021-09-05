from base64 import b64encode
from IPython.display import Image, display, HTML


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
                display(HTML(f"<img src='{self.render_photo(_photo)}' width='100'>"))
                # display(self.render_photo(_photo))


    def render_photo(self, photo):
        try:
            path = photo["img"]
            img = open(path, 'rb').read()
        except:
            img = open("diopark/photos/without_animals/reeds.png", 'rb').read()
        data_url = 'data:image/jpeg;base64,' + b64encode(img).decode()
        return data_url
        # return Image(path)
