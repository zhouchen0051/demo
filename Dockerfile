# ============================================
# Dockerfile - 容器化部署
# ============================================

# 基础镜像：Python 3.12  slim 版本（轻量）
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（可选）
# RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*

# 复制依赖文件，先安装依赖（利用 Docker 层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com



# 复制项目代码
COPY . .

# 暴露端口（Gradio 默认 7860）
EXPOSE 7860

# 启动命令
CMD ["python", "app.py"]
