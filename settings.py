from http import HTTPStatus

# Nazwa musi składać się z jednego lub więcej słów w skład których wchodza jedynie litery i cyfry
TAG_NAME_VALIDATION_REGEX = "^[\w\d](?:\s?[\w\d])*$"


INVALID_TAG_NAME_ERROR = {
    "code": "invalid_tag_name",
    "type": "https://127.0.0.1/v1/docs/problem-details/invalid_tag_name",
    "detail": "Nieprawna nazwa taga. Nazwa musi składać się z jednego lub więcej słów w skład których wchodza jedynie litery i cyfry.",
    "status": HTTPStatus.BAD_REQUEST,
}
INVALID_DATA_FORMAT_ERROR = {
    "code": "invalid_format",
    "type": "https://127.0.0.1/v1/docs/problem-details/invalid_format",
    "detail": "Nieprawny format danych. Oczekiwano application/json",
    "status": HTTPStatus.METHOD_NOT_ALLOWED,
}
