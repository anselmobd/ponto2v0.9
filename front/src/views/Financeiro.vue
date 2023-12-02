<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'

const route = useRoute();

</script>

<template>
  <div>
    <h2 class="my-4 font-bold text-xl">Financeiro do pedido <span class="text-indigo-700">{{ route.params.id }}</span></h2>
  </div>
</template>
