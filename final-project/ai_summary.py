import os
from openai import OpenAI
from typing import List, Dict, Any

def get_ai_task_summary(tasks: List[Dict[str, Any]]) -> str:
    """
    Generate an AI-powered summary of tasks using OpenAI's API.
    
    :param tasks: List of task dictionaries
    :return: AI-generated summary string
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return "❌ Error: OPENAI_API_KEY environment variable not set.\nPlease set your API key with: $env:OPENAI_API_KEY = \"your-key-here\""
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Prepare task data for the prompt
        if not tasks:
            return "📝 No tasks to summarize."
        
        task_details = []
        for task in tasks:
            task_info = f"- {task['description']} (Utility: {task['utility_score']}, Cost: {task['cost_hours']}hrs, Status: {task['status']}"
            if task.get('deadline'):
                task_info += f", Deadline: {task['deadline']}"
            task_info += ")"
            task_details.append(task_info)
        
        tasks_text = "\n".join(task_details)
        
        prompt = f"""You are an AI assistant helping students prioritize their tasks. 
Analyze the following tasks and provide a brief, insightful summary (3-5 sentences) that:
1. Identifies high-priority tasks based on utility/cost ratio
2. Highlights any urgent deadlines
3. Suggests a recommended order of completion
4. Provides motivational advice

Tasks:
{tasks_text}

Provide a concise, actionable summary."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful task management assistant for students studying economics and computer science."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        summary = response.choices[0].message.content
        return f"🤖 AI Task Summary:\n\n{summary}"
        
    except Exception as e:
        return f"❌ Error generating AI summary: {str(e)}"
