# Copyright 2016 gRPC authors.
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
"""A client that makes both Greeter and RouteGuide RPCs."""

from __future__ import print_function

import random
import time
import logging

import grpc

from gRPCDemo.a_multiplex import helloworld_pb2
from gRPCDemo.a_multiplex import helloworld_pb2_grpc
from gRPCDemo.a_multiplex import route_guide_pb2
from gRPCDemo.a_multiplex import route_guide_pb2_grpc
from gRPCDemo.a_multiplex import route_guide_resources


def guide_get_one_feature(route_guide_stub, point):
    feature = route_guide_stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print("Found no feature at %s" % feature.location)


def guide_get_feature(route_guide_stub):
    guide_get_one_feature(
        route_guide_stub,
        route_guide_pb2.Point(latitude=409146138, longitude=-746188906))
    guide_get_one_feature(route_guide_stub,
                          route_guide_pb2.Point(latitude=0, longitude=0))


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        greeter_stub = helloworld_pb2_grpc.GreeterStub(channel)
        route_guide_stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        greeter_response = greeter_stub.SayHello(
            helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + greeter_response.message)
        print("-------------- GetFeature --------------")
        guide_get_feature(route_guide_stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
