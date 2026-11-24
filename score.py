import sys

from scoring import score_answers

path = sys.argv[1] if len(sys.argv) > 1 else "ai_answers.sql"
score_answers(open(path, encoding="utf-8").read())
