# tasks4 🚀

A small command-line tool that summarizes long task descriptions into a very short, actionable phrase (5 words or less) using the OpenAI API. It's designed as a tiny demo/utility for converting verbose requirements into concise task titles that are easy to slot into a project board.

Features
- Uses OpenAI's chat API to generate short, predictable summaries.
- Includes a simple CLI entry point so you can run it with `python -m tasks4`.
- Prints sample summaries for a couple of example tasks.

Quickstart

1. Install Python 3.8+ and pip.
2. Install the required package (the script uses the official OpenAI SDK):

```powershell
pip install openai
```

3. Set your OpenAI API key in PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

4. Run the summarizer:

```powershell
python -m tasks4
```

What it does
- Reads a small list of sample task descriptions included in `src/tasks4/__main__.py`.
- Sends each description to the OpenAI API with a system prompt that instructs the model to return a terse phrase (5 words or fewer).
- Prints the original description and the generated short summary.

Notes & troubleshooting
- Make sure `OPENAI_API_KEY` is set correctly; the script will print an error if it's missing.
- The script sets a low temperature and token limit to encourage concise, repeatable outputs.
- If you want to summarize your own tasks, modify the `tasks_to_summarize` list in `src/tasks4/__main__.py` or adapt the code to read from a file or stdin.

License
- This repository does not include a license file by default. Add one if you plan to publish the project publicly.

Enjoy! ✨

