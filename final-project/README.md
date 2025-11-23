# 📊 Task Manager CLI

A Python CLI tool for Economics & Computer Science students to manage tasks with utility-based prioritization. 🎓💻

## ✨ Features

- **➕ Add Tasks**: Create tasks with description, utility score (1-100), and time cost (hours)
- **📋 List Tasks**: View all tasks sorted by ROI (Return on Investment = utility / cost)
- **🔍 Search Tasks**: Find tasks by keyword (case-insensitive)
- **🗑️ Delete Tasks**: Remove tasks by ID
- **🧠 Smart Prioritization**: Automatically calculates and displays ROI to help make rational choices

## 🚀 Installation

1. Create a virtual environment (optional but recommended):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies:
```powershell
pip install typer rich
```

## 💡 Usage

### ➕ Add a Task
```powershell
python main.py add "Study microeconomics" 90 5
python main.py add "Complete Python assignment" 80 3
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

## 📦 Data Structure

Each task is stored with the following fields:
- **id** (int): Auto-incrementing unique identifier
- **description** (str): Task description
- **utility_score** (int): Value/importance of the task (1-100)
- **cost_hours** (float): Estimated time to complete in hours
- **status** (str): Task status ('pending' or 'complete')

Tasks are stored in `tasks.json` in the same directory.

## 📈 ROI Calculation

**ROI (Return on Investment) = Utility Score / Cost (Hours)**

This metric helps prioritize tasks that provide the most value for the least time investment - a key concept in economics for rational decision-making. 💰⏱️

## 📋 Requirements

- Python 3.12+
- typer
- rich

## 📁 Project Structure

```
final-project/
├── main.py           # 🖥️ CLI interface
├── task_manager.py   # 🔧 TaskManager class
├── tasks.json        # 💾 Task data storage
└── README.md         # 📖 This file
```
