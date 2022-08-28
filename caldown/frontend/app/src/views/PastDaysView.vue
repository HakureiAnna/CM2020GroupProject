<script setup>
import PlanCard from "@/components/PlanCard.vue";

import { ref } from "vue";
import { storeToRefs } from "pinia";

import { sanitizeDate } from "@/helpers";
import { useUsersStore } from "@/stores";

const usersStore = useUsersStore();
const { history } = storeToRefs(usersStore);

const date = ref();

const handleDate = (modelData) => {
  let [startDate, endDate] = modelData;

  if (!startDate || !endDate) return;

  startDate = sanitizeDate(startDate);
  endDate = sanitizeDate(endDate);

  date.value = [startDate, endDate];
}

const onClosed = () => {
  if (!date.value || !date.value[0] || !date.value[1]) return;
  const [startDate, endDate] = date.value;

  usersStore.get_history(startDate, endDate);
}
</script>

<template>
  <div class="container">
    <Datepicker v-model="date" @update:modelValue="handleDate" :enableTimePicker="false" @closed="onClosed" range />
    <div class="col" v-for="plan in history">
      <PlanCard :plannedDate="plan['plannedDate']" :calories="plan['calories']" :planId="plan['planId']" />
    </div>
  </div>
</template>
