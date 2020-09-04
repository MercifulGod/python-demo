from concurrent import futures
import logging

import grpc
from grpc_reflection.v1alpha import reflection

from gRPCDemo.a_helloworld import helloworld_pb2
from gRPCDemo.a_helloworld import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def create_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # with reflection start
    SERVICE_NAMES = (
        helloworld_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    # with reflection end

    server.add_insecure_port('[::]:50051')
    return server


def main():
    server = create_server()
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    main()
