## 自托管 Runner 部署指南（CD via GH Actions）

本文档描述如何在自托管 Runner 上，通过新工作流 `.github/workflows/cd.yml` 实现端到端的构建、推送 GHCR、部署、迁移与健康检查，并支持按 tag 回滚。

### 前置条件（自托管 Runner）

- 操作系统：Linux（推荐）且已安装 Docker 与 Docker Compose v2。
- 运行用户：用于运行 runner 的系统用户需要加入 `docker` 组：
  - `sudo usermod -aG docker <runner_user>`，重新登录后 `groups` 应包含 `docker`。
  - 验证：`docker ps`、`docker run --rm hello-world` 可正常运行。
- Runner 常驻：建议以 systemd 服务方式安装 self-hosted runner，确保机器重启后自动恢复。
- 网络：Runner 能访问 `ghcr.io` 拉取镜像；若网络不稳，可在仓库 Secrets 配置 `GHCR_USERNAME/GHCR_TOKEN`，工作流将优先使用它们登录 GHCR。

### 目录与环境

- 部署目录：仓库中的 `deploy/docker/`。
- 需要的文件：
  - `deploy/docker/docker-compose.yml`
  - `deploy/docker/.env`（你需要从 `.env.example` 复制并按需修改）

`.env.example` 样例：

```
IMAGE_TAG=latest
FRONTEND_IMAGE=ghcr.io/<owner>/cslibrary-frontend:${IMAGE_TAG}
BACKEND_IMAGE=ghcr.io/<owner>/cslibrary-backend:${IMAGE_TAG}
POSTGRES_IMAGE=ghcr.io/<owner>/cslibrary-postgres:${IMAGE_TAG}
POSTGRES_DB=cslibrary
POSTGRES_USER=csuser
POSTGRES_PASSWORD=change_me
```

复制到 Runner 上：

```
cp deploy/docker/.env.example deploy/docker/.env
# 如需固定镜像所有者，可将 <owner> 替换为你的 GitHub org/owner（小写）。
```

注意：工作流会在运行时通过环境变量覆盖 `.env` 中的 `IMAGE_TAG`，以支持临时回滚；你仍可把 `.env` 中的镜像前缀（ghcr.io/<owner>/cslibrary-*）常驻。

### 触发方式

- Push 到 `main`：构建三镜像并推送，部署 `latest`。
- Release Published：以发布 tag 构建并部署该 tag。
- 手动 `workflow_dispatch`：可输入 `version` 覆盖部署 tag，用于回滚或灰度。

### 首次上线步骤

1. 确认 Runner：
   - `whoami && groups`
   - `docker info` 正常；`docker compose version` 存在。
2. 准备 `.env`：
   - `cp deploy/docker/.env.example deploy/docker/.env`
   - 若需指定 GHCR owner，替换 `<owner>` 为你的组织/用户名（小写）。
3. 触发工作流：
   - Push 到 `main`（默认 `IMAGE_TAG=latest`），或
   - 手动运行 `cd` 工作流并设置 `version`，或
   - 发布 Release（取 `tag_name`）。
4. 验证健康检查：工作流会依次等待 Postgres、执行 Alembic 迁移、检查 Backend `/healthz`、Frontend `/` 与 `/api/healthz`，均通过后成功。

### 回滚

使用 `workflow_dispatch` 触发并设置：

- `version=v1.1.0`

流程将：

- 跳过 tag 推断，直接使用 `v1.1.0` 作为 `IMAGE_TAG`；
- `docker compose pull && up -d` 拉起对应 tag 的镜像；
- 再次执行 Alembic 迁移与健康检查。

注意：如果 `deploy/docker/.env` 存在且未设置 `IMAGE_TAG`，本工作流同样会以 `version` 为准覆盖运行时的 `IMAGE_TAG`。

### 健康检查细节

- Postgres：容器内 `pg_isready` 轮询 60s，不 ready 则打印日志并失败。
- Backend：容器内 `curl -fsS http://127.0.0.1:8000/healthz`，每 2s 轮询，总 60s。
- Frontend：分两阶段，容器内 `wget --spider` 探活 `/` 与 `index.html`，再探活 `/api/healthz`，总 120s。失败时输出 `nginx -T` 片段与 `error.log` 尾部。

### 故障排查（常见问题）

- GHCR 登录失败：
  - 为仓库添加 Secrets：`GHCR_USERNAME`、`GHCR_TOKEN`（含 `write:packages`）。工作流会优先使用它们。
  - 也可使用默认 `GITHUB_TOKEN` 登录 GHCR。
- 迁移失败（alembic）：
  - 查看 `docker compose logs backend`；
  - 确认 `DATABASE_URL` 指向 `postgresql` 网络别名，且账号、库名与 `.env` 一致。
- Frontend 探活失败：
  - 查看 `docker compose logs frontend`；
  - 输出的 `nginx -T` 与静态目录 `/usr/share/nginx/html/` 是否包含 `index.html`；
  - `/api/healthz` 失败时同时排查 Backend。
- Backend 探活失败：
  - `docker compose logs backend`；
  - 进程与端口：`ps -ef | grep -E 'gunicorn|uvicorn'`、`ss -ltnp` 或 `netstat -tlnp`。
- 镜像拉取问题：
  - 网络抖动会自动轻量重试；仍失败请检查 Runner 到 `ghcr.io` 的连通性与配额。
- 磁盘空间不足：
  - 清理镜像/卷：`docker system prune -af`、`docker volume prune`（谨慎操作）。

### 可配置项

- 覆写部署目录：在工作流中通过 `env.DEPLOY_DIR` 设置（默认 `deploy/docker`）。
- 镜像命名：固定为 `ghcr.io/<owner>/cslibrary-frontend|backend|postgres:<tag>`。
- `tag` 解析：
  - `workflow_dispatch.inputs.version` 存在则使用；
  - 其次使用 `release.tag_name`；
  - `push main` 使用 `latest`。

### 约束与建议

- 前端镜像防呆校验：禁止 `npm run dev`/`vite` 作为启动命令，`CMD ["nginx","-g","daemon off;"]` 为必须。工作流在构建前会校验 `frontend/Dockerfile.prod`。
- 不再产出 `.tar` 工件；历史 `build-tar` 工作流已被废弃并禁用自动触发。

## Release 驱动部署

### 发布步骤

- 在 GitHub → Releases → Draft a new release。
- 选择 Tag：`vX.Y.Z`（从 `main` 分支创建）。
- 勾选 Pre-release：仅构建镜像并推送 GHCR，不部署到生产。
- 发布正式 Release（非 Pre-release）：构建镜像并部署到生产环境（若仓库启用 Environments 审批，将在 `production` 环境审批通过后继续部署）。

### 手动部署/回滚

- 打开 GitHub → Actions → 选择 `CD: Build, Push to GHCR and Deploy` 工作流。
- 点击 Run workflow，并填写 `version` 为要部署的镜像 tag（如 `v1.1.0`）。
- 该方式用于热修或回滚：会拉取对应 tag 的镜像，执行迁移并完成健康检查。

### 版本策略

- 生产仅使用不可变的版本 tag（如 `vX.Y.Z`）进行部署。
- 禁止使用 `latest` 作为生产切换手段，以避免不确定性部署。
