import logging
from django.utils.deprecation import MiddlewareMixin
from .sync_manager import sincronizar_banco_da_sessao

logger = logging.getLogger(__name__)

class RuralSyncMiddleware(MiddlewareMixin):
    """
    Middleware responsável por:
    1. Sincronizar mutações salvas na sessão do usuário com o banco SQLite da instância
       (essencial para persistência em ambientes serverless como Vercel, onde lambdas são efêmeras).
    2. Aplicar cabeçalhos estritos de controle de cache (no-cache, no-store) para que o navegador
       e proxies nunca exibam listas defasadas ao alternar entre abas.
    """

    def process_request(self, request):
        try:
            sincronizar_banco_da_sessao(request)
        except Exception as e:
            logger.warning("Erro no processamento do RuralSyncMiddleware: %s", str(e))
        return None

    def process_response(self, request, response):
        path = request.path
        # Não interfere em arquivos estáticos (CSS, JS, Imagens gerenciados pelo WhiteNoise)
        if not path.startswith('/static/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response
