# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import demo_pb2 as demo__pb2


class GRPCDemoStub(object):
  """service是用来给GRPC服务定义方法的, 格式固定, 类似于Golang中定义一个接口
  `service` is used to define methods for GRPC services in a fixed format, similar to defining an interface in Golang
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SimpleMethod = channel.unary_unary(
        '/demo.GRPCDemo/SimpleMethod',
        request_serializer=demo__pb2.Request.SerializeToString,
        response_deserializer=demo__pb2.Response.FromString,
        )
    self.ClientStreamingMethod = channel.stream_unary(
        '/demo.GRPCDemo/ClientStreamingMethod',
        request_serializer=demo__pb2.Request.SerializeToString,
        response_deserializer=demo__pb2.Response.FromString,
        )
    self.ServerStreamingMethod = channel.unary_stream(
        '/demo.GRPCDemo/ServerStreamingMethod',
        request_serializer=demo__pb2.Request.SerializeToString,
        response_deserializer=demo__pb2.Response.FromString,
        )
    self.BidirectionalStreamingMethod = channel.stream_stream(
        '/demo.GRPCDemo/BidirectionalStreamingMethod',
        request_serializer=demo__pb2.Request.SerializeToString,
        response_deserializer=demo__pb2.Response.FromString,
        )


class GRPCDemoServicer(object):
  """service是用来给GRPC服务定义方法的, 格式固定, 类似于Golang中定义一个接口
  `service` is used to define methods for GRPC services in a fixed format, similar to defining an interface in Golang
  """

  def SimpleMethod(self, request, context):
    """简单模式
    unary-unary
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ClientStreamingMethod(self, request_iterator, context):
    """客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
    stream-unary (In a single call, the client can transfer data to the server several times,
    but the server can only return a response once.)
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerStreamingMethod(self, request, context):
    """服务端流模式（在一次调用中, 客户端只能一次向服务器传输数据, 但是服务器可以多次返回响应）
    unary-stream (In a single call, the client can only transmit data to the server at one time,
    but the server can return the response many times.)
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def BidirectionalStreamingMethod(self, request_iterator, context):
    """双向流模式 (在一次调用中, 客户端和服务器都可以向对方多次收发数据)
    stream-stream (In a single call, both client and server can send and receive data
    to each other multiple times.)
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GRPCDemoServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SimpleMethod': grpc.unary_unary_rpc_method_handler(
          servicer.SimpleMethod,
          request_deserializer=demo__pb2.Request.FromString,
          response_serializer=demo__pb2.Response.SerializeToString,
      ),
      'ClientStreamingMethod': grpc.stream_unary_rpc_method_handler(
          servicer.ClientStreamingMethod,
          request_deserializer=demo__pb2.Request.FromString,
          response_serializer=demo__pb2.Response.SerializeToString,
      ),
      'ServerStreamingMethod': grpc.unary_stream_rpc_method_handler(
          servicer.ServerStreamingMethod,
          request_deserializer=demo__pb2.Request.FromString,
          response_serializer=demo__pb2.Response.SerializeToString,
      ),
      'BidirectionalStreamingMethod': grpc.stream_stream_rpc_method_handler(
          servicer.BidirectionalStreamingMethod,
          request_deserializer=demo__pb2.Request.FromString,
          response_serializer=demo__pb2.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'demo.GRPCDemo', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
