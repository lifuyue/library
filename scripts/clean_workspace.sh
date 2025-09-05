#!/usr/bin/env bash
# 清理本地构建/缓存/临时产物，不删除虚拟环境（如需删除手动传 --with-venv）
# 使用方法:
#   bash scripts/clean_workspace.sh            # 普通清理
#   bash scripts/clean_workspace.sh --with-venv # 额外删除 .venv / backend/.venv
set -euo pipefail

WITH_VENV=0
if [[ "${1:-}" == "--with-venv" ]]; then
  WITH_VENV=1
fi

echo '==> 清理前统计:'
count() { eval "$1" | wc -l | xargs -I{} printf "%-22s %s\n" "$2" "{}"; }
count "find . -type d -name node_modules" "node_modules dirs" || true
count "find . -type d -name dist"          "dist dirs" || true
count "find . -type d -name build"         "build dirs" || true
count "find . -type d -name .vite"         ".vite dirs" || true
count "find . -type d -name coverage"      "coverage dirs" || true
count "find . -type d -name __pycache__"   "__pycache__ dirs" || true
count "find . -type f -name '*.py[co]'"    "py[co] files" || true
count "find . -type f -name '*.tsbuildinfo*'" "tsbuildinfo" || true
count "find . -type f -name '.eslintcache'"  ".eslintcache" || true
count "find . -type f -name '*.db'" "db files" || true

# 目录类
find . -type d -name node_modules -prune -exec rm -rf {} +
find . -type d -name dist        -prune -exec rm -rf {} +
find . -type d -name build       -prune -exec rm -rf {} +
find . -type d -name .vite       -prune -exec rm -rf {} +
find . -type d -name coverage    -prune -exec rm -rf {} +
# Python 缓存
find . -type d -name __pycache__ -prune -exec rm -rf {} +
find . -type f -name '*.py[co]' -delete || true
# TS/ESLint 缓存
find . -type f -name '*.tsbuildinfo*' -delete || true
find . -type f -name '.eslintcache' -delete || true
# 数据库快照/本地数据库文件（通用 *.db）
find . -type f -name '*.db' -delete || true
# PowerShell 脚本（若被错误提交到根目录）
find . -maxdepth 3 -type f -name '*.ps1' -not -path './.git/*' -delete || true

if [[ $WITH_VENV -eq 1 ]]; then
  echo '==> 删除虚拟环境 .venv backend/.venv'
  rm -rf .venv backend/.venv || true
fi

echo '==> 清理后统计:'
count "find . -type d -name node_modules" "node_modules dirs" || true
count "find . -type d -name dist"          "dist dirs" || true
count "find . -type d -name build"         "build dirs" || true
count "find . -type d -name .vite"         ".vite dirs" || true
count "find . -type d -name coverage"      "coverage dirs" || true
count "find . -type d -name __pycache__"   "__pycache__ dirs" || true
count "find . -type f -name '*.py[co]'"    "py[co] files" || true
count "find . -type f -name '*.tsbuildinfo*'" "tsbuildinfo" || true
count "find . -type f -name '.eslintcache'"  ".eslintcache" || true
count "find . -type f -name '*.db'" "db files" || true

echo '完成。'
