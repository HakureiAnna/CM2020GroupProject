<script setup>
import { ref } from "vue";
import axios from "axios";

let user = ref(null);

const vHomeDirective = {
  created: async () => {
    const response = await axios.get("user");
    console.log(response);

    user.value = response;
  },
};
</script>

<template>
  <div>
    <h1 v-if="user.username">Hi, {{ user }}</h1>
    <h1></h1>
  </div>
</template>

<style></style>
