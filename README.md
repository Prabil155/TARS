# TARS — Personal AI Assistant

TARS is a personal AI assistant project designed to bring a more natural, interactive, and movie-inspired AI experience to the desktop. The goal is to build an assistant that can communicate conversationally, interact with the system through tools, and respond through both text and voice.

## Features

- **Local AI integration** — Uses Ollama to run locally hosted language models.
- **Conversational assistant** — Interact with TARS through natural-language prompts.
- **System tools** — Access system information such as CPU, memory, disk, operating system, and battery status where supported.
- **Desktop interface** — A graphical interface for interacting with the assistant.
- **Voice interaction** — A separate Windows voice client supports speech recognition and text-to-speech.
- **Browser and application tools** — An evolving tool layer for browser and application interactions.
- **Modular architecture** — Separate components for the assistant, core logic, interface, and tools.

## Tech Stack

- Python
- Ollama
- Locally hosted language models
- Tkinter / Python GUI components, where used
- Faster-Whisper for speech recognition
- pyttsx3 for text-to-speech
- Linux / Ubuntu and Windows

## Project Structure

```text
my-ai-desktop/
├── agent.py
├── tars.py
├── tars_core.py
├── tars_gui.py
├── tools/
│   ├── system.py
│   ├── browser.py
│   └── apps.py
└── README.md
```

The exact structure may evolve as the project develops.

## Getting Started

### Prerequisites

- Python 3
- Git
- [Ollama](https://ollama.com/)
- A supported local language model

### 1. Clone the repository

```bash
git clone https://github.com/Prabil155/TARS.git
cd TARS
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the Python packages required by the project. If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

Install and start Ollama, then download a model:

```bash
ollama pull qwen3:4b
```

Make sure Ollama is running before starting the assistant.

### 5. Run TARS

Use the entry point configured for your current version. For example:

```bash
python tars.py
```

If your current version uses a different entry point, run that file instead.

## Voice Assistant

The voice client is developed separately for Windows and uses speech recognition and text-to-speech components.

Current development includes:
- Voice input using
