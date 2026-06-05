# ⚡ FlashCourse

> 帮助大学生在几天内（而非几周）掌握任何理工科科目的 Claude Code 技能。

两种模式自由切换：**深度学习**（第一性原理 + 项目实战）或 **考试冲刺**（闪卡 + 题海战术）。为需要学得快、学得好的大学生打造。

---

## 安装（30 秒搞定）

**方法一：一句话安装（推荐）**

在 Claude Code 中粘贴这句话：

```
Install the FlashCourse skill from https://github.com/buyicoder/FlashCourse
```

Claude Code 会自动克隆仓库并配置好技能。

**方法二：手动安装**

```bash
git clone https://github.com/buyicoder/FlashCourse.git
cp -r FlashCourse/.claude/skills/learn .claude/skills/
```

---

## 使用

```
/learn 线性代数              开始学习一门课
/learn --list                查看所有学习进度
/learn 信号与系统            恢复上次学习
```

用浏览器打开 `.claude/skills/learn/visualize/index.html` 查看可视化学习看板。

---

## 两种模式

| | 🧠 深度学习 | 📝 考试冲刺 |
|---|---|---|
| **理念** | 从第一性原理理解本质 | 最短时间拿最高分数 |
| **节奏** | 慢，学生主导 | 快，考点驱动 |
| **方法** | 苏格拉底提问 + 项目实战 | 闪卡记忆 + 刷题 + 错题复盘 |
| **产出** | 笔记 + 可运行的代码项目 | 闪卡 + 模拟卷 + 错题日志 |
| **适合** | 建立长期知识体系 | 搞定明天的期末考试 |

学习过程中随时可以说"切换到冲刺模式"或"切换到深度模式"。

---

## 可视化看板

- 🗺 **考点地图** — Mermaid 思维导图，按掌握度着色
- 🃏 **闪卡翻页** — CSS 3D 翻转动画，支持 KaTeX 公式
- 📊 **进度看板** — Chart.js 环形图 + 各考点掌握度
- 📋 **错题本** — 可展开的错题卡片，包含错因分析

---

## 支持的学习材料

- 纯文本主题名（如"线性代数"）
- PDF 课件 / 教材
- 课堂笔记截图
- 课程网站链接（自动抓取）
- 考试大纲和范围说明

没有材料也能学——FlashCourse 基于自身理工科知识直接教学。

---

## 项目结构

```
.claude/skills/learn/
├── skill.md          # 入口：信息收集 → 模式分发
├── shared.md         # 数据规范 & 跨模块协议
├── deep.md           # 深度学习子技能（七步教学）
├── sprint.md         # 考试冲刺子技能（五步训练）
└── visualize/
    ├── index.html    # 可视化看板（浏览器打开）
    └── data/         # 可视化数据镜像
```

---

## 环境要求

- [Claude Code](https://claude.ai/code)
- 现代浏览器（Chrome / Firefox / Edge）
- 无需服务器、无需安装、无需额外 API Key

---

## 许可证

MIT

---

> *The Claude Code skill that helps college students master any STEM subject in days, not weeks. Dual modes: deep understanding (first-principles + projects) or exam sprint (flashcards + drills).*
