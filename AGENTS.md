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
- 输出代码需包含 import / setup，可直接运行。
- 修改现有文件时，标明文件路径并给出替换后的完整内容。
- 新增文件时，提供文件名与完整内容。
- 修改后运行相关检查：后端 `make check-backend`；前端 `cd frontend && npm run build` 或 `make build-frontend`。

## 交互规范
- 回复保持简洁；中英文混合时保留技术关键词（API、Docker、JWT 等）。
- 运维/部署问题优先给出可执行的 bash 命令。

## 持续改进
- 安全提醒：`.env` 中存在默认 `SECRET_KEY`，且系统缺少速率限制。
- 可根据后续反馈持续扩展本文件。

