import os
from openai import OpenAI

# We'll use gpt-4o-mini, the latest fast and capable model
MODEL = "gpt-4o-mini"

# This is the system prompt that "instructs" the AI on its job.
# This is key to getting a short phrase instead of a full sentence.
SYSTEM_PROMPT = (
    "You are an expert project manager. Your job is to summarize a "
    "task description into a very short, actionable title or phrase. "
    "Limit your response to 5 words or less. "
    "Do not use punctuation. Just output the phrase."
)

def get_task_summary(client: OpenAI, task_description: str) -> str:
    """
    Sends a task description to the OpenAI API and returns a short summary.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": task_description},
            ],
            temperature=0.1,  # Low temperature for more predictable, less "creative" summaries
            max_tokens=20,    # Limit the output length just in case
        )
        # Extract the text content from the API's response
        summary = response.choices[0].message.content
        return summary.strip()
    
    except Exception as e:
        # Handle potential errors (like network issues or wrong API key)
        return f"[Error summarizing task: {e}]"

def main():
    """
    Main function to run the summarization loop.
    """
    print(f"🤖 Using model: {MODEL}\n")

    # Check if the API key is set before trying to create the client
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your API key and try again.")
        print(r'Example: $env:OPENAI_API_KEY = "your-key-here"')
        return

    # Initialize the OpenAI client
    # It automatically reads the OPENAI_API_KEY from the environment
    client = OpenAI()

    # --- Requirement 2: Add at least 2 sample descriptions ---
    tasks_to_summarize = [
        (
            "We need to go through the entire user database, identify all accounts "
            "that haven't logged in for over six months, and compile a report. "
            "This report should then be sent to the marketing team so they can "
            "run a re-engagement email campaign."
        ),
        (
            "The next major feature is the ability for users to upload a profile "
            "picture. This involves changes to the frontend UI to add the "
            "upload button, a new backend endpoint to handle the image file, "
            "and a new S3 bucket to store the images securely."
        ),
    ]

    print("--- 🚀 Starting Task Summarization ---")

    # --- Requirement 1: Add a loop to summarize multiple descriptions ---
    for i, task in enumerate(tasks_to_summarize, 1):
        print(f"\n[Task {i} Original]")
        print(f"'{task}'")
        
        # Get the summary from the API
        summary = get_task_summary(client, task)
        
        print(f"\n[Task {i} Summary]")
        print(f"-> {summary}")
        print("-" * 30)
    
    print("\n--- ✅ All tasks summarized. ---")

# This standard Python entry point makes the file runnable
if __name__ == "__main__":
    main()