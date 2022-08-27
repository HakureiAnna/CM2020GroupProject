<script setup>
import { RouterLink } from "vue-router";

import { defineProps } from "vue";
import { storeToRefs } from "pinia";

const props = defineProps({
    mealType: String,
    picture_src: String,
    picture_desc: String
});

// Dynamically load images
const getImageUrl = (name) => {
    return new URL(`../public/img/${name}`, import.meta.url).href
}
</script>

<template>
<div class="card mb-3 meal-select">
    <div class="row g-0">
        <div class="col-md-8">
            <img :src="getImageUrl(picture_src)" class="img-fluid rounded-start" :alt=picture_desc />
        </div>
        <div class="col-md-4">
        <div class="card-body text-end">
            <h5 class="card-title">{{ mealType }}</h5>
            <RouterLink :to="{ name: 'recommendation', params: { mealType: mealType }, query: { type: mealType, keyword: mealType } }">
                Start
            </RouterLink>
        </div>
    </div>
    </div>
</div>
</template>

<style>
.meal-select {
    max-width: 540px;
    margin: 10px;

    border: 0;
}

.meal-select img {
    border-radius: 100%;
}

.card-body a {
    color: black;
}

.card-body a:hover {
    color: rgb(31, 18, 225);
    font-size: 1.5em;
    transition: all 0.3s ease;
}

</style>