<script setup>
import { storeToRefs } from "pinia";

import { useQuestionsStore } from "@/stores";

const questionsStore = useQuestionsStore();
const { profile, message } = storeToRefs(questionsStore);

questionsStore.get_profile();
</script>

<template>

<!-- Make this into a card using bootstrap or anything you like -->

  <div>
    <ul v-if="!message.error">
      <li v-for="(value, key) in profile">
        {{ key }}: {{ value }}
      </li>
    </ul>
    <div v-if="message.error">{{ message.error }}</div>
  </div>
</template>
