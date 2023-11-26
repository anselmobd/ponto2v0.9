<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js';

const pedido_itens = ref(null)

function refreshToken(execFunction = null, param = null) {
  console.log('refreshToken');
  const auth = useAuthStore()
  let headers = {
    'Content-Type': 'application/json',
  };
  console.log(headers);

  const params = new URLSearchParams();
  params.append('format', 'json');
  console.log(params);

  const { setUser } = auth

  var result = 0;

  axios.post(
    'http://tt.o2:8902/api/token/refresh/',
    {refresh: auth.user.refresh},
    {params: params, headers: headers}
  )
  .then(response => {
    console.log('then');
    console.log(response.status);
    console.log(response.data);
    if (response.data.access) {
      setUser(
        auth.user.name,
        response.data.access,
        auth.user.refresh
      );
    }
    result = response.status;
  })
  .catch(error => {
    console.log('catch');
    console.log(error.status);
    console.log('Erro ao dar refresh na access key:', error);
    console.log(error.response.status);
    result = error.response.status;
  })
  .finally(function () {
    console.log('finally');
    if (result == 200 && execFunction != null) {
      execFunction(param);
    }
  });
}

function getPedidoItens(tentativa = 1) {
  console.log('getPedidoItens', tentativa);
  const auth = useAuthStore()
  let headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + auth.user.access
  };
  console.log(headers);

  const params = new URLSearchParams();
  params.append('format', 'json');
  console.log(params);

  var result = 0;

  axios.get(
    'http://tt.o2:8902/bordado/api/pedido_item/',
    {params: params, headers: headers}
  )
  .then(response => {
    console.log('then');
    console.log(response.data.results);
    pedido_itens.value = response.data.results;
    result = response.status;
  })
  .catch(error => {
    console.log('catch');
    console.log('Erro ao obter pedido_itens via API:', error);
    console.log(error.response.status);
    result = error.response.status;
  })
  .finally(function () {
    console.log('finally');
    if (result == '401' && tentativa == 1) {
      console.log('status == 401');
      refreshToken(getPedidoItens, 2);
    }
  });
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
