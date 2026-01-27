import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Load environment variables from .env
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    model_id = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    
    if not api_key:
        print("Error: GOOGLE_API_KEY is not set in .env file.")
        sys.exit(1)
        
    # 2. Read prompt.md file
    prompt_path = "prompt.md"
    if not os.path.exists(prompt_path):
        print(f"Error: {prompt_path} not found.")
        sys.exit(1)
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_content = f.read()
        
    # 3. Create google-genai Client
    client = genai.Client(api_key=api_key)
    
    try:
        # 4. Call Gemini model
        print(f"Calling model: {model_id}...")
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_content
        )
        
        # 5. Output response text
        print("\n--- Response From Gemini ---\n")
        print(response.text)
        
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
