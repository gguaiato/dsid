#!/bin/bash
proto_file="$1"
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $proto_file