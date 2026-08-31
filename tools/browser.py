import subprocess


BRAVE_PATH = "/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"


def open_brave():
    subprocess.Popen(
        [BRAVE_PATH],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return "Brave browser opened successfully."


def search_brave(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")

    subprocess.Popen(
        [BRAVE_PATH, url],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return f"Searching for {query}"
