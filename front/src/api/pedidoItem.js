import { axiosPrivate } from '../common/axiosPrivate.js';


export function getPedidoItensCB(callBack) {
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

export function getClientesCB(callBack) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  params.append('page_size', '999999');

  axiosPrivate.get(
    '/bordado/api/clientes/',
    {params: params}
  )
  .then(response => {
    callBack(response.data.results.map(
      clie => clie.apelido
    ));
  })
  .catch(error => {
    console.error('Erro ao obter clientes via API:', error);
    callBack(null, error);
  });
}
