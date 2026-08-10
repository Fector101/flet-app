import flet as ft

def main(page: ft.Page):
    page.padding = 20

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Android Notify Test Panel",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Markdown(
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        expand=True,
                    ),
                    ft.Button(content="Check Permission"),
                    ft.Button(content="Ask Permission If Needed"),
                    ft.Button(content="Send Basic Notification"),
                    ft.Button(content="Run Tests"),
                    ft.Button(content="Refresh Log Output"),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            )
        ),
    )


if __name__ == "__main__":
    ft.run(main)
