

import json
import ollama
import subprocess


# =========================
# SYSTEM TOOLS
# =========================


def open_brave():
    subprocess.Popen([
        "/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    ])

    return "Brave browser opened successfully."

def get_cpu_info():
    result = subprocess.run(
        ["lscpu"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "Model name:" in line:
            return line.split(":", 1)[1].strip()

    return "CPU information not found."


def get_ram_info():
    result = subprocess.run(
        ["free", "-h"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if line.startswith("Mem:"):
            parts = line.split()
            return {
                "total": parts[1],
                "used": parts[2],
                "available": parts[6]
            }

    return "RAM information not found."


def get_disk_info():
    result = subprocess.run(
        ["df", "-h", "/"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    if len(lines) >= 2:
        parts = lines[1].split()

        return {
            "total": parts[1],
            "used": parts[2],
            "available": parts[3],
            "usage": parts[4]
        }

    return "Disk information not found."


def get_os_info():
    result = subprocess.run(
        ["lsb_release", "-ds"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout.strip()

    return "Operating system information not found."


def get_battery_info():
    result = subprocess.run(
        ["bash", "-c", "upower -i $(upower -e | grep BAT | head -1)"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return "Battery information unavailable."

    for line in result.stdout.splitlines():
        if "percentage:" in line:
            return line.strip()

    return "Battery information unavailable."


# =========================
# TOOL DEFINITIONS
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "open_brave",
            "description": "Open the Brave web browser on the Windows computer.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
       } 
    },


    {
        "type": "function",
        "function": {
            "name": "get_cpu_info",
            "description": "Get the exact CPU model of this computer.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {

        "type": "function",
        "function": {
            "name": "get_ram_info",
            "description": "Get current RAM usage.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_disk_info",
            "description": "Get disk space usage for the main Linux filesystem.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_os_info",
            "description": "Get the Linux operating system information.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_battery_info",
            "description": "Get the current laptop battery percentage.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# =========================
# TOOL EXECUTION
# =========================

def execute_tool(name):
    if name == "open_brave":
        return open_brave()

    if name == "get_cpu_info":
        return get_cpu_info()

    if name == "get_ram_info":
        return get_ram_info()

    if name == "get_disk_info":
        return get_disk_info()

    if name == "get_os_info":
        return get_os_info()

    if name == "get_battery_info":
        return get_battery_info()

    return "Unknown tool."


# =========================
# AI AGENT
# =========================

print("TARS")
print("System tools: CPU, RAM, Disk, OS, Battery")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages = [
        {
            "role": "system",
            "content": """
You are TARS, a local AI desktop assistant.

you run on the user's computer and use tools
 to retrieve system information and perform specific 
safe actions.


you can open the Brave web browser

Rules:
- use tools when appropriate.
- Never guess hardware information.
- Use tools when the user asks about the computer.
- Use the exact information returned by tools.
- Never claim you performed an action unless a tool actually performed it.
"""
        },

        {
            "role": "user",
            "content": user_input
        }
    ]

    # First AI call
    response = ollama.chat(
        model="qwen3:1.7b",
        messages=messages,
        tools=tools
    )


    # Did the AI request tools?

    if response["message"].get("tool_calls"):

        messages.append(response["message"])


        for call in response["message"]["tool_calls"]:

            tool_name = call["function"]["name"]

            print(f"🔧 Using tool: {tool_name}")

            result = execute_tool(tool_name)

            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result)
                }
            )


        # Second AI call
        final_response = ollama.chat(
            model="qwen3:1.7b",
            messages=messages
        )

        print("AI:", final_response["message"]["content"])


    else:

        print("AI:", response["message"]["content"])


    print()
