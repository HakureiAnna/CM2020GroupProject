<script setup>
import { storeToRefs } from "pinia";

import { useQuestionsStore } from "@/stores";

const questionsStore = useQuestionsStore();
const { profile } = storeToRefs(questionsStore);

questionsStore.get_profile();
</script>

<template>

<!-- Make this into a card using bootstrap or anything you like -->

  <div>
    <ul>
      <li v-for="(value, key) in profile">
        {{ key }}: {{ value }}
      </li>
    </ul>
  </div>
</template>
