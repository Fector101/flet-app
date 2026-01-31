import flet as ft


def on_click(e):
    from jnius import autoclass
    Log = autoclass("android.util.Log")  # TODO Replace when on android
    Log.e("python","found java logger")

    from android_notify import Notification
    Notification(title="Hello Earth").send()

    Log.e("test","found android notify")

def main(page: ft.Page):
    page.title = "Logging Example"
    page.floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=on_click
        )

ft.app(target=main)
