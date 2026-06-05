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

项目根目录通过 `$CLAUDE_PROJECT_DIR` 获取（如果不可用，默认 `.`）。

---

## progress.json Schema

```json
{
  "subject": "string, 学科名称",
  "mode": "deep | sprint",
  "created_at": "YYYY-MM-DD",
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

## cards.json Schema

```json
{
  "subject": "string",
  "updated_at": "YYYY-MM-DDTHH:MM:SS",
  "cards": [
    {
      "id": "string, 与 exam_point.id 对应",
      "topic": "string",
      "front": "string, 正面问题",
      "back": "string, 背面答案（可含 KaTeX）",
      "difficulty": "简单 | 中等 | 困难",
      "last_reviewed": "YYYY-MM-DD | null",
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

## 跨模块调用约定

入口 skill 调用子 skill 的方式：在学生确认模式和学科后，入口 skill 提示模型"现在加载并遵循 {deep|sprint}.md 中的教学流程"。子 skill 的 prompt 内容由模型在上下文中参照执行。

子 skill 不需要重新收集已由入口 skill 确认的信息（学科、模式、材料摘要、约束）。这些信息在对话上下文中已经存在。
