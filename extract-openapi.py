# import json
#
# from uvicorn.importer import import_from_string
#
# app = import_from_string("./src/keyfort/main.py")
# openapi = app.openapi()
#
# with open("./spec.json") as f:
#     json.dump(openapi, f, indent=2)

from fastapi.openapi.utils import get_openapi
from src.keyfort.main import app
import json

with open('openapi.json', 'w') as f:
    json.dump(get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
        # openapi_prefix=app.openapi_prefix,
    ), f)
