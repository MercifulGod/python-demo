 启动HDFS
```shell script
hadoop-daemon.sh start namenode
hadoop-daemon.sh start datanode
```
启动Yarn
 ```shell script
yarn-daemon.sh  start resourcemanager
yarn-daemon.sh  start nodemanager
 ```
启动HBase
 ```shell script
./bin/hbase-daemon.sh start master
./bin/hbase-daemon.sh start regionserver
 ```
shell客户端
 ```shell script
./bin/hbase shell
 ```
获取所有表
 ```shell script
hbase(main):001:0> list
TABLE                                                                                                                                         
student                                                                                                                                       
weibo:content                                                                                                                                 
weibo:receive_content_email                                                                                                                   
weibo:relations                                                                                                                               
4 row(s) in 0.6050 seconds
 ```
查看表内容
 ```shell script
hbase(main):003:0> scan "weibo:relations"
ROW                                  COLUMN+CELL                                                                                              
 0001                                column=attends:0008, timestamp=1602134659273, value=0008                                                 
 0001                                column=attends:0009, timestamp=1602135209099, value=0009                                                 
 0008                                column=fans:0001, timestamp=1602135209099, value=0001                                                    
 0009                                column=fans:0001, timestamp=1602135209099, value=0001                                                    
3 row(s) in 0.2940 seconds
 ```
删除表
 ```shell script
disable "weibo:content"
disable "weibo:receive_content_email"
disable "weibo:relations"

drop "weibo:relations"
drop "weibo:receive_content_email"
drop "weibo:content"
 ```




