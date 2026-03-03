# 初始化 Git 仓库并关联远程仓库
git init

# 添加所有文件到暂存区
git add .

# 创建初始提交
git commit -m "Initial commit: Add Claude Code Router Chinese documentation"

# 关联远程仓库
git remote add origin git@github.com:wuyif97/mydocs.git

# 推送到远程仓库（使用 -u 设置上游分支）
git push -u origin main
