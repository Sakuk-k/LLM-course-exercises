# Llama 3.1 Model Interaction Script

This script provides a simple way to load a Llama 3.1 language model from Hugging Face and interact with it through a command-line interface. It supports streaming output for real-time text generation.

---

## Features

* **Model Loading:** Easily loads Llama 3.1 models using `transformers`.
* **Hugging Face Authentication:** Supports authentication via a Hugging Face token for gated models.
* **GPU Acceleration:** Utilizes `torch_dtype` and `device_map` for efficient model loading and inference on available hardware (e.g., GPU).
* **Streaming Output:** Generates text in a streaming fashion, displaying tokens as they are produced.
* **Interactive Prompt:** Allows continuous interaction with the model by entering prompts.

---

## Prerequisites

Before running this script, ensure you have the following:

* **Python 3.8+**

### Installing Dependencies

Use the existing `requirements.txt` file to install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

---

## Setup

### Hugging Face Token

To download models from Hugging Face, especially gated models like Llama 3.1, you need a **Hugging Face access token**.

1.  **Generate a Token:** Go to your Hugging Face settings: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and create a new token with "read" access.
2.  **Set Environment Variable:** Set the `HF_TOKEN` environment variable before running the script.

    * **Linux/macOS:**
        ```bash
        export HF_TOKEN='YOUR_HUGGING_FACE_TOKEN'
        ```
    * **Windows (Command Prompt):**
        ```bash
        set HF_TOKEN=YOUR_HUGGING_FACE_TOKEN
        ```
    * **Windows (PowerShell):**
        ```powershell
        $env:HF_TOKEN='YOUR_HUGGING_FACE_TOKEN'
        ```

    Replace `YOUR_HUGGING_FACE_TOKEN` with your actual token.

---

## How to Run

1.  **Run the script:** Execute the script from your terminal:

    ```bash
    python llama3-base.py
    ```

2.  **Enter prompts:** The script will prompt you to enter your text. Type your prompt and press Enter. The model's response will stream directly to your console.

    ```
    Enter your prompt (or type 'exit' to quit): Tell me a story about a brave knight.
    ```

3.  **Exit:** Type `exit` and press Enter to quit the application.

---

## Code Overview

### `load_model_and_tokenizer` Function

This function is responsible for loading the pre-trained Llama 3.1 model and its corresponding tokenizer from Hugging Face.

* `model_name_or_path`: Specifies the model to load (e.g., `"meta-llama/Llama-3.1-405B"`).
* `use_auth_token`: Your Hugging Face token for authentication.
* `torch_dtype`: Sets the data type for the model weights (defaults to `torch.float16` for memory efficiency).
* `device_map`: Determines how the model is distributed across available devices (e.g., "auto" for automatic placement).
* `low_cpu_mem_usage`: Attempts to reduce CPU memory consumption during loading.

### `generate_stream` Function

This function handles the text generation process with streaming output.

* `model`, `tokenizer`: The loaded Llama 3.1 model and tokenizer.
* `prompt`: The input text to generate a response from.
* **Generation Parameters:** Includes various parameters to control the generation behavior, such as `max_new_tokens`, `temperature`, `top_p`, `top_k`, `repetition_penalty`, and `do_sample`.
* `TextStreamer`: A Hugging Face utility used to print the generated tokens as they are produced, providing a real-time experience.

### `main` Function

The main entry point of the script.

* Retrieves the Hugging Face token from the `HF_TOKEN` environment variable.
* Calls `load_model_and_tokenizer` to load the model.
* Enters an infinite loop, continuously prompting the user for input.
* Calls `generate_stream` to produce and display the model's response.
* Allows the user to exit by typing `exit`.

---

## Customization

You can modify the `main` function to:

* **Change the model:** Update the `model_name` variable to a different Llama 3.1 variant or another compatible Hugging Face model.
* **Adjust generation parameters:** Modify the default values passed to `generate_stream` (e.g., `max_new_tokens`, `temperature`) to experiment with different generation styles.

---