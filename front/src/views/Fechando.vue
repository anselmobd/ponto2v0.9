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
    <h2 class="my-4 font-bold text-xl">Fechando pedido <span class="text-indigo-700">{{ route.params.id }}</span></h2>
    <div v-if="pedido_item">
      <table class="w-full">
        <thead>
          <tr>
            <th>Usuário</th>
            <th>Data</th>
            <th>Cliente</th>
            <th>Bordado</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ pedido_item.usuario.username }}</td>
            <td>{{inserido_em}}</td>
            <td>{{pedido_item.pedido.cliente.apelido}}</td>
            <td>{{pedido_item.bordado.nome}}</td>
          </tr>
        </tbody>
      </table>
      <h3 class="my-4 font-bold text-lg">Dados do bordado</h3>
      <form @submit.prevent="formGrava()">
        <table class="w-full">
          <thead>
            <tr>
              <th><label for="data">Data de entrega</label></th>
              <th><label for="quantidade">Quantidade</label></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input
                  class="px-2 py-1 w-40 border-2 rounded"
                  type="date"
                  name="data"
                  id="data"
                  v-focus
                  v-model="data"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  name="quantidade"
                  id="quantidade"
                  placeholder="0"
                  v-model="quantidade"
                  @input="alerta = ''"
                  required>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="alerta" class="my-4 text-red-600">{{ alerta }}</p>
        <button
          class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100"
          type="submit"
        >Grava</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
th, td {
  @apply border border-solid border-slate-300 text-center
}
</style>