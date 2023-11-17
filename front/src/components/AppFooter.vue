<script setup>
import { ref } from 'vue'

const thisYear = new Date().getFullYear()
const year = ref(thisYear)
</script>

<template>
  <footer class="sticky bottom-0 text-center border-t border-solid border-gray-800 shadow-[0_-6px_5px_-5px] shadow-gray-800">
    <span class="whitespace-nowrap">Copyright &copy; {{ year }}</span>&ThinSpace;
    <span class="whitespace-nowrap">RPR & Oxigenai</span>
  </footer>
</template>

<style scoped>
</style>
