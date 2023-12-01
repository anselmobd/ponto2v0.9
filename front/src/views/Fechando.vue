<script setup>
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <div>
    <h2 class="font-bold text-lg">Fechando pedido {{ route.params.id }}</h2>
  </div>
</template>
