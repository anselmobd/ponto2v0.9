<script setup>
</script>

<template>
  <div id="nav" class="flex row items-center justify-between border-b border-solid border-slate-800 shadow-[0_3px_3px_-1px] shadow-slate-700">
    <h1 class="inline text-2xl font-bold">RPR - Ponto2</h1>
    <div>
      <router-link :to="{ name: 'Bordado' }">Bordado</router-link> |
      <router-link :to="{ name: 'Sobre' }">Sobre</router-link>
    </div>
    <div>
      admin
      <button type="button" class="px-2 border border-solid border-slate-800 rounded-lg bg-blue-600 font-bold text-slate-100">Encerrar</button>
    </div>
  </div>
</template>
