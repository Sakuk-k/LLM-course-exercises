# Gemini First API Call

A minimal demo that sends a single prompt to Google's **Gemini API** and prints the response. This is the simplest possible starting point for working with Gemini before moving on to more advanced patterns like RAG.

---

## How It Works

1. The script reads your Gemini API key from an environment variable.
2. It configures the `google-generativeai` library and creates a **Gemini 2.5 Flash Lite** model instance.
3. A hardcoded question is sent to the model using `generate_content`.
4. The model's response is printed to the console.

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* A Gemini API key. You can get one here: [Get a Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)

### Virtual Environment

A **virtual environment** (venv) is an isolated Python environment that keeps this project's dependencies separate from your system-wide Python installation and other projects. This prevents version conflicts — for example, if one project needs `google-generativeai 0.8` and another needs a different version, each can have its own without interference.

1. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
    This creates a `venv/` folder in the project directory containing a standalone Python installation.

2. **Activate the virtual environment**:
    Once activated, any `pip install` and `python` commands will use the isolated environment instead of the system Python.
    * **Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```
    * **Windows (Command Prompt)**:
        ```bash
        venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell)**:
        ```powershell
        venv\Scripts\Activate.ps1
        ```

    You should see `(venv)` appear at the beginning of your terminal prompt, indicating the virtual environment is active.

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Deactivate** when you're done working:
    ```bash
    deactivate
    ```

> **Note:** Always activate the virtual environment before running the script or installing packages. If you open a new terminal, you need to activate it again.

### Configuration

Set the `GEMINI_API_KEY` environment variable to your Gemini API key before running the script.

* **Linux/macOS**:
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```
* **Windows (Command Prompt)**:
    ```bash
    set GEMINI_API_KEY="YOUR_API_KEY"
    ```
* **Windows (PowerShell)**:
    ```powershell
    $env:GEMINI_API_KEY="YOUR_API_KEY"
    ```

Replace `"YOUR_API_KEY"` with your actual key. The script will raise an error on startup if this variable is not set.

### Running the Code

```bash
python gemini-hello.py
```

You should see output similar to:

```
Configuring Gemini API...
Gemini API configured.

Question: What are the three laws of robotics?
Sending prompt to Gemini API...

Answer: The Three Laws of Robotics were introduced by Isaac Asimov...
```

---
