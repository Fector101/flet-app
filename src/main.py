import os
import traceback
import unittest
from contextlib import redirect_stdout

import flet as ft
from jnius import autoclass

from android_notify.core import get_app_root_path, asks_permission_if_needed
from android_notify import Notification


# -------------------------------------------------
# Safe Java class existence check
# -------------------------------------------------
def java_class_exists(class_name: str) -> bool:
    """
    Check if a Java class exists on Android.
    Uses autoclass() with exception catching to prevent crashes.
    """
    try:
        autoclass(class_name)  # Try to load the class
        return True
    except Exception as e:
        print("reason:",e)
        traceback.print_exc()
        # Any failure (ClassNotFound, NoClassDefFoundError, static init error)
        return False


# -------------------------------------------------
# Main Flet app
# -------------------------------------------------
def main(page: ft.Page):
    page.title = "Android Java Class Probe"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 20

    # -------------------------------------------------
    # Header
    # -------------------------------------------------
    page.add(
        ft.Text(
            "Android Notify Test Panel",
            size=28,
            weight=ft.FontWeight.BOLD,
        )
    )

    # -------------------------------------------------
    # Log path
    # -------------------------------------------------
    try:
        logs_path = os.path.join(get_app_root_path(), "last.txt")
    except Exception:
        logs_path = "/sdcard/last.txt"

    # -------------------------------------------------
    # Markdown output
    # -------------------------------------------------
    md_view = ft.Markdown(
        "",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        expand=True,
    )
    page.add(md_view)

    # -------------------------------------------------
    # Java class input
    # -------------------------------------------------
    class_input = ft.TextField(
        label="Java Class Name",
        hint_text="android.app.Notification | androidx.core.app.ActivityCompat",
        expand=True,
    )

    # -------------------------------------------------
    # Handlers
    # -------------------------------------------------
    def check_class(_):
        class_name = class_input.value.strip()

        if not class_name:
            md_view.value = "⚠ Please enter a Java class name"
            md_view.update()
            return

        try:
            exists = java_class_exists(class_name)
            md_view.value = (
                f"✅ **Class exists**\n\n`{class_name}`"
                if exists
                else f"❌ **Class NOT found**\n\n`{class_name}`"
            )
        except Exception as err:
            # Prevent crashes even if the class has static init issues
            md_view.value = f"💥 Error checking class `{class_name}`:\n```\n{err}\n```"

        md_view.update()

    def send_basic(_):
        try:
            Notification(
                title="Hello World",
                message="From android_notify",
            ).send()
            md_view.value = "✅ Notification sent"
        except Exception as err:
            md_view.value = f"❌ Notification error:\n```\n{err}\n```"
        md_view.update()

    def refresh_console(_):
        try:
            content = ""
            if os.path.exists(logs_path):
                with open(logs_path, "r") as f:
                    content = f.read()
            md_view.value = content or "ℹ No logs yet"
        except Exception as err:
            md_view.value = f"❌ Log read error:\n{err}"
        md_view.update()

    def ensure_tests_folder():
        try:
            base = get_app_root_path()
        except Exception:
            base = os.path.dirname(__file__)

        tests_path = os.path.join(base, "tests")
        os.makedirs(tests_path, exist_ok=True)

        init_file = os.path.join(tests_path, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, "w").close()

        return tests_path

    def run_tests(_):
        try:
            tests_path = ensure_tests_folder()
            with open(logs_path, "w") as logf, redirect_stdout(logf):
                loader = unittest.TestLoader()
                suite = loader.discover(tests_path, pattern="test_*.py")

                print("Discovered tests:", suite.countTestCases())

                runner = unittest.TextTestRunner(stream=logf, verbosity=2)
                runner.run(suite)

            md_view.value = f"✅ Tests finished\n\nLog saved to:\n`{logs_path}`"
        except Exception:
            md_view.value = f"❌ Test error:\n```\n{traceback.format_exc()}\n```"

        md_view.update()

    # -------------------------------------------------
    # UI layout
    # -------------------------------------------------
    page.add(
        ft.Column(
            [
                ft.Text("Java Class Probe", size=20, weight=ft.FontWeight.BOLD),
                class_input,
                ft.OutlinedButton("Check Class Exists", on_click=check_class),
                ft.Divider(),
                ft.OutlinedButton("Ask Permission If Needed", on_click=lambda _: asks_permission_if_needed()),
                ft.OutlinedButton("Send Basic Notification", on_click=send_basic),
                ft.OutlinedButton("Run Tests", on_click=run_tests),
                ft.OutlinedButton("Refresh Log Output", on_click=refresh_console),
            ],
            expand=False,
        )
    )


# -------------------------------------------------
# Run app
# -------------------------------------------------
ft.app(main)
