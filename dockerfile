FROM python:3.6.4

# 工作目录
WORKDIR /app
COPY . /app

# 安装依赖
RUN pip3 install -r requirement.txt

# 运行
CMD ["python3", "main.py"]