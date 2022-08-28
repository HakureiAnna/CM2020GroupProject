<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useUsersStore } from "@/stores";

import MealSelectOption from "@/components/MealSelectOption.vue";
import { sanitizeDate } from "@/helpers";

const usersStore = useUsersStore();
const { plan } = storeToRefs(usersStore);

// Calender Plugin Format
const date = ref(plan.date); // Vue ref creates a different 'ref' object, which I do not understand how it works... This is a BAD! way of keeping state value.

const format = (date) => {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  return `${year}/${month}/${day}`;
};

const saveDate = () => {
  if (!date.value) return;
  plan.date = sanitizeDate(date.value);
}

const submit = () => {
  if (!plan.date) {
    return;
  };

  usersStore.post_plan(plan.date);
}


</script>

<template>
  <div class="container">
    <Datepicker v-model="date" :format="format" @closed="saveDate" />
    <MealSelectOption mealType="Breakfast" picture_src="breakfast.jpg" picture_desc="amazing breakfast" />
    <MealSelectOption mealType="Lunch" picture_src="lunch.jpg" picture_desc="amazing lunch" />
    <MealSelectOption mealType="Dinner" picture_src="dinner.jpg" picture_desc="amazing dinner" />
    <button @click="submit" type="submit" class="btn btn-secondary">Submit Plan</button>
  </div>
</template>

<style></style>
