# 📊 Task Manager CLI

A Python CLI tool for Economics & Computer Science students to manage tasks with utility-based prioritization. 🎓💻

## ✨ Features

- **➕ Add Tasks**: Create tasks with description, utility score (1-100), time cost (hours), and optional deadlines
- **📋 List Tasks**: View all tasks sorted by ROI (Return on Investment = utility / cost)
- **✏️ Edit Tasks**: Update task properties (description, utility, cost, deadline, status)
- **🔍 Search Tasks**: Find tasks by keyword (case-insensitive)
- **👁️ View Task Details**: See comprehensive information about a task including linked tasks
- **🔗 Link Tasks**: Create relationships between related or dependent tasks
- **🗑️ Delete Tasks**: Remove tasks by ID
- **🤖 AI Task Summary**: Get AI-powered insights and recommendations for your tasks using OpenAI
- **🧠 Smart Prioritization**: Automatically calculates and displays ROI to help make rational choices

## 🚀 Installation

1. Create a virtual environment (optional but recommended):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies:
```powershell
pip install typer rich openai
```

3. Set up your OpenAI API key (for AI summary feature):
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

## 💡 Usage

### ➕ Add a Task
```powershell
python main.py add "Study microeconomics" 90 5
python main.py add "Complete Python assignment" 80 3 --deadline "2024-12-15"
python main.py add "Read research paper" 60 2
```

### 📋 List All Tasks
```powershell
python main.py list
```
Tasks are displayed in a table sorted by ROI (highest first) - showing "The Rational Choice" at the top! 🏆

### 🔍 Search for Tasks
```powershell
python main.py search "python"
python main.py search "study"
```

### 🗑️ Delete a Task
```powershell
python main.py delete 1
```

### ✏️ Edit a Task
```powershell
python main.py edit 1 --description "Study microeconomics chapter 5"
python main.py edit 2 --utility 95 --cost 4
python main.py edit 3 --deadline "2024-12-20" --status "complete"
```
Update any combination of task properties. Only specified fields will be changed.

### 👁️ View Task Details
```powershell
python main.py view 1
```
See all details about a task including its linked tasks in a formatted panel.

### 🔗 Link Tasks Together
```powershell
python main.py link 1 2
```
Create a bidirectional link between two tasks to show they're related or dependent.

### 🔓 Unlink Tasks
```powershell
python main.py unlink 1 2
```
Remove the relationship between two tasks.

### 🤖 Get AI Task Summary
```powershell
python main.py ai-summary
```
Get AI-powered insights, priority recommendations, and motivational advice based on your current tasks! Requires `OPENAI_API_KEY` environment variable.

## 📦 Data Structure

Each task is stored with the following fields:
- **id** (int): Auto-incrementing unique identifier
- **description** (str): Task description
- **utility_score** (int): Value/importance of the task (1-100)
- **cost_hours** (float): Estimated time to complete in hours
- **status** (str): Task status ('pending' or 'complete')
- **deadline** (str, optional): Due date for the task
- **linked_tasks** (list[int]): IDs of tasks linked to this one

Tasks are stored in `tasks.json` in the same directory.

## 🔗 Task Linking System

The task linking system allows you to create relationships between tasks:
- **Dependencies**: Link a task to prerequisite tasks that must be completed first
- **Related Work**: Group similar or related tasks together
- **Project Phases**: Connect tasks that are part of the same larger project

Links are **bidirectional** - linking task A to task B automatically links B to A. The `view` command shows all linked tasks, and the `list` command displays the number of links each task has.

## 📈 ROI Calculation

**ROI (Return on Investment) = Utility Score / Cost (Hours)**

This metric helps prioritize tasks that provide the most value for the least time investment - a key concept in economics for rational decision-making. 💰⏱️

## 📋 Requirements

- Python 3.12+
- typer
- rich
- openai (for AI task summary feature)

## 📁 Project Structure

```
final-project/
├── main.py           # 🖥️ CLI interface
├── task_manager.py   # 🔧 TaskManager class
├── ai_summary.py     # 🤖 AI integration for task summaries
├── tasks.json        # 💾 Task data storage
└── README.md         # 📖 This file
```
