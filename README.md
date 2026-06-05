# ⚡ FlashCourse

> The Claude Code skill that helps college students master any STEM subject in days, not weeks.

Built for students who need to learn fast and learn well. Dual modes: **Deep Understanding** (first-principles + projects) or **Exam Sprint** (flashcards + drills).

---

## Quick Start

### Install

Copy the skill into your Claude Code project:

```bash
# From your project root
mkdir -p .claude/skills
git clone https://github.com/buyicoder/FlashCourse.git
cp -r FlashCourse/.claude/skills/learn .claude/skills/
```

Or add as a submodule:

```bash
git submodule add https://github.com/buyicoder/FlashCourse.git .claude/skills/learn
```

### Usage

```
/learn 线性代数              Start learning a subject
/learn --list                View all learning progress
/learn 信号与系统            Resume a previous session
```

Open `.claude/skills/learn/visualize/index.html` in your browser to see the study dashboard.

---

## Two Modes, One Goal

| | 🧠 Deep Learning | 📝 Exam Sprint |
|---|---|---|
| **Philosophy** | Understand from first principles | Maximize score in minimum time |
| **Pace** | Slow, student-driven | Fast, exam-point-driven |
| **Method** | Socratic questioning + projects | Flashcards + drills + error review |
| **Output** | Notes + runnable project code | Flashcards + mock exams + error log |
| **Best for** | Building lasting knowledge | Crushing tomorrow's final |

You can switch modes anytime during a session.

---

## Dashboard

The built-in visualization page shows:

- 🗺 **Exam Point Map** — Mermaid mind map colored by mastery
- 🃏 **Flashcards** — CSS 3D flip cards with KaTeX formulas
- 📊 **Progress** — Chart.js doughnut + per-topic mastery bars
- 📋 **Error Review** — Expandable error cards with root cause analysis

---

## Supported Materials

FlashCourse can work with:
- Plain text topic names
- PDF courseware / textbooks
- Screenshots of notes
- Course website URLs (auto-scraped)
- Exam syllabi and scope descriptions

No materials? No problem — FlashCourse teaches from its own STEM knowledge.

---

## Project Structure

```
.claude/skills/learn/
├── skill.md          # Entry point: info collection → mode dispatch
├── shared.md         # Data schemas & cross-module protocols
├── deep.md           # Deep learning sub-skill (7-step flow)
├── sprint.md         # Exam sprint sub-skill (5-step drill)
└── visualize/
    ├── index.html    # Study dashboard (open in browser)
    └── data/         # Mirrored session data for visualization
```

---

## Requirements

- [Claude Code](https://claude.ai/code)
- A modern browser (Chrome / Firefox / Edge) for the dashboard
- No server, no install, no API keys beyond Claude Code

---

## License

MIT
