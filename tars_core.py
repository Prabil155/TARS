import json
import platform
import shutil
import subprocess
import os

import ollama

from tools.apps import (
    open_calculator,
    open_notepad,
    open_file_explorer,
    open_command_prompt,
    open_powershell,
)

from memory import Memory
from tools.computer import ComputerTool


class TARS:

    def __init__(self):

        # ==================================================
        # MODELS
        # ==================================================

        self.fast_model = "qwen3:1.7b"
        self.smart_model = "qwen3:4b"
        self.memory_model = "qwen3:1.7b"

        # ==================================================
        # LONG-TERM MEMORY
        # ==================================================

        self.memory = Memory()
        self.computer = ComputerTool()

        # ==================================================
        # PERSONALITY
        # ==================================================

        self.system_prompt = """
You are TARS, a local AI desktop assistant.

PERSONALITY:
- Intelligent, calm, witty, and slightly sarcastic.
- Friendly and natural.
- Talk like a real voice assistant.
- Do not sound like a customer-service bot.
- Keep simple answers short.
- Give detailed explanations when requested.
- Use occasional humor.
- Do not spam emojis.
- Never reveal internal reasoning.
- Never pretend a tool worked if it failed.

CONVERSATION:
- Have natural casual conversations.
- Respond directly to what the user says.
- Avoid unnecessary explanations.
- Keep voice responses reasonably concise.

MEMORY:
- You have persistent local memory.
- Important long-term information can be remembered.
- Do not claim to remember something unless it is actually stored.

MULTI-STEP TASKS:

When a user requests multiple actions, complete ALL requested actions.

For example:
"Open calculator and calculate 2+2"

You must:
1. Call open_calculator.
2. Then call calculate with expression "2+2".
3. Only after all requested actions are completed, provide the final response.

Do not claim an action was completed unless you actually called the corresponding tool.

If multiple tools are required, continue using tools until the entire user request is completed.

TOOL EXECUTION RULES:

Complete each requested action only once.

Never repeat the same tool call with the same arguments
unless the previous tool call failed.

After all requested actions have successfully completed,
stop calling tools and provide the final answer.

Do not call a tool simply because the previous tool result
was successful.

Do not claim an action was completed unless the tool was
actually executed.
"""

        # ==================================================
        # CONVERSATION HISTORY
        # ==================================================

        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        # ==================================================
        # TOOLS
        # ==================================================

        self.tools = [

            # ------------------------------------------------
            # CPU
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "get_cpu_info",
                    "description": "Get the exact CPU model of this computer.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # RAM
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "get_ram_info",
                    "description": "Get the current RAM usage.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # DISK
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "get_disk_info",
                    "description": "Get disk storage information.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # OS
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "get_os_info",
                    "description": "Get operating system information.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # BATTERY
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "get_battery_info",
                    "description": "Get battery percentage and charging status.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # BRAVE
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "open_brave",
                    "description": "Open the Brave web browser.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # CALCULATOR
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "open_calculator",
                    "description": "Open the Windows Calculator application.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # CALCULATE
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": (
                        "Calculate a mathematical expression and return "
                        "the numerical result. Use this for arithmetic "
                        "such as 2+2, 25*4, or (10+5)/3."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": (
                                    "The mathematical expression to calculate."
                                ),
                            }
                        },
                        "required": ["expression"],
                    },
                },
            },

            # ------------------------------------------------
            # NOTEPAD
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "open_notepad",
                    "description": "Open Windows Notepad.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # FILE EXPLORER
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "open_file_explorer",
                    "description": "Open Windows File Explorer.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # COMMAND PROMPT
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "open_command_prompt",
                    "description": "Open the Windows Command Prompt.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            # ------------------------------------------------
            # POWERSHELL
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "open_powershell",
                    "description": "Open Windows PowerShell.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

                        # RUN WINDOWS COMMAND
            {
                "type": "function",
                "function": {
                    "name": "computer_run_command",
                    "description": (
                        "Execute a command on the Windows computer "
                        "and return its output."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": (
                                    "The Windows command to execute."
                                ),
                            },
                        },
                        "required": [
                            "command"
                        ],
                    },
                },
            },

            # ------------------------------------------------
            # SAVE MEMORY
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "save_memory",
                    "description": (
                        "Save an important long-term fact about the user."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "memory": {
                                "type": "string",
                                "description": (
                                    "Important information to remember."
                                ),
                            }
                        },
                        "required": ["memory"],
                    },
                },
            },

            # ------------------------------------------------
            # SEARCH MEMORY
            # ------------------------------------------------

            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search TARS's long-term memory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "Keyword to search for.",
                            }
                        },
                        "required": ["keyword"],
                    },
                },
            },

            # ==================================================
            # COMPUTER CONTROL
            # ==================================================

            {
                "type": "function",
                "function": {
                    "name": "computer_open_notepad",
                    "description": (
                        "Open Windows Notepad on the user's desktop."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "computer_open_calculator",
                    "description": (
                        "Open Windows Calculator on the user's desktop."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

                        # VS CODE
            {
                "type": "function",
                "function": {
                    "name": "computer_open_vscode",
                    "description": "Open Visual Studio Code.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },

            {

                "type": "function",
                "function": {
                    "name": "computer_write_code_to_vscode",
                    "description": (
                        "Write a generated program directly into "
                        "Visual Studio Code on the Windows desktop. "
                        "Use this when the user asks TARS to create, "
                        "write, or type code into VS Code."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": (
                                "The complete source code "
                                "to write into VS Code."
                        )
                   },
                   "filename": {
                        "type": "string",
                        "description": (
                            "Python filename to save, "
                            "for example add_two_numbers.py."
                        )
                    }
                },
                "required": [
                    "code"
                ]
            }
        }
    },

            {
                "type": "function",
                "function": {
                    "name": "computer_type_text",
                    "description": (
                        "Type text into the currently focused "
                        "Windows application."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to type.",
                            }
                        },
                        "required": ["text"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "computer_press",
                    "description": (
                        "Press a keyboard key such as enter, tab, "
                        "escape, backspace, or a letter."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Keyboard key to press.",
                            }
                        },
                        "required": ["key"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "computer_hotkey",
                    "description": (
                        "Press multiple keyboard keys together, "
                        "such as ctrl+s or alt+tab."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keys": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": (
                                    "Keys to press together."
                                ),
                            }
                        },
                        "required": ["keys"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "computer_click",
                    "description": (
                        "Click the Windows desktop at a specific "
                        "screen coordinate."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {
                                "type": "integer",
                                "description": (
                                    "Horizontal screen coordinate."
                                ),
                            },
                            "y": {
                                "type": "integer",
                                "description": (
                                    "Vertical screen coordinate."
                                ),
                            },
                        },
                        "required": ["x", "y"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "computer_screenshot",
                    "description": (
                        "Take a screenshot of the current Windows "
                        "desktop."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },
        ]

    # ==================================================
    # MODEL ROUTER
    # ==================================================

    def choose_model(self, user_input):

        text = user_input.lower().strip()

        tool_keywords = [
            "cpu",
            "processor",
            "ram",
            "memory usage",
            "disk",
            "storage",
            "battery",
            "operating system",
            "os",
            "open brave",
            "open browser",
            "launch brave",
            "launch browser",
            "open calculator",
            "open notepad",
            "open file explorer",
            "open command prompt",
            "open powershell",
        ]

        for keyword in tool_keywords:
            if keyword in text:
                return self.smart_model

        complex_keywords = [
            "open",
            "launch",
            "start",
            "close",
            "run",
            "explain",
            "analyze",
            "debug",
            "write code",
            "create code",
            "program",
            "how does",
            "how do",
            "why does",
            "why do",
            "compare",
            "difference between",
            "architecture",
            "design",
            "calculate",
            "solve",
            "implement",
            "build",
            "configure",
            "install",
            "error",
            "problem",
            "issue",
        ]

        for keyword in complex_keywords:
            if keyword in text:
                return self.smart_model

        return self.fast_model

    # ==================================================
    # AUTOMATIC MEMORY
    # ==================================================

    def check_for_memory(self, user_input):

        text = user_input.lower().strip()

        memory_triggers = [
            "my name is",
            "i am",
            "i'm",
            "i live",
            "i study",
            "i work",
            "i use",
            "i like",
            "i love",
            "i prefer",
            "my favorite",
            "my favourite",
            "remember that",
            "remember this",
            "don't forget",
            "do not forget",
            "keep in mind",
            "i'm building",
            "i am building",
            "my project",
            "my goal",
        ]

        possible_memory = any(
            trigger in text
            for trigger in memory_triggers
        )

        if not possible_memory:
            return

        try:

            memory_prompt = f"""
You are the memory manager for TARS.

Determine whether this user message contains
important information that should be remembered
for future conversations.

User message:
"{user_input}"

SAVE information such as:
- Name
- Long-term projects
- Important goals
- Important preferences
- Important computer/software setup
- Information explicitly requested to be remembered

DO NOT SAVE:
- Temporary information
- Casual conversation
- One-time requests
- Questions
- Jokes

Return ONLY:

SAVE: <short memory>

OR

IGNORE
"""

            response = ollama.chat(
                model=self.memory_model,
                messages=[
                    {
                        "role": "user",
                        "content": memory_prompt,
                    }
                ],
                think=False,
            )

            result = response["message"].get(
                "content",
                "",
            ).strip()

            if result.startswith("SAVE:"):

                memory_text = result[
                    len("SAVE:")
                ].strip()

                if memory_text:

                    self.memory.save(
                        memory_text
                    )

                    print(
                        f"Memory saved: {memory_text}"
                    )

        except Exception as e:

            print(
                f"Memory check failed: {e}"
            )

    # ==================================================
    # CPU
    # ==================================================

    def get_cpu_info(self):

        try:

            result = subprocess.run(
                ["lscpu"],
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():

                if "Model name:" in line:

                    return line.split(
                        ":",
                        1,
                    )[1].strip()

            processor = platform.processor()

            if processor:
                return processor

            return "CPU information unavailable."

        except Exception as e:

            return f"CPU error: {e}"

    # ==================================================
    # RAM
    # ==================================================

    def get_ram_info(self):

        try:

            result = subprocess.run(
                ["free", "-h"],
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():

                if line.startswith("Mem:"):

                    parts = line.split()

                    if len(parts) >= 7:

                        return (
                            f"Total RAM: {parts[1]}, "
                            f"Used: {parts[2]}, "
                            f"Available: {parts[6]}"
                        )

            return "RAM information unavailable."

        except Exception as e:

            return f"RAM error: {e}"

    # ==================================================
    # DISK
    # ==================================================

    def get_disk_info(self):

        try:

            total, used, free = shutil.disk_usage("/")

            total_gb = total / (1024 ** 3)
            used_gb = used / (1024 ** 3)
            free_gb = free / (1024 ** 3)

            return (
                f"Disk total: {total_gb:.1f} GB, "
                f"used: {used_gb:.1f} GB, "
                f"free: {free_gb:.1f} GB"
            )

        except Exception as e:

            return f"Disk error: {e}"

    # ==================================================
    # OS
    # ==================================================

    def get_os_info(self):

        try:

            return (
                f"System: {platform.system()}, "
                f"Release: {platform.release()}, "
                f"Architecture: {platform.machine()}"
            )

        except Exception as e:

            return f"OS error: {e}"

    # ==================================================
    # BATTERY
    # ==================================================

    def get_battery_info(self):

        try:

            result = subprocess.run(
                [
                    "bash",
                    "-c",
                    (
                        "cat /sys/class/power_supply/"
                        "BAT0/capacity 2>/dev/null"
                    ),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            battery = result.stdout.strip()

            if not battery:

                return (
                    "Battery information is not available "
                    "through WSL."
                )

            status_result = subprocess.run(
                [
                    "bash",
                    "-c",
                    (
                        "cat /sys/class/power_supply/"
                        "BAT0/status 2>/dev/null"
                    ),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            status = status_result.stdout.strip()

            if not status:
                status = "Unknown status"

            return (
                f"Battery: {battery}% "
                f"({status})"
            )

        except Exception as e:

            return f"Battery error: {e}"

    # ==================================================
    # BRAVE
    # ==================================================

    def open_brave(self):

        try:

            brave_path = (
                "/mnt/c/Program Files/"
                "BraveSoftware/"
                "Brave-Browser/"
                "Application/"
                "brave.exe"
            )

            if not os.path.exists(brave_path):

                return (
                    "Could not find Brave at: "
                    f"{brave_path}"
                )

            subprocess.Popen(
                [brave_path]
            )

            return (
                "Brave browser opened successfully."
            )

        except Exception as e:

            return (
                f"Could not open Brave: {e}"
            )

    # ==================================================
    # CALCULATOR
    # ==================================================

    def calculate(self, expression):

        try:

            allowed = "0123456789+-*/().% "

            if not all(
                character in allowed
                for character in expression
            ):
                return "Invalid mathematical expression."

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                {},
            )

            return str(result)

        except Exception as e:

            return f"Could not calculate expression: {e}"

    # ==================================================
    # SAVE MEMORY TOOL
    # ==================================================

    def save_memory(self, memory):

        if not memory:
            return "No memory was provided."

        try:

            self.memory.save(
                memory
            )

            return (
                f"Memory saved successfully: {memory}"
            )

        except Exception as e:

            return (
                f"Memory save error: {e}"
            )

    # ==================================================
    # SEARCH MEMORY TOOL
    # ==================================================

    def search_memory(self, keyword):

        if not keyword:
            return "No search keyword was provided."

        try:

            results = self.memory.search(
                keyword
            )

            if not results:
                return "No matching memories found."

            memories = []

            for item in results:

                if item and len(item) > 0:

                    memories.append(
                        str(item[0])
                    )

            if not memories:
                return "No matching memories found."

            return "\n".join(
                memories
            )

        except Exception as e:

            return (
                f"Memory search error: {e}"
            )

    # ==================================================
    # EXECUTE TOOL
    # ==================================================

    def execute_tool(
        self,
        tool_name,
        arguments,
    ):

        if tool_name == "computer_open_vscode":

            try:

                return self.computer.open_vscode()

            except Exception as e:

                return f"Could not open VS Code: {e}"

        if tool_name == "computer_write_code_to_vscode":

            try:

                return self.computer.write_code_to_vscode(
                    arguments.get(
                        "code",
                        ""
                    ),
                    arguments.get(
                        "filename",
                        "tars_program.py"
                    )
                )

            except Exception as e:

                return (
                    "Could not write code to VS Code: "
                    f"{e}"
                )

        if tool_name == "computer_run_command":

            try:

                return self.computer.run_command(
                    arguments.get(
                        "command",
                        "",
                    )
                )

            except Exception as e:

                return (
                    f"Could not execute command: {e}"
                )

        if isinstance(arguments, str):

            try:
                arguments = json.loads(arguments)

            except json.JSONDecodeError:
                arguments = {}

        if not isinstance(arguments, dict):
            arguments = {}

        # ----------------------------------------------
        # CALCULATOR
        # ----------------------------------------------

        if tool_name == "calculate":

            return self.calculate(
                arguments.get(
                    "expression",
                    "",
                )
            )

        # ----------------------------------------------
        # SYSTEM INFORMATION
        # ----------------------------------------------

        if tool_name == "get_cpu_info":
            return self.get_cpu_info()

        if tool_name == "get_ram_info":
            return self.get_ram_info()

        if tool_name == "get_disk_info":
            return self.get_disk_info()

        if tool_name == "get_os_info":
            return self.get_os_info()

        if tool_name == "get_battery_info":
            return self.get_battery_info()

        # ----------------------------------------------
        # APPLICATIONS
        # ----------------------------------------------

        if tool_name == "open_brave":
            return self.open_brave()

        if tool_name == "open_calculator":

            try:
                return open_calculator()

            except Exception as e:
                return f"Could not open Calculator: {e}"

        if tool_name == "open_notepad":

            try:
                return open_notepad()

            except Exception as e:
                return f"Could not open Notepad: {e}"

        if tool_name == "open_file_explorer":

            try:
                return open_file_explorer()

            except Exception as e:
                return f"Could not open File Explorer: {e}"

        if tool_name == "open_command_prompt":

            try:
                return open_command_prompt()

            except Exception as e:
                return f"Could not open Command Prompt: {e}"

        if tool_name == "open_powershell":

            try:
                return open_powershell()

            except Exception as e:
                return f"Could not open PowerShell: {e}"

        # ----------------------------------------------
        # MEMORY
        # ----------------------------------------------

        if tool_name == "save_memory":

            return self.save_memory(
                arguments.get(
                    "memory",
                    "",
                )
            )

        if tool_name == "search_memory":

            return self.search_memory(
                arguments.get(
                    "keyword",
                    "",
                )
            )

        # ----------------------------------------------
        # COMPUTER CONTROL
        # ----------------------------------------------

        if tool_name == "computer_open_notepad":

            try:
                return self.computer.open_notepad()

            except Exception as e:
                return f"Could not open Notepad: {e}"

        if tool_name == "computer_open_calculator":

            try:
                return self.computer.open_calculator()

            except Exception as e:
                return f"Could not open Calculator: {e}"

        if tool_name == "computer_type_text":

            try:
                return self.computer.type_text(
                    arguments.get("text", "")
                )

            except Exception as e:
                return f"Could not type text: {e}"

        if tool_name == "computer_press":

            try:
                return self.computer.press(
                    arguments.get("key", "")
                )

            except Exception as e:
                return f"Could not press key: {e}"

        if tool_name == "computer_hotkey":

            try:
                return self.computer.hotkey(
                    arguments.get("keys", [])
                )

            except Exception as e:
                return f"Could not press hotkey: {e}"

        if tool_name == "computer_click":

            try:
                return self.computer.click(
                    arguments.get("x", 0),
                    arguments.get("y", 0),
                )

            except Exception as e:
                return f"Could not click desktop: {e}"

        if tool_name == "computer_screenshot":

            try:
                return self.computer.screenshot()

            except Exception as e:
                return f"Could not take screenshot: {e}"

        return f"Unknown tool: {tool_name}"

    # ==================================================
    # CLEAN RESPONSE
    # ==================================================

    def clean_response(self, text):

        if not text:
            return ""

        text = text.strip()

        if "</think>" in text:

            text = text.split(
                "</think>",
                1,
            )[1].strip()

        if "<think>" in text:

            text = text.split(
                "<think>",
                1,
            )[0].strip()

        return text

    # ==================================================
    # FAST SYSTEM COMMANDS
    # ==================================================

    def fast_system_command(self, user_input):

        """
        Handle simple deterministic desktop requests
        directly in Python.

        This avoids sending simple system requests
        through the 4B model + tool-call cycle.
        """

        text = user_input.lower().strip()

        # ----------------------------------------------
        # CPU
        # ----------------------------------------------

        if (
            "what is my cpu" in text
            or "what's my cpu" in text
            or "which cpu" in text
            or "which processor" in text
            or "what processor" in text
        ):

            result = self.execute_tool(
                "get_cpu_info",
                {},
            )

            return (
                f"Your CPU is {result}. "
                "Pretty decent little brain for a laptop."
            )

        # ----------------------------------------------
        # RAM
        # ----------------------------------------------

        if (
            "how much ram" in text
            or "how much memory" in text
            or "what is my ram" in text
            or "what's my ram" in text
            or "ram usage" in text
            or "memory usage" in text
        ):

            result = self.execute_tool(
                "get_ram_info",
                {},
            )

            return (
                f"Your current RAM status is: {result}."
            )

        # ----------------------------------------------
        # DISK / STORAGE
        # ----------------------------------------------

        if (
            "storage" in text
            or "disk space" in text
            or "disk usage" in text
            or "how much storage" in text
            or "how much disk" in text
        ):

            result = self.execute_tool(
                "get_disk_info",
                {},
            )

            return (
                f"Here's your storage status: {result}"
            )

        # ----------------------------------------------
        # OPERATING SYSTEM
        # ----------------------------------------------

        if (
            "what os" in text
            or "what's my os" in text
            or "which os" in text
            or "operating system" in text
        ):

            result = self.execute_tool(
                "get_os_info",
                {},
            )

            return (
                f"You're running {result}."
            )

        # ----------------------------------------------
        # BATTERY
        # ----------------------------------------------

        if (
            "battery" in text
            or "battery level" in text
            or "battery percentage" in text
            or "how much battery" in text
        ):

            result = self.execute_tool(
                "get_battery_info",
                {},
            )

            return (
                f"Your battery status is: {result}"
            )

        # ----------------------------------------------
        # OPEN BRAVE
        # ----------------------------------------------

        if (
            "open brave" in text
            or "open browser" in text
            or "launch brave" in text
            or "launch browser" in text
        ):

            return self.execute_tool(
                "open_brave",
                {},
            )

        # ----------------------------------------------
        # OPEN CALCULATOR
        # ----------------------------------------------

        if (
            "open calculator" in text
            or "launch calculator" in text
        ):

            return self.execute_tool(
                "open_calculator",
                {},
            )

        # ----------------------------------------------
        # OPEN NOTEPAD
        # ----------------------------------------------

        if (
            "open notepad" in text
            or "launch notepad" in text
        ):

            return self.execute_tool(
                "open_notepad",
                {},
            )

        # ----------------------------------------------
        # OPEN FILE EXPLORER
        # ----------------------------------------------

        if (
            "open file explorer" in text
            or "open explorer" in text
            or "launch file explorer" in text
        ):

            return self.execute_tool(
                "open_file_explorer",
                {},
            )

        # ----------------------------------------------
        # OPEN COMMAND PROMPT
        # ----------------------------------------------

        if (
            "open command prompt" in text
            or "open cmd" in text
            or "launch command prompt" in text
        ):

            return self.execute_tool(
                "open_command_prompt",
                {},
            )

        # ----------------------------------------------
        # OPEN POWERSHELL
        # ----------------------------------------------

        if (
            "open powershell" in text
            or "launch powershell" in text
        ):

            return self.execute_tool(
                "open_powershell",
                {},
            )
        # ----------------------------------------------
        # SIMPLE WINDOWS COMMANDS
        # ----------------------------------------------

        if text in (
            "python --version",
            "python version",
            "check python version",
            "what is my python version",
            "what's my python version",
        ):

            result = self.execute_tool(
                "computer_run_command",
                {
                    "command": "python --version"
                },
            )

            return (
                f"Your Python version is "
                f"{result.strip()}."
            )

        # ----------------------------------------------
        # ECHO
        # ----------------------------------------------

        if text.startswith("echo "):

            command = user_input.strip()

            result = self.execute_tool(
                "computer_run_command",
                {
                    "command": command
                },
            )

            return result.strip()

        # ----------------------------------------------
        # WINDOWS DIRECTORY
        # ----------------------------------------------

        if (
            text == "show current directory"
            or text == "show windows directory"
            or text == "list files"
        ):

            result = self.execute_tool(
                "computer_run_command",
                {
                    "command": "dir"
                },
            )

            return result.strip()
        
        return None

    # ==================================================
    # RETRIEVE RELEVANT MEMORIES
    # ==================================================

    def get_relevant_memories(self, user_input):

        try:

            memories = self.memory.search(
                user_input
            )

            if not memories:
                return []

            result = []

            for memory in memories[:5]:

                if not memory:
                    continue

                memory_text = str(
                    memory[0]
                )

                if memory_text not in result:

                    result.append(
                        memory_text
                    )

            return result

        except Exception as e:

            print(
                f"Memory retrieval error: {e}"
            )

            return []

    # ==================================================
    # ASK TARS
    # ==================================================

    def ask(self, user_input):

        # --------------------------------------------------
        # FAST SYSTEM COMMAND
        # --------------------------------------------------

        fast_result = self.fast_system_command(
            user_input
        )

        if fast_result is not None:
            return fast_result

        # --------------------------------------------------
        # AUTOMATIC MEMORY
        # --------------------------------------------------

        self.check_for_memory(
            user_input
        )

        # --------------------------------------------------
        # RETRIEVE RELEVANT MEMORIES
        # --------------------------------------------------

        relevant_memories = (
            self.get_relevant_memories(
                user_input
            )
        )

        # --------------------------------------------------
        # BUILD USER MESSAGE
        # --------------------------------------------------

        user_content = user_input

        if relevant_memories:

            memory_text = "\n".join(
                f"- {memory}"
                for memory in relevant_memories
            )

            user_content = f"""
Relevant memories about the user:

{memory_text}

Current user message:

{user_input}

Use the relevant memories when answering.
Do not mention the memory system unless necessary.
"""

            print(
                "Relevant memory found."
            )

        # --------------------------------------------------
        # ADD USER MESSAGE
        # --------------------------------------------------

        self.messages.append(
            {
                "role": "user",
                "content": user_content,
            }
        )

        # --------------------------------------------------
        # SELECT MODEL
        # --------------------------------------------------

        model = self.choose_model(
            user_input
        )

        print(
            f"Model: {model}"
        )

        # --------------------------------------------------
        # FIRST MODEL REQUEST
        # --------------------------------------------------

        if model == self.fast_model:

            response = ollama.chat(
                model=model,
                messages=self.messages,
                think=False,
            )

        else:

            response = ollama.chat(
                model=model,
                messages=self.messages,
                tools=self.tools,
                think=False,
            )

        # --------------------------------------------------
        # TOOL LOOP
        # --------------------------------------------------

        max_tool_rounds = 5
        tool_rounds = 0
        executed_tools = set()

        while (
            response["message"].get("tool_calls")
            and tool_rounds < max_tool_rounds
        ):

            tool_rounds += 1

            assistant_message = response["message"]

            self.messages.append(
                assistant_message
            )

            tool_calls = assistant_message.get(
                "tool_calls",
                []
            )

            for tool_call in tool_calls:

                function = tool_call["function"]

                tool_name = function["name"]

                arguments = function.get(
                    "arguments",
                    {},
                )

                # Create a unique signature for this tool call.
                try:

                    normalized_arguments = json.dumps(
                        arguments,
                        sort_keys=True,
                    )

                except TypeError:

                    normalized_arguments = str(
                        arguments
                    )

                tool_signature = (
                    tool_name,
                    normalized_arguments,
                )

                if tool_signature in executed_tools:

                    print(
                        f"Skipping duplicate tool: {tool_name}"
                    )

                    continue

                executed_tools.add(
                    tool_signature
                )

                print(
                    f"Using tool: {tool_name}"
                )

                tool_result = self.execute_tool(
                    tool_name,
                    arguments,
                )

                self.messages.append(
                    {
                        "role": "tool",
                        "content": str(
                            tool_result
                        ),
                    }
                )

            # Ask the smart model to interpret the tool results.
            response = ollama.chat(
                model=self.smart_model,
                messages=self.messages,
                tools=self.tools,
                think=False,
            )

        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------

        response_text = response[
            "message"
        ].get(
            "content",
            "",
        )

        response_text = self.clean_response(
            response_text
        )

        # --------------------------------------------------
        # SAVE ASSISTANT RESPONSE
        # --------------------------------------------------

        self.messages.append(
            {
                "role": "assistant",
                "content": response_text,
            }
        )

        return response_text


# ======================================================
# TERMINAL MODE
# ======================================================

if __name__ == "__main__":

    tars = TARS()

    print()
    print("======================================")
    print("             TARS ONLINE")
    print("======================================")
    print()

    print(
        f"Fast model : {tars.fast_model}"
    )

    print(
        f"Smart model: {tars.smart_model}"
    )

    print(
        "Memory     : SQLite"
    )

    print()

    print("Tools:")

    print(
        "CPU | RAM | Disk | OS | Battery | "
        "Brave | Calculator | Notepad | "
        "File Explorer | CMD | PowerShell"
    )

    print()

    print("Type 'exit' to quit.")
    print()

    while True:

        try:

            user_input = input(
                "You: "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "TARS: Goodbye."
            )

            break

        except EOFError:

            print()
            print(
                "TARS: Goodbye."
            )

            break

        if not user_input:
            continue

        if user_input.lower() == "exit":

            print(
                "TARS: Goodbye."
            )

            break

        try:

            answer = tars.ask(
                user_input
            )

            print(
                "TARS:",
                answer,
            )

        except Exception as e:

            print(
                f"TARS: Something went wrong: {e}"
            )
