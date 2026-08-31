import subprocess


def open_application(command):

    try:

        subprocess.Popen(
            [command],
            start_new_session=True
        )

        return f"{command} opened."

    except Exception as e:

        return f"Could not open {command}: {e}"


def open_calculator():

    return open_application("calc.exe")


def open_notepad():

    return open_application("notepad.exe")


def open_file_explorer():

    return open_application("explorer.exe")


def open_command_prompt():

    return open_application("cmd.exe")


def open_powershell():

    return open_application("powershell.exe")