"""Generate Russian answers for exam questions.

This script reads questions from ``anatomy.txt`` and ``cytology.txt`` and
creates a separate text file for each answer inside the ``answers``
directory. File names are derived from the questions so they are valid on all
platforms. Existing files are not overwritten, which allows the script to be
run incrementally.
"""

import openai
import re
import os
from pathlib import Path

openai.api_key = os.environ.get("OPENAI_API_KEY")

# parse questions from text files
questions=[]
with open('anatomy.txt', encoding='utf8') as f:
    for line in f:
        t=line.strip()
        if not t or t.startswith('Вопросы'):
            continue
        questions.append(t)
with open('cytology.txt', encoding='utf8') as f:
    for line in f:
        t=line.strip()
        if not t or t.startswith('Перечень'):
            continue
        t=re.sub(r'^\d+\.\s*','',t)
        questions.append(t)

print("total questions", len(questions))

# Create directory for individual answer files
ans_dir = Path("answers")
ans_dir.mkdir(exist_ok=True)

def slugify(text: str) -> str:
    """Return a filesystem-friendly name derived from *text*."""
    text = re.sub(r"[^\w\s-]", "", text)
    text = "_".join(text.split())
    return text[:50] or "question"

max_questions = int(os.environ.get("MAX_Q", "124"))
for idx, q in enumerate(questions, 1):
    fname = ans_dir / f"{slugify(q)}.txt"
    if fname.exists():
        print(f"skip existing {fname.name}")
        continue
    prompt = f"Ответь на следующий вопрос на русском языке подробно (минимум 400 слов): {q}"
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        ans = resp.choices[0].message.content.strip()
    except Exception as e:
        ans = f"Не удалось получить ответ из-за ошибки: {e}"
    fname.write_text(ans + "\n", encoding="utf8")
    if idx >= max_questions:
        break
print("done")
