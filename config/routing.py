from channels.routing import ProtocolTypeRouter, URLRouter
import apps.apis.routing

application = ProtocolTypeRouter({
    'http': URLRouter(apps.apis.routing.urlpatterns),
})
