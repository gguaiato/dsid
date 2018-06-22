import pickle

import grpc
from concurrent import futures
import time

import simple_operations_pb2
import simple_operations_pb2_grpc
import settings
import simple_operations


class RemoteTesterServicer(simple_operations_pb2_grpc.RemoteTesterServicer):

    def EmptyCall(self, request, context):
        simple_operations.empty_call()
        return simple_operations_pb2.Empty()

    def LongCall(self, request, context):
        response = simple_operations_pb2.LongParam()
        response.value = simple_operations.one_long_and_one_long_return(
            request.value
        )
        return response

    def EightLongCalls(self, request, context):
        response = simple_operations_pb2.LongParam()
        response.value = simple_operations.eight_long_arguments_and_one_long_return(
            request.long1, request.long2, request.long3, request.long4,
            request.long5, request.long6, request.long7, request.long8
        )
        return response

    def StrCall(self, request, context):
        response = simple_operations_pb2.StrParam()
        response.value = simple_operations.str_argument_and_one_str_return(
            request.value
        )
        return response

    def ComplexCall(self, request, context):
        response = simple_operations_pb2.ComplexParam()
        complex_object = simple_operations.complex_argument_and_one_complex_return(
            pickle.loads(request.complex)
        )
        response.complex = pickle.dumps(complex_object)
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
simple_operations_pb2_grpc.add_RemoteTesterServicer_to_server(
        RemoteTesterServicer(), server
)
print('Starting server. Listening on port {}.'.format(settings.PORT))
server.add_insecure_port('[::]:{port}'.format(port=settings.PORT))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)