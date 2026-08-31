import json
import ollama

from tools.system import (
    get_cpu_info,
    get_ram_info,
    get_disk_info,
    get_os_info
)

from tools.browser import (
    open_brave,
    search_brave
)

from tools.apps import (
    open_calculator,
    open_notepad
)


MODEL = "qwen3:1.7b"


# =========================
# TOOL DEFINITIONS
# =========================

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_cpu_info",
            "description": "Get the exact CPU model.",
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
            "description": "Get disk space information.",
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
            "description": "Get operating system information.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "open_brave",
            "description": "Open the Brave web browser.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_brave",
            "description": "Open Brave and search Google for a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "open_calculator",
            "description": "Open the Windows calculator.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "open_notepad",
            "description": "Open Windows Notepad.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# =========================
# TOOL EXECUTOR
# =========================

def execute_tool(name, arguments):

    if name == "get_cpu_info":
        return get_cpu_info()

    if name == "get_ram_info":
        return get_ram_info()

    if name == "get_disk_info":
        return get_disk_info()

    if name == "get_os_info":
        return get_os_info()

    if name == "open_brave":
        return open_brave()

    if name == "search_brave":
        return search_brave(arguments["query"])

    if name == "open_calculator":
        return open_calculator()

    if name == "open_notepad":
        return open_notepad()

    return "Unknown tool."


# =========================
# TARS
# =========================

print()
print("╔══════════════════════════════════╗")
print("║               TARS             ║")
print("║   Task Automation & Reasoning    ║")
print("║             System               ║")
print("╚══════════════════════════════════╝")
print()
print("TARS is online.")
print("Type 'exit' to shut down.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("TARS: Shutting down.")
        break


    messages = [

        {
            "role": "system",
            "content": """
You are TARS, a local AI desktop assistant.

You can interact with the user's computer through
the tools provided to you.

You can:
- retrieve system information
- open applications
- open Brave
- perform web searches

Use tools whenever appropriate.

Never invent system information.

Never claim you performed an action unless the
corresponding tool was actually executed.

Be concise, helpful and conversational.
"""
        },

        {
            "role": "user",
            "content": user_input
        }

    ]


    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools
    )


    if response["message"].get("tool_calls"):

        messages.append(response["message"])


        for call in response["message"]["tool_calls"]:

            tool_name = call["function"]["name"]
            arguments = call["function"].get("arguments", {})

            print(f"TARS → 🔧 {tool_name}")

            result = execute_tool(
                tool_name,
                arguments
            )


            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result)
                }
            )


        final_response = ollama.chat(
            model=MODEL,
            messages=messages
        )


        print(
            "TARS:",
            final_response["message"]["content"]
        )


    else:

        print(
            "TARS:",
            response["message"]["content"]
        )


    print()
