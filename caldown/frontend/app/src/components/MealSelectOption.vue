<script setup>
import { defineProps } from "vue";
import { RouterLink } from "vue-router";
import { storeToRefs } from "pinia";

import { useUsersStore } from "@/stores";

const props = defineProps({
    mealType: String,
    picture_src: String,
    picture_desc: String
});

const usersStore = useUsersStore();
const { plan } = storeToRefs(usersStore);

// Dynamically load images
const getImageUrl = (name) => {
    return new URL(`../public/img/${name}`, import.meta.url).href
}
</script>

<template>
<div class="card mb-3 meal-select">
    <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col col-lg-6 mb-4 mb-lg-0">
            <div class="row g-0 justify-content-center align-items-center">
                <div class="col-lg-8 col-sm-6">
                    <img :src="getImageUrl(picture_src)" class="img-fluid rounded-start" :alt=picture_desc />
                </div>
                <div class="col-lg-4 col-sm-6">
                    <div class="card-body text-end">
                        <div class="row">
                            <h5 class="card-title">{{ mealType }}</h5>
                            <RouterLink :to="{ name: 'recommendation', params: { mealType: mealType }, query: { type: mealType, keyword: mealType } }">
                                Start
                            </RouterLink>
                        </div>
                        <div class="row">
                            <p class="card-text" v-if="plan[mealType]">
                                <small class="text-muted">
                                    {{ plan[mealType].name }}
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style>
.meal-select {
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