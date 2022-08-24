<script setup>
import { useField } from "vee-validate";
import { defineProps, toRef } from "vue";

const props = defineProps({
    name: String,
});

const nameRef = toRef(props, "name");
const { errorMessage, value } = useField(nameRef);
</script>

<template>
  <div class="form-group">
    <input v-if="'text' === dynamicInputType" v-model="value" type="text" class="form-control">
    <input v-else v-model="value" type="password" class="form-control">
    <span>{{ errorMessage }}</span>
  </div>
</template>