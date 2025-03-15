python -m grpc_tools.protoc -I ./tahrirchi-backend-protos --python_out=app --pyi_out=app \
         --grpc_python_out=app ./tahrirchi-backend-protos/query-service/query_service.proto
