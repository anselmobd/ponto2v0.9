<script setup>
import router from '@/router'
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'

const route = useRoute();

</script>

<template>
  <div>
    <div class="flex my-4 place-content-between">
      <h2 class="inline font-bold text-xl">Financeiro do pedido <span class="text-indigo-700">{{ route.params.id }}</span></h2>
      <a title="Voltar" class="button text-xl cursor-pointer" @click.prevent="router.go(-1)">&#x2190;</a>
    </div>
  </div>
</template>

<style scoped>
button, .button {
  @apply mx-0.5 my-[1px] px-2 py-0.5 rounded-lg bg-sky-700 font-bold text-slate-100
}
button:disabled {
  @apply bg-slate-500
}
</style>