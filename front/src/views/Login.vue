<script setup>
// import axios from 'axios';
import { ref } from 'vue'
import router from '@/router'
import { useAuthStore } from '@/stores/auth.js';
import { axiosPublic } from '../common/axiosPublic.js';

const auth = useAuthStore()
const { setUser } = auth

const username = ref('')
const password = ref('')
const alerta = ref('')

function login() {
  return axiosPublic
    .post('/api/token/', {
      username: username.value,
      password: password.value
    })
    .then(response => {
      if (response.data.access) {
        setUser(
          username.value,
          response.data.access,
          response.data.refresh
        );
        username.value = '';
        password.value = '';
        router.push({ name: 'home' });
      }
    })
    .catch(error => {
      console.error('Erro ao solicitar token:', error.response.data.detail);
      alerta.value = error.response.data.detail;
    });
}

</script>

<template>
  <div>
    <h2 class="font-bold text-lg">Identificação</h2>
    <form @submit.prevent="login()">
      <p class="my-4">
        <label class="block" for="username">Usuário:</label>
        <input
          class="px-2 py-1 w-full border-2 rounded-xl"
          type="text"
          name="username"
          id="username"
          placeholder="login"
          v-focus
          v-model="username"
          @input="alerta = ''"
          required>
      </p>
      <p class="my-4">
        <label class="block" for="password">Senha:</label>
        <input
          class="px-2 py-1 w-full border-2 rounded-xl"
          type="password"
          name="password"
          id="password"
          placeholder="senha"
          v-model="password"
          @input="alerta = ''"
          required>
      </p>
      <p v-if="alerta" class="my-4 text-red-600">{{ alerta }}</p>
      <button
        class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100"
        type="submit"
      >Enviar</button>
    </form>
  </div>
</template>
