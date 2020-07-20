# python实现的日志分割工具

### docker中
``` yml
version: "3"

services:
  #nginx容器
  nginx:
    image: nginx:1.18
    restart: unless-stopped
    ports:
      - 9999:80
    volumes:
      # nginx日志映射到宿主机
      - ./logs/:/var/log/nginx/
  #日志收集agent
  py-logrotate:
    image: py-logrotate:fri
    container_name: py-logrotate
    build:
      context: .
      dockerfile: ./Dockerfile
    command:
      #指定多个日志目录
      - --path=/logs/
      - --path=/logs-1/
      - --path=/logs-2/
      #指定文件size阈值
      - --max_size=10240
    restart: unless-stopped
    volumes:
      # 映射宿主机日志目录
      - ./logs/:/logs/
```
### k8s中
logrotate和app跑在同一个pod中，共享volume实现日志分割