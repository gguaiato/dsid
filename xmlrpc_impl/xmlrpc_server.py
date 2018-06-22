import pickle
from xmlrpc.client import Marshaller
from xmlrpc.server import SimpleXMLRPCServer
import time

import settings
import simple_operations


def empty_call():
    return simple_operations.empty_call()


def long_call(long_param):
    return simple_operations.one_long_and_one_long_return(
        long_param
    )


def eight_long_calls(
    long1, long2, long3, long4, long5, long6, long7, long8
):
    return simple_operations.eight_long_arguments_and_one_long_return(
        long1, long2, long3, long4, long5, long6, long7, long8
    )


def str_call(str_param):
    return simple_operations.str_argument_and_one_str_return(
        str_param
    )


def complex_call(complex_param):
    complex_object = simple_operations.complex_argument_and_one_complex_return(
        pickle.loads(complex_param.data)
    )
    return pickle.dumps(complex_object)


server = SimpleXMLRPCServer(("0.0.0.0", settings.PORT), allow_none=True)
Marshaller.dispatch[type(0)] = lambda _, v, w: w("<value><i8>%d</i8></value>" % v)
print("Listening on port {}...".format(settings.PORT))
server.register_function(empty_call, empty_call.__name__)
server.register_function(long_call, long_call.__name__)
server.register_function(eight_long_calls, eight_long_calls.__name__)
server.register_function(str_call, str_call.__name__)
server.register_function(complex_call, complex_call.__name__)

server.serve_forever()
