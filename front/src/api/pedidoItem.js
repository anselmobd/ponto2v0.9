import { axiosPrivate } from '../common/axiosPrivate.js';

export function getPedidoItens({
  page=1,
  cliente_apelido=null,
  callBack=()=>{}
}) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  if (page && page >1) {
    params.append('page', page);
  }
  if (cliente_apelido) {
    params.append('pedido__cliente__apelido', cliente_apelido);
  }
  axiosPrivate.get(
    '/bordado/api/pedido_item/',
    {params: params}
  )
  .then(response => {
    callBack(response.data);
  })
  .catch(error => {
    console.error('Erro ao obter pedido_itens via API:', error)
    callBack(null, error);
  });
}

export function getPedidoItem({
  id=null,
  callBack=()=>{}
}) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  axiosPrivate.get(
    `/bordado/api/pedido_item/${id}/`,
    {params: params}
  )
  .then(response => {
    callBack(response.data);
  })
  .catch(error => {
    console.error('Erro ao obter pedido_item '+id+' via API:', error)
    callBack(null, error);
  });
}

export function addClienteBordado(
  cliente_apelido,
  bordado_nome,
  callBack
) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  params.append('page_size', '999999');

  axiosPrivate.post(
    '/bordado/api/pedido_item/',
    {
      cliente: {apelido: cliente_apelido},
      bordado: {nome: bordado_nome}
    },
    {params: params},
  )
  .then(response => {
    callBack(response.data);
  })
  .catch(error => {
    console.error('Erro ao gravar "cliente / bordado" via API:', error);
    callBack(null, error.response.data);
  });
}

export function delClienteBordado(
  index,
  key,
  callBack
) {
  const params = new URLSearchParams();
  params.append('format', 'json');

  axiosPrivate.delete(
    `/bordado/api/pedido_item/${key}/`,
    {params: params},
  )
  .then(response => {
    callBack(index);
  })
  .catch(error => {
    console.error('Erro ao apagar "cliente / bordado" via API:', error);
    callBack(-1);
  });
}