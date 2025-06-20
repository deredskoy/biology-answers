# Biology Answers

This repository contains exam questions for anatomy and cytology.
The `generate_answers.py` script can generate Russian answers
using OpenAI's API. Each answer is saved in a separate text file
within the `answers` directory.

## Usage

1. Install dependencies
   ```bash
   pip install openai
   ```
2. Export your OpenAI API key
   ```bash
   export OPENAI_API_KEY="sk-proj-..."
   ```
3. Run the script (set `MAX_Q` to limit the number of questions)
   ```bash
   MAX_Q=2 python3 generate_answers.py
   ```
   The script creates `answers/<question>.txt` for each question it
   processes. Existing files are skipped, so you can rerun the script
   to continue generating the rest.
