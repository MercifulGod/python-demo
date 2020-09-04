# Copyright 2019 The gRPC Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Server of the Python example of customizing authentication mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from concurrent import futures

import grpc
from gRPCDemo.a_helloworld import helloworld_pb2
from gRPCDemo.a_helloworld import helloworld_pb2_grpc
from gRPCDemo.b_auth import _credentials

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

_LISTEN_ADDRESS_TEMPLATE = 'localhost:%d'
_SIGNATURE_HEADER_KEY = 'x-signature'


class SignatureValidationInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid signature')

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method.split('/')[-1]
        expected_metadata = (_SIGNATURE_HEADER_KEY, method_name[::-1])
        if expected_metadata in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._abortion


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def create_server():
    server = grpc.server(futures.ThreadPoolExecutor(),
                         interceptors=(SignatureValidationInterceptor(),))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # Loading credentials
    server_credentials = grpc.ssl_server_credentials(
        ((_credentials.SERVER_CERTIFICATE_KEY, _credentials.SERVER_CERTIFICATE),),
    )

    # Pass down credentials
    server.add_secure_port('[::]:50051', server_credentials)

    return server


def main():
    server = create_server()
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
