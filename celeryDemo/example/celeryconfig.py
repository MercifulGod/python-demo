

broker_url = 'redis://:123456@localhost:6379/0'

# 保存结果
result_backend = 'redis://:123456@localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True

# 这是将错误行为的任务路由到专用队列的方式：
task_routes = {
    'tasks.add': 'low-priority',
}

# 对任务进行速率限制, 在一分钟（10 / m）内只能处理10个此类任务：
task_annotations = {
    'tasks.add': {'rate_limit': '10/m'}
}
