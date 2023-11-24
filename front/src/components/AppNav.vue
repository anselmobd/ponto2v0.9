<script setup>
import { useAuthStore } from '../stores/auth.js';
import { storeToRefs } from 'pinia';

const auth = useAuthStore()
const { user } = storeToRefs(auth)
const { encerrar } = auth
</script>

<template>
  <div id="nav" class="px-4 flex row items-center justify-between border-b border-solid border-slate-800 shadow-[0_3px_3px_-1px] shadow-slate-700">
    <router-link :to="{ name: 'home' }" class="text-2xl font-bold">RPR - Ponto2</router-link>

    <div class="menu">
      <router-link :to="{ name: 'bordado' }">Bordado</router-link> |
      <router-link :to="{ name: 'sobre' }">Sobre</router-link>
    </div>

    <div>
      <span v-if="user.id">{{user.name}}&ThickSpace;</span>
      <router-link v-if="!user.id" :to="{ name: 'login' }" class="px-2 py-0.5 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100">Indentificar-se</router-link>
      <button
        type="button"
        class="px-2 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100"
        v-if="user.id" 
        @click.stop="encerrar()"
      >Encerrar</button>
    </div>
  </div>
</template>

<style scoped>
.menu .router-link-active {
  color: rgb(52, 136, 161);
  font-weight: bold;
}
</style>