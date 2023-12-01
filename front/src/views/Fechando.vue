<script setup>
import { useRoute } from "vue-router";
import { onMounted } from 'vue'
import { getPedidoItem } from '../api/pedidoItem.js';

const route = useRoute();

// DB API calls (do) and callbacks (cb)

function cbPedidoItem(data, error) {
  if (data) {
    console.log(data);
    // if (data?.results) pedido_itens.value = data.results;
  }
}

function doGetPedidoItem() {
  getPedidoItem({
    id: route.params.id,
    callBack: cbPedidoItem
  });
}

// Lifecycle Hooks

onMounted(() => {
  doGetPedidoItem();
})

</script>

<template>
  <div>
    <h2 class="font-bold text-lg">Fechando pedido {{ route.params.id }}</h2>
  </div>
</template>
