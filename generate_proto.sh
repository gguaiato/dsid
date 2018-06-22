#!/bin/bash
proto_file="$1"
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $proto_file