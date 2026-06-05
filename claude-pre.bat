@echo off
chcp 65001
title 正版 Claude-Pre
echo ====================================
echo      正版 Claude Code 独立运行
echo ====================================
echo.

set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
set ANTHROPIC_API_KEY=sk-dc92ae512daf42b1bb2633133710deb6
set CLAUDE_AUTO_APPROVE=true

:: 🔥 全局跳过权限确认 + 正版启动
npx -y @anthropic-ai/claude-code --dangerously-load-development-channels server:wechat --dangerously-skip-permissions %*

pause