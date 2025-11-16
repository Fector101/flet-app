import os
import traceback
import unittest
import flet as ft
from contextlib import redirect_stdout
from android_notify.core import get_app_root_path, asks_permission_if_needed
from android_notify import Notification

class NotificationTester:
    def __init__(self, page):
        self.page = page
        self.logs_path = os.path.join(get_app_root_path(), 'last.txt')
        self.md_obj = None
        
    def create_ui(self):
        """Create the main UI layout"""
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text("Android Notify Test Results", 
                       size=24, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.colors.BLUE_900),
                ft.Divider(height=1, color=ft.colors.GREY_400)
            ]),
            padding=10
        )
        
        # Results display
        self.md_obj = ft.Markdown(
            "# Test Results will appear here\n\nRun tests or send notifications to see results.",
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: self.page.launch_url(e.data),
            expand=True,
        )
        
        results_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.RECEIPT),
                        title=ft.Text("Test Results", weight=ft.FontWeight.BOLD),
                    ),
                    ft.Divider(height=1),
                    ft.Container(
                        content=self.md_obj,
                        padding=15,
                        expand=True,
                    )
                ]),
                margin=10,
            ),
            expand=True,
        )
        
        # Control buttons
        button_style = ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_600,
            padding=15,
        )
        
        controls = ft.ResponsiveRow([
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.NOTIFICATIONS, color=ft.colors.GREEN),
                    ft.Text("Send Basic Notification", size=14),
                ]),
                on_click=self.send_basic,
                style=button_style,
                col={"sm": 12, "md": 6}
            ),
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.REFRESH, color=ft.colors.BLUE),
                    ft.Text("Refresh Results", size=14),
                ]),
                on_click=self.refresh_results,
                style=button_style,
                col={"sm": 12, "md": 6}
            ),
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.PLAY_ARROW, color=ft.colors.ORANGE),
                    ft.Text("Run Tests", size=14),
                ]),
                on_click=self.run_tests,
                style=button_style,
                col={"sm": 12, "md": 6}
            ),
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.SECURITY, color=ft.colors.PURPLE),
                    ft.Text("Check Permission", size=14),
                ]),
                on_click=self.check_permission,
                style=button_style,
                col={"sm": 12, "md": 6}
            ),
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.PERMISSION, color=ft.colors.RED),
                    ft.Text("Request Permission", size=14),
                ]),
                on_click=self.request_permission,
                style=button_style,
                col={"sm": 12, "md": 6}
            ),
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.IMAGE, color=ft.colors.TEAL),
                    ft.Text("Test Icon", size=14),
                ]),
                on_click=self.test_icon,
                style=button_style,
                col={"sm": 12, "md": 6}
            ),
        ])
        
        # Progress indicator
        self.progress = ft.ProgressBar(visible=False, width=400)
        self.status_text = ft.Text("", size=12, color=ft.colors.GREY_600)
        
        # Assemble the page
        self.page.add(
            header,
            results_card,
            ft.Container(
                content=ft.Column([
                    controls,
                    ft.Row([self.progress], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.status_text], alignment=ft.MainAxisAlignment.CENTER)
                ]),
                padding=15
            )
        )
    
    def update_status(self, message, show_progress=False):
        """Update status text and progress indicator"""
        self.status_text.value = message
        self.progress.visible = show_progress
        self.status_text.update()
        self.progress.update()
    
    def update_results(self, content):
        """Update the markdown results display"""
        self.md_obj.value = content
        self.md_obj.update()
    
    def send_basic(self, e):
        """Send a basic notification"""
        self.update_status("Sending notification...", True)
        try:
            Notification(title="Hello World", message="From android_notify").send()
            self.update_results("# ✅ Notification Sent Successfully\n\nBasic notification was sent successfully.")
            self.update_status("Notification sent successfully")
        except Exception as err:
            error_msg = f"# ❌ Notification Failed\n\nError: {err}\n\n```python\n{traceback.format_exc()}\n```"
            self.update_results(error_msg)
            self.update_status(f"Notification failed: {err}")
    
    def refresh_results(self, e):
        """Refresh the results display"""
        self.update_status("Refreshing results...", True)
        try:
            # Try to read from console output
            console_content = ""
            if os.getenv("FLET_APP_CONSOLE"):
                with open(os.getenv("FLET_APP_CONSOLE"), "r") as f:
                    console_content = f.read()
            
            # Try to read from log file
            log_content = ""
            if os.path.exists(self.logs_path):
                with open(self.logs_path, 'r') as logf:
                    log_content = logf.read()
            
            combined_content = f"# 🔄 Refreshed Results\n\n## Console Output:\n```\n{console_content}\n```\n\n## Log File:\n```\n{log_content}\n```"
            self.update_results(combined_content)
            self.update_status("Results refreshed")
        except Exception as err:
            self.update_results(f"# ❌ Error Refreshing\n\nError: {err}")
            self.update_status(f"Refresh failed: {err}")
    
    def run_tests(self, e):
        """Run unit tests"""
        self.update_status("Running tests...", True)
        tests_path = self.ensure_tests_folder()
        
        try:
            with open(self.logs_path, "w") as logf, redirect_stdout(logf):
                loader = unittest.TestLoader()
                suite = loader.discover(start_dir=tests_path, pattern="test_*.py")
                test_count = suite.countTestCases()
                
                print(f"Discovered {test_count} test cases")
                if test_count == 0:
                    print("No tests found in tests/ directory")
                
                runner = unittest.TextTestRunner(stream=logf, verbosity=2)
                result = runner.run(suite)
            
            # Read and display results
            with open(self.logs_path, "r") as logf:
                log_content = logf.read()
            
            result_msg = f"# 🧪 Tests Complete\n\n**Test Cases:** {test_count}\n**Log File:** `{self.logs_path}`\n\n## Results:\n```\n{log_content}\n```"
            self.update_results(result_msg)
            self.update_status(f"Tests complete - {test_count} cases run")
            
        except Exception as err:
            error_msg = f"# ❌ Test Error\n\nError running tests:\n```python\n{traceback.format_exc()}\n```"
            self.update_results(error_msg)
            self.update_status(f"Test error: {err}")
    
    def check_permission(self, e):
        """Check notification permission status"""
        self.update_status("Checking permission...", True)
        try:
            from android_notify import NotificationHandler
            has_perm = NotificationHandler.has_permission()
            status = "✅ Granted" if has_perm else "❌ Denied"
            self.update_results(f"# 🔐 Permission Status\n\n**Notification Permission:** {status}")
            self.update_status(f"Permission: {'Granted' if has_perm else 'Denied'}")
        except Exception as err:
            self.update_results(f"# ❌ Permission Check Failed\n\nError: {err}")
            self.update_status(f"Permission check failed: {err}")
    
    def request_permission(self, e):
        """Request notification permission"""
        self.update_status("Requesting permission...", True)
        try:
            asks_permission_if_needed()
            self.update_results("# 📝 Permission Requested\n\nNotification permission has been requested.")
            self.update_status("Permission requested")
        except Exception as err:
            self.update_results(f"# ❌ Permission Request Failed\n\nError: {err}")
            self.update_status(f"Permission request failed: {err}")
    
    def test_icon(self, e):
        """Test notification with icon"""
        self.update_status("Testing notification icon...", True)
        try:
            n = Notification(title="Icon Test", message="Testing packaged icon")
            n.tell()  # This might show the notification
            self.update_results("# 🖼️ Icon Test\n\nNotification with icon has been triggered.")
            self.update_status("Icon test completed")
        except Exception as err:
            self.update_results(f"# ❌ Icon Test Failed\n\nError: {err}")
            self.update_status(f"Icon test failed: {err}")
    
    def ensure_tests_folder(self):
        """Ensure tests folder exists"""
        try:
            base_path = get_app_root_path()
        except Exception:
            base_path = os.path.dirname(__file__)
        
        tests_path = os.path.join(base_path, "tests")
        os.makedirs(tests_path, exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = os.path.join(tests_path, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, "w").close()
        
        return tests_path

def main(page: ft.Page):
    # Page configuration
    page.title = "Android Notify Tester"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 10
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Initialize and create UI
    tester = NotificationTester(page)
    tester.create_ui()


ft.app(main)
