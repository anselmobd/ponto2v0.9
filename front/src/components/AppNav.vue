<script setup>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth.js';
import router from '@/router'

const auth = useAuthStore()
const { user } = storeToRefs(auth)
const { encerrar } = auth
</script>

<template>
  <div id="nav" class="px-4 flex row items-center justify-between border-b border-solid border-slate-800 shadow-[0_2px_2px_-1px] shadow-slate-700">
    <router-link :to="{ name: 'home' }" class="text-2xl font-bold">RPR - Ponto2</router-link>

    <div>
      <router-link 
        class="px-1 border-l border-cyan-600"
        v-if="user.name"
        :to="{ name: 'bordado' }"
        :exact-active-class="'text-cyan-600 font-bold'"
      >Bordado</router-link>
      <router-link
        class="px-1 border-l border-cyan-600"
        :to="{ name: 'sobre' }"
        :exact-active-class="'text-cyan-600 font-bold'"
      >Sobre</router-link>
      <span class="border-l border-cyan-600"></span>
    </div>

    <div>
      <span v-if="user.name">{{user.name}}&ThickSpace;</span>
      <router-link v-if="!user.name" :to="{ name: 'login' }" class="px-2 py-0.5 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100">Indentificar-se</router-link>
      <button
        type="button"
        class="px-2 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100"
        v-if="user.name" 
        @click.stop="encerrar(); router.push({ name: 'home' })"
      >Encerrar</button>
    </div>
  </div>
</template>

<style scoped>
</style>