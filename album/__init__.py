import os
import json

with open("diopark/data/map.json","r") as f:
  map = json.load(f)

class Album:
    def __init__(self, content):
        self.content = content

    def show(self):
        if len(self.content) > 20:
            print("Слишком много фотографий. Не могу показать.")
        else:
            for _photo in self.content:
                self.render_photo(_photo)

    def render_photo(self, photo):
        path = photo["img"]
        return open(path, 'rb')
