import os
import google.generativeai as genai

# Initialize environment variable for Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it.")

# Configure Gemini API
print("Configuring Gemini API...")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')
print("Gemini API configured.")

# Send a simple prompt
question = "What are the three laws of robotics?"
print(f"\nQuestion: {question}")
print("Sending prompt to Gemini API...")

token_check = model.count_tokens(question)
print(f"This prompt will use {token_check.total_tokens} tokens.")

response = model.generate_content(question)

# Accessing the token counts
usage = response.usage_metadata

print(f"\nAnswer: {response.text}")
print("-" * 20)
print(f"Prompt Tokens: {usage.prompt_token_count}")
print(f"Response Tokens: {usage.candidates_token_count}")
print(f"Total Tokens: {usage.total_token_count}")
