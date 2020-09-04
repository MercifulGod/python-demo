### 知识点：

- 在一个 .proto 文件内定义服务。
- 用 protocol buffer 编译器生成服务器和客户端代码。
- 使用 gRPC 的 Python API 为你的服务实现一个简单的客户端和服务器。


### helloworld.proto 文件讲解
消息定义
```text
message HelloRequest {
  string name = 1;
}

```
```text
关键字 消息名称 {
  字段类型 字段名称 = 字段编号;
}
```
- message: Protocol Buffers 关键字, 代表一个消息  
- 字段编号： 用来序列化消息, 1-15 为一个字节,常用于使用频繁的字段



####生成客户端和服务器端代码
方式一
```commandline
 python3 -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/helloworld.proto
```
+ -I ： 依赖.proto文件搜索路径

方式二
```commandline
python3 run_codegen.py 
```


查看帮助文档
```commandline
python3 -m grpc_tools.protoc   --help
```




