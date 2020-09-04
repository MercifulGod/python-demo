### 目标：  
随突出了知识点,减少细枝末节的影响

注：想要进一步了解的,可看官方文档

#### 安装gRPC

``` commandline
sudo pip3 install grpcio
sudo pip3 install grpcio-tools
sudo pip3 install grpcio-channelz
sudo apt install protobuf-compiler  # protocol buffer编译器
```


#### 生成客户端和服务器端代码
``` commandline
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/addressbook.proto
```



### 参考文档
[protocol-buffers开发文档][protocol-buffers]  
[grpc官方文档][grpc]  
[grpc中文文档][grpc-cn]   
[页间跳转][b]   




[protocol-buffers]: https://developers.google.com/protocol-buffers/docs/overview  
[grpc]: https://grpc.io/docs/languages/python/quickstart/  
[grpc-cn]: http://doc.oschina.net/grpc  
[b]: ./examples/README.md
