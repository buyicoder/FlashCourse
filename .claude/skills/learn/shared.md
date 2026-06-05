# Learn Skill — 共享规范

本文件定义所有子 skill 共用的数据格式、文件路径和协作协议。

---

## 数据目录

所有学习数据统一存储在项目根目录下的 `learn-sessions/`：

```
learn-sessions/
├── _index.json          ← 跨学科索引
└── {科目名}/
    ├── progress.json    ← 核心学习状态
    ├── notes.md         ← 学生笔记（深度学习模式主输出）
    └── cards.json       ← 闪卡数据（考试冲刺模式主输出）
```

### _index.json Schema

```json
[
  {
    "subject": "string, 学科名称",
    "mode": "deep | sprint",
    "status": "not_started | in_progress | completed",
    "updated": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

跨学科索引是一个数组，每个元素代表一门课程的学习状态摘要。入口 skill 在创建/更新学习记录时维护此文件，`/learn --list` 命令读取此文件展示所有进度。

项目根目录通过 `$CLAUDE_PROJECT_DIR` 获取（如果不可用，默认 `.`）。

所有路径均相对于项目根目录（`$CLAUDE_PROJECT_DIR` 或当前工作目录）。

---

## progress.json Schema

```json
{
  "schema_version": 1,
  "subject": "string, 学科名称",
  "mode": "deep | sprint",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS",
  "status": "not_started | in_progress | completed",
  "current_stage": "string, 当前教学阶段描述",
  "exam_points": [
    {
      "id": "string, 考点唯一ID",
      "topic": "string, 考点名称",
      "weight": "高频 | 中频 | 低频",
      "difficulty": "简单 | 中等 | 困难",
      "question_types": ["选择", "计算", "证明"],
      "flashcard": {
        "front": "string, 闪卡正面（问题）",
        "back": "string, 闪卡背面（答案，可含 KaTeX）"
      },
      "mastery": "number 0-5, 掌握度评分",
      "total_questions": "number, 总做题数",
      "correct": "number, 正确数"
    }
  ],
  "deep_topics": [
    {
      "id": "string",
      "topic": "string",
      "mastery": "number 0-5",
      "notes_summary": "string, 学生笔记摘要",
      "project_status": "not_started | in_progress | completed"
    }
  ],
  "weak_points": ["string array, 薄弱考点ID"],
  "material_summary": "string, 已解析材料概述",
  "constraints": "string | null, 时间/范围约束"
}
```

**模式与字段对应关系：**
- `sprint` 模式使用 `exam_points` 数组（考点驱动），`deep_topics` 为空数组
- `deep` 模式使用 `deep_topics` 数组（主题驱动），`exam_points` 为空数组
- `mode` 字段决定哪个数组为主要数据源，可视化页面根据 `mode` 选择渲染哪个数组

### 掌握度评分标准

| 分数 | 含义 |
|------|------|
| 0 | 未开始学习 |
| 1 | 初步接触，能识别概念 |
| 2 | 能回忆关键公式/定义，需提示才能应用 |
| 3 | 能独立解决基础题目，合格线 |
| 4 | 能解决中等难度题目，理解概念间联系 |
| 5 | 能解决综合/挑战题，可用自己语言讲解给他人 |

## cards.json Schema

```json
{
  "schema_version": 1,
  "subject": "string",
  "updated_at": "YYYY-MM-DDTHH:MM:SS",
  "cards": [
    {
      "id": "string, 与 exam_point.id 对应",
      "topic": "string",
      "front": "string, 正面问题",
      "back": "string, 背面答案（可含 KaTeX）",
      "difficulty": "简单 | 中等 | 困难",
      "last_reviewed": "YYYY-MM-DDTHH:MM:SS | null",
      "correct_count": "number",
      "wrong_count": "number"
    }
  ]
}
```

## 可视化页面协议

每次教学阶段完成后，skill 必须将最新的 `progress.json` 和 `cards.json` 同步写入以下两个位置：

1. **数据源**：`learn-sessions/{科目名}/progress.json` 和 `cards.json`
2. **可视化镜像**：`.claude/skills/learn/visualize/data/progress.json` 和 `cards.json`

确保 `visualize/data/` 目录存在后再写入。学生用浏览器打开 `visualize/index.html` 即可看到最新数据。

所有路径均相对于项目根目录（`$CLAUDE_PROJECT_DIR` 或当前工作目录）。

## 跨模块调用约定

Claude Code skill 系统通过对话上下文传递状态，不通过函数调用或文件传递。

**分发机制：**
入口 skill（skill.md）完成信息收集后，在对话中明确指示：
"现在请按照 deep.md 中定义的深度学习教学流程开始教学。学科、模式、材料信息已在对话上下文中，不需要重新收集。"

模型在上下文中同时持有 skill.md 和 deep.md（或 sprint.md）的内容，自动切换行为模式。

**输入约定：**
- 入口 skill 已将学科、模式、材料摘要、约束条件写入对话上下文
- 子 skill 不需要重新收集这些信息（已在上下文中存在）
- 子 skill 的 prompt 被加载后，直接按照其定义的教学流程开始执行

**输出约定：**
- 子 skill 将学习数据写入 `learn-sessions/{科目名}/`（通过 Write 工具）
- 每个教学阶段完成后同步写入 `visualize/data/`（可视化镜像）
- 进度数据结构遵循本文档定义的 JSON schema
