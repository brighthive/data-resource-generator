import os
from data_resource import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

env = os.getenv("APP_ENV", "")

app = application = create_app(actually_run=True)
# app = ProxyFix(app)
