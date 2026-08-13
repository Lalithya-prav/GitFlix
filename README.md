# 🎬 GitFlix — Repository History Visualizer & Replay Engine

> Turn your Git commit history into an interactive retro movie reel and visual web dashboard.

![GitFlix Banner](https://img.shields.io/badge/GitFlix-v1.0-brightgreen?style=for-the-badge&logo=git)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow?style=for-the-badge&logo=javascript)

---

## 🍿 What is GitFlix?

**GitFlix** is a dual-interface developer tool that turns boring `git log` outputs into an engaging, visual timeline. Whether you prefer a retro terminal experience (TUI) or an interactive browser dashboard, GitFlix lets you **replay repository history frame-by-frame** like a movie.

### ✨ Key Features
* 📺 **Retro Terminal HUD (Rich TUI):** High-level repository metrics right in your console.
* 🎬 **TUI Movie Reel (`--replay`):** Watch commits unfold frame-by-frame chronologically in ASCII styling.
* 📊 **Interactive Web Dashboard:** Animated growth charts powered by Chart.js.
* 🔄 **Shared Data Pipeline:** Single-pass Git parsing exported to JSON for seamless TUI and browser sync.

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
* Python 3.8+
* Git installed on your system

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Lalithya-prav/gitflix.git](https://github.com/Lalithya-prav/gitflix.git)
   cd gitflix

1. Set up a virtual environment:
   python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

2. Install dependencies:
pip install rich

## 🎮 Usage
### 1. Terminal Dashboard (TUI)
Run GitFlix inside any local Git repository:


python main.py

### 2. Run the Movie Reel Replay Mode
Replay the commit timeline frame-by-frame:


python main.py --replay

### 3. Launch the Web Dashboard
Serve the local web dashboard to view animated growth charts:


python -m http.server 8000

Open http://localhost:8000 in your browser and click ▶ Play Replay!

---

# 🏗️ How It Works (Architecture)

GitFlix uses a **decoupled, single-parse architecture**. A Python-based backend analyzes the local Git history once, powering both a terminal-based rich user interface (TUI) and an interactive web dashboard through a shared JSON data contract.

---

### 🔄 Data Flow Diagram

```text
┌─────────────────────────────────────────────────────────┐
│                 Local Git Repository                    │
└────────────────────────────┬────────────────────────────┘
                             │ (Subprocess / Git CLI)
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    git_parser.py                        │
│  • Extracts SHAs, authors, dates, and commit messages   │
│  • Calculates file changes, insertions, and deletions   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                 stats_calculator.py                     │
│  • Computes high-level metrics (net growth, lifespan)   │
│  • Identifies top contributors and peak commits        │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│        Rich TUI          │   │   gitflix_data.json      │
│  • Interactive Dashboard │   │     (Shared Bridge)      │
│  • Frame-by-Frame Reel   │   └──────────┬───────────────┘
└──────────────────────────┘              │
                                          ▼
                               ┌──────────────────────────┐
                               │   Web Browser Dashboard  │
                               │  • Chart.js Visualizer   │
                               │  • Interactive Replay    │
                               └──────────────────────────┘

```

## 🛠️ Built With

* **Python & Rich Library:** Powers the Terminal UI (TUI) components, layout splitting, and frame-by-frame rendering engine.
* **JavaScript & Chart.js:** Handles the responsive, animated timeline growth charts and interactive browser replays.
* **HTML5 & CSS3:** Provides a modern, responsive dark-mode web dashboard interface.

---
