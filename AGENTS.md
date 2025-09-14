# Agents Guidelines

## 项目上下文
- 架构：FastAPI + SQLAlchemy 后端，Vue3 + Vite 前端，PostgreSQL 数据库，Docker Compose 编排。
- 使用场景：CS 素材库 / 学术资料管理。

## 角色定位
- 你是智能助手，负责代码生成、调试、文档撰写和架构改进。
- 输出以「清晰、直接、可运行」为优先。

## 代码生成原则
- 默认语言：Python（FastAPI 风格）与 TypeScript（Vue3 风格）。
- 后端：保持与现有 SQLAlchemy ORM、Alembic 迁移、JWT 认证兼容。
- 前端：遵循 Vue3 + Vite 项目结构，避免破坏路由与构建配置。
- Docker：镜像命名 `lifuyue/cslibrary-<service>:<version>`。

## 效率优化规则
- 遇到不确定需求，先提澄清性问题。
- 输出代码需包含 import / setup，可直接运行，并给出最少必要的运行指令。
- **修改现有文件**：默认仅提供「最小可读变更」，优先使用 unified diff（或补丁块：包含必要上下文 + 新旧片段）。仅当变更范围极大或对比入口无法正确渲染时，才提供完整文件内容。
- **新增文件**：提供「路径 + 文件名 + 用途简述 + 关键片段」。当文件 < 80 行或用户明确要求时，再附上完整内容。
- 每次变更均附带**变更摘要**（影响范围、兼容性/回滚提示），并明确可在专用对比入口查看完整 diff。
- 修改后运行相关检查：后端 `make check-backend`；前端 `cd web && npm run build` 或 `make build-frontend`。

## 交互规范
- 回复保持简洁；中英文混合时保留技术关键词（API、Docker、JWT 等）。
- 运维/部署问题优先给出可执行的 bash 命令。

## 持续改进
- 安全提醒：`.env` 中存在默认 `SECRET_KEY`，且系统缺少速率限制。
- 可根据后续反馈持续扩展本文件。

