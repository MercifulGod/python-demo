## Compression with gRPC Python

gRPC提供了无损压缩选项，以减少通过网络传输的位数。 提供三种压缩级别：

 - `grpc.Compression.NoCompression` - 没有压缩应用于有效负载. (default)
 - `grpc.Compression.Deflate` - Deflate”算法应用于有效负载.
 - `grpc.Compression.Gzip` -  Gzip”算法应用于有效负载.

客户端和服务端上的默认选项是：`grpc.Compression.NoCompression`.

See [the gRPC Compression Spec](https://github.com/grpc/grpc/blob/master/doc/compression.md)
for more information.

### 客户端压缩

此外，可以在客户端端两个级别设置压缩。

#### channel级别

```python
with grpc.insecure_channel('foo.bar:1234', compression=grpc.Compression.Gzip) as channel:
    use_channel(channel)
```

#### Call 级别

在call级别设置压缩方法将覆盖channel级别的所有设置。


```python
stub = helloworld_pb2_grpc.GreeterStub(channel)
response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'),
                         compression=grpc.Compression.Deflate)
```


### 服务端压缩

此外，可以在服务端两个级别设置压缩。

#### 在整个服务端

```python
server = grpc.server(futures.ThreadPoolExecutor(),
                     compression=grpc.Compression.Gzip)
```

#### 对单个RPC

```python
def SayHello(self, request, context):
    context.set_response_compression(grpc.Compression.NoCompression)
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
```

为单个RPC设置压缩方法将覆盖服务端创建时提供的任何设置。
