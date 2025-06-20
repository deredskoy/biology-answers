import openai, re, os, json
from pathlib import Path

openai.api_key = os.environ.get('OPENAI_API_KEY')

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

print('total questions', len(questions))

answers = []
# open existing answers file if exists to resume
existing = {}
if Path('answers.txt').exists():
    with open('answers.txt', encoding='utf8') as f:
        cur_q = None
        cur_a = []
        for line in f:
            if line.startswith('## '):
                if cur_q:
                    existing[cur_q] = '\n'.join(cur_a).strip()
                    cur_a=[]
                cur_q=line[3:].strip()
            else:
                cur_a.append(line.rstrip())
        if cur_q:
            existing[cur_q] = '\n'.join(cur_a).strip()

start=len(existing)
print('existing answers', len(existing))

with open('answers.txt', 'w', encoding='utf8') as out:
    out.write('# Ответы на вопросы\n\n')
    max_questions = int(os.environ.get('MAX_Q', '124'))
    for idx, q in enumerate(questions, 1):
        out.write(f'## {q}\n')
        if q in existing:
            out.write(existing[q]+'\n\n')
            continue
        prompt=f"""Ответь на следующий вопрос на русском языке подробно (минимум 230 слов): {q}"""
        try:
            resp = openai.chat.completions.create(
                model='gpt-4o',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            ans = resp.choices[0].message.content.strip()
        except Exception as e:
            ans=f'Не удалось получить ответ из-за ошибки: {e}'
        out.write(ans+'\n\n')
        if idx >= max_questions:
            break
print('done')
