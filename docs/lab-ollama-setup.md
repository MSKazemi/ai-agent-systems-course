# Lab Ollama Setup — SSH Port Forwarding

The course LLM runs on a shared lab server. You do **not** need to install Ollama on your own machine.

To use it, you open an SSH tunnel that forwards the lab's Ollama port to your laptop. Once the tunnel is running, every course example works automatically — no other changes needed.

> **Your instructor will give you `YOUR_USERNAME` and `LAB_SERVER` privately.**  
> The SSH port is **2223**.

---

## Step 1 — Open the SSH tunnel

Run this command in a terminal and **leave it open** the entire time you work on the course.

### Linux / macOS

```bash
ssh YOUR_USERNAME@LAB_SERVER -p 2223 -L 11434:localhost:11434
```

### Windows (PowerShell or Command Prompt)

```bat
ssh YOUR_USERNAME@LAB_SERVER -p 2223 -L 11434:localhost:11434
```

### Windows (Git Bash)

```bash
ssh YOUR_USERNAME@LAB_SERVER -p 2223 -L 11434:localhost:11434
```

The terminal will appear to hang after you enter your password — that is correct. The tunnel is active. **Do not close this terminal.**

---

## Step 2 — Verify the tunnel works

Open a **second** terminal and run:

```bash
curl http://localhost:11434/api/tags
```

You should see a JSON list of available models. If you get `Connection refused`, the tunnel is not running — go back to Step 1.

---

## Step 3 — Configure your `.env`

In your root `.env` (copied from `.env.example`), make sure these lines are set:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:35b
```

`localhost:11434` is correct — it refers to the local end of the SSH tunnel, which the course code sees as if Ollama were installed on your machine.

---

## How it works

```text
Your laptop                      Lab server
───────────────────────────────────────────────────
your code
  │  http://localhost:11434
  ▼
SSH tunnel ─── encrypted ──────► Ollama on server
  (port 11434)                    (port 11434)
```

The tunnel is completely transparent to all course examples — nothing in the code knows or cares that Ollama is remote.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Connection refused` on port 11434 | SSH tunnel not running — reopen it |
| `Permission denied (publickey)` | Wrong username — double-check with your instructor |
| Tunnel drops after a few minutes | Use the keepalive command below |
| Windows: `ssh` command not found | Install [Git for Windows](https://git-scm.com/download/win) or use PowerShell 7+ |

---

## Keeping the tunnel alive (optional)

If the tunnel drops on idle networks, add keepalive flags:

```bash
ssh YOUR_USERNAME@LAB_SERVER -p 2223 -L 11434:localhost:11434 -o ServerAliveInterval=60 -o ServerAliveCountMax=5
```

This sends a heartbeat every 60 seconds so the connection stays open.
