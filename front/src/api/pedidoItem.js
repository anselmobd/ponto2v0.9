import { axiosPrivate } from '../common/axiosPrivate.js';

export function getPedidoItens(callBack) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  axiosPrivate.get(
    '/bordado/api/pedido_item/',
    {params: params}
  )
  .then(response => {
    callBack(response.data.results);
  })
  .catch(error => {
    console.error('Erro ao obter pedido_itens via API:', error)
    callBack(null, error);
  });
}
