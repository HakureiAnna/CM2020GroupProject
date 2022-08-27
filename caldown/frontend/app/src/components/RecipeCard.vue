<script setup>
import { defineProps } from "vue";

const props = defineProps({
    picture_src: String,
    name: String,
    calories: Number
});

</script>

<template>
<div class="card recipe-card">
    <img :src="picture_src" class="card-img-top" :alt="name">
    <div class="card-body">
        <h5 class="card-title">{{ name }}</h5>
        <p class="card-text">Calories(J):  {{ parseInt(calories) }}</p>
    </div>
</div>
</template>

<style>
.recipe-card {
    max-height: 500px;
}
</style>