import re
import urllib.request
import urllib.parse
import pafy
from random import *

import flet
from flet import (
    Page,
    padding,
    TextField,
    Column,
    Icon,
    AppBar,
    Row,
    Text,
    IconButton,
    Image,
    border_radius,
    UserControl,
    ElevatedButton,
    colors,
    icons,
    Container
)
mylist = ["D1ADFC", "B0B2FF", "A8CEFB"]

def search(name):  # หาลิ้ง youtube จากชื่อ
    query_string = urllib.parse.urlencode({"search_query": name})
    formatUrl = urllib.request.urlopen(
        "https://www.youtube.com/results?" + query_string)

    search_results = re.findall(
        r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip2 = "{}".format(search_results[0])
    return clip2


def picture(link, name):
    video = pafy.new(link)
    picture_url = video.bigthumbhd  # url รูป title ของ video
    path = '/Users/Onlyjune/Desktop/untitled folder 3/file_save/' + \
        name+'.jpg'  # path ที่ต้องการจะ save + ชื่อไฟล์
    urllib.request.urlretrieve(picture_url, path)  # ดาวโหลด
    return path


def name(link):
    video = pafy.new(link)
    name_video = video.title  # ชื่อวิดิโอ
    return name_video


def imagelink(url):
    urls = "https://img.youtube.com/vi/" + url + "/0.jpg"
    print(urls)
    return urls


class Song(UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.display_task = Text(value=name(search(self.task_name)),expand=True)
        im = imagelink(search(self.task_name))

        self.display_view = Container(
            Row(
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    Image(
                        src=f"{im}",
                        width=100,
                        height=100,
                        fit="contain",
                        border_radius=border_radius.all(10),
                    ),
                    self.display_task,
                    Row(
                        spacing=0,
                        controls=[
                            IconButton(
                                icons.DELETE_OUTLINE,
                                on_click=self.delete_clicked,
                            ),
                        ],
                    ),
                ],
            ),
            bgcolor=colors.WHITE,
            padding=padding.only(left=10),
            border_radius=10,
        )
        return Column(controls=[self.display_view])

    def delete_clicked(self, e):
        self.task_delete(self)


class MyApp(UserControl):
    def build(self):
        self.new_task = TextField(
            hint_text="Search song",
            expand=True,
            filled=True,
            border_radius=30,
            border_color=colors.TRANSPARENT,
            bgcolor=colors.WHITE
        )
        self.tasks = Column()

        self.items_left = Text("No song")       

        return Column(
            width=600,
            controls=[
                Row([Text(value="Add song", style="titleLarge", font_family="Arial")], alignment="center"),
                Row(
                    controls=[
                        self.new_task,
                        ElevatedButton(
                            "Send ➤", on_click=self.add_clicked, bgcolor="0xffB0B2FF", color=colors.WHITE),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.items_left,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        if not self.new_task.value:
            self.new_task.error_text = "Please type something"
            self.update()
        else:
            if self.items_left.value == "5/5":
                self.new_task.error_text = "You already add 5 songs"
                self.update()
                self.new_task.value = ""
            else:
                self.up()

    def up(self):
        task = Song(self.new_task.value, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.songupdate()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.songupdate()

    def songupdate(self):
        count = 0
        for task in self.tasks.controls:
            if not task.completed:
                count += 1
        self.items_left.value = f"{count}/5"
        super().update()


def main(page: Page):
    page.fonts = {
        "Arial": "/fonts/Arial Rounded Bold.ttf",
        "Berlyna": "/fonts/BerlynaDemo-Pp8r.ttf",
        "Comfortaa": "/fonts/Comfortaa-VariableFont_wght.ttf"
    }
    page.title = "Poet Phleng"
    page.horizontal_alignment = "center"
    page.bgcolor = "0xffE1EAFF"
    page.scroll = True
    page.appbar = AppBar(
        leading=Icon(icons.MUSIC_NOTE_SHARP),
        leading_width=40,
        title=Text("Poet Phleng", font_family="Arial"),
        center_title=False,
        bgcolor=colors.WHITE,
    )

    # call MyApp
    app = MyApp()

    page.add(app)


flet.app(target=main, assets_dir="assets")
