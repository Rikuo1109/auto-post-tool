from datetime import datetime

from ninja.renderers import BaseRenderer

import orjson


class Renderer(BaseRenderer):
    """Renderer response to format of Horusoftaceae

    Example:
        {
            "data": {
                "id": 1,
                "name": "Horusoftaceae",
            },
            "message_code": "SUCCESS",
            "message": "Success",
            "error_code": 0,
            "current_time": "2021-09-01T00:00:00.000000"
        }
    """

    media_type = "application/json"
    format = "json"
    charset = ""

    def render(self, data, **options):
        return orjson.dumps(
            {
                "data": data,
                "message_code": "SUCCESS",
                "message": "Success",
                "error_code": 0,
                "current_time": datetime.now(),
            }
        )
