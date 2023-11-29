import { axiosPrivate } from '../common/axiosPrivate.js';

export function getBordadosCB(cliente_apelido, callBack) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  params.append('cliente__apelido', cliente_apelido);

  axiosPrivate.get(
    '/bordado/api/bordado/',
    {params: params}
  )
  .then(response => {
    callBack(response.data.results.map(
      bord => bord.nome
    ));
  })
  .catch(error => {
    console.error('Erro ao obter clientes via API:', error);
    callBack(null, error);
  });
}
