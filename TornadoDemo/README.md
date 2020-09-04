## server 服务器Bug汇总  
1. 设备断电没有下线操作
2. 设备不会重连服务器：
    > 设备正常与服务器通信，网络故障（拔掉网线），  
    > 重启服务器，恢复网络（连上网线），设备不会重连服务器
3. 坐标：  
4. ERROR:asyncio:Exception in callback BaseSelectorEventLoop._sock_connect_cb(<Future finished result=None>, <socket.socke...0.0.1', 3306)>, ('127.0.0.1', 3306))
handle: <Handle BaseSelectorEventLoop._sock_connect_cb(<Future finished result=None>, <socket.socke...0.0.1', 3306)>, ('127.0.0.1', 3306))>
Traceback (most recent call last):
  File "/usr/lib/python3.6/asyncio/events.py", line 145, in _run
    self._callback(*self._args)
  File "/usr/lib/python3.6/asyncio/selector_events.py", line 476, in _sock_connect_cb
    fut.set_result(None)
asyncio.base_futures.InvalidStateError: invalid state
  > 该异常为：当服务器正在数据库时，关闭服务器，再次重启时会出现


* [E 190925 20:38:13 base_events:1148] Fatal read error on socket transport
    protocol: <asyncio.streams.StreamReaderProtocol object at 0x7f3b5fe8ceb8>
    transport: <_SelectorSocketTransport fd=14 read=polling write=<idle, bufsize=0>>
    Traceback (most recent call last):
      File "/usr/lib/python3.5/asyncio/selector_events.py", line 662, in _read_ready
        data = self._sock.recv(self.max_size)
    TimeoutError: [Errno 110] Connection timed out
    
## 未完成任务
1. 集控器故障上报，集控器校时、三段时间定时异步通知
2. WIFI


## 集控器
> 集控器的控制通过电信平台
>

## AP
1. 多倍通高级调试工具,设备登录账号 admin/dbcom2017

## 服务器参数
* IP：http://27.128.181.220:9998  
    ** 用户名：zd  
    ** 密码：zhida20190923!!@@##%%
* 充电桩：8777
* 主控板：8778




## 经纬度测试
http://www.gpsspg.com/maps.htm

测试地点：石家庄西二环北路66号  
燕肖上传的数据：lat": "38.02"   "lng": "114.25",  


谷歌地图：38.0478007636,114.4355240179  
百度地图：38.0535759505,114.4421034390  
腾讯高德：38.0477900000,114.4355100000  
图吧地图：38.0501543500,114.4392969200  
谷歌地球：38.0469643500,114.4292369200  
北纬N38°02′49.07″ 东经E114°25′45.25″  


## 在线进制转换
http://lostphp.com/hexconvert/

## 智达主控板上传参数解码
aa0001003180100123011101030137080100005c4801000000000100000000010000000001000000000100000000010000010000000c01f4ff

aa 帧头   
0001 0031 8010  ID 长度  命令字
01 23 温度  
01 11 湿度  
01 03 PM2.5  
01 3708 噪声  
01 00005c48 电流  
01 00000000 电压  
01 00000000 经度   
01 00000000 维度    
01 00000000 有功功率  
01 00000000 视在功率  
01 0000     功率因数  
01 0000000c 累计电能  
01 f4 校验码   
ff 帧尾   