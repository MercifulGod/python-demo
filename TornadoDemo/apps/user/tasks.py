import asyncio


async def user_task(name):
    print("定时执行任务：%s" % name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(user_task("张三"))
