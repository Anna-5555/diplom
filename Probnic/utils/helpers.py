"""Вспомогательные функции для тестов."""

import json
import allure
from typing import Dict, Any, List


def attach_response_data(response, name: str = "response"):
    """Прикрепить данные ответа к Allure отчету."""
    try:
        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "data": response.json() if response.content else "Empty response"
        }

        allure.attach(
            json.dumps(response_data, indent=2, ensure_ascii=False),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )
    except Exception as e:
        allure.attach(f"Error attaching response: {str(e)}", name=f"{name}_error")


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """Валидация JSON схемы."""
    errors = []

    def _validate(obj, sch, path=""):
        if "type" in sch:
            expected_type = sch["type"]
            actual_type = type(obj).__name__

            if expected_type == "array" and actual_type != "list":
                errors.append(f"Expected array at {path}, got {actual_type}")
            elif expected_type == "object" and actual_type != "dict":
                errors.append(f"Expected object at {path}, got {actual_type}")
            elif expected_type not in ["array", "object"] and actual_type != expected_type:
                errors.append(f"Expected {expected_type} at {path}, got {actual_type}")

        if "required" in sch and isinstance(obj, dict):
            for field in sch["required"]:
                if field not in obj:
                    errors.append(f"Missing required field: {path}.{field}")

        if "properties" in sch and isinstance(obj, dict):
            for field, field_schema in sch["properties"].items():
                if field in obj:
                    _validate(obj[field], field_schema, f"{path}.{field}" if path else field)

    _validate(data, schema)
    return errors


def retry_request(session, url, params=None, max_retries=3, delay=1):
    """Повторять запрос в случае неудачи."""
    import time
    from requests.exceptions import RequestException

    for attempt in range(max_retries):
        try:
            response = session.get(url, params=params)
            if response.status_code == 200:
                return response
        except RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)

    return None
