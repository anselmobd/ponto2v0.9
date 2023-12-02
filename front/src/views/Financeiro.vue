<script setup>
import router from '@/router'
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'
import { getPedidoItens } from '../api/pedidoItem.js';

const route = useRoute();

// valores recebidos de DB

const pedido_itens = ref('')

// DB API calls (do) and callbacks (cb)

function cbGetPedidoItens(data, error) {
  if (data) {
    if (data?.results) pedido_itens.value = data.results;
  }
}

function doGetPedidoItens(callBack) {
  getPedidoItens({
    cliente_apelido: route.params.apelido,
    callBack: cbGetPedidoItens
  });
}

// Lifecycle Hooks

onMounted(() => {
  doGetPedidoItens();
})

</script>

<template>
  <div>
    <div class="flex my-4 place-content-between">
      <h2 class="inline font-bold text-xl">Financeiro do cliente <span class="text-indigo-700">{{ route.params.apelido }}</span></h2>
      <a title="Voltar" class="button text-xl cursor-pointer" @click.prevent="router.go(-1)">&#x2190;</a>
    </div>
    <div v-if="pedido_itens">
      <table class="w-full">
        <thead>
          <tr>
            <th>Data entrega</th>
            <th>Pedido</th>
            <th>Bordado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="pedido_item in pedido_itens"
            :key="pedido_item.id"
          >
            <td>{{pedido_item.pedido.entrega}}</td>
            <td>{{pedido_item.id}}</td>
            <td>{{pedido_item.bordado.nome}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
table  {
  @apply my-4
}
th, td {
  @apply border border-solid border-slate-300 text-center
}
button, .button {
  @apply mx-0.5 my-[1px] px-2 py-0.5 rounded-lg bg-sky-700 font-bold text-slate-100
}
button:disabled {
  @apply bg-slate-500
}
</style>