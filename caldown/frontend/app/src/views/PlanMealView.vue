<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { usePlanMealStore } from "@/stores";

import MealSelect from "@/components/MealSelect.vue";
import { sanitizeDate } from "@/helpers";


// Calender Plugin Format
const date = ref(new Date());
const format = (date) => {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  return `${year}/${month}/${day}`;
}

const planMealStore = usePlanMealStore();

const submit = () => {
  const selected_date = sanitizeDate(date.value);
  const response = planMealStore.post_plan(selected_date);
}


</script>

<template>
  <div class="container">
    <Datepicker v-model="date" :format="format" />
    <MealSelect mealType="Breakfast" picture_src="breakfast.jpg" picture_desc="amazing breakfast" />
    <MealSelect mealType="Lunch" picture_src="lunch.jpg" picture_desc="amazing lunch" />
    <MealSelect mealType="Dinner" picture_src="dinner.jpg" picture_desc="amazing dinner" />
    <button @click="submit" type="submit" class="btn btn-secondary">Submit Plan</button>
  </div>
</template>

<style></style>
