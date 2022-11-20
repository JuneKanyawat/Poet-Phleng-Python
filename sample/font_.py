import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = "light"
    page.padding = 100
    page.update()

    img = ft.Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit="contain",
    )
    images = ft.Row(expand=1, wrap=False, scroll="always")

    page.add(img, images)

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit="none",
                repeat="noRepeat",
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

ft.app(target=main)