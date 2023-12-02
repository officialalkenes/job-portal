from decouple import config

ENVIRONMENT = config("ENVIRONMENT")

if ENVIRONMENT == "dev":
    from .dev import *
elif ENVIRONMENT == "prod":
    from .prod import *
elif ENVIRONMENT == "test":
    from .test import *
else:
    raise ValueError("Invalid environment specified.")
