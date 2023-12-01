<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'
import { getPedidoItem } from '../api/pedidoItem.js';
import { dateTime2Text } from "../utils/date.js";
import { ptBrCurrencyFormat } from "../utils/numStr.js";

const route = useRoute();

// valores recebidos de DB

const pedido_item = ref('')
const inserido_em = ref(null)

// valores em inputs

const data = ref(null)
const quantidade = ref(0)
const valor_unitario = ref(0)
const programacao = ref(0)
const ajuste = ref(0)

// outros valores reativos

const valor = ref(0)
const valor_final = ref(0)
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

function formGrava() {
  console.log('grava');
}

// Lifecycle Hooks

onMounted(() => {
  doGetPedidoItem();
})

// watch

watch(quantidade, (_) => {
  calcValor();
  calcValorFinal();
})

watch(valor_unitario, (_) => {
  calcValor();
  calcValorFinal();
})

watch(programacao, (_) => {
  calcValorFinal();
})

watch(ajuste, (_) => {
  calcValorFinal();
})

// generic functions

function calcValor() {
  const calculo = quantidade.value * valor_unitario.value;
  valor.value = ptBrCurrencyFormat.format(calculo);
}

function calcValorFinal() {
  const calculo = quantidade.value * valor_unitario.value +
      programacao.value + ajuste.value;
  valor_final.value = ptBrCurrencyFormat.format(calculo);
}

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
              <th><label for="valor_unitario">Valor unitário</label></th>
              <th>Valor</th>
              <th><label for="programacao">Programação</label></th>
              <th><label for="ajuste">Ajuste</label></th>
              <th>Valor final</th>
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
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="valor_unitario"
                  id="valor_unitario"
                  placeholder="0,00"
                  v-model="valor_unitario"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                 {{ valor }}
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="programacao"
                  id="programacao"
                  placeholder="0,00"
                  v-model="programacao"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="ajuste"
                  id="ajuste"
                  placeholder="0,00"
                  v-model="ajuste"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                 {{ valor_final }}
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="alerta" class="my-4 text-red-600">{{ alerta }}</p>
        <button
          class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100 float-right"
          type="submit"
        >Grava</button>
      </form>
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
</style>
