<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useUsersStore } from "@/stores";

import MealSelectOption from "@/components/MealSelectOption.vue";
import { sanitizeDate } from "@/helpers";


// Calender Plugin Format
const date = ref(new Date());
const format = (date) => {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  return `${year}/${month}/${day}`;
}

const usersStore = useUsersStore();
const { plan } = storeToRefs(usersStore);

const submit = () => {
  const selected_date = sanitizeDate(date.value);
  plan["plannedDate"] = selected_date;
  usersStore.post_plan();
}


</script>

<template>
  <div class="container">
    <Datepicker v-model="date" :format="format" />
    <MealSelectOption mealType="Breakfast" picture_src="breakfast.jpg" picture_desc="amazing breakfast" />
    <MealSelectOption mealType="Lunch" picture_src="lunch.jpg" picture_desc="amazing lunch" />
    <MealSelectOption mealType="Dinner" picture_src="dinner.jpg" picture_desc="amazing dinner" />
    <button @click="submit" type="submit" class="btn btn-secondary">Submit Plan</button>
  </div>
</template>

<style></style>
