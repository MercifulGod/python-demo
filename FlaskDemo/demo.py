import time
import threading

import fasteners

from FlaskDemo.settings import PROCESS_FILE_LOCK

with PROCESS_FILE_LOCK:
    print('I have the lock')
    time.sleep(5)
# def test():

# gotten = lock.acquire(blocking=False)
# try:
#     if gotten:
#         print('I have the lock')
#         time.sleep(5)
#     else:
#         print('I do not have the lock')
#         time.sleep(5)
# finally:
#     pass


# threads = []
# for i in range(0, 10):
#     threads.append(threading.Thread(target=test))
#
# try:
#     for t in threads:
#         t.start()
# finally:
#     while threads:
#         t = threads.pop()
#         t.join()
print('I do not have the lock')
