<script setup>
import { ref } from 'vue'

const thisYear = new Date().getFullYear()
const year = ref(thisYear)
</script>

<template>
  <footer class="sticky bottom-0 bg-slate-100 text-slate-900 text-center text-base border-t border-solid border-slate-800 shadow-[0_-2px_2px_-1px] shadow-slate-700">
    <span class="whitespace-nowrap">Copyright &copy; {{ year }} RPR & Oxigenai</span>
  </footer>
</template>

<style scoped>
</style>
