import pickle
import grpc
import math

import sys

from measurer import call_10_times_with_statistics
import settings
import simple_operations_pb2
import simple_operations_pb2_grpc
from simple_operations import ComplexObject


def test_rpc_string_calls(stub):
    for i in range(10):
        characters = int(math.pow(2, i))
        str_param = simple_operations_pb2.StrParam(
            value=settings.LOREM_IPSUM[:characters]
        )
        n_chars_rpc_string_rpc_call(stub, str_param)


@call_10_times_with_statistics
def empty_rpc_call(stub, empty_param):
    stub.EmptyCall(empty_param)


@call_10_times_with_statistics
def n_chars_rpc_string_rpc_call(stub, str_param):
    return stub.StrCall(str_param)


@call_10_times_with_statistics
def long_rpc_call(stub, long_param):
    return stub.LongCall(long_param)


@call_10_times_with_statistics
def eight_longs_rpc_call(stub, eight_longs_param):
    return stub.EightLongCalls(eight_longs_param)


@call_10_times_with_statistics
def complex_rpc_call(stub, complex_param):
    return stub.ComplexCall(complex_param)


def run_methods():
    channel = grpc.insecure_channel('{endpoint}:{port}'.format(
        endpoint=settings.ENDPOINT, port=settings.PORT
    ))
    stub = simple_operations_pb2_grpc.RemoteTesterStub(channel)

    empty_rpc_call(stub, simple_operations_pb2.Empty())
    test_rpc_string_calls(stub)

    chosen_long = sys.maxsize
    long_param = simple_operations_pb2.LongParam(value=chosen_long)
    long_rpc_call(stub, long_param)

    eight_longs_param = simple_operations_pb2.EightLongsParam(
        long1=chosen_long, long2=chosen_long, long3=chosen_long,
        long4=chosen_long, long5=chosen_long, long6=chosen_long,
        long7=chosen_long, long8=chosen_long
    )
    eight_longs_rpc_call(stub, eight_longs_param)

    complex_param = simple_operations_pb2.ComplexParam(
        complex=pickle.dumps(ComplexObject())
    )
    complex_rpc_call(stub, complex_param)


if __name__ == '__main__':
    run_methods()
