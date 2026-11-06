import os
from dotenv import load_dotenv, find_dotenv

print("env file found at:", find_dotenv())
load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print("key found:", bool(key))
print("key length:", len(key) if key else 0)

print("starts with:", key[:4] if key else None)
print("contains name:", "GEMINI" in key if key else None)