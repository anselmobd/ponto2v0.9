<script setup>
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <div id="app">
    <div id="nav">
      <router-link :to="{ name: 'Bordado' }">Bordado</router-link> |
      <router-link :to="{ name: 'Sobre' }">Sobre</router-link>
    </div>
    <router-view class="main-body"/>
  </div>
  <app-footer />
</template>

<style scoped>
</style>
