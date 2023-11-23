<script setup>
import AppFooter from './components/AppFooter.vue'
import AppNav from './components/AppNav.vue'
</script>

<template>
  <app-nav />
  <router-view class="main-body"/>
  <app-footer />
</template>

<style scoped>
.main-body {
    /* viewport height - footer height - nav/header height */
    min-height: calc(100vh - 1.5rem - 1px - 2rem - 1px );
}
</style>
