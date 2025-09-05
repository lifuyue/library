#!/bin/bash
set -e

# CS素材库数据库管理脚本

# 检查 Docker Compose 命令
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose 未安装"
    exit 1
fi

CONTAINER_NAME="postgresql"
DB_USER="csuser"
DB_NAME="cslibrary"

# 检查容器是否运行
check_container() {
    if ! docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo "❌ 数据库容器 ${CONTAINER_NAME} 未运行"
        echo "请先启动服务: $COMPOSE_CMD up -d"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "CS素材库数据库管理脚本"
    echo ""
    echo "用法: ./db-manage.sh <command>"
    echo ""
    echo "命令:"
    echo "  status      显示数据库状态"
    echo "  connect     连接到数据库"
    echo "  backup      备份数据库"
    echo "  restore     恢复数据库 (需要指定备份文件)"
    echo "  reset       重置数据库 (危险操作)"
    echo "  migrate     执行数据库迁移"
    echo "  logs        查看数据库日志"
    echo ""
    echo "示例:"
    echo "  ./db-manage.sh backup"
    echo "  ./db-manage.sh restore backup_20250830_120000.sql"
    echo "  ./db-manage.sh connect"
}

# 显示数据库状态
show_status() {
    check_container
    echo "📊 数据库状态:"
    echo ""
    docker exec $CONTAINER_NAME pg_isready -U $DB_USER
    echo ""
    echo "📈 数据库信息:"
    docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "
        SELECT 
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
        FROM pg_tables 
        WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
    "
}

# 连接数据库
connect_db() {
    check_container
    echo "🔌 连接到数据库..."
    echo "提示: 使用 \\q 退出"
    docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME
}

# 备份数据库
backup_db() {
    check_container
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    echo "💾 备份数据库到: $backup_file"
    docker exec $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > $backup_file
    echo "✅ 备份完成: $backup_file"
    echo "📦 备份文件大小: $(du -h $backup_file | cut -f1)"
}

# 恢复数据库
restore_db() {
    local backup_file=$1
    if [ -z "$backup_file" ]; then
        echo "❌ 请指定备份文件"
        echo "用法: ./db-manage.sh restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        echo "❌ 备份文件不存在: $backup_file"
        exit 1
    fi
    
    check_container
    
    echo "⚠️  警告: 这将覆盖当前数据库内容!"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 恢复取消"
        exit 1
    fi
    
    echo "🔄 恢复数据库从: $backup_file"
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME < $backup_file
    echo "✅ 恢复完成"
}

# 重置数据库
reset_db() {
    check_container
    
    echo "⚠️  危险操作: 这将删除所有数据!"
    echo "建议先备份数据库: ./db-manage.sh backup"
    echo ""
    read -p "是否继续重置? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 重置取消"
        exit 1
    fi
    
    echo "🗑️  重置数据库..."
    
    # 删除所有表
    docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO $DB_USER;
        GRANT ALL ON SCHEMA public TO public;
    "
    
    # 重新运行迁移
    migrate_db
    
    echo "✅ 数据库重置完成"
}

# 执行迁移
migrate_db() {
    echo "🔧 执行数据库迁移..."
    $COMPOSE_CMD exec cslibrary-backend alembic upgrade head
    echo "✅ 迁移完成"
}

# 查看日志
show_logs() {
    echo "📋 数据库日志:"
    $COMPOSE_CMD logs postgresql --tail=50 -f
}

# 主程序
case "$1" in
    "status")
        show_status
        ;;
    "connect")
        connect_db
        ;;
    "backup")
        backup_db
        ;;
    "restore")
        restore_db "$2"
        ;;
    "reset")
        reset_db
        ;;
    "migrate")
        migrate_db
        ;;
    "logs")
        show_logs
        ;;
    "")
        show_help
        ;;
    *)
        echo "❌ 未知命令: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
