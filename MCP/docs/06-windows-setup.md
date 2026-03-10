# 06 – Setup for Windows

Guide to install Git, Python, and VS Code on Windows so you can run this course.

---

## 1. Git (command line)

Git is needed to clone the repo and run `git` commands.

### Install

1. Download: [git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer.
3. **Important:** On the "Adjusting your PATH environment" step, choose **"Git from the command line and also from 3rd-party software"** so `git` works in any terminal.
4. Finish the installer.

### Verify

Open **Command Prompt** or **PowerShell** (Win+R → type `cmd` or `powershell`):

```cmd
git --version
```

You should see something like `git version 2.43.0`. If you get "git is not recognized", close and reopen the terminal, or check that Git was added to PATH during install.

---

## 2. Python

Python is needed to run the MCP server and client.

### Install

1. Download: [python.org/downloads](https://www.python.org/downloads/) – get the latest 3.x.
2. Run the installer.
3. **Important:** Check **"Add python.exe to PATH"** at the bottom before clicking Install.
4. Click "Install Now" (or "Customize" if you want to change the install folder).
5. Finish the installer.

### Verify

Open a **new** Command Prompt or PowerShell:

```cmd
python --version
```

You should see e.g. `Python 3.12.0`. If you get "python is not recognized", run the installer again and ensure "Add to PATH" was checked.

---

## 3. VS Code

VS Code is the editor where you can add MCP servers and use them in Chat.

### Install

1. Download: [code.visualstudio.com](https://code.visualstudio.com/)
2. Run the installer.
3. Optional: Check **"Add to PATH"** so you can open folders with `code .` from the command line.
4. Finish the installer.

### Python extension

1. Open VS Code.
2. Press `Ctrl+Shift+X` to open Extensions.
3. Search for **Python** (by Microsoft).
4. Click **Install**.

### Open the project from terminal

After cloning:

```cmd
cd C:\Users\YourName\MCP-LBDA
code .
```

This opens the folder in VS Code.

---

## 4. Run the course (Windows)

From **Command Prompt** or **PowerShell**:

```cmd
git clone https://github.com/MSKazemi/MCP-LBDA.git
cd MCP-LBDA

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python examples/01-calculator/server.py
```

**Note:** Use `python` (not `python3`) on Windows. Use `.venv\Scripts\activate` to activate the venv. The prompt will show `(.venv)` when active.

---

## 5. MCP config paths on Windows

When adding MCP servers in VS Code or Cursor, use Windows paths.

**Python in venv:**
```
C:\Users\YourName\MCP-LBDA\.venv\Scripts\python.exe
```

**Server script:**
```
C:\Users\YourName\MCP-LBDA\examples\01-calculator\server.py
```

**In JSON**, escape backslashes or use forward slashes:

```json
{
  "servers": {
    "calculator": {
      "command": "C:/Users/YourName/MCP-LBDA/.venv/Scripts/python.exe",
      "args": ["C:/Users/YourName/MCP-LBDA/examples/01-calculator/server.py"]
    }
  }
}
```

Replace `YourName` with your Windows username. Forward slashes work in JSON on Windows.
