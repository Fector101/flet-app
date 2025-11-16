import os, traceback, io, sys, unittest
import flet as ft
from contextlib import redirect_stdout
from android_notify.core import get_app_root_path, asks_permission_if_needed
from android_notify import Notification

# Global log mirror
md_cache = ""
counter = 0


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 20

    page.add(ft.Text(
        "Android Notify Test Panel",
        size=28,
        weight=ft.FontWeight.BOLD,
    ))

    # Path to log file
    try:
        logs_path = os.path.join(get_app_root_path(), "last.txt")
    except Exception:
        logs_path = "/sdcard/last.txt"   # fallback for safety

    # Markdown output viewer
    md_view = ft.Markdown(
        md_cache,
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data),
        expand=True,
    )
    page.add(md_view)

    # ---------------------------------------------------
    # UTIL: Refresh console output
    # ---------------------------------------------------
    def refresh_console(_):
        nonlocal md_cache, counter
        counter += 1
        print("Refresh attempt:", counter)

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

    # ---------------------------------------------------
    # Send a basic notification
    # ---------------------------------------------------
    def send_basic(_):
        try:
            Notification(title="Hello World", message="From android_notify").send()
        except Exception as err:
            md_view.value = f"❌ Notification error:\n{err}"
            md_view.update()

    # ---------------------------------------------------
    # Show packaged icon (debug)
    # ---------------------------------------------------
    def see_packaged_icon(_):
        try:
            n = Notification(title="Icon Test", message="Checking icon load…")
            n.tell()     # non-sending debug function
        except Exception as err:
            md_view.value = f"❌ Icon test error:\n{err}"
            md_view.update()

    # ---------------------------------------------------
    # Ensure tests folder (safe, auto-created)
    # ---------------------------------------------------
    def ensure_tests_folder():
        try:
            base_path = get_app_root_path()
        except Exception:
            base_path = os.path.dirname(__file__)

        tests_path = os.path.join(base_path, "tests")
        os.makedirs(tests_path, exist_ok=True)

        init_file = os.path.join(tests_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("")     # create empty file

        return tests_path

    # ---------------------------------------------------
    # Run unittest test suite
    # ---------------------------------------------------
    def run_tests(_):
        tests_path = ensure_tests_folder()

        try:
            with open(logs_path, "w") as logf, redirect_stdout(logf):
                loader = unittest.TestLoader()
                suite = loader.discover(start_dir=tests_path, pattern="test_*.py")

                print("Discovered tests:", suite.countTestCases())

                if suite.countTestCases() == 0:
                    print("⚠ No tests found")

                runner = unittest.TextTestRunner(stream=logf, verbosity=2)
                runner.run(suite)

            md_view.value = f"Tests complete.\nLog saved at:\n`{logs_path}`"
        except Exception as err:
            md_view.value = f"❌ Test error:\n{traceback.format_exc()}"

        md_view.update()

    # ---------------------------------------------------
    # Check permission
    # ---------------------------------------------------
    def check_permission(_):
        try:
            from android_notify import NotificationHandler
            md_view.value = f"Permission: {NotificationHandler.has_permission()}"
            md_view.update()
        except Exception as err:
            md_view.value = f"Error checking permission:\n{err}"
            md_view.update()

    # ---------------------------------------------------
    # Add buttons
    # ---------------------------------------------------
    page.add(
        ft.Column([
            ft.OutlinedButton("Send Basic Notification", on_click=send_basic),
            ft.OutlinedButton("Refresh Log Output", on_click=refresh_console),
            ft.OutlinedButton("Run Tests", on_click=run_tests),
            ft.OutlinedButton("Check Permission", on_click=check_permission),
            ft.OutlinedButton("Ask Permission If Needed", on_click=lambda _: asks_permission_if_needed()),
            ft.OutlinedButton("See Packaged Icon", on_click=see_packaged_icon),
        ], expand=False)
    )


ft.app(main)
