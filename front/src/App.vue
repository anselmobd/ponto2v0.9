<script setup>
import AppFooter from './components/AppFooter.vue'
import AppNav from './components/AppNav.vue'
</script>

<template>
  <app-nav />
  <router-view class="main-body"/>
  <app-footer />
</template>
