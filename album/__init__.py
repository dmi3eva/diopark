import os
import json
from IPython.display import Image, display, HTML
Image('bp.png')

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
                display(HTML(f"<img src='{self.render_photo(_photo)}'>"))
                # display(self.render_photo(_photo))

    def render_photo(self, photo):
        path = photo["img"]
        return Image(path)
