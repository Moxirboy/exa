FROM python:3.7

#
RUN mkdir /service
WORKDIR /service

# Install SWIG
RUN apt update && apt install build-essential swig -y

COPY . ./

# Installing python dependencies
RUN python -m pip install -U pip setuptools wheel
RUN python -m pip install --no-cache-dir --upgrade -r ./requirements.txt
# RUN python -m grpc_tools.protoc -I./tahrirchi-backend-protos/ --python_out=app/ --pyi_out=app/  --grpc_python_out=app/ ./tahrirchi-backend-protos/speller_service/translation_service.proto


EXPOSE 9006
ENTRYPOINT [ "python", "app/run.py" ]