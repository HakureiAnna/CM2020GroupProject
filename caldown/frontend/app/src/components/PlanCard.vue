<script setup>
import { defineProps } from "vue";

const props = defineProps({
    plannedDate: String,
    calories: Number,
    planId: String,
});

</script>

<template>
<div class="card">
    <div class="card-body">
        <h5 class="card-title">{{ plannedDate }}</h5>
        <p class="card-text">Calories(J):  {{ parseInt(calories) }}</p>
    </div>
</div>
</template>

<style>
</style>