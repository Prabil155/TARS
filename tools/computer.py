import requests


# ============================================================
# WINDOWS COMPUTER CONTROLLER
# ============================================================

COMPUTER_URL = "http://172.20.144.1:5001/computer"


class ComputerTool:

    def __init__(self):
        self.url = COMPUTER_URL

    # ========================================================
    # CORE HTTP CALL
    # ========================================================

    def call(self, action, **kwargs):

        try:

            response = requests.post(
                self.url,
                json={
                    "action": action,
                    **kwargs,
                },
                timeout=(5, 60),
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("success", False):

                return (
                    "Computer error: "
                    + str(
                        data.get(
                            "error",
                            "Unknown error",
                        )
                    )
                )

            return data.get(
                "result",
                "",
            )

        except requests.exceptions.ConnectionError as e:

            return (
                "Computer connection error: "
                "Windows computer controller is not running. "
                f"{e}"
            )

        except requests.exceptions.Timeout:

            return (
                "Computer error: "
                "Windows computer controller timed out."
            )

        except requests.exceptions.RequestException as e:

            return (
                f"Computer HTTP error: {e}"
            )

        except ValueError as e:

            return (
                f"Computer response error: {e}"
            )

        except Exception as e:

            return (
                f"Computer error: {e}"
            )

    # ========================================================
    # SCREEN
    # ========================================================

    def screen_size(self):

        return self.call(
            "screen_size"
        )

    def mouse_position(self):

        return self.call(
            "mouse_position"
        )

    def screenshot(self):

        return self.call(
            "screenshot"
        )

    # ========================================================
    # MOUSE
    # ========================================================

    def move_mouse(self, x, y):

        return self.call(
            "move_mouse",
            x=x,
            y=y,
        )

    def click(self, x=None, y=None):

        return self.call(
            "click",
            x=x,
            y=y,
        )

    def double_click(self, x=None, y=None):

        return self.call(
            "double_click",
            x=x,
            y=y,
        )

    def right_click(self, x=None, y=None):

        return self.call(
            "right_click",
            x=x,
            y=y,
        )

    def scroll(self, amount):

        return self.call(
            "scroll",
            amount=amount,
        )

    # ========================================================
    # KEYBOARD
    # ========================================================

    def type_text(self, text):

        return self.call(
            "type_text",
            text=text,
        )

    def press(self, key):

        return self.call(
            "press",
            key=key,
        )

    def hotkey(self, *keys):

        return self.call(
            "hotkey",
            keys=list(keys),
        )

    # ========================================================
    # APPLICATIONS
    # ========================================================

    def open_calculator(self):

        return self.call(
            "open_calculator"
        )

    def open_notepad(self):

        return self.call(
            "open_notepad"
        )

    def open_file_explorer(self):

        return self.call(
            "open_file_explorer"
        )

    def open_command_prompt(self):

        return self.call(
            "open_command_prompt"
        )

    def open_powershell(self):

        return self.call(
            "open_powershell"
        )

    def open_application(self, command):

        return self.call(
            "open_application",
            command=command,
        )

    def run_command(self, command):

        return self.call(
            "run_command",
            command=command,
        )

    def open_vscode(self):

        return self.call(
            "open_application",
            command="code",
        )

    def open_vscode_file(self, path):

        return self.call(
            "open_vscode_file",
            path=path,
        )
    def focus_vscode(self):

        return self.call(
            "focus_vscode"
        )

    def write_code_to_vscode(
        self,
        code,
        filename="tars_program.py"
    ):

        return self.call(
            "write_code_to_vscode",
            code=code,
            filename=filename,
        )


    # ========================================================
    # WINDOW
    # ========================================================

    def close_window(self):

        return self.call(
            "close_window"
        )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    computer = ComputerTool()

    print(
        "Screen:",
        computer.screen_size(),
    )

    print(
        "Mouse:",
        computer.mouse_position(),
    )