import pickle
import xmlrpc.client
import math

import sys
from xmlrpc.client import Marshaller
from measurer import call_10_times_with_statistics
import settings
from simple_operations import ComplexObject


def test_rpc_string_calls(proxy):
    for i in range(10):
        characters = int(math.pow(2, i))
        n_chars_rpc_string_rpc_call(proxy, settings.LOREM_IPSUM[:characters])


@call_10_times_with_statistics
def empty_rpc_call(proxy):
    proxy.empty_call()


@call_10_times_with_statistics
def n_chars_rpc_string_rpc_call(proxy, str_param):
    return proxy.str_call(str_param)


@call_10_times_with_statistics
def long_rpc_call(proxy, long_param):
    return proxy.long_call(long_param)


@call_10_times_with_statistics
def eight_longs_rpc_call(
        proxy, long1, long2, long3, long4, long5, long6, long7, long8
):
    return proxy.eight_long_calls(
        long1, long2, long3, long4, long5, long6, long7, long8
    )


@call_10_times_with_statistics
def complex_rpc_call(proxy, complex_param):
    call = proxy.complex_call(pickle.dumps(complex_param))
    return pickle.loads(call.data)


def run_methods():
    uri = 'http://{endpoint}:{port}/'.format(
        endpoint=settings.ENDPOINT, port=settings.PORT
    )
    with xmlrpc.client.ServerProxy(uri) as proxy:
        force_long_type()
        empty_rpc_call(proxy)
        chosen_long = sys.maxsize
        test_rpc_string_calls(proxy)
        long_rpc_call(proxy, chosen_long)
        eight_longs_rpc_call(
            proxy, long1=chosen_long, long2=chosen_long, long3=chosen_long,
            long4=chosen_long, long5=chosen_long, long6=chosen_long,
            long7=chosen_long, long8=chosen_long
        )
        complex_rpc_call(proxy, ComplexObject())


def force_long_type():
    '''
    Since in python3 theres no long type anymore, we have to force the use of long type at xmlrpc here.
    :return:
    '''
    Marshaller.dispatch[type(0)] = lambda _, v, w: w(
        "<value><i8>%d</i8></value>" % v)


if __name__ == '__main__':
    run_methods()
