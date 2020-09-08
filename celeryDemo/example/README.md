# Celery Demo


安装celery
```commandline
# 安装celery
sudo pip3 install celery  


# 启动celery worker
cd celeryDemo/example
celery -A tasks worker --loglevel=info

```

### 使用supervisor守护celery进程

装supervisor
```commandline
sudo apt-get install supervisor
```
生成celery配置文件
```commandline
sudo sh gen_supervisor.sh 
```
启动supervisor服务
```commandline
sudo service supervisor start
```
查看supervisor是否启动
```commandline
ps aux | grep supervisor
```
查看celery是否启动成功
```commandline
tail -200f /var/log/demo/celery.std
```


