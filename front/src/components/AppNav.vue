<script setup>
</script>

<template>
  <div id="nav" class="px-4 flex row items-center justify-between border-b border-solid border-slate-800 shadow-[0_3px_3px_-1px] shadow-slate-700">
    <router-link :to="{ name: 'home' }" class="text-2xl font-bold">RPR - Ponto2</router-link>

    <div>
      <router-link :to="{ name: 'bordado' }">Bordado</router-link> |
      <router-link :to="{ name: 'sobre' }">Sobre</router-link>
    </div>
    <div>
      admin
      <router-link :to="{ name: 'Login' }" class="px-2 py-0.5 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100">Indentificar-se</router-link>
      <button type="button" class="px-2 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100">Encerrar</button>
    </div>
  </div>
</template>
