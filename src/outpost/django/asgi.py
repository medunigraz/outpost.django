import os
import logging
import django
from importlib import import_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "outpost.django.settings")

django.setup()

from a2wsgi import WSGIMiddleware
from django.apps import apps
#from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter



logger = logging.getLogger(__name__)

#django_asgi_app = get_asgi_application()
django_asgi_app = WSGIMiddleware(get_wsgi_application())

urls = list()
worker = dict()

for app in sorted(apps.get_app_configs(), key=lambda app: app.label):
    try:
        logger.debug(f"Looking for channels in {app.name}")
        module = import_module(f"{app.name}.channels")
        urls.extend(getattr(module, "urls", []))
        worker.update({k: v for k, v in getattr(module, "worker", {}).items()})
    except ModuleNotFoundError:
        pass
    except Exception:
        logger.warn(f"Failed to import channels from {app.name}")
        pass

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(urls),
        "channel": ChannelNameRouter(worker),
        "http": django_asgi_app,
    }
)
