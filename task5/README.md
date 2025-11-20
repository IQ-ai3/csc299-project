# 📋 Name Storage CLI

## 🌟 Overview
The Name Storage CLI is a command-line tool designed to store and manage a list of names. It allows users to add names to a local JSON file and list them in alphabetical order (case insensitive).

## ✨ Features
- ➕ Add names to the storage.
- 📜 List all stored names in alphabetical order.
- 💾 Data is persisted in a local JSON file.

## 🔧 Requirements
- 🐍 Python 3.14 or higher.
- 📦 Dependencies managed using `uv`.

## 🚀 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/IQ-ai3/csc299-project.git
   cd csc299-project/task5
   ```
2. Install dependencies:
   ```bash
   uv pip install click pytest
   ```

## 📖 Usage
1. Add a name:
   ```bash
   python main.py add "John Doe"
   ```
2. List all names:
   ```bash
   python main.py list-names
   ```

## 🧪 Testing
Run the following command to execute all tests:
```powershell
python -m pytest
```

## 🛠️ Development
- ✅ Ensure all changes are tested before committing.
- 📝 Follow the project's contribution guidelines.

## 📄 License
This project is licensed under the MIT License.