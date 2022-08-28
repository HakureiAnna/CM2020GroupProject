<script setup>
import { defineProps, ref } from "vue";
import { storeToRefs } from "pinia";

import { useUsersStore } from "@/stores";
import RecipeCard from "@/components/RecipeCard.vue";

const usersStore = useUsersStore();
const { history } = storeToRefs(usersStore);

const props = defineProps({
    plannedDate: String,
    calories: Number,
    planId: String,
});

const isExpanded = ref(null);

const toggleExpand = async id => {
  await usersStore.get_plan(id);
  isExpanded.value = !isExpanded.value;
}
</script>

<template>
<div class="card text-center">
  <div class="card-body">
    <h5 class="card-title">{{ plannedDate }}</h5>
    <div class="row">
        <div class="col-sm-6">
            <h6>Total Calories(J): </h6>
        </div>
        <div class="col-sm-6">
            <p class="card-text text-muted">{{ calories }}</p>
        </div>
    </div>
    <a @click="toggleExpand(planId)">Details</a>
    <hr class="mt-0 mb-4">
    <div v-if="history[planId]" v-show="isExpanded">
      <div class="row">
        <div class="col-sm-4">
          <p>Breakfast</p>
          <RecipeCard :picture_src="history[planId]['breakfast'].image" :name="history[planId]['breakfast'].name" :calories="history[planId]['breakfast'].calories" />
        </div>
        <div class="col-sm-4">
          <p>Lunch</p>
          <RecipeCard :picture_src="history[planId]['lunch'].image" :name="history[planId]['lunch'].name" :calories="history[planId]['lunch'].calories" />
        </div>
        <div class="col-sm-4">
          <p>Dinner</p>
          <RecipeCard :picture_src="history[planId]['dinner'].image" :name="history[planId]['dinner'].name" :calories="history[planId]['dinner'].calories" />
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<style>
</style>