<script setup>
import { RouterView } from "vue-router";
import Nav from "@/components/Nav.vue";
</script>

<template>
  <Nav v-if = "!['login', 'signup'].includes($route.name)"/>
  <RouterView />
</template>

<style>
@import "@/assets/base.css";

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0;

  font-weight: normal;
}

@media (min-width: 1024px) {
  /* body {
    display: flex;
    place-items: center;
  } */

  /* #app {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 2rem;
  } */
}


</style>
