<script setup>
import router from '@/router'
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'
import { getPedidoItens } from '../api/pedidoItem.js';
import { date2InputText } from "../utils/date.js";
import { ptBrCurrencyFormat } from "../utils/numStr.js";

const route = useRoute();

// valores recebidos de DB

const pedido_itens = ref('')
const pedidos_selecionados = ref([])
const comunicado = ref({})

// variaveis comuns

  // para inicializar com data atual
  const dataAtual = new Date();
  const strDataAtual = date2InputText(dataAtual);

// outros valores reativos

const status = ref('b'); // 'b' browsing; 'c' inserting comunicado;

// get set refs

function clearComunicado() {
  comunicado.value = {
    valor_total: 0,
    tipo: '',
    nf: null,
    data: strDataAtual,
    parcelamento: '',
  };
}

// DB API calls (do) and callbacks (cb)

function cbGetPedidoItens(data, error) {
  if (data) {
    if (data?.results) pedido_itens.value = data.results.map((ped_item) => {
      ped_item.valor_final =
        ped_item.quantidade * parseFloat(ped_item.preco)
        + parseFloat(ped_item.programacao) + parseFloat(ped_item.ajuste);
      return ped_item;
    });
  }
}

function doGetPedidoItens(callBack) {
  getPedidoItens({
    cliente_apelido: route.params.apelido,
    callBack: cbGetPedidoItens
  });
}

// events

function handleComunicarClick(event) {
  event.preventDefault();
  comunicado.value.valor_total = pedido_itens.value.map((ped_item) => {
    return pedidos_selecionados.value.includes(ped_item.id) ? ped_item.valor_final : 0
  }).reduce((soma, valor) => soma + valor, 0);
  comunicado.value.data = strDataAtual;
  status.value = 'c';
}

function handleCancelaClick(event) {
  event.preventDefault();
  status.value = 'b';
  clearComunicado();
}

// Lifecycle Hooks

onMounted(() => {
  doGetPedidoItens();
})

</script>

<template>
  <div>
    <div class="flex pt-4 place-content-between">
      <h2 class="inline font-bold text-xl">Financeiro do cliente <span class="text-indigo-700">{{ route.params.apelido }}</span></h2>
      <a title="Voltar" class="button text-xl cursor-pointer" @click.prevent="router.go(-1)">&#x2190;</a>
    </div>
    <div v-if="pedido_itens">

      <h3 class="my-4 font-bold text-lg text-center">Pedidos</h3>
      <button
        class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100"
        @click="handleComunicarClick"
      >Comunicar</button>

      <table class="w-full">
        <thead>
          <tr>
            <th>Seleção</th>
            <th>Data entrega</th>
            <th>Pedido</th>
            <th>Bordado</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="pedido_item in pedido_itens"
            :key="pedido_item.id"
          >
            <td>
              <input
                type="checkbox"
                :id="`pedido_item_${pedido_item.id}`"
                :name="`pedido_item_${pedido_item.id}`"
                :value="pedido_item.id"
                v-model="pedidos_selecionados"
              >
            </td>
            <td>{{pedido_item.pedido.entrega}}</td>
            <td>{{pedido_item.id}}</td>
            <td>{{pedido_item.bordado.nome}}</td>
            <td class="!text-right">{{ ptBrCurrencyFormat.format(pedido_item.valor_final) }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="status == 'c'">
        <h3 class="my-4 font-bold text-lg text-center">Inserindo comunicado</h3>
        <table class="w-full">
          <thead>
            <tr>
              <th>Valor</th>
              <th>Tipo</th>
              <th>Nº NF</th>
              <th>Data</th>
              <th>Parcelamento</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input
                  class="w-36 mx-0.5 border border-solid border-slate-500 rounded"
                  v-model="comunicado.valor_total"
                  type="number"
                  step="0.01"
                  name="valor_total"
                  id="valor_total"
                  placeholder="0,00"
                  required
                >
              </td>
              <td>
                <input
                  class="mx-0.5 border border-solid border-slate-500 rounded"
                  v-model.trim="comunicado.tipo"
                  type="text"
                  name="tipo"
                  id="tipo"
                  placeholder="Tipo"
                  list="tipo-list"
                  required
                  v-focus
                >
                <datalist id="tipo-list">
                  <option>Mail</option>
                  <option>Zap</option>
                </datalist>
              </td>
              <td>
                <input
                  class="w-20 mx-0.5 border border-solid border-slate-500 rounded"
                  v-model="comunicado.nf"
                  type="number"
                  name="nf"
                  id="nf"
                  placeholder="999"
                >
              </td>
              <td>
                <input
                  class="mx-0.5 border border-solid border-slate-500 rounded"
                  v-model="comunicado.data"
                  type="date"
                  name="data"
                  id="data"
                  required
                >
              </td>
              <td>
                <input
                  class="mx-0.5 border border-solid border-slate-500 rounded"
                  v-model.trim="comunicado.parcelamento"
                  type="text"
                  name="parcelamento"
                  id="parcelamento"
                  placeholder="10 30 60"
                  list="parcelamento-list"
                  required
                >
                <datalist id="parcelamento-list">
                  <option>0</option>
                  <option>10</option>
                  <option>10 30 60</option>
                  <option>30 60 90</option>
                </datalist>
              </td>
            </tr>
          </tbody>
        </table>
        <p class="flex flex-row-reverse place-content-between">
          <button
            type="button"
            @click="handleSalvaFiltraClick"
          >Grava</button>
          <button
            type="button"
            @click="handleCancelaClick"
          >Cancela</button>
        </p>
      </div>

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