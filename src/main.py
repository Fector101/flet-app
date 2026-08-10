import logging
import os, traceback, unittest
import flet as ft

from contextlib import redirect_stdout

from android_notify.config import on_android_platform

from android_notify.core import get_app_root_path, asks_permission_if_needed
from android_notify import Notification
from android_notify.internal.logger import android_print, logger
from android_notify.config import __version__

android_print("successful imported android_notify...")

md_cache = ""
counter = 0

logger.setLevel(logging.DEBUG)

def main(page: ft.Page):
    page.padding = 20

    # Path to log file
    try:
        logs_path = os.path.join(get_app_root_path(), "test_logs.txt") if on_android_platform() else os.path.join(os.getcwd(), "src", "test_logs.txt")
    except Exception as error_local_test_path:
        android_print(f"error_local_test_path: {error_local_test_path}")
        logs_path = "/sdcard/test_logs.txt"   # fallback for safety

    # Markdown output viewer
    md_view = ft.Markdown(
        md_cache,
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data),
        expand=True,
    )

    # UTIL: Refresh console output
    def refresh_console(_):
        global md_cache, counter
        counter += 1
        print("This is a print statement:", counter,"\n")

        try:
            # APP console output (if running inside Flet debug runner)
            flet_console = os.getenv("FLET_APP_CONSOLE")
            if flet_console and os.path.exists(flet_console):
                with open(flet_console, "r") as f:
                    md_cache = f.read()

            # android-notify log file
            if os.path.exists(logs_path):
                with open(logs_path, "r") as f:
                    md_cache = f.read() + "\n\n" + md_cache

            md_view.value = md_cache
        except Exception as err:
            md_view.value = f"❌ Error reading log: {err}"
        md_view.update()

    # Send a basic notification
    def send_basic(_):
        try:
            Notification(title=__version__+" Hello World", message="From android_notify").send()
        except Exception as err:
            md_view.value = f"❌ Notification error:\n{err}"
            md_view.update()

    # Ensure tests folder (safe, auto-created)
    def ensure_tests_folder():
        try:
            base_path = get_app_root_path() if on_android_platform() else os.path.join(os.getcwd(), "src")
        except Exception as error_getting_app_root_path:
            android_print(error_getting_app_root_path)
            base_path = os.path.dirname(__file__)

        tests_path = os.path.join(base_path, "tests")
        os.makedirs(tests_path, exist_ok=True)

        init_file = os.path.join(tests_path, "__init__.py")
        if not os.path.exists(init_file):
            android_print("No tests.__init__ file")
            with open(init_file, "w") as f:
                f.write("")     # create empty file

        return tests_path

    # Run unittest test suite
    def run_tests(_):
        android_print('clicked')
        tests_path = ensure_tests_folder()
        android_print(f"test folder: {tests_path}, Test File exists: {os.path.exists(os.path.join(tests_path,'test_android_notify_full.py'))}")
        try:
            android_print("running tests")
            with open(logs_path, "w") as logf, redirect_stdout(logf):
                loader = unittest.TestLoader()
                suite = loader.discover(start_dir=tests_path, pattern="test_*.py")
                android_print(f"Discovered tests: {suite.countTestCases()}")

                if suite.countTestCases() == 0:
                    android_print("⚠ No tests found")

                runner = unittest.TextTestRunner(stream=logf, verbosity=2)
                runner.run(suite)
            print("ran all tests")

            md_view.value = f"Tests complete.\nLog saved at:\n`{logs_path}`"
            android_print(str(md_view.value))
        except Exception as err:
            android_print(err)
            md_view.value = f"❌ Test error:\n{traceback.format_exc()}"

        md_view.update()

    # Check permission
    def check_permission(_):
        try:
            from android_notify import NotificationHandler
            state = f"Permission: {NotificationHandler.has_permission()}"
            md_view.value = state
            android_print(state)
            md_view.update()
        except Exception as err:
            md_view.value = f"Error checking permission:\n{err}"
            md_view.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Android Notify Test Panel",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    md_view,
                    ft.Button(
                        content="Check Permission",
                        on_click=check_permission,
                    ),
                    ft.Button(
                        content="Ask Permission If Needed",
                        on_click=lambda _: asks_permission_if_needed(),
                    ),
                    ft.Button(
                        content="Send Basic Notification",
                        on_click=send_basic,
                    ),
                    ft.Button(
                        content="Run Tests",
                        on_click=run_tests,
                    ),
                    ft.Button(
                        content="Refresh Log Output",
                        on_click=refresh_console,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            )
        ),
    )


if __name__ == "__main__":
    ft.run(main)
