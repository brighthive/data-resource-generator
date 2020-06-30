import os
from data_resource import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

environment = os.getenv('APP_ENV', None)

isprod = environment == 'PRODUCTION'

app = application = create_app(actually_run=True)

if isprod:
    app = ProxyFix(app)
