import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
from typing import Optional, List
import os


#Load .env file and set environment variables
from dotenv import load_dotenv
load_dotenv() # Load environment variables from a .env file if it exists

# Set memory management environment variable
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

def load_model_and_tokenizer(
    model_name_or_path: str,
    use_auth_token: Optional[str] = None,
    low_cpu_mem_usage: bool = True,
):
    """
    Loads the Llama 3.1 model and tokenizer with quantization and CPU offloading.

    Args:
        model_name_or_path (str): The name or path of the Llama 3 model.
        use_auth_token (Optional[str], optional): Hugging Face authentication token.
        low_cpu_mem_usage (bool): Try to use less CPU memory.

    Returns:
        tuple: (tokenizer, model)
            - tokenizer: The tokenizer for the Llama 3 model.
            - model: The Llama 3 model. Returns None if there's an error.
    """
    try:
        # Clear GPU memory cache
        torch.cuda.empty_cache()

        # Configure 4-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,  # Enable 4-bit quantization
            bnb_4bit_compute_dtype=torch.float16,  # Use FP16 for computations
            bnb_4bit_use_double_quant=True,  # Double quantization for extra memory savings
            bnb_4bit_quant_type="nf4",  # Normalizing 4-bit quantization
            llm_int8_enable_fp32_cpu_offload=True,  # Enable FP32 CPU offloading
        )

        # Create a custom device map to prioritize GPU but offload to CPU if needed
        device_map = {
            "model.embed_tokens": "cuda",
            "model.layers": "cuda",  # Try to keep most layers on GPU
            "model.norm": "cuda",
            "lm_head": "cpu",  # Offload output layer to CPU to save VRAM
        }

        tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path,
            use_auth_token=use_auth_token,
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            use_auth_token=use_auth_token,
            quantization_config=quantization_config,
            device_map=device_map,  # Use custom device map
            low_cpu_mem_usage=low_cpu_mem_usage,
        )
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        return None, None

def generate_stream(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.95,
    top_k: int = 50,
    repetition_penalty: float = 1.1,
    do_sample: bool = True,
    eos_token_ids: Optional[List[int]] = None,
):
    """
    Generates text using the Llama 3 model with streaming output.

    Args:
        model: The Llama 3 model.
        tokenizer: The tokenizer for the Llama 3 model.
        prompt (str): The input prompt.
        max_new_tokens (int, optional): Maximum number of new tokens to generate.
        temperature (float, optional): Temperature for sampling.
        top_p (float, optional): Top-p value for sampling.
        top_k (int, optional): Top-k value for sampling.
        repetition_penalty (float, optional): Repetition penalty.
        do_sample (bool, optional): Whether to use sampling.
        eos_token_ids (Optional[List[int]]): List of end-of-sequence token ids.

    Yields:
        str: The generated text, streamed token by token.
    """
    # Determine device for inputs (use GPU if available, else CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Tokenize the prompt and move to the appropriate device
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Extract input_ids and attention_mask
    input_ids = inputs["input_ids"]
    attention_mask = inputs.get("attention_mask", None)

    streamer = TextStreamer(tokenizer, skip_prompt=True, decode_kwargs={"skip_special_tokens": True})

    # Prepare generation kwargs
    generation_kwargs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "repetition_penalty": repetition_penalty,
        "do_sample": do_sample,
        "streamer": streamer,
    }
    
    if eos_token_ids is not None:
        generation_kwargs["eos_token_id"] = eos_token_ids

    # Run the generation with no gradient computation
    with torch.no_grad():
        _ = model.generate(**generation_kwargs)

def main():
    model_name = "meta-llama/Llama-3.1-8B"

    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        print("HF_TOKEN environment variable not set. Please set it and try again.")
        print("You can set it like this: export HF_TOKEN='YOUR_TOKEN'")
        print("or in Windows: set HF_TOKEN=YOUR_TOKEN")
        return

    # Load the model and tokenizer with quantization and offloading
    tokenizer, model = load_model_and_tokenizer(model_name, use_auth_token=hf_token)

    if model is None or tokenizer is None:
        print("Failed to load the model. Please check your model name and ensure you have the necessary files/permissions.")
        return

    # Check if the model was loaded successfully
    print(f"Model successfully loaded with device map")
    while True:
        prompt = input("Enter your prompt (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            break

        # Generate and stream the output
        generate_stream(model, tokenizer, prompt)
        print("\n")  # Add a newline for better readability

if __name__ == "__main__":
    main()