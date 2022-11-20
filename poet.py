import re
import urllib.request
import urllib.parse
import pafy

import flet
from flet import (
    Page,
    TextField,
    FloatingActionButton,
    Column,
    Row,
    Text,
    IconButton,
    OutlinedButton,
    Tabs,
    Image,
    border_radius,
    Tab,
    UserControl,
    AlertDialog,
    BottomSheet,
    Checkbox,
    colors,
    icons,
    Container
)


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
        self.display_task = Text(value=name(search(self.task_name)))
        im = imagelink(search(self.task_name))

        self.display_view = Row(
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
        )
        return Column(controls=[self.display_view])

    def delete_clicked(self, e):
        self.task_delete(self)


class MyApp(UserControl):
    def build(self):
        self.new_task = TextField(hint_text="Search song", expand=True)
        self.tasks = Column()

        self.items_left = Text("No song")

        return Column(
            width=600,
            controls=[
                Row([Text(value="Add", style="headlineMedium")], alignment="center"),
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(
                            icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
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
            if self.items_left.value == "3 song(s)":
                self.new_task.error_text = "You already add 3 songs"
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
        self.items_left.value = f"{count} song(s)"
        super().update()


def main(page: Page):
    page.title = "Poet Phleng"
    page.horizontal_alignment = "center"

    # call MyApp
    app = MyApp()

    page.add(app)


flet.app(target=main, view=flet.FLET_APP)
