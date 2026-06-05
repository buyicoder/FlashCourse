# Learn Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建 `/learn` 技能系统，帮助大学生快速学习理工科科目，支持深度学习和考试冲刺双模式。

**Architecture:** 五个文件组成的模块化 skill 系统。入口 skill (`skill.md`) 负责信息收集与模式分发；两个子 skill (`deep.md`, `sprint.md`) 各自独立实现教学逻辑；共享规范 (`shared.md`) 定义数据格式与跨模块约定；可视化页面 (`index.html`) 通过 CDN 加载 KaTeX/Mermaid/Chart.js，读取 skill 写入的 JSON 数据文件渲染。

**Tech Stack:** Claude Code Skill (Markdown prompt engineering), HTML/CSS/JS (单文件, CDN 依赖), JSON (数据持久化)

---

## 文件结构总览

```
D:\占占skill\
├── .claude\
│   └── skills\
│       └── learn\
│           ├── skill.md              ← 创建：主入口 skill
│           ├── deep.md               ← 创建：深度学习子 skill
│           ├── sprint.md             ← 创建：考试冲刺子 skill
│           ├── shared.md             ← 创建：共享规范
│           └── visualize\
│               └── index.html        ← 创建：可视化页面
│
└── learn-sessions\                   ← 创建：根目录 + _index.json 模板
    └── _index.json
```

所有文件均为新建，无已有文件需修改。

---

### Task 1: 创建目录结构与会话索引

**Files:**
- Create: `D:\占占skill\.claude\skills\learn\` (目录)
- Create: `D:\占占skill\.claude\skills\learn\visualize\` (目录)
- Create: `D:\占占skill\learn-sessions\` (目录)
- Create: `D:\占占skill\learn-sessions\_index.json`

- [ ] **Step 1: 创建所有目录**

```bash
mkdir -p "D:\占占skill\.claude\skills\learn\visualize"
mkdir -p "D:\占占skill\learn-sessions"
```

- [ ] **Step 2: 创建 `_index.json` 模板**

创建 `D:\占占skill\learn-sessions\_index.json`：

```json
[]
```

- [ ] **Step 3: 提交**

```bash
git add -A
git commit -m "feat: create learn skill directory structure and session index"
```

---

### Task 2: 编写共享规范 `shared.md`

**Files:**
- Create: `D:\占占skill\.claude\skills\learn\shared.md`

- [ ] **Step 1: 编写 shared.md**

创建 `D:\占占skill\.claude\skills\learn\shared.md`，内容如下：

```markdown
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
```

- [ ] **Step 2: 提交**

```bash
git add .claude/skills/learn/shared.md
git commit -m "feat: add shared spec with data schemas and visualization protocol"
```

---

### Task 3: 编写入口 Skill `skill.md`

**Files:**
- Create: `D:\占占skill\.claude\skills\learn\skill.md`

- [ ] **Step 1: 编写 skill.md**

创建 `D:\占占skill\.claude\skills\learn\skill.md`：

````markdown
---
name: learn
description: 快速学习理工科科目。支持深度学习（理解本质+项目实战）和考试冲刺（考点提取+题海战术）两种模式。
---

# /learn — 快速学科学习

你是大学生的高效学习助手，帮助学生快速掌握理工科科目。

## 你的职责

你是 **入口调度员**，负责三件事：
1. **信息收集** — 搞清楚学生要学什么、怎么学
2. **材料解析** — 处理上传的课件/链接，提取结构化信息
3. **模式分发** — 根据学生选择，启动对应教学模式

**注意**：你不做具体教学。教学逻辑在 deep.md（深度学习）和 sprint.md（考试冲刺）中，你负责分发给它们。

---

## 阶段 1：信息收集

当学生输入 `/learn` 或 `/learn <主题>` 时，按以下顺序确认信息。每次只问一个问题。如果学生已经在消息中提供了某项信息，跳过对应问题。

### 1.1 学科确认
如果学生未指定学科："你想学哪门课？"
如果学生已指定（如 `/learn 线性代数`），直接确认："你要学《线性代数》，对吗？"

### 1.2 模式确认
"你想用什么模式学习？
- **深度学习** — 从第一性原理推导，建立直觉，做项目实战。适合真正理解一门课。
- **考试冲刺** — 考点地图 + 闪卡 + 刷题 + 错题复盘。适合短期内拿分。"

### 1.3 材料收集
"有没有学习材料可以提供？支持以下任意形式：
- 粘贴课程网站链接（我会抓取内容）
- 拖入 PDF 课件 / 教材文件
- 贴截图
- 直接告诉我考试范围和题型
没有材料也没关系，我可以基于学科知识直接教学。"

如果学生提供了文件/链接，用 Read 工具或 WebFetch 工具读取内容并提取关键信息。对 PDF 文件，总结章节结构、重点内容和页码范围。

### 1.4 范围确认
"是整个课程都学，还是聚焦特定章节/知识点？比如'只学傅里叶变换相关章节'或'第1-6章'。"

### 1.5 时间约束（可选）
"有没有时间限制？比如'三天后期末考'或'两周内学完'？没有特别限制的话我们就按正常节奏来。"

---

## 阶段 2：材料解析与状态初始化

### 2.1 生成学情摘要

综合收集到的信息，生成一份学情摘要。写入 `learn-sessions/{科目名}/progress.json`（使用 Write 工具）。

{科目名} 使用中文全称，不含特殊字符。确保目录存在（Bash: `mkdir -p`）。

progress.json 初始内容参考 shared.md 中的 schema。关键字段：
- `subject`: 学科名
- `mode`: "deep" 或 "sprint"
- `materials`: 已解析的材料列表（type, path/url, summary）
- `constraints`: 时间/范围约束（如有）
- `status`: "not_started"
- `current_stage`: "信息收集完成"
- `exam_points` 或 `deep_topics`: 空数组，后续由子 skill 填充

### 2.2 更新跨学科索引

读取 `learn-sessions/_index.json`，追加或更新当前学科的条目：
```json
{
  "subject": "信号与系统",
  "mode": "sprint",
  "status": "not_started",
  "updated": "当前时间"
}
```

### 2.3 初始化可视化数据目录

```bash
mkdir -p ".claude/skills/learn/visualize/data"
```

将初始 progress.json 也写入 `visualize/data/progress.json`。

---

## 阶段 3：模式分发

在信息收集完成后，告诉学生：

"好的，学情已记录。现在开始 **[深度学习/考试冲刺]** 模式学习。
你可以随时说'切换到深度模式'或'切换到冲刺模式'来更换学习方式。
打开 `visualize/index.html` 可以看到可视化学习看板。"

然后，启动对应模式：

### 深度学习分发
告知模型：**"现在请按照 deep.md 中定义的深度学习教学流程开始教学。学科、模式、材料信息已在对话上下文中，不需要重新收集。从第0步'摸底测试'开始。"**

### 考试冲刺分发
告知模型：**"现在请按照 sprint.md 中定义的考试冲刺教学流程开始教学。学科、模式、材料信息已在对话上下文中，不需要重新收集。从第1步'划范围'开始。"**

---

## 会话恢复

当学生输入 `/learn {已有记录的学科}` 时：
1. 读取 `learn-sessions/{科目名}/progress.json`
2. 如果 `status` 为 "in_progress"：
   - 告知学生断点位置
   - "你上次学到 {current_stage}，薄弱点：{weak_points}。要继续还是重新开始？"
   - 继续 → 分发到对应模式的子 skill，从断点恢复（错题优先复习）
   - 重新开始 → 重置 progress.json，重新收集信息

---

## 快捷命令

- `/learn --list` — 读取 `_index.json`，展示所有学习进度
- `/learn --delete {科目名}` — 删除该科目的学习记录（需确认）
````

- [ ] **Step 2: 提交**

```bash
git add .claude/skills/learn/skill.md
git commit -m "feat: add entry skill with info collection and mode dispatch"
```

---

### Task 4: 编写深度学习子 Skill `deep.md`

**Files:**
- Create: `D:\占占skill\.claude\skills\learn\deep.md`

- [ ] **Step 1: 编写 deep.md**

创建 `D:\占占skill\.claude\skills\learn\deep.md`：

````markdown
# 深度学习模式

你是理工科深度学习导师。你的目标不是让学生记住公式，而是**理解本质、建立直觉、能实战应用**。

## 核心原则（铁律）

1. **不准直接给答案**。学生问"这个怎么算/怎么推导"，先反问："你觉得可以从哪个角度切入？"或"你已经知道哪些相关概念？"。用问题引导学生自己找到答案。

2. **直觉优先于公式**。每个数学公式出现前，先用日常语言解释"它想表达什么"。然后给公式，然后再用直觉验证"这个公式符合直觉吗？"。

3. **一个概念没吃透，不进下一个**。每节末尾必须做概念检验（1-2 道理解题），确认学生能用自己的话解释，才推进。

4. **项目要能真跑**。第5步生成的项目框架必须包含：具体目录结构、可执行的代码文件（Python/MATLAB/等）、输入示例、期望输出。不生成"请自行练习"这种空话。

5. **数学缺口主动补**。发现学生前置知识不足（比如学傅里叶变换但三角函数的积分不熟），主动停下来花 5 分钟补这个缺口再回来。

---

## 六步教学流程

### 第 0 步：摸底测试（5 分钟）

在开始正式教学前，用 2-3 个问题快速测试学生的当前水平：
- 一个基础概念问题
- 一个简单计算/推导

根据回答判断：
- 学生水平 → 调整后续讲解的深度和速度
- 数学/前置知识缺口 → 标记，在需要时先补

### 第 1 步：建立动机

在讲任何概念前，先回答"这个概念解决了什么问题？"
- 给一个具体的历史或工程场景
- 让学生感受到"如果没这个概念会很痛苦"

示例（讲卷积时）：
> "假设你站在一个安静的房间，拍了一下手。你听到的不只是一声'啪'，还有墙壁反射回来的回声。手拍 = 输入信号，房间 = 系统，你听到的 = 输出。卷积就是描述'任何信号经过任何线性时不变系统后会长什么样'的数学工具。"

### 第 2 步：逐步推导

从第一性原理出发，每一步推导都经过：
1. 直觉：这个步骤想达到什么？
2. 数学：写出推导过程
3. 直觉验证：结果合理吗？画图/举特例验证

使用 KaTeX 格式写公式。示例：
```
$$F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-j\omega t} dt$$
```

### 第 3 步：苏格拉底式反问

推导完成后，用反问确认理解：
- "如果我把这个条件去掉会怎样？"
- "这个公式在 t→∞ 时会怎么行为？合理吗？"
- "你能用一个你自己的例子来套这个公式吗？"
- "这个推导中哪一步你感觉最'不显然'？"

等学生回答后再评论。如果回答有偏差，用更简单的问题引导。

### 第 4 步：概念检验

出 1-2 道**概念理解题**（不是纯计算题）。比如：
- "不用公式，用日常语言解释为什么时域卷积等于频域乘积"
- "如果一个 LTI 系统的冲击响应是 δ(t-2)，这个系统做了什么？"

学生回答后给予反馈。如果理解有偏差，回到第 2 步重新讲解那个环节。

**只有学生正确回答后，才进入下一节。**

### 第 5 步：项目实战

设计一个小型但完整的项目，让学生把刚学的概念用起来。

项目要求：
- 有明确的输入和输出规格
- 提供完整的项目目录结构
- 提供骨架代码（关键接口写好，实现留空或半空）
- 包含测试用例（输入 → 期望输出）

示例（信号与系统的卷积项目）：
```
项目：mini-convolver/
├── main.py          ← 入口：读取信号文件，调用卷积
├── convolve.py      ← 实现离散卷积（你来写）
├── signals/
│   ├── impulse.csv  ← 测试信号1
│   └── step.csv     ← 测试信号2
└── test.py          ← 自动测试：对比你的输出和 numpy.convolve
```

### 第 6 步：跨域关联

讲解这个概念在其他领域的应用，建立知识网络：
- "傅里叶变换在图像处理中就是 JPEG 压缩的核心"
- "这个线性代数的特征值概念在 Google 的 PageRank 算法中就是..."
- "你之前学的泰勒展开其实也是一种'基函数分解'，和傅里叶变换是亲戚"

---

## 每节结束后的记录

每学完一个主题（概念单元），更新学习数据：

### 更新 progress.json
读取 `learn-sessions/{科目名}/progress.json`，更新：
- `updated_at`
- `current_stage`：当前进度描述
- `deep_topics[]`：新增/更新已学主题条目
- `status`：改为 "in_progress"

### 追加 notes.md
如果学生在该节中产出了自己的理解/推导/笔记，追加到 `notes.md`。

### 同步可视化数据
将 progress.json 复制到 `visualize/data/progress.json`。

---

## 响应风格

- 用"你"不用"您"，亲切但保持专业
- 适当使用 emoji 标记阶段（🧠 摸底、💡 动机、📐 推导、❓ 反问、✅ 检验、🔧 实战、🔗 关联）
- 代码块标注语言类型
- 公式使用 KaTeX 格式（`$$` 块级、`$` 行内）
````

- [ ] **Step 2: 提交**

```bash
git add .claude/skills/learn/deep.md
git commit -m "feat: add deep learning sub-skill with six-step teaching flow"
```

---

### Task 5: 编写考试冲刺子 Skill `sprint.md`

**Files:**
- Create: `D:\占占skill\.claude\skills\learn\sprint.md`

- [ ] **Step 1: 编写 sprint.md**

创建 `D:\占占skill\.claude\skills\learn\sprint.md`：

````markdown
# 考试冲刺模式

你是理工科考试冲刺教练。你的目标只有一个：**让学生在最短时间内拿到最高的考试分数**。

## 核心原则（铁律）

1. **不拓展**。考试不考的内容绝对不讲。学生问你一个超出考试范围的概念，你可以说"这个不在考试范围内，如果你好奇我们考完再聊"。

2. **先骨架后血肉**。先给考点全局地图，让学生看到整个课程的考点分布和权重，再逐个击破。不要一头扎进某个考点让学生失去方向感。

3. **题量堆熟练度**。用大量中低难度题目堆熟练度，而不是用难题堆深度。目标是"看到类似题就本能反应出解法"。

4. **错题不过夜**。每道错题必须当场复盘（分析错因类型），然后立刻给同类型题重做验证。

---

## 五步教学流程

### 第 1 步：划范围 — 考点地图

基于学生提供的材料（课件/教材/考纲）和学科知识，提取完整考点清单。

每个考点标注：
- **权重**：高频 / 中频 / 低频（基于题型分布和历年规律）
- **难度**：简单 / 中等 / 困难
- **常见题型**：选择 / 填空 / 计算 / 证明 / 简答
- **预估用时**：掌握这个考点建议花多长时间

输出格式（示例）：
```
📊 信号与系统 — 考点地图（共 8 个考点）

🔴 高频（占分约 60%）
  □ ss-01 信号分类与基本运算      简单 | 选择+填空    | ~20min
  □ ss-02 卷积积分                中等 | 计算         | ~45min
  □ ss-03 傅里叶变换的性质        困难 | 计算+证明    | ~90min

🟡 中频（占分约 25%）
  □ ss-04 拉普拉斯变换            中等 | 计算         | ~45min
  □ ss-05 采样定理                简单 | 选择+简答    | ~20min

🟢 低频（占分约 15%）
  □ ss-06 系统的稳定性判据        中等 | 选择         | ~15min
  □ ss-07 z变换基础              中等 | 计算         | ~30min
  □ ss-08 系统的物理可实现性      简单 | 简答         | ~10min
```

写入 progress.json 中的 `exam_points` 数组，每个考点初始化 `mastery: 0`。

### 第 2 步：速通 — 精简讲解 + 闪卡

**按考点优先级从高到低**逐个讲解。每个考点的速通包含：

#### 2a. 三句话讲解
用最多三句话讲清楚核心思想。不推导，只给结论和最关键的公式。

示例（傅里叶变换）：
> "① 任何信号都可以分解为一堆不同频率的正弦波之和。② 傅里叶变换就是告诉你每个频率的'含量'有多少。③ 核心公式：$F(\omega)=\int f(t)e^{-j\omega t}dt$，记住：时域越宽，频域越窄，反之亦然。"

#### 2b. 记忆口诀
给一个方便记忆的口诀或类比。可以很"野"，管用就行。

#### 2c. 生成闪卡
每个考点生成 1-3 张闪卡。格式：
```json
{
  "id": "考点ID",
  "topic": "考点名",
  "front": "时域卷积对应频域什么运算？",
  "back": "乘积。$f(t)*g(t) \\leftrightarrow F(\\omega)G(\\omega)$",
  "difficulty": "中等"
}
```

所有闪卡写入 `cards.json`。

### 第 3 步：刷题 — 从易到难三档

按考点逐个出题，每个考点 3 档难度（如果考点只有选择题，每档多出几道）：

- **热身**（2-3 题）：直接套公式的基础题
- **巩固**（2-3 题）：需要一步推理的进阶题
- **挑战**（1 题）：综合应用或需要技巧的题

题目格式：
```
📝 [ss-03] 傅里叶变换 — 热身题 1/3
题目：求 $x(t)=e^{-at}u(t), a>0$ 的傅里叶变换。
（学生作答）
---
✅ 正确答案：$X(\omega)=\frac{1}{a+j\omega}$
💡 要点：直接用定义式积分，注意收敛条件 a>0。
```

学生每做完一题，立即判定正误：
- 正确 → 简短肯定 + 进入下一题
- 错误 → 简单指出错误点 → 进入复盘

**做完一个考点的所有题目后**，评估掌握度（mastery 0-5），更新 progress.json。

### 第 4 步：复盘 — 错题收集与分析

所有错题自动收集，分析错因：

**错因分类**：
- 🔴 概念不清 — 没理解概念本身
- 🟡 计算失误 — 会做但算错了
- 🟠 题型不熟 — 没见过这种问法
- ⚪ 粗心 — 符号搞错、漏条件等

每道错题记录格式（追加到 progress.json 的 weak_points 相关字段）：
```
[ss-03] 傅里叶变换性质
错题：求 $e^{-|t|}$ 的傅里叶变换
你的答案：$1/(1+\omega^2)$
正确答案：$2/(1+\omega^2)$
错因：计算失误——忘了绝对值分段积分有个系数 2
```

### 第 5 步：补刀 — 薄弱考点围剿

针对薄弱考点（mastery < 3 或错题集中的考点），生成同类型新题。

学生做完后再次评估。直到：
- mastery >= 3（及格线），或
- 学生选择"先跳过，进入下一个考点"

**薄弱考点全部处理完毕后**，生成一份「考前检查清单」：
```
📋 考前检查清单
✅ ss-01 信号分类        mastery 5/5 稳
⚠️ ss-02 卷积积分        mastery 3/5 再做5道保底
❌ ss-03 傅里叶变换       mastery 2/5 重点复习
...
```

---

## 每步结束后的记录

### 更新 progress.json
每完成一个考点或阶段，更新：
- `updated_at`
- `current_stage`
- `exam_points[].mastery` / `total_questions` / `correct`
- `weak_points[]`

### 更新 cards.json
第 2 步生成的闪卡写入 `learn-sessions/{科目名}/cards.json`。

### 同步可视化数据
将 progress.json 和 cards.json 同步写入 `visualize/data/`。

---

## 响应风格

- 简洁、有力、有紧迫感（学生在赶考！）
- 用 emoji 标记状态：📊 地图、📝 刷题、❌ 错题、🔄 补刀、✅ 通过
- 公式用 KaTeX
- 适当使用 ASCII 进度条显示考点完成情况
````

- [ ] **Step 2: 提交**

```bash
git add .claude/skills/learn/sprint.md
git commit -m "feat: add exam sprint sub-skill with five-step drill flow"
```

---

### Task 6: 编写可视化页面 `index.html`

**Files:**
- Create: `D:\占占skill\.claude\skills\learn\visualize\index.html`

- [ ] **Step 1: 编写 index.html**

创建 `D:\占占skill\.claude\skills\learn\visualize\index.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Learn — 学习看板</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  :root {
    --bg: #0f172a;
    --surface: #1e293b;
    --border: #334155;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --green: #4ade80;
    --yellow: #fbbf24;
    --red: #f87171;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.6;
  }
  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  header h1 { font-size: 1.5rem; }
  .mode-badge {
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
  }
  .mode-deep { background: #1e3a5f; color: var(--accent); }
  .mode-sprint { background: #3b1f1f; color: var(--red); }
  nav {
    display: flex;
    gap: 4px;
    padding: 12px 24px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
  }
  nav button {
    background: none;
    border: none;
    color: var(--muted);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s;
  }
  nav button:hover { color: var(--text); background: var(--border); }
  nav button.active { color: var(--accent); background: #1e3a5f; }
  main { max-width: 900px; margin: 24px auto; padding: 0 24px; }
  .tab { display: none; }
  .tab.active { display: block; }
  .empty-state {
    text-align: center;
    padding: 80px 20px;
    color: var(--muted);
  }
  .empty-state .icon { font-size: 4rem; margin-bottom: 16px; }
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
  }
  .flashcard-container {
    perspective: 1000px;
    width: 100%;
    max-width: 500px;
    height: 280px;
    margin: 24px auto;
    cursor: pointer;
  }
  .flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s;
    transform-style: preserve-3d;
  }
  .flashcard-inner.flipped { transform: rotateY(180deg); }
  .flashcard-front, .flashcard-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px;
    font-size: 1.2rem;
    text-align: center;
  }
  .flashcard-front {
    background: linear-gradient(135deg, #1e3a5f, #0f172a);
    border: 2px solid var(--accent);
  }
  .flashcard-back {
    background: linear-gradient(135deg, #14532d, #0f172a);
    border: 2px solid var(--green);
    transform: rotateY(180deg);
  }
  .flashcard-nav {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    margin-top: 16px;
  }
  .flashcard-nav button {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 8px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
  }
  .flashcard-nav button:hover { background: var(--border); }
  .progress-bar {
    width: 100%;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    margin: 8px 0 16px;
  }
  .progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s;
  }
  .fill-green { background: var(--green); }
  .fill-yellow { background: var(--yellow); }
  .fill-red { background: var(--red); }
  .point-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
  }
  .mastery-dots { display: flex; gap: 4px; }
  .dot {
    width: 12px; height: 12px; border-radius: 50%;
    background: var(--border);
  }
  .dot.filled { background: var(--green); }
  .dot.filled-yellow { background: var(--yellow); }
  .dot.filled-red { background: var(--red); }
  .error-card {
    background: var(--surface);
    border-left: 4px solid var(--red);
    padding: 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 12px;
  }
  .error-card summary { cursor: pointer; font-weight: 600; margin-bottom: 8px; }
  .tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    margin-right: 4px;
  }
  .tag-concept { background: #7f1d1d; color: #fca5a5; }
  .tag-calc { background: #78350f; color: #fcd34d; }
  .tag-unfamiliar { background: #1e3a5f; color: #93c5fd; }
  .tag-careless { background: #334155; color: #cbd5e1; }
  .chart-wrap { max-width: 400px; margin: 24px auto; }
  #mermaid-diagram { text-align: center; }
  .subject-selector {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.9rem;
  }
</style>
</head>
<body>

<header>
  <div>
    <h1 id="subject-title">📚 学习看板</h1>
    <span style="font-size:0.85rem;color:var(--muted)" id="info-line">等待加载数据...</span>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <span class="mode-badge" id="mode-badge">--</span>
    <span style="font-size:0.8rem;color:var(--muted)" id="update-time"></span>
  </div>
</header>

<nav>
  <button class="active" data-tab="map">🗺 考点地图</button>
  <button data-tab="flashcards">🃏 闪卡</button>
  <button data-tab="progress">📊 进度</button>
  <button data-tab="errors">📋 错题本</button>
</nav>

<main>
  <!-- Tab 1: 考点地图 -->
  <div class="tab active" id="tab-map">
    <div class="card">
      <div id="mermaid-diagram"></div>
      <div class="empty-state" id="map-empty">
        <div class="icon">🗺️</div>
        <p>考点地图将在开始学习后生成</p>
      </div>
    </div>
  </div>

  <!-- Tab 2: 闪卡 -->
  <div class="tab" id="tab-flashcards">
    <div class="empty-state" id="flashcards-empty">
      <div class="icon">🃏</div>
      <p>闪卡将在开始学习后生成</p>
      <p style="font-size:0.85rem;color:var(--muted)">点击正面翻转查看答案</p>
    </div>
    <div id="flashcards-content" style="display:none">
      <div class="flashcard-container" id="flashcard">
        <div class="flashcard-inner" id="flashcard-inner">
          <div class="flashcard-front" id="fc-front"></div>
          <div class="flashcard-back" id="fc-back"></div>
        </div>
      </div>
      <div class="flashcard-nav">
        <button id="fc-prev">◀ 上一张</button>
        <span id="fc-counter" style="color:var(--muted)">1 / 1</span>
        <button id="fc-next">下一张 ▶</button>
      </div>
    </div>
  </div>

  <!-- Tab 3: 进度看板 -->
  <div class="tab" id="tab-progress">
    <div class="empty-state" id="progress-empty">
      <div class="icon">📊</div>
      <p>进度数据将在学习开始后显示</p>
    </div>
    <div id="progress-content" style="display:none">
      <div class="card">
        <h3>总体进度</h3>
        <div class="progress-bar"><div class="progress-fill fill-green" id="overall-bar" style="width:0%"></div></div>
        <p style="color:var(--muted)" id="overall-text">0 / 0 考点掌握</p>
      </div>
      <div class="card">
        <h3>掌握度分布</h3>
        <div class="chart-wrap"><canvas id="mastery-chart"></canvas></div>
      </div>
      <div class="card" id="points-list"></div>
    </div>
  </div>

  <!-- Tab 4: 错题本 -->
  <div class="tab" id="tab-errors">
    <div class="empty-state" id="errors-empty">
      <div class="icon">📋</div>
      <p>暂无错题，继续保持！</p>
    </div>
    <div id="errors-content" style="display:none"></div>
  </div>
</main>

<script>
// --- Data Loading ---
let progressData = null;
let cardsData = null;
let currentCardIndex = 0;
let masteryChart = null;

async function loadData() {
  try {
    const [progResp, cardsResp] = await Promise.all([
      fetch('./data/progress.json'),
      fetch('./data/cards.json')
    ]);
    if (progResp.ok) progressData = await progResp.json();
    if (cardsResp.ok) cardsData = await cardsResp.json();
    if (progressData) renderAll();
  } catch(e) {
    document.getElementById('info-line').textContent = '未找到数据文件，请先通过 /learn 开始学习';
  }
}

function renderAll() {
  const p = progressData;
  document.getElementById('subject-title').textContent = '📚 ' + (p.subject || '学习看板');
  document.getElementById('info-line').textContent =
    (p.mode === 'deep' ? '🧠 深度学习' : '📝 考试冲刺') +
    (p.current_stage ? ' · ' + p.current_stage : '');
  const badge = document.getElementById('mode-badge');
  badge.textContent = p.mode === 'deep' ? '深度学习' : '考试冲刺';
  badge.className = 'mode-badge ' + (p.mode === 'deep' ? 'mode-deep' : 'mode-sprint');
  document.getElementById('update-time').textContent = p.updated_at || '';

  renderMap(p);
  renderFlashcards();
  renderProgress(p);
  renderErrors(p);
}

// --- Tab Switching ---
document.querySelectorAll('nav button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    if (btn.dataset.tab === 'progress' && progressData) renderProgress(progressData);
    if (btn.dataset.tab === 'map' && progressData) renderMap(progressData);
  });
});

// --- Map Tab ---
let mermaidInitialized = false;
async function renderMap(p) {
  const points = p.exam_points || [];
  const deepTopics = p.deep_topics || [];
  if (points.length === 0 && deepTopics.length === 0) {
    document.getElementById('map-empty').style.display = 'block';
    document.getElementById('mermaid-diagram').innerHTML = '';
    return;
  }
  document.getElementById('map-empty').style.display = 'none';

  let mermaidCode = 'graph TD\n';
  mermaidCode += '  Root["' + (p.subject || '课程') + '"]\n';

  if (p.mode === 'sprint') {
    const high = points.filter(pt => pt.weight === '高频');
    const mid = points.filter(pt => pt.weight === '中频');
    const low = points.filter(pt => pt.weight === '低频');
    if (high.length) {
      mermaidCode += '  subgraph High[🔴 高频考点]\n';
      high.forEach(pt => {
        mermaidCode += '  ' + pt.id + '["' + pt.topic + ' ' + masteryIcon(pt.mastery) + '"]\n';
      });
      mermaidCode += '  end\n';
    }
    if (mid.length) {
      mermaidCode += '  subgraph Mid[🟡 中频考点]\n';
      mid.forEach(pt => {
        mermaidCode += '  ' + pt.id + '["' + pt.topic + ' ' + masteryIcon(pt.mastery) + '"]\n';
      });
      mermaidCode += '  end\n';
    }
    if (low.length) {
      mermaidCode += '  subgraph Low[🟢 低频考点]\n';
      low.forEach(pt => {
        mermaidCode += '  ' + pt.id + '["' + pt.topic + ' ' + masteryIcon(pt.mastery) + '"]\n';
      });
      mermaidCode += '  end\n';
    }
    mermaidCode += '  Root';
    if (high.length) mermaidCode += ' --> High';
    if (mid.length) mermaidCode += ' --> Mid';
    if (low.length) mermaidCode += ' --> Low';
  } else {
    deepTopics.forEach(t => {
      mermaidCode += '  ' + t.id + '["' + t.topic + ' ' + masteryIcon(t.mastery) + '"]\n';
      mermaidCode += '  Root --> ' + t.id + '\n';
    });
  }

  document.getElementById('mermaid-diagram').innerHTML = '<pre class="mermaid">' + mermaidCode + '</pre>';
  try {
    await mermaid.run({ querySelector: '.mermaid' });
    mermaidInitialized = true;
  } catch(e) {
    // mermaid render error, show raw code
  }
}

function masteryIcon(m) {
  if (m >= 4) return '✅';
  if (m >= 2) return '⚠️';
  return '❌';
}

// --- Flashcards Tab ---
function renderFlashcards() {
  const cards = cardsData?.cards || [];
  // Also check progressData for inline flashcard data
  const examPoints = progressData?.exam_points || [];
  const inlineCards = examPoints.filter(p => p.flashcard).map(p => ({
    id: p.id, topic: p.topic,
    front: p.flashcard.front, back: p.flashcard.back,
    difficulty: p.difficulty
  }));
  const allCards = cards.length >= inlineCards.length ? cards : inlineCards;

  if (allCards.length === 0) {
    document.getElementById('flashcards-empty').style.display = 'block';
    document.getElementById('flashcards-content').style.display = 'none';
    return;
  }
  document.getElementById('flashcards-empty').style.display = 'none';
  document.getElementById('flashcards-content').style.display = 'block';

  window._allCards = allCards;
  currentCardIndex = 0;
  showCard(0);

  document.getElementById('flashcard').onclick = () => {
    document.getElementById('flashcard-inner').classList.toggle('flipped');
  };
  document.getElementById('fc-prev').onclick = (e) => { e.stopPropagation(); showCard(currentCardIndex - 1); };
  document.getElementById('fc-next').onclick = (e) => { e.stopPropagation(); showCard(currentCardIndex + 1); };
}

function showCard(i) {
  const cards = window._allCards || [];
  if (cards.length === 0) return;
  currentCardIndex = (i + cards.length) % cards.length;
  const card = cards[currentCardIndex];
  document.getElementById('fc-front').innerHTML = '<div>' + card.front + '</div><div style="font-size:0.8rem;color:var(--muted);margin-top:12px">' + (card.topic || '') + '</div>';
  document.getElementById('fc-back').innerHTML = card.back;
  document.getElementById('flashcard-inner').classList.remove('flipped');
  document.getElementById('fc-counter').textContent = (currentCardIndex + 1) + ' / ' + cards.length;
}

// --- Progress Tab ---
function renderProgress(p) {
  const points = p.exam_points || [];
  const deepTopics = p.deep_topics || [];
  const items = points.length > 0 ? points : deepTopics;

  if (items.length === 0) {
    document.getElementById('progress-empty').style.display = 'block';
    document.getElementById('progress-content').style.display = 'none';
    return;
  }
  document.getElementById('progress-empty').style.display = 'none';
  document.getElementById('progress-content').style.display = 'block';

  const mastered = items.filter(it => (it.mastery || 0) >= 3).length;
  const pct = items.length > 0 ? Math.round((mastered / items.length) * 100) : 0;
  document.getElementById('overall-bar').style.width = pct + '%';
  document.getElementById('overall-text').textContent = mastered + ' / ' + items.length + ' 考点掌握 (' + pct + '%)';

  // Mastery chart
  const bins = [0, 0, 0, 0, 0, 0]; // mastery 0-5
  items.forEach(it => bins[Math.min(it.mastery || 0, 5)]++);
  const ctx = document.getElementById('mastery-chart');
  if (masteryChart) masteryChart.destroy();
  masteryChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['0 - 未开始', '1', '2', '3', '4', '5 - 完全掌握'],
      datasets: [{
        data: bins,
        backgroundColor: ['#475569','#f87171','#fbbf24','#fbbf24','#4ade80','#22c55e']
      }]
    },
    options: {
      plugins: { legend: { labels: { color: '#e2e8f0' } } }
    }
  });

  // Point detail list
  const list = document.getElementById('points-list');
  list.innerHTML = '<h3>各考点详情</h3>';
  items.forEach(it => {
    const mastery = it.mastery || 0;
    let dots = '';
    for (let i = 0; i < 5; i++) {
      let cls = 'dot';
      if (i < mastery) {
        cls += mastery >= 4 ? ' filled' : mastery >= 2 ? ' filled-yellow' : ' filled-red';
      }
      dots += '<span class="' + cls + '"></span>';
    }
    const questions = it.total_questions ? ' · 做题' + it.total_questions + ' · 正确' + (it.correct || 0) : '';
    const weight = it.weight ? ' <span style="color:var(--muted);font-size:0.8rem">[' + it.weight + ']</span>' : '';
    list.innerHTML += '<div class="point-row"><div><strong>' + it.topic + '</strong>' + weight + '<br><span style="font-size:0.8rem;color:var(--muted)">' + (it.difficulty || '') + questions + '</span></div><div class="mastery-dots">' + dots + '</div></div>';
  });
}

// --- Errors Tab ---
function renderErrors(p) {
  const weakPoints = p.weak_points || [];
  const points = p.exam_points || [];
  const weakPointDetails = points.filter(pt => weakPoints.includes(pt.id) || (pt.mastery || 0) < 3);

  if (weakPointDetails.length === 0 && weakPoints.length === 0) {
    document.getElementById('errors-empty').style.display = 'block';
    document.getElementById('errors-content').style.display = 'none';
    return;
  }
  document.getElementById('errors-empty').style.display = 'none';
  document.getElementById('errors-content').style.display = 'block';

  let html = '<h3>⚠️ 薄弱考点 / 错题</h3>';
  weakPointDetails.forEach(pt => {
    const correctPct = pt.total_questions > 0 ? Math.round((pt.correct / pt.total_questions) * 100) : 0;
    html += '<details class="error-card"><summary><strong>' + pt.topic + '</strong> — 掌握度 ' + pt.mastery + '/5 · 正确率 ' + correctPct + '%</summary>';
    html += '<p style="margin-top:8px;color:var(--muted)">权重: ' + (pt.weight || '未知') + ' | 难度: ' + (pt.difficulty || '未知') + '</p>';
    html += '<p style="margin-top:4px;color:var(--muted)">做题 ' + (pt.total_questions || 0) + ' 道，正确 ' + (pt.correct || 0) + ' 道</p>';
    html += '<p style="margin-top:8px">💡 建议：针对此考点做更多同类题目加强练习</p>';
    html += '</details>';
  });
  document.getElementById('errors-content').innerHTML = html;
}

// --- Init ---
loadData();
</script>
</body>
</html>
```

- [ ] **Step 2: 验证 HTML 页面可打开**

```bash
# 创建测试数据以便验证
mkdir -p "D:\占占skill\.claude\skills\learn\visualize\data"
```

创建 `D:\占占skill\.claude\skills\learn\visualize\data\progress.json` 作为测试数据：

```json
{
  "subject": "信号与系统",
  "mode": "sprint",
  "created_at": "2026-06-05",
  "updated_at": "2026-06-05T14:30:00",
  "status": "in_progress",
  "current_stage": "刷题_傅里叶变换",
  "exam_points": [
    {
      "id": "ss-01",
      "topic": "信号分类与基本运算",
      "weight": "高频",
      "difficulty": "简单",
      "question_types": ["选择", "填空"],
      "flashcard": {
        "front": "什么是能量信号？",
        "back": "能量有限的信号，即 $\\int_{-\\infty}^{\\infty} |x(t)|^2 dt < \\infty$"
      },
      "mastery": 5,
      "total_questions": 8,
      "correct": 8
    },
    {
      "id": "ss-02",
      "topic": "卷积积分",
      "weight": "高频",
      "difficulty": "中等",
      "question_types": ["计算"],
      "flashcard": {
        "front": "卷积的交换律是什么？",
        "back": "$f(t)*g(t) = g(t)*f(t)$"
      },
      "mastery": 3,
      "total_questions": 12,
      "correct": 7
    },
    {
      "id": "ss-03",
      "topic": "傅里叶变换的性质",
      "weight": "高频",
      "difficulty": "困难",
      "question_types": ["计算", "证明"],
      "flashcard": {
        "front": "时域卷积对应频域什么？",
        "back": "乘积。$f(t)*g(t) \\leftrightarrow F(\\omega)G(\\omega)$"
      },
      "mastery": 1,
      "total_questions": 5,
      "correct": 1
    }
  ],
  "weak_points": ["ss-03"],
  "material_summary": "已解析：课件.pdf（第1-6章）"
}
```

创建 `D:\占占skill\.claude\skills\learn\visualize\data\cards.json`：

```json
{
  "subject": "信号与系统",
  "updated_at": "2026-06-05T14:30:00",
  "cards": [
    {
      "id": "ss-01",
      "topic": "信号分类",
      "front": "什么是能量信号？",
      "back": "能量有限的信号，即 $\\int_{-\\infty}^{\\infty} |x(t)|^2 dt < \\infty$",
      "difficulty": "简单",
      "last_reviewed": null,
      "correct_count": 0,
      "wrong_count": 0
    },
    {
      "id": "ss-02",
      "topic": "卷积积分",
      "front": "卷积的交换律是什么？",
      "back": "$f(t)*g(t) = g(t)*f(t)$",
      "difficulty": "中等",
      "last_reviewed": null,
      "correct_count": 0,
      "wrong_count": 0
    },
    {
      "id": "ss-03",
      "topic": "傅里叶变换的性质",
      "front": "时域卷积对应频域什么？",
      "back": "乘积。$f(t)*g(t) \\leftrightarrow F(\\omega)G(\\omega)$",
      "difficulty": "困难",
      "last_reviewed": null,
      "correct_count": 0,
      "wrong_count": 0
    }
  ]
}
```

用浏览器打开 `D:\占占skill\.claude\skills\learn\visualize\index.html`，确认四个 Tab 都能正常渲染。

- [ ] **Step 3: 提交**

```bash
git add .claude/skills/learn/visualize/
git commit -m "feat: add visualization page with 4 tabs (map, flashcards, progress, errors)"
```

---

### Task 7: 集成测试与收尾

**Files:**
- Create: `D:\占占skill\learn-sessions\信号与系统\progress.json` (示例数据，同 Task 6 测试数据)

- [ ] **Step 1: 创建 learn-sessions 示例数据**

创建 `D:\占占skill\learn-sessions\信号与系统\progress.json`（内容同 Task 6 的测试 progress.json）。

创建 `D:\占占skill\learn-sessions\信号与系统\cards.json`（内容同 Task 6 的测试 cards.json）。

更新 `D:\占占skill\learn-sessions\_index.json`：

```json
[
  {
    "subject": "信号与系统",
    "mode": "sprint",
    "status": "in_progress",
    "updated": "2026-06-05T14:30:00"
  }
]
```

- [ ] **Step 2: 验证完整数据流**

确认以下路径都正确：
1. `learn-sessions/_index.json` 可读 ✅
2. `learn-sessions/信号与系统/progress.json` 格式符合 shared.md 定义 ✅
3. `visualize/data/progress.json` 与上一步内容一致 ✅
4. `visualize/index.html` 用浏览器打开四个 Tab 正常 ✅

- [ ] **Step 3: 提交**

```bash
git add learn-sessions/ .claude/skills/learn/visualize/data/
git commit -m "feat: add sample session data and complete integration wiring"
```

---

## 实现顺序说明

```
Task 1 (目录) → Task 2 (shared.md)
                ↓
           Task 3 (skill.md 入口)
                ↓
    ┌───────────┴───────────┐
    ↓                       ↓
Task 4 (deep.md)    Task 5 (sprint.md)
    │                       │
    └───────────┬───────────┘
                ↓
          Task 6 (index.html)
                ↓
          Task 7 (集成收尾)
```

- Task 2 必须先做，因为后续所有 skill 文件都引用 shared.md 中的规范
- Task 4 和 Task 5 可以并行（两个子 skill 完全独立）
- Task 6 可以与其他 task 并行（前端独立于 skill prompt）
