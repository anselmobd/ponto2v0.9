<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted } from 'vue'
import { getPedidoItem } from '../api/pedidoItem.js';
import { dateTime2Text } from "../utils/date.js";

const route = useRoute();

const pedido_item = ref('')
const inserido_em = ref(null)

const data = ref('')
const quantidade = ref('')
const alerta = ref('')

// DB API calls (do) and callbacks (cb)

function cbPedidoItem(data, error) {
  if (data) {
    console.log(data);
    pedido_item.value = data;
    const date = new Date(pedido_item.value.inserido_em);
    inserido_em.value = dateTime2Text(date);
  }
}

function doGetPedidoItem() {
  getPedidoItem({
    id: route.params.id,
    callBack: cbPedidoItem
  });
}

// events

function formGrava(event) {
  event.preventDefault();
}

// Lifecycle Hooks

onMounted(() => {
  doGetPedidoItem();
})

</script>

<template>
  <div>
    <h2 class="my-4 font-bold text-lg">Fechando pedido {{ route.params.id }}</h2>
    <div v-if="pedido_item">
      <p class="my-4">Cliente: {{ pedido_item.pedido.cliente.apelido }}</p>
      <p class="my-4">Bordado: {{ pedido_item.bordado.nome }}</p>
      <p class="my-4">Inserido em: {{ inserido_em }}</p>
      <p class="my-4">Usuário: {{ pedido_item.usuario.username }}</p>
      <form @submit.prevent="formGrava()">
        <p class="my-4">
          <label class="block" for="username">Data de entrega</label>
          <input
            class="px-2 py-1 w-40 border-2 rounded-xl"
            type="date"
            name="data"
            id="data"
            v-focus
            v-model="data"
            @input="alerta = ''"
            required>
        </p>
        <p class="my-4">
          <label class="block" for="password">Quantidade</label>
          <input
            class="px-2 py-1 w-24 border-2 rounded-xl"
            type="number"
            name="quantidade"
            id="quantidade"
            placeholder="0"
            v-model="quantidade"
            @input="alerta = ''"
            required>
        </p>
        <p v-if="alerta" class="my-4 text-red-600">{{ alerta }}</p>
        <button
          class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100"
          type="submit"
        >Grava</button>
      </form>
    </div>
  </div>
</template>
