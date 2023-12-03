from django.urls import include, path
from rest_framework import routers

from .views.views import *
from .api.rest import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'dificuldade_bordado', DificuldadeBordadoViewSet)
router.register(r'bordado', BordadoViewSet)
router.register(r'pedido', PedidoViewSet)
router.register(r'pedido_item', PedidoItemViewSet)
router.register(r'cobranca', CobrancaViewSet)
router.register(r'pedido_item_cobranca', PedidoItemCobrancaViewSet)
router.register(r'ordem_producao', OrdemProducaoViewSet)
router.register(r'apontamento_producao', ApontamentoProducaoViewSet)

app_name = 'bordado'
urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('sobre', sobre, name='sobre'),
]
