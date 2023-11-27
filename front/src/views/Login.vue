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
    <h2 class="login__h2">Identificação</h2>
    <form @submit.prevent="login()" class="login__form">
      <p class="login__p">
        <label class="login__label" for="username">Usuário:</label>
        <input
          class="login__input"
          type="text"
          name="username"
          id="username"
          placeholder="login"
          v-focus
          v-model="username"
          @input="alerta = ''"
          required>
      </p>
      <p class="login__p">
        <label class="login__label" for="password">Senha:</label>
        <input
          class="login__input"
          type="password"
          name="password"
          id="password"
          placeholder="senha"
          v-model="password"
          @input="alerta = ''"
          required>
      </p>
      <p v-if="alerta" class="text-red-600">{{ alerta }}</p>
      <button class="login__button" type="submit">Enviar</button>
    </form>
  </div>
</template>

<style scoped>
/* || CONTACT */

.login__h2 {
    margin: 0;
    font-weight: bold;
    font-size: larger;
}

.login__p {
    margin: 1em 0;
}

.login__label {
    display: block;
    font-weight: bold;
}

.login__input,
.login__textarea {
    padding: 0.5em;
    border-radius: 15px;
    border-width: 2px;
    width: 100%;
}

.login__button {
    padding: 0.5em;
    border-radius: 15px;
    background-color: rgb(52, 136, 161);
    color: whitesmoke;
    font-weight: bold;
}
</style>