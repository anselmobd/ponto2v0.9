<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js';
import { axiosPublic } from '../common/axiosPublic.js';
import { refreshAccessToken } from '../common/refreshToken.js';
import { authHeader } from '../services/auth-header.js'

const pedido_itens = ref(null)

// function refreshToken(execFunction = null, param = null) {
//   console.log('refreshToken');
//   const auth = useAuthStore()

//   const params = new URLSearchParams();
//   params.append('format', 'json');
//   console.log(params);

//   const { setUser } = auth

//   var result = 0;

//   axiosPublic.post(
//     '/api/token/refresh/',
//     {refresh: auth.user.refresh},
//     {params: params} // , headers: headers}
//   )
//   .then(response => {
//     console.log('refreshToken then');
//     console.log(response.status);
//     console.log(response.data);
//     if (response.data.access) {
//       setUser(
//         auth.user.name,
//         response.data.access,
//         auth.user.refresh
//       );
//     }
//     result = response.status;
//   })
//   .catch(error => {
//     console.log('refreshToken catch');
//     console.log(error.status);
//     console.log('Erro ao dar refresh na access key:', error);
//     console.log(error.response.status);
//     result = error.response.status;
//   })
//   .finally(function () {
//     console.log('refreshToken finally');
//     if (result == 200 && execFunction != null) {
//       execFunction(param);
//     }
//   });
//   console.log('refreshToken fim');
// }

function getPedidoItens(tentativa = 1) {
  console.log('getPedidoItens', tentativa);

  let headers = authHeader();
  console.log(headers);

  const params = new URLSearchParams();
  params.append('format', 'json');
  console.log(params);

  var result = 0;

  axiosPublic.get(
    '/bordado/api/pedido_item/',
    {params: params, headers: headers}
  )
  .then(response => {
    console.log('getPedidoItens then');
    console.log(response.data.results);
    pedido_itens.value = response.data.results;
    result = response.status;
  })
  .catch(error => {
    console.log('getPedidoItens catch');
    console.log('Erro ao obter pedido_itens via API:', error);
    console.log(error.response.status);
    result = error.response.status;
  })
  .finally(function () {
    console.log('getPedidoItens finally');
    if (result == '401' && tentativa == 1) {
      console.log('status == 401');
      console.log('call refreshAccessToken');
      // let refreshStatus =
      refreshAccessToken()
      .then(refreshStatusResponse => {
        console.log('refreshAccessToken then')
        console.log('refreshStatusResponse', refreshStatusResponse);
        if (refreshStatusResponse == 200) {
          console.log('entrou no if do then');
          getPedidoItens(2);
        // } else {
        //   console.log('Não entrou no if do then');
        }
      });
      // console.log('refreshStatus', refreshStatus);
      // if (refreshStatus == 200) {
      //   console.log('entrou no if');
      //   getPedidoItens(2);
      // }
      // refreshToken(getPedidoItens, 2);
    }
  });
  console.log('getPedidoItens fim');
}

onMounted(() => {
  console.log('onMounted');
  getPedidoItens();
  console.log(pedido_itens);
})
</script>

<template>
  <div>
    <p>pedido_itens</p>
    {{pedido_itens}}
  </div>
</template>
