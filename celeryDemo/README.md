# Celery Demo



如果您使用RabbitMQ或Redis作为代理，则可以在运行时为任务设置新的速率限制：
```commandline
$ celery -A tasks control rate_limit tasks.add 10/m
worker@example.com: OK
    new rate limit set successfully
```