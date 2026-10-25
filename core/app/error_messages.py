from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

_TYPE_MESSAGES = {
    "missing": "Обязательное поле",
    "string_too_short": "Слишком короткое значение (минимум {min_length} симв.)",
    "string_too_long": "Слишком длинное значение (максимум {max_length} симв.)",
    "greater_than": "Значение должно быть больше {gt}",
    "greater_than_equal": "Значение должно быть не меньше {ge}",
    "less_than": "Значение должно быть меньше {lt}",
    "less_than_equal": "Значение должно быть не больше {le}",
    "int_parsing": "Ожидалось целое число",
    "float_parsing": "Ожидалось число",
    "decimal_parsing": "Ожидалось число",
    "string_type": "Ожидалась строка",
    "bool_type": "Ожидалось true или false",
    "json_invalid": "Некорректный формат JSON",
    "value_error": "Некорректное значение",
}


def _translate_error(error: dict) -> str:
    error_type = error.get("type", "")
    template = _TYPE_MESSAGES.get(error_type)
    if template is None:
        return error.get("msg", "Некорректное значение")
    return template.format(**error.get("ctx", {}))


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    detail = [{**error, "msg": _translate_error(error)} for error in exc.errors()]
    return JSONResponse(status_code=422, content=jsonable_encoder({"detail": detail}))
