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
配置工作目录
 ```shell script
hdfs dfs -mkdir -p /usr/ztf/input
hdfs dfs -rmdir /usr/ztf/output
 ```
打包程序，重命名为wc.jar, 执行mapreduce任务
```shell script
hadoop jar wc.jar org.example.WordCountDriver /usr/ztf/input /usr/ztf/output
```

查看执行结果
```shell script
hdfs dfs -get /usr/ztf/output/part-r-00000
cat part-r-00000 
```

