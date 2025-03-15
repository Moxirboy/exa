# Speller service
Its job is to check for spelling mistakes

## How to run

`$ python app/app.py`

## Compile proto file

`protoc --proto_path=tahrirchi-backend-protos --python_out=app/speller_service tahrirchi-backend-protos/speller_service/speller_service.proto --experimental_allow_proto3_optional`

## Features

1. Spelling error - `SUGGESTION_SPELL`
2. Case error - `SUGGESTION_CASE`
3. Merge error - `SUGGESTION_MERGE`
4. Split error - `SUGGESTION_SPLIT`

# exa
