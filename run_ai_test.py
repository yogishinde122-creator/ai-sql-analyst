"""Fully automated test: ask Gemini for SQL, then score it against the golden set.

Setup: put GEMINI_API_KEY=... in a local .env file (it is git-ignored).
Optional: GEMINI_MODEL=<model name> (default below).
Usage:  uv run make_prompt.py && uv run run_ai_test.py
"""
import os
import sys
import time

from dotenv import load_dotenv
from google import genai

from scoring import score_answers

load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    sys.exit("GEMINI_API_KEY is not set. Add it to a local .env file.")

model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
prompt = open("prompt_for_ai.txt", encoding="utf-8").read()

client = genai.Client()
start = time.time()
response = client.models.generate_content(model=model, contents=prompt)
elapsed = time.time() - start

out_path = f"ai_answers_api_{model}.sql".replace("/", "_")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(response.text)
print(f"Model: {model} | {elapsed:.1f}s | saved {out_path}\n")

score_answers(response.text)
