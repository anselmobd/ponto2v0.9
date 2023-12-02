<script setup>
import router from '@/router'
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'
import { getPedidoItens } from '../api/pedidoItem.js';
import { ptBrCurrencyFormat } from "../utils/numStr.js";

const route = useRoute();

// valores recebidos de DB

const pedido_itens = ref('')
const pedidos_selecionados = ref([])
const comunicado = ref({})

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
  event.preventDefault(pedidos_selecionados.value);
  comunicado.value.valor_total = pedido_itens.value.map((ped_item) => {
    return pedidos_selecionados.value.includes(ped_item.id) ? ped_item.valor_final : 0
  }).reduce((soma, valor) => soma + valor, 0);
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
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="valor_total"
                  id="valor_total"
                  placeholder="0,00"
                  v-model="comunicado.valor_total"
                  @input="alerta = ''"
                  required>
            </td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
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