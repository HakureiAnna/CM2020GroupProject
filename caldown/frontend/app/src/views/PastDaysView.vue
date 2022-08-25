<script setup>
import { ref, onMounted } from "vue";
import PlanCard from "@/components/PlanCard.vue";

const date = ref(0);

onMounted (() => {
  const startDate = new Date();
  const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
  date.value = [startDate, endDate];
});

const handleDate = (modelData) => {
  date.value = modelData;
  console.log(modelData);
}
</script>

<template>
  <main>
    <Datepicker v-model="date" @update:modelValue="handleDate" range />
    <!-- <PlanCard plannedDate="" calories="" planId="" /> -->
  </main>
</template>
