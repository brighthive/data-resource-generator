import os
from data_resource import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

env = os.getenv("APP_ENV", "")

if env.upper() != "PRODUCTION":
    raise RuntimeError("Must run WSGI with APP_ENV=PRODUCTION")

app = application = create_app(actually_run=False)
app = ProxyFix(app)
