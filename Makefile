export PYTHONPATH=$(PWD)

clean:
	rm -f simple_operations_pb2.py
	rm -f simple_operations_pb2_grpc.py

compile-proto: clean
	./generate_proto.sh simple_operations.proto

run-client-grpc:
	python grpc_impl/grpc_client.py

run-server-grpc: compile-proto
	python grpc_impl/grpc_server.py

run-client-xmlrpc:
	python xmlrpc_impl/xmlrpc_client.py

run-server-xmlrpc:
	python xmlrpc_impl/xmlrpc_server.py